const searchFieldEl = document.getElementById("search-field")
const submitButtonEl = document.getElementById("submit-button")
const resultsEl = document.getElementById("results")
const noResultsEl = document.getElementById("no-results")

submitButtonEl.addEventListener("click", handleSubmit)

chrome.storage.local.get(["state"], (result) => updateElements(result.state))

chrome.storage.onChanged.addListener((changes) => {
    updateElements(changes.state.newValue)
});

function handleSubmit(evt) {
    evt.preventDefault()

    // Get Results
    chrome.runtime.sendMessage({query: searchFieldEl.value});
}


function updateElements(state) {
    updateSubmitButton(state)
    updateSearchField(state)
    updateResultContainer(state)
}

function updateSearchField(state) {
    switch (state.type) {
        case "ERROR":
            searchFieldEl.classList.add("is-danger")
            searchFieldEl.removeAttribute("disabled")
            break
        case "LOADING":
            searchFieldEl.classList.remove("is-danger")
            searchFieldEl.setAttribute("disabled", null)
            break
        case "SUCCESS":
            searchFieldEl.classList.remove("is-danger")
            searchFieldEl.removeAttribute("disabled")
            searchFieldEl.value = state.query
            break
    }
}


function updateSubmitButton(state) {
    switch (state.type) {
        case "ERROR":
            submitButtonEl.removeAttribute("disabled")
            break
        case "LOADING":
            submitButtonEl.classList.add("is-loading")
            submitButtonEl.setAttribute("disabled", null)
            break
        case "SUCCESS":
            submitButtonEl.classList.remove("is-loading")
            submitButtonEl.removeAttribute("disabled")
            break
    }
}


function updateResultContainer(state) {
    console.log(state)
    if (state.results && state.results.length > 0) {
        noResultsEl.classList.add("is-hidden")
    } else {
        noResultsEl.classList.remove("is-hidden")
    }

    resultsEl.replaceChildren()
    for (let i in state.results) {
        const result = state.results[i]
        const el = createTagEl(result.segment, result.frequency, state.query)
        resultsEl.appendChild(el)
    }
}

function createTagEl(segment, frequency, query) {
    const el = document.createElement("a")
    el.classList.add("tag", "is-primary", "is-rounded", "is-light", getTagColor(frequency))
    el.setAttribute("data-frequency", frequency)
    el.innerText = segment
    el.href = `https://twitter.com/search?q=${segment} ${query}`
    el.target = "_blank"
    return el
}

function getTagColor(frequency) {
    let tagClass = ""
    switch (true) {
        case frequency < 5:
            tagClass = "is-danger"
            break
        case frequency < 10:
            tagClass = "is-warning"
    }

    return tagClass
}