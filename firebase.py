import pyrebase
import streamlit as st

firebaseConfig = {
  "apiKey": "AIzaSyBNG1qn6ifqFPl51nhw7m1ri8bhbOeTTpI",
  "authDomain": "portability-55894.firebaseapp.com",
  "projectId": "portability-55894",
  "storageBucket": "portability-55894.appspot.com",
  "messagingSenderId": "25950230197",
  "appId": "1:25950230197:web:5905b77232c86e3d5cd0fc",
  "measurementId": "G-XCFM083G0H",
  "databaseURL" : "https://portability-55894-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
st.session_state.db = db
storage = firebase.storage()
