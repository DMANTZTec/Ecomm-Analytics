# # import streamlit_authenticator as stauth
# # from pathlib import Path
# # import pickle
# import streamlit as st
# # # from evadellaapp import *
# import pandas as pd
# # import hashlib
# # from streamlit import session_state as state

# # # user authentication
# # names = ["Giridhar", "Yerra"]
# # usernames = ["evadellagiri", "evadellayerra"]


# # file_path = Path(__file__).parent / "hashed_pw.pkl"
# # with file_path.open("rb") as file:
# #     hashed_passwords = pickle.load(file)
    
# #     credentials = {
# #         "usernames":{
# #             usernames[0]:{
# #                 "name":names[0],
# #                 "password":hashed_passwords[0]
# #                 },
# #             usernames[1]:{
# #                 "name":names[1],
# #                 "password":hashed_passwords[1]
# #                 }            
# #             }
# #         }

# # authenticator = stauth.Authenticate(credentials,
# #     "dashborad", "abcdefg", cookie_expiry_days = 30)

# # name, authentication_status, username = authenticator.login("login", "main")

# # # if state.authentication_status:
# # #     return

# # if authentication_status == False:
# #     st.error("Username/Password is incorrect")


# # if authentication_status:
# #     state.authentication_status = True
# #     st.success("You have successfully logged in.")
# #     authenticator.logout("logout")

    
# import mysql.connector

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "swapna2021",
#     database = "ecomm"
# )

# getOrderStatusDf = "SELECT * FROM ecomm.order_status"

# statusDf = pd.read_sql_query(getOrderStatusDf, mydb)

# def highlight_rows(statusDf):
#     if statusDf['status_cd'] == 'PAID':
#         return['background-color : green'] * len(statusDf)
#     else:
#         return['background-color : red'] * len(statusDf)
    
# df = statusDf.style.apply(highlight_rows, axis=1)

# st.dataframe(df)

import streamlit as st
import mysql.connector

# Function to create a database connection
def create_connection():
    conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "swapna2021",
            database = "ecomm"
        )
    return conn

# Function to check login credentials in the database
def check_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ecomm.user WHERE email_id = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Main Streamlit app
def main():
    st.title("Login Page")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = check_login(username, password)
        if user:
            st.success("Logged in successfully!")
            # You can set up session management here
            # For example, store the user's ID or a token in a session state
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()


