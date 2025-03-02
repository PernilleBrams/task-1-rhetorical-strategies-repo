'''
formerly app_marking_v2_attempt100.py

This works but has two buttons, update and gem annotation. Also is a bit clunky.
Doesnt save to sheets atm when on eduroam? should be fine when deployed on streamlit tho
'''

import streamlit as st
import pandas as pd
import gspread
import datetime
import os
import threading
from google.oauth2.service_account import Credentials
from streamlit_text_label import label_select

# --- GOOGLE SHEETS SETUP ---
GOOGLE_CREDENTIALS = st.secrets["GOOGLE_CREDENTIALS"]
SHEET_ID = st.secrets["SHEET_ID"]

# Authenticate Google Sheets
creds = Credentials.from_service_account_info(GOOGLE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)

# --- GOOGLE SHEETS FUNCTIONS ---
def fetch_allowed_users():
    """Fetch allowed users from the 'allowed_users' tab in the connected Google Sheet."""
    spreadsheet = gc.open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet("allowed_users_CE")  
    allowed_users = worksheet.col_values(1)  
    return set(allowed_users)

def get_user_worksheet(user_id):
    """ Ensure each user has a personal worksheet. Create one if it doesn’t exist. """
    spreadsheet = gc.open_by_key(SHEET_ID)
    try:
        return spreadsheet.worksheet(user_id)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=user_id, rows="1500", cols="7")
        worksheet.insert_row(
            ["user_id", "text_index", "full_text", "stretch", "dodge", "omission", "deflection", "timestamp"],
            index=1
        )
        return worksheet

def get_annotated_texts(user_id):
    """ Fetch already annotated texts for the user. """
    worksheet = get_user_worksheet(user_id)
    data = worksheet.get_all_values()
    if len(data) > 1:
        df_annotations = pd.DataFrame(data[1:], columns=["user_id", "text_index", "full_text", "stretch", "dodge", "omission", "deflection", "timestamp"])
        return set(df_annotations["full_text"].tolist())
    return set()

def save_annotations(user_id, annotations):
    """ Save annotations asynchronously to Google Sheets. """
    worksheet = get_user_worksheet(user_id)
    worksheet.append_rows(annotations)

# --- STREAMLIT APP SETUP ---
st.sidebar.title("Brugerlogin")

# ✅ Load allowed users only once per session
if "ALLOWED_USERS" not in st.session_state:
    st.session_state.ALLOWED_USERS = fetch_allowed_users()

# ✅ Check if user is logged in
if "user_id" not in st.session_state:
    user_id = st.sidebar.text_input("Indtast dit bruger-ID:")
    if st.sidebar.button("Log in") and user_id.strip():
        if user_id.strip() in st.session_state.ALLOWED_USERS:
            st.session_state.user_id = user_id.strip()
            st.session_state.text_index = -1
            st.session_state.annotations = []
            st.session_state.annotated_texts = get_annotated_texts(user_id)
            st.session_state.worksheet_ready = False
            st.session_state.finished = False
            st.rerun()
        else:
            st.sidebar.error("❌ Adgang nægtet: Dit bruger-ID er ikke autoriseret.")
else:
    user_id = st.session_state.user_id
    st.sidebar.success(f"✅ Du er logget ind som: **{user_id}**")

    if st.sidebar.button("Log ud"):
        if st.session_state.annotations:
            threading.Thread(target=save_annotations, args=(user_id, st.session_state.annotations), daemon=True).start()
            st.session_state.annotations = []
        st.session_state.clear()
        st.rerun()

# 🚨 Block annotation until user logs in
if "user_id" not in st.session_state:
    st.warning("Indtast dit bruger-ID ude til venstre for at begynde at annotere.")
    st.stop()

# ✅ Ensure each user has their personal worksheet (but do not block UI)
if not st.session_state.get("worksheet_ready", False):
    threading.Thread(target=get_user_worksheet, args=(user_id,), daemon=True).start()
    st.session_state.worksheet_ready = True

