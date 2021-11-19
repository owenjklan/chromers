function createButtonClicked() {
    let message = {
        "code": "CREATE_NEW_LIST",
    }
    sendMessageToActiveTabs(message);
}

function addRuleButtonClicked() {
    let message = {
        "code": "ADD_RULE_TO_CSV",
    }
    sendMessageToActiveTabs(message);
}

function exportButtonClicked() {
    let message = {
        "code": "EXPORT_LIST",
    }
    sendMessageToActiveTabs(message);
}

// Once DOM finishes loading, start running our JS
document.addEventListener('DOMContentLoaded', function() {
    const createButton = document.getElementById('createNewList');
    const addRuleButton = document.getElementById('addRuleToList');
    const exportButton = document.getElementById('exportRuleList');

    createButton.addEventListener('click', createButtonClicked, false);
        addRuleButton.addEventListener('click', addRuleButtonClicked, false);
        exportButton.addEventListener('click', exportButtonClicked, false);
    }, false);

function sendMessageToActiveTabs(message) {
    let query = {active: true, currentWindow: true};

    chrome.tabs.query(query, function (tabs) {
        console.log("Sending message... " + message.code);
        let targetTab = tabs[0].id;
        console.log("Target tab ID: " + targetTab);
        console.log("      Tab URL: " + tabs[0].url);

        chrome.tabs.sendMessage(tabs[0].id, {"code": "ADD_RULE_TO_CSV"});
    });
}
