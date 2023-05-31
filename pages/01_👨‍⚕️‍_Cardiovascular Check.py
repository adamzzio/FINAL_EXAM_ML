# ===== IMPORT LIBRARY =====
# for data wrangling
import pandas as pd
import numpy as np

# for web app
import streamlit as st
from streamlit_chat import message
from streamlit_lottie import st_lottie
from streamlit import components

# for modelling
import pickle as pkl
from lightgbm import LGBMClassifier

# for database
# import firebase_admin
# import csv
# import google.cloud
# from firebase_admin import credentials, firestore

# etc
from PIL import Image
import requests
import pyautogui
from sklearn import preprocessing
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from io import BytesIO

# ===== SET PAGE =====
pageicon = Image.open("aset_foto/CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

# ===== SET SIDEBAR =====
st.sidebar.header("CardioAI : Check Your Patient Heart Attack Risk")

jenis_metode = st.sidebar.selectbox(
    'Pilih Metode Input Data',
    ('AI Chatbot',
     'Form',
     'Batch (Excel)'))
# ===== LOAD MODEL & DATA =====

filename_model = 'model/finalized_model_dt_tuning_v1.sav'

@st.cache_resource
def load_model():
    model = pkl.load(open(filename_model, 'rb'))
    return model

model = load_model()

# ===== SET PAGE IF INPUT EQUAL TO AI =====
if jenis_metode == 'AI Chatbot':
    # Generate empty lists for generated and past.
    ## generated stores AI generated responses
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hi! Aku CardioAI siap membantu Anda. Berapa usia pasien Anda?"]
    ## past stores User's questions
    if 'past' not in st.session_state:
        st.session_state['past'] = [
            'Hi! Saya membutuhkan bantuan Anda untuk memprediksi penyakit jantung dari pasien saya. Apakah Anda bisa membantu saya?']

    # Variables to store user responses
    if 'age' not in st.session_state:
        st.session_state['age'] = None
    if 'gender' not in st.session_state:
        st.session_state['gender'] = None
    if 'heart_rate' not in st.session_state:
        st.session_state['heart_rate'] = None
    if 'systolic' not in st.session_state:
        st.session_state['systolic'] = None
    if 'diastolic' not in st.session_state:
        st.session_state['diastolic'] = None
    if 'blood_sugar' not in st.session_state:
        st.session_state['blood_sugar'] = None
    if 'ckmb' not in st.session_state:
        st.session_state['ckmb'] = None
    if 'troponin' not in st.session_state:
        st.session_state['troponin'] = None

    # Layout of input/response containers
    # input_container = st.container()
    response_container = st.container()
    input_container = st.container()

    # User input
    ## Function for taking user provided prompt as input
    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    ## Applying the user input box
    with input_container:
        user_input = get_text()

    # Response output
    ## Function for taking user prompt as input followed by producing AI generated responses
    def generate_response(prompt):
        if prompt == 'Ya!':
            response = "Berapa usia pasien Anda?"
        elif prompt.isdigit():
            if st.session_state['age'] is None:
                st.session_state['age'] = prompt
                response = "Apa jenis kelamin pasien Anda? (1 jika Laki-laki; 0 jika Perempuan)"
            elif st.session_state['gender'] is None:
                st.session_state['gender'] = prompt
                response = "Berapa detak jantung pasien Anda?"
            elif st.session_state['heart_rate'] is None:
                st.session_state['heart_rate'] = prompt
                response = "Berapa tekanan darah sistolik pasien Anda?"
            elif st.session_state['systolic'] is None:
                st.session_state['systolic'] = prompt
                response = "Berapa tekanan darah diastolik pasien Anda?"
            elif st.session_state['diastolic'] is None:
                st.session_state['diastolic'] = prompt
                response = "Berapa kadar gula darah pasien Anda?"
            elif st.session_state['blood_sugar'] is None:
                st.session_state['blood_sugar'] = prompt
                response = "Berapa kadar CK-MB pasien Anda?"
            elif st.session_state['ckmb'] is None:
                st.session_state['ckmb'] = prompt
                response = "Berapa kadar troponin pasien Anda?"
            elif st.session_state['troponin'] is None:
                st.session_state['troponin'] = prompt
                response = "Terima kasih. Data pasien telah tercatat. Silakan melihat hasil diagnosisnya di bawah"
            else:
                response = "Oke. Terima kasih."

        elif prompt.replace('.', '', 1).isdigit():
            if st.session_state['age'] is None:
                st.session_state['age'] = float(prompt)
                response = "Apa jenis kelamin pasien Anda? (1 jika Laki-laki; 0 jika Perempuan)"
            elif st.session_state['gender'] is None:
                st.session_state['gender'] = float(prompt)
                response = "Berapa detak jantung pasien Anda?"
            elif st.session_state['heart_rate'] is None:
                st.session_state['heart_rate'] = float(prompt)
                response = "Berapa tekanan darah sistolik pasien Anda?"
            elif st.session_state['systolic'] is None:
                st.session_state['systolic'] = float(prompt)
                response = "Berapa tekanan darah diastolik pasien Anda?"
            elif st.session_state['diastolic'] is None:
                st.session_state['diastolic'] = float(prompt)
                response = "Berapa kadar gula darah pasien Anda?"
            elif st.session_state['blood_sugar'] is None:
                st.session_state['blood_sugar'] = float(prompt)
                response = "Berapa kadar CK-MB pasien Anda?"
            elif st.session_state['ckmb'] is None:
                st.session_state['ckmb'] = float(prompt)
                response = "Berapa kadar troponin pasien Anda?"
            elif st.session_state['troponin'] is None:
                st.session_state['troponin'] = float(prompt)
                response = "Terima kasih. Data pasien telah tercatat. Silakan melihat hasil diagnosisnya di bawah"
            else:
                response = "Oke. Terima kasih."

        else:
            response = "Maaf, saya tidak mengerti. Bisakah Anda memberikan informasi lebih lanjut?"
        return response

    # Conditional display of AI generated responses as a function of user provided prompts
    with response_container:
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)

        if 'generated' in st.session_state:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

    if st.button("Reset", use_container_width=True):
