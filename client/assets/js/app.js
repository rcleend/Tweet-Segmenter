const searchFieldEl = document.getElementById("search-field")
const submitButtonEl = document.getElementById("submit-button")
const resultsEl = document.getElementById("results")
const noResultsEl = document.getElementById("no-results")

submitButtonEl.addEventListener("click", handleSubmit)


function handleSubmit(evt) {
    evt.preventDefault()

    // Get Results
    chrome.runtime.sendMessage({query: searchFieldEl.value});
}

chrome.storage.onChanged.addListener((changes, namespace) => {
    updateSubmitButton(changes.state.newValue)
    updateSearchField(changes.state.newValue)
    updateResultContainer(changes.state.newValue)
});

function updateSearchField(background) {
    switch (background.background) {
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
    if (state.results) {
        noResultsEl.classList.add("is-hidden")
    } else {
        noResultsEl.classList.remove("is-hidden")
    }

    resultsEl.replaceChildren()
    for (let i in state.results) {
        const el = document.createElement("a")
        const segment = state.results[i]["segment"]
        el.classList.add("tag", "is-primary", "is-rounded")
        el.innerText = segment
        el.href = `https://twitter.com/search?q=${segment}`
        el.target = "_blank"
        resultsEl.appendChild(el)
    }
}