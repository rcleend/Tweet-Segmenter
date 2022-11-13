let initialState = {
    type: "SUCCESS",
    error: null,
    results: null,
    query: null
}

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ state: initialState })
})


chrome.runtime.onMessage.addListener(
    async (request) => {
        // Get current active tab for selected text
        const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });

        // If no tab is found get results without selected text
        if (tab) {
            chrome.scripting.executeScript({
                target: {tabId: tab.id},
                func: getSelectedText
            },
                selectedText => {
                    getResults(request.query, selectedText[0].result)
                }
            );
        } else {
            getResults(request.query, "")
        }
    }
)

function getResults(query, selectedText) {
    chrome.storage.local.get(["state"], (result) => {
        const oldState = result.state

        if (!query) {
            updateState(getErrorState(oldState, "Query can't be empty!"))
            return
        }

        const loadingState = getLoadingState(oldState, query)
        updateState(loadingState)

        const options = {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query,
                "selected_text": selectedText,
                "amount_multiplier": 10
            })
        }
        fetch('http://localhost:8000/twitter', options)
            .then(response => response.json())
            .then(data => updateState(getSuccessState(loadingState, data.results)))
            .catch(error => updateState(getErrorState(loadingState, error)))
    })
}

// Function used to get selected text from active tab
// ONLY USE THIS FUNCTION AS FUNC PARAMETER IN THE CHROME TABS API
function getSelectedText() {
    return window.getSelection().toString()
}

function updateState(state) {
   chrome.storage.local.set({state});
}

function getLoadingState(oldState, query) {
    return {
        ...oldState,
        type: "LOADING",
        error: null,
        query
    }
}

function getErrorState(oldState, error) {
    return {
        ...oldState,
        type: "ERROR",
        error
    }
}

function getSuccessState(oldState, results) {
    console.log(results)
    return{
        ...oldState,
        type: "SUCCESS",
        error: null,
        results
    }
}

