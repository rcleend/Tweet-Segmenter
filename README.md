# Detecting Novel Topics Related to Twitter News Events

**Preprocess Wiki Page Titles**
1. Download most recent Wiki Page Title Dump: https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz
2. Preprocess titles `python ./api/wiki_titles_preprocess.py`

**Setup Server:**
1. Install Python dependencies: `pip install -r requirements.txt`
2. Create a new project in the Twitter Developer portal: https://developer.twitter.com/en/portal/dashboard
3. Rename `.env.example` to `.env` and add the Twitter API bearer token
4. Run server: `cd api && uvicorn main:app`

**Setup Chrome extension:**
1. Install NPM dependencies `cd client && npm i`
2. Load the `client` directory using the 'Load unpacked' button in the Chrome browser: chrome://extensions/
3. Navigate to any given website and test the extension

**Behold results:**

![Alt Text](./app.gif)