# --- LOAD TEXTS FROM LOCAL FILE ---
BASE_DIR = os.getcwd()
DATA_FILE = os.path.join(BASE_DIR, "data", "clean", "processed_texts.txt")

if not os.path.exists(DATA_FILE):
    st.error("Text file missing! Run `preprocess.py` first.")
    st.stop()

with open(DATA_FILE, "r", encoding="utf-8") as file:
    texts = [line.strip() for line in file if line.strip()]

df_texts = pd.DataFrame(texts, columns=["text"])

# ✅ Remove already annotated texts
unannotated_texts = df_texts[~df_texts["text"].isin(st.session_state.annotated_texts)]["text"].tolist()

# ✅ Ensure `text_index` is initialized correctly
if "text_index" not in st.session_state or st.session_state.text_index == -1:
    st.session_state.text_index = 0

# ✅ If all texts are annotated, trigger completion message immediately
if len(unannotated_texts) == 0 or st.session_state.get("finished", False):
    st.session_state.finished = True
    st.success("🎉 Du har annoteret alle tekster!")
    st.info("✅ Du kan nu logge ud via knappen i sidebaren.")
    
    if st.session_state.annotations:
        threading.Thread(target=save_annotations, args=(user_id, st.session_state.annotations), daemon=True).start()
        st.session_state.annotations = []
    
    st.stop()

# ✅ If user has finished all texts, show completion message
if st.session_state.text_index >= len(unannotated_texts):
    st.session_state.finished = True
    st.success("🎉 Du har annoteret alle tekster!")
    st.info("✅ Du kan nu logge ud via knappen i sidebaren.")

    if st.session_state.annotations:
        threading.Thread(target=save_annotations, args=(user_id, st.session_state.annotations.copy()), daemon=True).start()
        st.session_state.annotations = []

    st.stop()

# ✅ Get the next text properly
current_text = unannotated_texts[st.session_state.text_index]

# --- TEXT HIGHLIGHTING ---
st.markdown("## Vælg en komponent, og marker tekst:")
st.markdown("#### Du må gerne markere flere - der kan f.eks. være flere påstande end én i et tekststykke.")

#selections = label_select(
#    body=current_text,
#    labels=["Stretch", "Dodge", "Omission", "Deflection"]
#)

# Convert Markdown-style bold (**text**) to HTML-style bold (<b>text</b>)
formatted_text = current_text.replace("**", "<b>", 1).replace("**", "</b>", 1)

selections = label_select(
    body=formatted_text,
    labels=["Stretch", "Dodge", "Omission", "Deflection"]
)

# Convert selections to a list of dictionaries if needed
selection_data = selections if isinstance(selections, list) else []

# --- Format Selections nicely ---
formatted_selections = {}
for s in selection_data:
    for label in s.labels:
        formatted_selections.setdefault(label, []).append(s.text)

# Display formatted selections
st.markdown("#### Dine annotationer:")
for label, texts in formatted_selections.items():
    st.write(f"**{label}:** {' , '.join(texts)}")

# Automatically disable the button if no selections are made
submit_button_disabled = len(selection_data) == 0

# --- Submit button ---
submit_button = st.button("Gem annotation", disabled=submit_button_disabled)

if submit_button:
    # Extract text per label from recorded selections
    stretch_text = " ".join([s.text for s in selection_data if 'Stretch' in s.labels])
    dodge_text = " ".join([s.text for s in selection_data if 'Dodge' in s.labels])
    omission_text = " ".join([s.text for s in selection_data if 'Omission' in s.labels])
    deflection_text = " ".join([s.text for s in selection_data if 'Deflection' in s.labels])

    annotation_data = [
        user_id,
        st.session_state.text_index,
        current_text,
        stretch_text,
        dodge_text,
        omission_text,
        deflection_text,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

    st.session_state.annotations.append(annotation_data)

    # Save annotations in batches of 5
    if len(st.session_state.annotations) >= 5:
        threading.Thread(target=save_annotations, args=(user_id, st.session_state.annotations.copy()), daemon=True).start()
        st.session_state.annotations = []

    # Move to the next text
    st.session_state.text_index += 1
    st.rerun()
