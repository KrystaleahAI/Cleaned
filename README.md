# Cleaned — Racial Slur Auto-Labeler and Regenerator

A hackathon project (Women in AI) that detects racial slurs in text, masks
them, and can optionally rewrite the passage in a respectful, non-offensive way.
Built with [spaCy](https://spacy.io/) for detection and [Streamlit](https://streamlit.io/)
for the interface.

---

## Content Warning

**This repository contains, references, and processes highly offensive material,
including racial slurs, hate speech, and other derogatory language.**

- [`slurs.csv`](slurs.csv) is a database of slurs and derogatory terms (scraped
  from a public slur database) used purely as a **detection lookup list**.
- [`Data/labeled_data.csv`](Data/labeled_data.csv) is a research dataset of tweets
  labeled as hate speech / offensive language, which contains offensive text and
  third-party usernames.

This content is included **solely** to build and evaluate a tool that **identifies
and removes** such language. It is **not** an endorsement of any of the terms it
contains. If encountering this kind of language is harmful to you, please do not
proceed.

This tool is intended for research, moderation, and educational purposes only.

---

## What it does

The app has three panels:

1. **Input Text** — you paste in a passage.
2. **Labeled Text** — every detected slur is replaced with the placeholder `SLUR`.
3. **Regenerated Text** — (optional) an AI-generated respectful rewrite of the
   sanitized text.

## How it works

- `slur_labeler.py` builds a blank spaCy pipeline with a custom component that
  flags any token matching an entry in `slurs.csv` (via a custom `is_slur`
  token attribute).
- `slur_autolabeler.py` is the Streamlit app. `process_text()` masks flagged
  tokens; `summarize_text()` sends the sanitized text to OpenAI for a respectful
  rewrite.
- `scrape_racial_slurs.py` is the one-off scraper used to build `slurs.csv`.

## Setup

```bash
# 1. Install dependencies
pip install streamlit spacy openai python-dotenv

# 2. (Optional) configure OpenAI for the "Regenerate" feature
#    Copy the example and add your own key:
cp .env.example .env
#    then edit .env and set OPENAI_API_KEY=sk-...
```

> **Note:** The detection/labeling half of the app works with **no API key**.
> Only the optional "Regenerated Text" panel calls OpenAI and requires a key.
> No API key is included in this repository — you must supply your own.

## Run

```bash
streamlit run slur_autolabeler.py
```

## Project structure

| File | Purpose |
|------|---------|
| `slur_autolabeler.py` | Streamlit app (UI + labeling + regeneration) |
| `slur_labeler.py` | spaCy pipeline and slur-detection component |
| `scrape_racial_slurs.py` | Scraper that generated `slurs.csv` |
| `slurs.csv` | Slur lookup list used for detection |
| `Data/labeled_data.csv` | Hate-speech research dataset |

## Notes & limitations

- Detection is an **exact, case-insensitive token match** against `slurs.csv`.
  It will miss obfuscated spellings, misspellings, and slurs used in multi-word
  or contextual forms — it is **not** a complete safety filter.
- `summarize_text()` uses the deprecated `text-davinci-003` model / `openai.Completion`
  API and may need updating to a current model and the newer OpenAI SDK.
- The datasets are included for reproducibility; please review their original
  sources and licenses before redistributing.

## License / data attribution

Please verify and respect the licenses of the third-party data before reusing:
`slurs.csv` is derived from a public slur database, and `Data/labeled_data.csv`
originates from a publicly released hate-speech research dataset.
