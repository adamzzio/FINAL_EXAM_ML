# ===== IMPORT LIBRARY =====
# for data wrangling
import pandas as pd
import numpy as np

# for web app
import streamlit as st
from streamlit_star_rating import st_star_rating

# for database
import firebase_admin
import csv
import google.cloud
from firebase_admin import credentials, firestore

# etc
from PIL import Image
import requests

# SET PAGE
pageicon = Image.open("aset_foto/CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

def get_firebase_app():
    # Periksa apakah aplikasi Firebase sudah ada
    if not firebase_admin._apps:
        # Jika belum ada, inisialisasi Firebase Admin SDK
        cred = credentials.Certificate("test-db-19c39-firebase-adminsdk-3noie-95deabbed0.json")
        firebase_admin.initialize_app(cred)
    # Kembalikan referensi ke aplikasi Firebase
    return firebase_admin.get_app()

def save_data_to_firebase_feedback(feedback):
    app = get_firebase_app()
    db = firestore.client(app)
    collection_name = "feedback"
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(feedback)

# SET HEADER
st.header('Formulir Feedback')
st.markdown('<hr>', unsafe_allow_html=True)

st.write('### Berikan rating Anda untuk Web App ini!')

_, star, _ = st.columns([6,9,1])
with star:
    stars = st_star_rating(label = " ", maxValue = 5, defaultValue = 3,
                           key = "rating", dark_theme = True)

option = st.selectbox(
    'Bagaimana perasaan Anda dengan performa Web App ini?',
    ('Puas', 'Tidak Puas'))

ulasan = st.text_area('Berikan ulasan Anda mengenai web app ini!')

submit = st.button('Submit')
if submit:
    dict_result = {'Stars':str(stars),
                   'Tingkat Kepuasan':option,
                   'Ulasan':ulasan}

    save_data_to_firebase_feedback(dict_result)
    st.success("Feedback Anda sudah berhasil disimpan ke database")
