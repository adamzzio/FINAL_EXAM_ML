# ===== IMPORT LIBRARY =====
# for data wrangling
import pandas as pd
import numpy as np

# for web app
import streamlit as st
from streamlit_star_rating import st_star_rating

# etc
from PIL import Image
import requests

# SET PAGE
pageicon = Image.open("aset_foto/CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

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

    st.write(dict_result)