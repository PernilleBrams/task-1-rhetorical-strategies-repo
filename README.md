### 📑 **README.md for Streamlit Annotation Tool**

---

# 📝 Streamlit Annotation Tool for Factual Claim Detection

This is an interactive annotation tool built with [Streamlit](https://streamlit.io/). The tool allows users to log in, read sentences, and annotate whether a sentence contains a factual claim and if that claim is important. All annotations are stored securely in a Google Sheet associated with each user.

---

## 🚀 **Features**

- 🔐 **User Login:** Each user gets a personal annotation session and their own Google Sheet tab for storing data.
- 📄 **Sentence Annotation:** Quickly classify sentences as:
  - No factual claim
  - Factual but unimportant
  - Important factual claim
- ☁️ **Google Sheets Integration:** Automatically syncs annotations to a Google Sheet for easy collaboration and analysis.
- 🌙 **Dark Mode Support:** Automatically adapts based on Streamlit’s dark/light theme settings.
- ⏭️ **Skip Sentences:** Users can skip sentences they don't want to annotate.

---

## 📂 **Project Structure**

```
annotation-tool/
│
├── app.py                      # Main Streamlit app
├── requirements.txt            # List of dependencies
├── .streamlit/
│   └── secrets.toml            # Google Sheets API credentials (for Streamlit Cloud)
├── data/
│   └── clean/
│       └── processed_sentences.txt  # Preprocessed sentences for annotation
├── .gitignore                  # Files to ignore in version control
└── README.md                   # This documentation file
```

---

## 🔑 **How to Use the App**

1. Log in using your **User ID** from the sidebar.
2. Read the displayed sentence.
3. Annotate by selecting:
   - ❌ No factual claim
   - ⚪ Factual but unimportant
   - ✅ Important factual claim
4. Skip sentences if unsure.
5. Log out when finished — your annotations will automatically save.

---

## 🛠️ **Tech Stack**

- [Streamlit](https://streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Pandas](https://pandas.pydata.org/)
- [gspread](https://gspread.readthedocs.io/en/latest/)
