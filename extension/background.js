const API_URL = "http://127.0.0.1:8000/api/v1";

const FLUSH_MINUTES = 2;
const STORE = "currentSession";
const QUEUE_KEY = "pendingActivities";
const MAX_QUEUE = 500;

// ---- storage -----------------------------------------------------------------

async function getStoredSession() {
    const result = await chrome.storage.session.get(STORE);
    return result[STORE] || null;
}

async function setStoredSession(session) {
    await chrome.storage.session.set({ [STORE]: session });
}

async function clearStoredSession() {
    await chrome.storage.session.remove(STORE);
}

async function getQueue() {
    const result = await chrome.storage.local.get(QUEUE_KEY);
    return result[QUEUE_KEY] || [];
}

async function setQueue(queue) {
    await chrome.storage.local.set({ [QUEUE_KEY]: queue });
}

// ---- delivery ---------------------------------------------------------------
//
// trySend returns:
//   true     accepted by the backend
//   "retry"  backend unreachable or server error (5xx) -> keep for later
//   "drop"   payload rejected as invalid (4xx) -> discard, retrying is pointless

async function trySend(session) {
    try {
        const res = await fetch(`${API_URL}/activities`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: session.title,
                url: session.url,
                started_at: new Date(session.startedAt * 1000).toISOString(),
                ended_at: new Date(session.endedAt * 1000).toISOString()
            })
        });
        if (res.ok) return true;
        return res.status >= 500 ? "retry" : "drop";
    } catch (e) {
        return "retry";
    }
}

async function pushToQueue(session) {
    const queue = await getQueue();
    queue.push(session);
    if (queue.length > MAX_QUEUE) {
        queue.splice(0, queue.length - MAX_QUEUE);
    }
    await setQueue(queue);
}

async function deliverOrQueue(session) {
    const result = await trySend(session);
    if (result === true) {
        await drainQueue();
    } else if (result === "retry") {
        await pushToQueue(session);
    }
}

async function drainQueue() {
    let queue = await getQueue();
    while (queue.length > 0) {
        const result = await trySend(queue[0]);
        if (result !== true) break;  // still offline: leave the rest queued
        queue = queue.slice(1);
    }
    await setQueue(queue);
}

// ---- session tracking ---------------------------------------------------------

async function getActiveTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab || null;
}

function isTrackable(url) {
    return Boolean(
        url &&
        /^https?:/i.test(url) &&
        !/^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?/i.test(url)
    );
}

function epochSeconds() {
    return Math.round(Date.now() / 1000);
}

async function flushSession() {
    const session = await getStoredSession();
    if (!session) return;

    session.endedAt = epochSeconds();
    session.duration = Math.max(0, session.endedAt - session.startedAt);
    await clearStoredSession();

    if (session.duration <= 0) return;
    await deliverOrQueue(session);
    console.log("Flushed:", session.title, session.duration, "s");
}

async function startSession(tab, startedAt = epochSeconds()) {
    await setStoredSession({
        tabId: tab.id,
        title: tab.title || tab.url,
        url: tab.url,
        startedAt
    });
}

async function refreshSession() {
    const tab = await getActiveTab();
    if (!tab || !isTrackable(tab.url)) {
        await flushSession();
        return;
    }
    const session = await getStoredSession();
    if (session && session.url === tab.url) return;

    await flushSession();
    await startSession(tab);
}

async function chunkAndContinue() {
    const tab = await getActiveTab();
    const session = await getStoredSession();
    if (!tab || !isTrackable(tab.url) || !session || session.url !== tab.url) return;

    await flushSession();
    await startSession(tab);
}

async function ensureFlushAlarm() {
    await chrome.alarms.create("flush", { periodInMinutes: FLUSH_MINUTES });
}

async function restoreOrStart() {
    const tab = await getActiveTab();
    const session = await getStoredSession();
    if (!tab || !isTrackable(tab.url)) return;

    if (session && session.url === tab.url) return;
    await flushSession();
    await startSession(tab);
}

// ---- events ------------------------------------------------------------------

chrome.tabs.onActivated.addListener(refreshSession);

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete") {
        refreshSession();
    }
});

chrome.tabs.onRemoved.addListener(async (tabId) => {
    const session = await getStoredSession();
    if (session && session.tabId === tabId) {
        await flushSession();
    }
});

chrome.windows.onFocusChanged.addListener(async (windowId) => {
    if (windowId === chrome.windows.WINDOW_ID_NONE) {
        await flushSession();
    } else {
        await refreshSession();
    }
});

chrome.runtime.onInstalled.addListener(async () => {
    await ensureFlushAlarm();
    await drainQueue();
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (alarm.name !== "flush") return;
    await chunkAndContinue();
    await drainQueue();
});

ensureFlushAlarm();
restoreOrStart();
drainQueue();