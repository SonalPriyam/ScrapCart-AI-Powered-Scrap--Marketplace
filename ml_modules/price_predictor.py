import numpy as np
import pandas as pd
import joblib
import streamlit as st
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

DATA_FILE = "ml_modules/scrap_price_dataset.csv"

@st.cache_resource
def get_model_and_encoder():
    model = joblib.load("ml_modules/price_model.pkl")
    encoder = joblib.load("ml_modules/price_encoder.pkl")
    return model, encoder

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

def train_and_save_model():
    df = load_data()
    X = df[["scrap_type", "quantity", "location", "condition"]]
    y = df["expected_price"]

    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_cat = encoder.fit_transform(X[["scrap_type", "location", "condition"]])
    X_final = np.hstack([X_cat, X[["quantity"]].values])

    model = LinearRegression()
    model.fit(X_final, y)
    joblib.dump(model, "ml_modules/price_model.pkl")
    joblib.dump(encoder, "ml_modules/price_encoder.pkl")

def predict_price(scrap_type, quantity, location, condition):
    model, encoder = get_model_and_encoder()
    try:
        X_cat = encoder.transform([[scrap_type, location, condition]])
    except Exception as e:
        # If error, handle unknown value by using all zeros for one-hot features
        n_features = encoder.transform([["Metal", "Delhi", "New"]]).shape[1]
        X_cat = np.zeros((1, n_features))
    X_final = np.hstack([X_cat, np.array([[quantity]])])
    pred_price = model.predict(X_final)
    return round(float(pred_price), 2)

