import streamlit as st
import pandas as pd
from PIL import Image
import re
import sqlite3 

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


st.set_page_config(page_title="Forecasting Crime Trends", page_icon="fevicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Welcome To Forecasting Crime Trends")
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://img.freepik.com/free-vector/gray-abstract-wireframe-background_53876-99911.jpg?semt=ais_hybrid");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()


menu = ["Home","SignUp","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.markdown(
    """
    <p align="justify">
    <b style="color:black">This study explores the use of machine learning and data analytics to forecast crime trends against women in India, leveraging historical crime data from publicly available sources. With crimes against women remaining a critical societal issue, this project aims to uncover patterns, identify high-risk regions, and predict future trends to support proactive policy-making and resource allocation. Key techniques include data preprocessing, exploratory data analysis (EDA), and predictive modeling using time-series forecasting and regression techniques. The findings highlight significant temporal and spatial trends, offering data-driven insights into factors influencing women's safety. By integrating visualization tools and actionable recommendations, this work aims to aid stakeholders in enhancing preventive measures and fostering a safer environment for women.</b>
    </p>
    """
    ,unsafe_allow_html=True)
    
elif choice == "SignUp":
    FirstName = st.text_input("Firstname")
    LastName = st.text_input("Lastname")
    Mobile = st.text_input("Mobile")
    City = st.text_input("City")
    Email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    Cpassword = st.text_input("Confirm Password",type='password')
    if st.button("Signup"):
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                add_userdata(FirstName,LastName,Mobile,City,Email,new_password,Cpassword)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                 st.warning("Not Valid Email")
        else:
             st.warning("Not Valid Mobile Number")
             
elif choice == "Login":
    st.subheader("Login Section")
    Email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type='password')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if st.sidebar.checkbox("Login"):
        if re.fullmatch(regex, Email):
            if Email=="a@a.com" and password=="123":
                st.success("Welcome to Admin")
                create_usertable()
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)              
            else:               
                result = login_user(Email,password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    st.subheader("Upload .CSV File Only")
                    uploaded_file = st.file_uploader("Choose a file")
                    if uploaded_file:
                        dataframe = pd.read_csv(uploaded_file)
                        st.dataframe(dataframe, 1500, 200)
                        task2 = st.selectbox("Selection ML",["LR","SVR","KNN","DT"])
                        st.button("Apply Regression")
                    else:
                        st.error("upload .csv file")                           
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")