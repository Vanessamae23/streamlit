import json
import os
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from models import load_sentiment_pipeline, load_skills_regonition_pipeline, generate_recommendations
from firebase import db
from firebase import auth


# Streamlit page configs

page_icon = Image.open('images/compass.png')
st.set_page_config(layout="wide", page_title="Nautical HR Analytics", page_icon=page_icon)
st.image('images/banner.png')
st.title("Nautical HR Analytics")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)



# Create a function for each view or tab
def employee_data():
    st.header("Employee Data")
        
    # Apply styling to the DataFrame
    th_props = [
      ('font-size', '14px'),
      ('text-align', 'left'),
      ('font-weight', 'bold'),
      ('color', '#fff'),
      ('text-transform', 'uppercase'),
      ('background-color', '#808080')
      ]
                                  
    td_props = [
      ('font-size', '12px'),
      ('text-align', 'left'),
      ('text-transform', 'uppercase'),
      ]
    styles = [
      dict(selector="th", props=th_props),
      dict(selector="td", props=td_props)
    ]
    df2 = df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df2)
if 'authenticated' not in st.session_state:
  email = st.sidebar.text_input('Enter your email address')
  password = st.sidebar.text_input('Enter your password', type = 'password')
  submit = st.sidebar.button('Sign In')
  if submit :
      try: 
          user = auth.sign_in_with_email_and_password(email, password)
          username = db.child('employees').child(user['localId']).get()
          admin = db.child('employees').child(user['localId']).child('isAdmin').get()
          
          if admin == False:
            raise ValueError("User is not an admin")  # Raise a ValueError when the user is not an admin
         
          if user is not None :
              st.session_state.authenticated = True
          st.success("Successfully signed in")
          def employee_data():
                  st.header("Employee Data")
                  
                  data = db.child('employees').get()
                  json_data = json.dumps(data.val(), indent=4)
                  json_dict = json.loads(json_data)
                  df = pd.DataFrame(json_dict.values())
                  
                  # Apply styling to the DataFrame
                  th_props = [
                    ('font-size', '14px'),
                    ('text-align', 'left'),
                    ('font-weight', 'bold'),
                    ('color', '#fff'),
                    ('text-transform', 'uppercase'),
                    ('background-color', '#808080')
                    ]
                                                
                  td_props = [
                    ('font-size', '12px'),
                    ('text-align', 'left'),
                    ('text-transform', 'uppercase'),
                    ]
                  styles = [
                    dict(selector="th", props=th_props),
                    dict(selector="td", props=td_props)
                  ]
                  df2 = df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
                  st.table(df2)


          def analytics_dashboard():
              st.header("Analytics Dashboard")
              #Skills
              data = db.child('employees').get()
              json_data = json.dumps(data.val(), indent=4)
              df = pd.read_json(json_data).T

              skills_data = db.child('skills').get()
              skills_json_data = json.dumps(skills_data.val(), indent=4)
              skills_df = pd.read_json(skills_json_data).T
              skills_df.style
              # Calculate the mean for each skill
              skill_means = skills_df.mean()
              db.child("skill_means").set(skill_means.to_dict())
              # Display the mean values in a bar chart using Streamlit
              st.bar_chart(skill_means)

              # Perform linear regression and create regression line plots for each skill
              for skill_column in skills_df.columns:
                  
                  y = df['performance'].tolist()
                  x = skills_df[skill_column].tolist()[0:len(y)]
                  y = y[0:min(len(x), len(y))]
                  # Adding the constant term
                  x = sm.add_constant(x)
                  
                  # Performing the regression and fitting the model
                  result = sm.OLS(y, x).fit()
                  # Create a new figure for each skill plot
                  fig, ax = plt.subplots(figsize=(8, 6))
                  
                  max_x = skills_df[skill_column].max()
                  min_x = skills_df[skill_column].min()
                  x_values = np.arange(min_x, max_x, 1)
                  y_values = result.params[1] * x_values + result.params[0]
                  
                  # Plot the regression line
                  ax.plot(x_values, y_values, 'r', label='Regression Line')
                  
                  # Set labels and legend
                  ax.set_xlabel(skill_column.upper())
                  ax.set_ylabel("Performance")
                  ax.legend()
                  
                  final = round(result.params[1], 2)
                  st.subheader(skill_column.upper())
                  st.markdown("By increasing the company's " + skill_column + " skill, performance can change by " + str(final))

                  
                  # Display the plot in Streamlit
                  st.pyplot(fig)


          def ai_insights():
              st.header("Artificial Intelligence Insights")
              #Feedback
              feedback_sentiment_pipeline = load_sentiment_pipeline()
              feedback_data = db.child('feedback').get()
              feedback_json_data = json.dumps(feedback_data.val(), indent=4)
              json_dict = json.loads(feedback_json_data)
              feedback_df = pd.DataFrame(json_dict.values())
              feedback_df.rename(columns = {0:'feedback'}, inplace = True)
              feedback_df['Sentiment (1 to 5)'] = feedback_df['feedback'].apply(lambda x: feedback_sentiment_pipeline(x)[0]['label'][:-5])
              feedback_df['score'] = feedback_df['feedback'].apply(lambda x: feedback_sentiment_pipeline(x)[0]['score'])

              # Define a function to apply text wrap styling to the DataFrame
              th_props = [
                ('font-size', '14px'),
                ('text-align', 'left'),
                ('font-weight', 'bold'),
                ('color', '#fff'),
                ('text-transform', 'uppercase'),
                ('background-color', '#808080')
                ]
                                            
              td_props = [
                ('font-size', '12px'),
                ('text-align', 'left'),
                ('text-transform', 'uppercase'),
                ]
              styles = [
                dict(selector="th", props=th_props),
                dict(selector="td", props=td_props)
              ]
              df2 = feedback_df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
              st.table(df2)


          # Create a sidebar with tabs
          selected_view = st.sidebar.selectbox("Select a view:", ["Employee Data", "Analytics Dashboard",  "Artificial Intelligence Insights"])

          # Define a dictionary to map view names to functions
          views = {
              "Employee Data": employee_data,
              "Analytics Dashboard": analytics_dashboard,
              "Artificial Intelligence Insights": ai_insights
          }

          # Display the selected view
          if selected_view in views:
              views[selected_view]()  # Call the selected view function
          else:
              st.write("Invalid view selection.")




      except Exception as e : 
              st.info(e)
      else :    
          st.write("Welcome")
