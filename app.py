import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("churn_model.pkl")

st.title("Customer Churn Prediction")

st.write("Enter customer details:")

# Inputs
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)
total_charges = st.number_input("Total Charges", 0.0, 10000.0, 500.0)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# Create input dictionary
input_dict = {}

# Default all features = 0
for col in model.feature_names_in_:
    input_dict[col] = 0

# Fill numeric
input_dict['tenure'] = tenure
input_dict['MonthlyCharges'] = monthly_charges
input_dict['TotalCharges'] = total_charges

# Encode contract
if contract == "One year":
    input_dict['Contract_One year'] = 1
elif contract == "Two year":
    input_dict['Contract_Two year'] = 1

# Encode internet
if internet == "Fiber optic":
    input_dict['InternetService_Fiber optic'] = 1
elif internet == "No":
    input_dict['InternetService_No'] = 1

input_df = pd.DataFrame([input_dict])

# Prediction
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    
    if prediction == 1:
        st.error("⚠ Customer likely to churn")
    else:
        st.success("✅ Customer likely to stay")