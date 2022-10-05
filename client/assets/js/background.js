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
    (request) => {
        getResults(request.query)
    }
)

function getResults(query) {
    chrome.storage.local.get(["state"], (result) => {
        const oldState = result.state

        if (!query)
            updateState(getErrorState(oldState, "Query can't be empty!"))

        updateState(getLoadingState(oldState, query))

        const options = {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query,
                "selected_text": "",
                "amount_multiplier": 1
            })
        }

        fetch('http://localhost:8000/twitter', options)
            .then(response => response.json())
            .then(data => updateState(getSuccessState(oldState, data.results)))
            .catch(error => updateState(getErrorState(oldState, error)))
    })
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
    return{
        ...oldState,
        type: "SUCCESS",
        error: null,
        results
    }
}

