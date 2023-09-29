import pyrebase
import streamlit as st

firebaseConfig = {
  "apiKey": st.secrets["apiKey"],
  "authDomain": st.secrets["authDomain"],
  "projectId": st.secrets["projectId"],
  "storageBucket": st.secrets["storageBucket"],
  "messagingSenderId": st.secrets["messagingSenderId"],
  "appId": st.secrets["appId"],
  "measurementId": st.secrets["measurementId"],
  "databaseURL" : st.secrets["databaseURL"]
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
st.session_state.db = db