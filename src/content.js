console.log("CONTENT SCRIPT LOADED");

let csvRows;

function messageReceived(message, sender, sendResponse) {
    const locationUrl = location.href;
    const locationPath = location.pathname;

    // Assume the Rule's human name is output in the first and theoretically,
    // only, H1 tag.
    const ruleNameHeader = document.getElementsByTagName("h1")[0];
    const ruleName = ruleNameHeader.innerText;
    // Last element of path should be the rule ID
    const ruleId = locationPath.split('/').at(-1);

    switch (message.code) {
        case "ADD_RULE_TO_LIST": {
            csvRows.push(ruleName, ruleId, 5);
        }
        case "CREATE_NEW_LIST": {
            csvRows = [];  // New, empty array
            console.log("New list created");
        }
        case "EXPORT_LIST": {
            alert("Will export list...");
            for (row in csvRows) {
                console.log("Row: " + row);
            }
        }
    }
}

console.log("Adding message listener to content script...");
chrome.runtime.onMessage.addListener(messageReceived);
