import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

pipline = load("artifact/pipline.joblib")
df = load("artifact/df.joblib")

# st.title("Car Price Prediction Australia Market App")
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 28px;
        text-align: left;
        color: white;
        font-weight: black;
    }
    </style>
    <h1 class="custom-title">Car Price Prediction App Australia Market </h1>
    """,
    unsafe_allow_html=True
)
st.markdown("<h5 style='text-align: left; color: white;'>Enter Car Details</h5>", unsafe_allow_html=True)

# Config for sorting descending where needed
sort_year_descending = True
sort_cc_descending = True

# Dropdown for Brand
brand_options = sorted(df['brand'].unique())
chosen_brand = st.selectbox("Brand", options=brand_options, key="brand")

# Dropdown for Model (filtered by Brand)
filtered_models = df[df['brand'] == chosen_brand]['model'].unique()
model_options = sorted(filtered_models)
chosen_model = st.selectbox("Model", options=model_options, key="model")

# Dropdown for Name (filtered by Model and Brand)
filtered_names = df[(df['brand'] == chosen_brand) & (df['model'] == chosen_model)]['name'].unique()
name_options = sorted(filtered_names)
chosen_name = st.selectbox("Name", options=name_options, key="name")

# Dividing the rest of the selections into 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Dropdown for Year (sorted descending)
    year_options = sorted(df['year'].unique(), reverse=sort_year_descending)  # Sort years in descending order
    chosen_year = st.selectbox("Year", options=year_options, key="year")

    # Dropdown for Gearbox
    gearbox_options = sorted(df['gearbox'].unique())
    chosen_gearbox = st.selectbox("Gearbox", options=gearbox_options, key="gearbox")

with col2:
    # Input for Kilometers (step 10,000, min = 1, max = 1,100,000)
    chosen_kilometers = st.number_input(
        "Kilometers",
        min_value=1,
        max_value=1_100_000,
        step=10_000,
        value=10_000,  # Default value
        key="kilometers"
    )

    # Dropdown for Status
    status_options = sorted(df['status'].unique())
    chosen_status = st.selectbox("Status", options=status_options, key="status")





with col3:
    # Dropdown for Fuel Type
    fuel_options = sorted(df['fuel'].unique())
    chosen_fuel = st.selectbox("Fuel Type", options=fuel_options, key="fuel")

    # Dropdown for Color
    color_options = sorted(df['color'].unique())
    chosen_color = st.selectbox("Color", options=color_options, key="color")

with col4:
    # Dropdown for Engine CC (sorted ascending)
    cc_options = sorted(df['cc'].unique(), reverse= sort_cc_descending)  # Sort engine capacities ascending
    chosen_cc = st.selectbox("Engine CC", options=cc_options, key="cc")



list_columns = ['brand', 'name', 'model', 'year', 'kilometers', 'gearbox', 'fuel',
       'status', 'cc', 'color', 'price']
if "message_shown" not in st.session_state:
    st.session_state.message_shown = False
if st.button("Predict Car Price"):
    dataframe = pd.DataFrame({
        "brand": [chosen_brand],
        "model": [chosen_model],
        "name": [chosen_name],
        "year": [chosen_year],
        "kilometers": [chosen_kilometers],
        "gearbox": [chosen_gearbox],
        "fuel": [chosen_fuel],
        "status": [chosen_status],
        "cc": [chosen_cc],
        "color": [chosen_color]
    })
    predict = pipline.predict(dataframe)
    st.success(f"Price Estimation: $ {round(predict[0]):,}")
    if not st.session_state.message_shown:
        st.success("Change some details and play with the app!")
        st.session_state.message_shown = True
    st.balloons()


