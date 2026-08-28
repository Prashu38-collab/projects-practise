let startTime = null;

chrome.tabs.onActivated.addListener(function(activeInfo) {

    let endTime = Date.now();

    if (startTime !== null) {

        let duration = endTime - startTime;
        let durationSeconds = duration / 1000;

        console.log("Time spent:", durationSeconds, "seconds");
    }

    startTime = Date.now();

    chrome.tabs.query(
        { active: true, currentWindow: true },
        function(tabs) {

            console.log("Title:", tabs[0].title);
            console.log("URL:", tabs[0].url);
            console.log("Start time:", startTime);
        }
    );

});