#         pyautogui.hotkey("ctrl","F5")
        st.markdown('<meta http-equiv="refresh" content="0;URL=https://cardiocheck-v2.streamlit.app/%E2%80%8D_Cardiovascular_Check" />', unsafe_allow_html=True)

    # SAVE RESULT TO DATAFRAME
    df_result = pd.DataFrame({'Age': [st.session_state['age']],
                              'Gender': [st.session_state['gender']],
                              'Heart rate': [st.session_state['heart_rate']],
                              'Systolic blood pressure': [st.session_state['systolic']],
                              'Diastolic blood pressure': [st.session_state['diastolic']],
                              'Blood sugar': [st.session_state['blood_sugar']],
                              'CK-MB': [st.session_state['ckmb']],
                              'Troponin': [st.session_state['troponin']]})

    # Display DataFrame if all variables are filled
    if all(value is not None for value in df_result.iloc[0].values):
        st.dataframe(df_result, use_container_width=True)
        result = model.predict(df_result.values)
        result_proba = model.predict_proba(df_result.values)
        # result_proba = str(result_proba)
        result_proba = np.max(result_proba[0])
        result_proba = np.round(result_proba, 2)
        result_proba = result_proba * 100
        st.write(result)
        st.write(result_proba)
        if result == 0:
            text_result = "Pasien Anda memiliki peluang untuk dinyatakan negatif memiliki penyakit jantung"
            st.success(text_result)
            st.balloons()
            # SUBMIT PREDICTIONS TO DATABASE
            # df_result['Result'] = result
            # df_result['Result'] = df_result['Result'].replace(0, 'negative')
            # df_result['Result'] = df_result['Result'].replace(1, 'positive')
            # st.dataframe(df_result)
        else:
            text_result = "Pasien Anda memiliki peluang untuk dinyatakan positif memiliki penyakit jantung"
            st.error(text_result)
            st.balloons()
            # SUBMIT PREDICTIONS TO DATABASE
            # df_result['Result'] = result
            # df_result['Result'] = df_result['Result'].replace(0, 'negative')
            # df_result['Result'] = df_result['Result'].replace(1, 'positive')
            # st.dataframe(df_result)

        st.markdown('<hr>', unsafe_allow_html=True)

    js = f"""
    <script>
        function scroll(dummy_var_to_force_repeat_execution){{
            var textAreas = parent.document.querySelectorAll('section.main');
            for (let index = 0; index < textAreas.length; index++) {{
                textAreas[index].style.color = 'white'
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}
        scroll({len(st.session_state.generated)})
    </script>
    """

    st.components.v1.html(js)