else :
  
  def employee_data():
      st.header("Employee Data")
      
      data = db.child('employees').get()
      json_data = json.dumps(data.val(), indent=4)
      df = pd.read_json(json_data).T
      
      # Apply styling to the DataFrame
      th_props = [
        ('font-size', '14px'),
        ('text-align', 'left'),
        ('font-weight', 'bold'),
        ('color', '#fff'),
        ('text-transform', 'uppercase'),
        ('background-color', '#808080')
        ]
                                    
      td_props = [
        ('font-size', '12px'),
        ('text-align', 'left'),
        ('text-transform', 'uppercase'),
        ]
      styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
      ]
      df2 = df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
      st.table(df2)


  def analytics_dashboard():
      st.header("Analytics Dashboard")
      #Skills
      data = db.child('employees').get()
      json_data = json.dumps(data.val(), indent=4)
      df = pd.read_json(json_data).T

      skills_data = db.child('skills').get()
      skills_json_data = json.dumps(skills_data.val(), indent=4)
      skills_df = pd.read_json(skills_json_data).T
      skills_df.style
      # Calculate the mean for each skill
      skill_means = skills_df.mean()
      db.child("skill_means").set(skill_means.to_dict())
      # Display the mean values in a bar chart using Streamlit
      st.bar_chart(skill_means)

      cols = st.columns([1,1,1,1])

      # Perform linear regression and create regression line plots for each skill
      col_num = 0
      for skill_column in skills_df.columns:
        y = df['performance'].tolist()
        x = skills_df[skill_column].tolist()[0:len(y)]
        y = y[0:min(len(x), len(y))]
        # Adding the constant term
        x = sm.add_constant(x)
        
        # Performing the regression and fitting the model
        result = sm.OLS(y, x).fit()
        # Create a new figure for each skill plot
        fig, ax = plt.subplots(figsize=(8, 6))
        
        max_x = skills_df[skill_column].max()
        min_x = skills_df[skill_column].min()
        x_values = np.arange(min_x, max_x, 1)
        y_values = result.params[1] * x_values + result.params[0]
        
        # Plot the regression line
        ax.plot(x_values, y_values, 'r', label='Regression Line')
        
        # Set labels and legend
        ax.set_xlabel(skill_column.upper())
        ax.set_ylabel("Performance")
        ax.legend()
        
        final = round(result.params[1], 2)
        st.subheader(skill_column.upper())
        st.markdown("By increasing the company's " + skill_column + " skill, performance can change by " + str(final))

        
        # Display the plot in Streamlit
        with cols[col_num]:
          st.pyplot(fig)
        col_num += 1


def ai_insights():
    st.header("Artificial Intelligence Insights")
    #Feedback
    feedback_sentiment_pipeline = load_sentiment_pipeline()
    feedback_data = db.child('feedback').get()
    feedback_json_data = json.dumps(feedback_data.val(), indent=4)
    json_dict = json.loads(feedback_json_data)
    feedback_df = pd.DataFrame(json_dict.values())
    feedback_df.rename(columns = {0:'feedback'}, inplace = True)
    feedback_df['Sentiment (1 to 5)'] = feedback_df['feedback'].apply(lambda x: feedback_sentiment_pipeline(x)[0]['label'][:-5])
    feedback_df['score'] = feedback_df['feedback'].apply(lambda x: feedback_sentiment_pipeline(x)[0]['score'])
    
    # Define a function to apply text wrap styling to the DataFrame
    th_props = [
      ('font-size', '14px'),
      ('text-align', 'left'),
      ('font-weight', 'bold'),
      ('color', '#fff'),
      ('background-color', '#808080')
      ]
                                  
    td_props = [
      ('font-size', '12px'),
      ('text-align', 'left'),
      ]
    styles = [
      dict(selector="th", props=th_props),
      dict(selector="td", props=td_props)
    ]
    df2 = feedback_df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df2)

      #Employee upskilling

    employee_data = db.child('employees').get()
    employee_df = pd.DataFrame(map(lambda x: generate_recommendations(x),list(employee_data)), columns=['Recommendations'])


    df3 = employee_df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df3)


# Create a sidebar with tabs
selected_view = st.sidebar.selectbox("Select a view:", ["Employee Data", "Analytics Dashboard",  "Artificial Intelligence Insights"])

# Define a dictionary to map view names to functions
views = {
    "Employee Data": employee_data,
    "Analytics Dashboard": analytics_dashboard,
    "Artificial Intelligence Insights": ai_insights
}

# Display the selected view
if selected_view in views:
    views[selected_view]()  # Call the selected view function
else:
    st.write("Invalid view selection.")
