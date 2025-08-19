# auth.py

import streamlit as st
import smtplib
import random

# Email sender configuration - replace with your credentials
SENDER_EMAIL = "your_gmail@gmail.com"
APP_PASSWORD = "your_app_password"

# In-memory database for users and OTP storage
users = {}
otps = {}


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp_email(email, otp):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        subject = "Your Scrap Marketplace OTP"
        body = f"Your OTP for login is: {otp}"
        msg = f"Subject: {subject}\n\n{body}"
        smtp.sendmail(SENDER_EMAIL, email, msg)


# Seller registration
def seller_registration(username, password, email=None, caller_app=False):
    if not username or not password:
        if not caller_app:
            st.error("Please fill username and password.")
        return False

    if username in users:
        if not caller_app:
            st.error("Username already exists.")
        return False
    else:
        users[username] = {"password": password, "role": "seller", "email": email}
        if not caller_app:
            st.success("Seller registered successfully! Please login.")
        return True


# Seller login
def seller_login(username, password, caller_app=False):
    if username in users and users[username]["password"] == password and users[username]["role"] == "seller":
        if not caller_app:
            st.success(f"Logged in as seller: {username}")
        return username
    else:
        if not caller_app:
            st.error("Invalid seller credentials.")
        return None


# Buyer registration
def buyer_registration(username, password, email=None, caller_app=False):
    if not username or not password:
        if not caller_app:
            st.error("Please fill username and password.")
        return False

    if username in users:
        if not caller_app:
            st.error("Username already exists.")
        return False
    else:
        users[username] = {"password": password, "role": "buyer", "email": email}
        if not caller_app:
            st.success("Registration successful! Please login using your username and password.")
        return True


# Buyer login
def buyer_login(username, password, caller_app=False):
    if username in users and users[username]["password"] == password and users[username]["role"] == "buyer":
        if not caller_app:
            st.success(f"Logged in as buyer: {username}")
        return username
    else:
        if not caller_app:
            st.error("Invalid buyer credentials.")
        return None