elif jenis_metode == 'Form':
    st.header('Formulir Data Prediksi Jantung')
    st.markdown('<hr>', unsafe_allow_html=True)

    # CREATE FORM
    age = st.number_input(label='Masukkan usia pasien : ', min_value=18, max_value=80, step=1, key='1')
    gender = st.selectbox('Masukkan jenis kelamin pasien', ('Laki-Laki', 'Perempuan'))
    heart_rate = st.number_input(label='Masukkan detak jantung pasien : ', min_value=0, max_value=200, step=10, key='2')
    systolic = st.number_input(label='Masukkan tekanan sistolik pasien : ', min_value=0, max_value=200, step=10,
                               key='3')
    diastolic = st.number_input(label='Masukkan tekanan diastolik pasien : ', min_value=0, max_value=200, step=10,
                                key='4')
    blood_sugar = st.number_input(label='Masukkan kadar gula darah pasien : ', min_value=0, max_value=1000, step=10,
                                  key='5')
    ckmb = st.number_input(label='Masukkan kadar CK-Mb pasien : ', min_value=0.0, max_value=100, step=0.1, key='6')
    troponin = st.number_input(label='Masukkan kadar troponin pasien : ', min_value=0.0, max_value=100.0, step=0.1,
                               key='7')

    submit = st.button("Submit", use_container_width=True)

    # ===== BACK-END SESSIONS ======
    # SAVE RESULT TO DATAFRAME
    df_result = pd.DataFrame({'Age': [age],
                              'Gender': [gender],
                              'Heart rate': [heart_rate],
                              'Systolic blood pressure': [systolic],
                              'Diastolic blood pressure': [diastolic],
                              'Blood sugar': [blood_sugar],
                              'CK-MB': [ckmb],
                              'Troponin': [troponin]})

    gender_dict = {'Laki-Laki': 1,
                   'Perempuan': 0}
    df_result['Gender'] = df_result['Gender'].map(gender_dict)

    # DO PREDICTIONS
    if submit:
        result = model.predict(df_result.values)
        result_proba = model.predict_proba(df_result.values)
        # result_proba = str(result_proba)
        result_proba = np.max(result_proba[0])
        result_proba = np.round(result_proba, 2)
        result_proba = result_proba * 100
        if result == 0:
            text_result = "Pasien Anda memiliki peluang " + str(
                result_proba) + "% dinyatakan negatif memiliki penyakit jantung"
            st.error(text_result)
            st.balloons()
            # SUBMIT PREDICTIONS TO DATABASE
            # df_result['Result'] = result
            # df_result['Result'] = df_result['Result'].replace(0, 'negative')
            # df_result['Result'] = df_result['Result'].replace(1, 'positive')
            # st.dataframe(df_result)
        else:
            text_result = "Pasien Anda memiliki peluang " + str(
                result_proba) + "% dinyatakan positif memiliki penyakit jantung"
            st.success(text_result)
            st.balloons()
            # SUBMIT PREDICTIONS TO DATABASE
            # df_result['Result'] = result
            # df_result['Result'] = df_result['Result'].replace(0, 'negative')
            # df_result['Result'] = df_result['Result'].replace(1, 'positive')
            # st.dataframe(df_result)

        st.markdown('<hr>', unsafe_allow_html=True)

elif jenis_metode == 'Batch (Excel)':
    st.header('Upload File Excel')
    st.markdown('<hr>', unsafe_allow_html=True)
    # LOAD DUMMY DATA
    @st.cache_resource
    def load_data():
        # Load dataset
        data_dummy = pd.read_excel('data/Data_Contoh.xlsx')
        return data_dummy


    data_dummy = load_data()

    st.error("WARNING : PASTIKAN FILE EXCEL MEMILIKI FORMAT SEBAGAI BERIKUT!!! ")
    # display dataframe
    st.dataframe(data_dummy, use_container_width=True)

    # list of expected column names and their corresponding data types
    EXPECTED_COLUMNS = [
        ('Age', object),
        ('Gender', int),
        ('Heart rate', float),
        ('Systolic blood pressure', float),
        ('Diastolic blood pressure', float),
        ('Blood sugar', float),
        ('CK-MB', float),
        ('Troponin', float)
    ]

    try:
        # read the user uploaded Excel file
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xls", "xlsx"])

        if uploaded_file is not None:
            # read the Excel file into a Pandas dataframe
            df = pd.read_excel(uploaded_file)

            # check if the dataframe has the expected columns and data types
            column_names = set(df.columns)
            expected_column_names = set([col[0] for col in EXPECTED_COLUMNS])
            if column_names != expected_column_names:
                raise ValueError(
                    f"Column names do not match. Expected {expected_column_names}, but got {column_names}.")

            for col, dtype in EXPECTED_COLUMNS:
                if col in df.select_dtypes(include=[int, float]).columns:
                    if not pd.api.types.is_integer_dtype(df[col]) and not pd.api.types.is_float_dtype(df[col]):
                        raise ValueError(
                            f"Column '{col}' has wrong data type. Expected {dtype}, but got {df[col].dtype}.")

            # if everything is OK, then predict it
            df_model = df.copy()
            prediksi = model.predict(df_model.values)
            df['Hasil_Prediksi'] = prediksi

            # if everything is OK, display the dataframe
            st.dataframe(df, use_container_width=True)

            # output
            # create a BytesIO object to hold the Excel data
            excel_data = BytesIO()

            # write the DataFrame to the BytesIO object as an Excel file
            df.to_excel(excel_data, index=False)

            # create a download button for the Excel file
            button = st.download_button(
                label="Download file",
                data=excel_data.getvalue(),
                file_name="Hasil_Prediksi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        # throw exception error
    except ValueError as e:
        st.warning(str(e))
    except Exception as e:
        st.error(str(e))
