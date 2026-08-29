let startTime = null;
let currentTab=null;

chrome.tabs.onActivated.addListener(function(activeInfo) {

    let endTime = Date.now();

    if (startTime !== null) {

        let duration = endTime - startTime;
        let durationSeconds = duration / 1000;

        // activity records
        let activity={
            title:currentTab.title,
            url:currentTab.url,
            duration:durationSeconds
        };
        console.log("Activity: ",activity);


        console.log("Time spent:", durationSeconds, "seconds");
        // Send activity to Python
        fetch("http://127.0.0.1:8000/activity", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(activity)
        });
    }

    // Start timer for the new tab
    startTime = Date.now();

    chrome.tabs.query(
        { active: true, currentWindow: true },
        function(tabs) {

            currentTab = tabs[0];

            console.log("Current tab:", currentTab.title);
        }
    );

});