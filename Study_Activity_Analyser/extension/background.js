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
            duration:duration
        };
        console.log("Activity: ",activity)


        console.log("Time spent:", durationSeconds, "seconds");
    }

    startTime = Date.now();

    chrome.tabs.query(
        { active: true, currentWindow: true },
        function(tabs) {
            currentTab = tabs[0];
            console.log("Current tab:", currentTab.title);

            
        }
    );

});
