# ===== IMPORT LIBRARY =====
# for data wrangling
import pandas as pd
import numpy as np

# for web app
import streamlit as st
from streamlit_lottie import st_lottie

# for modelling
import pickle as pkl
# from lightgbm import LGBMClassifier

# for database
# import firebase_admin
# import csv
# import google.cloud
# from firebase_admin import credentials, firestore
# # from google.cloud import firestore

# etc
from PIL import Image
import requests

# ===== SET PAGE =====
pageicon = Image.open("aset_foto/CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

# ===== DEVELOP FRONT-END =====
# SET HEADER PAGE
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_uwWgICKCxj.json")

intro_column_left, intro_column_right = st.columns(2)
with st.container():
    with intro_column_left:
        # st.title(":bar_chart: Dashboard")
        st.markdown('<div style="text-align: justify; font-size:300%; line-height: 150%; margin-top: -55px;"> <b><br>CardioCheck: Your Reliable Cardiovascular Decision Support </b> </div>',
            unsafe_allow_html=True)
    with intro_column_right:
        st_lottie(lottie_coding, height=250, key="dashboard")

st.markdown('<hr>', unsafe_allow_html=True)

# SET DESCRIPTION
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> CardioCheck adalah sebuah aplikasi web yang bertujuan menjadi alat bantu pengambil keputusan yang handal dalam bidang kesehatan kardiovaskular. Dengan visi "Empowering Informed Decisions" CardioCheck dirancang untuk memberikan informasi yang akurat dan cepat kepada para tenaga ahli terkait, seperti dokter, dalam proses pengambilan keputusan terkait kondisi kardiovaskular.</div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Fungsi utama CardioCheck adalah melakukan pengecekan dan evaluasi kondisi kardiovaskular berdasarkan data pasien. Dengan menggunakan model Machine Learning yang terlatih, aplikasi ini memberikan prediksi risiko penyakit jantung berdasarkan faktor-faktor seperti usia, jenis kelamin, tekanan darah, kolesterol, dan variabel lainnya.</div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Kami adalah tim yang berdedikasi di balik CardioCheck, terdiri dari para ahli kesehatan dan ilmu data yang memiliki komitmen kuat terhadap pengembangan solusi inovatif dalam bidang kardiovaskular. Dengan pengetahuan medis yang mendalam dan keahlian dalam analisis data, kami berupaya memberikan alat yang dapat diandalkan bagi para tenaga ahli terkait dalam mendukung pengambilan keputusan yang lebih baik.</div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Dengan CardioCheck, kami berharap dapat memberikan solusi yang memberdayakan para dokter dalam membuat keputusan yang informasional dan terarah dalam hal kardiovaskular, sehingga meningkatkan kualitas perawatan pasien dan memberikan manfaat yang signifikan bagi komunitas medis. </div>',
            unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# SET PFP
col1, col2, col3 = st.columns(3)

foto_adamz = Image.open('aset_foto/Adam.png').resize((400,400))
foto_razin = Image.open('aset_foto/Razin.png').resize((400,400))
foto_fikri = Image.open('aset_foto/Fikri.png').resize((400,400))

# For columns 1 : Introduce Adam Maurizio Winata
col1.write('### Adam Maurizio Winata')
col1.image(foto_adamz, caption = "162012133045")

# For columns 2 : Introduce Razin Isyraq Thirafi
col2.write('### Razin Isyraq Thirafi')
col2.image(foto_razin, caption = "162012133056")

# For columns 3 : Introduce Fikri Arif Abdillah
col3.write('### Fikri Arif Abdillah')
col3.image(foto_fikri, caption = "162012133051")