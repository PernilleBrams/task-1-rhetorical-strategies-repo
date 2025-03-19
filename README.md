# Streamlit Annotation Tool for Rhetorical Strategies 🗣️📝

An interactive web-based tool built with **Streamlit** for annotating **rhetorical strategies** in political debates. Users log in with a unique ID, read debate transcripts or utterances, and label relevant rhetorical strategies. All annotations are stored securely in **Google Sheets** in per-user worksheets.  

## ✨ Key Features

1. **User Login & Individual Data** 🔐  
   - Users log in with their ID from the sidebar.  
   - Each user has a **personal worksheet** in Google Sheets and a **personal data file** (e.g., `data/clean/<USER_ID>/processed_texts_test.txt`).  
   - The tool automatically checks for an existing worksheet and creates one if it does not exist.

2. **Rhetorical Strategy Annotation** 🗣️  
   - Label each utterance with one or more categories:  
     - **Svar (Answer)**  
     - **Overdrivelse (Stretch/Exaggeration)**  
     - **Undvigelse/Udenomssnak (Dodge/Evasion)**  
     - **Selv-promovering/Personlig anekdote (Self-promotion/Personal Anecdote)**  
     - **Angreb/Provokation (Attack/Provocation)**  
     - **Andet (Other)**  
   - Highlight snippets of text and assign labels from the menu.  
   - A **comment box** allows users to include notes or highlight uncertainty.

3. **Google Sheets Integration** ☁️  
   - Annotations are automatically appended to a Google Sheet for each user.  
   - Batches of 5 annotations get saved at a time for efficiency. (Any remaining, smaller batch will save upon logging out.)

4. **Light Mode by Default** 🌞  
   - The tool enforces a light theme for better readability, regardless of user device or Streamlit’s default theme.

5. **Session Management** 🔄  
   - If you log out or close the browser, you can log back in later to resume from where you left off.  
   - Already annotated texts are skipped automatically, ensuring you never lose progress.

6. **Minimal Dependencies** 🛠️  
   - Uses `pandas`, `gspread`, and `streamlit_text_label`, plus standard Python libraries.  
   - No extra databases or servers required — just Google Sheets.

## 🗂️ Project Structure

```
annotation-tool/
├── app.py                       # (Previously: app_marking_v2_attempt100.py) Main Streamlit app
├── requirements.txt             # List of Python dependencies
├── .streamlit/
│   └── secrets.toml             # Google Sheets API credentials (for Streamlit Cloud or local usage)
├── data/
│   └── clean/
│       └── <USER_ID>/
│           └── processed_texts_test.txt  # Per-user data file for annotation
├── .gitignore                   # Ignore tokens, credentials, etc., in version control
└── README.md                    # This documentation file
```

## 🚀 How to Use

1. **Log In**  
   - Open the app (e.g., by running `streamlit run app.py`).  
   - Enter your **User ID** on the sidebar and click **“Log in.”**  
   - If your User ID is authorized, you’ll see the main annotation interface.

2. **Annotate**  
   - A debate text or utterance will appear in a **highlighting widget**.  
   - Highlight any snippet(s) and select the **rhetorical strategy** from the menu.  
   - Press **Update** (the blue button) to confirm your label selection(s).  

3. **Add Comments (Optional)**  
   - Use the text area below if you need to leave remarks about your annotations.

4. **Submit & Move On**  
   - Click **“Gem annotation”** to save your chosen labels and comment.  
   - You’ll then automatically see the next text.  
   - Annotations save in **batches of 5**. (Any unsaved batch is saved upon completing all texts or logging out.)

5. **Log Out**  
   - At any time, you can log out via the sidebar.  
   - Any unsaved annotations in your **current batch** will be saved before logging out.

6. **Completion**  
   - When you finish annotating all texts in your personal file, you’ll see a **completion message**.  
   - Congratulations, you’re done! 🎉

## ⚙️ Tech Stack

- **Streamlit** for the front-end interface.  
- **Python** (standard libraries plus):  
  - `pandas` for data handling.  
  - `gspread` + `google.oauth2.service_account` for Google Sheets API.  
  - `streamlit_text_label` for text highlighting/labeling.  
- **Google Sheets** for remote storage and collaboration.

## 📝 Notes & Tips

- **Batch Saving**: Annotations are pushed to Google Sheets in increments of 5. If you have partially annotated fewer than 5 items, they will still save when you finish or log out.  
- **Resuming Work**: Your progress is tracked by Streamlit’s session state and by skipping previously annotated text.  
- **Light Theme**: By design, the tool forces a white background for consistent readability.  
- **User-Specific Data**: Each user’s data is located in `/data/clean/<USER_ID>`.  
- **Expandability**: Easily customize rhetorical strategies, comment usage, or classification logic by editing labels and prompts in `app.py`.
