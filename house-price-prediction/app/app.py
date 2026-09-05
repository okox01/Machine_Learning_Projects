
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "house_price_model.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏠 House Price Prediction")

st.write(
    "Enter the characteristics of a house below "
    "to estimate its sale price."
)

st.divider()


# ============================================================
# INPUTS
# ============================================================

st.subheader("🏡 House Information")

col1, col2, col3 = st.columns(3)


with col1:

    overall_qual = st.slider(
        "Overall Quality",
        min_value=1,
        max_value=10,
        value=5
    )

    gr_liv_area = st.number_input(
        "Living Area (sq ft)",
        min_value=100,
        max_value=10000,
        value=1500,
        step=50
    )

    year_built = st.number_input(
        "Year Built",
        min_value=1800,
        max_value=2026,
        value=2000,
        step=1
    )


with col2:

    garage_cars = st.selectbox(
        "Garage Capacity",
        options=[0, 1, 2, 3, 4],
        index=2
    )

    total_bsmt_sf = st.number_input(
        "Basement Area (sq ft)",
        min_value=0,
        max_value=5000,
        value=800,
        step=50
    )

    first_flr_sf = st.number_input(
        "First Floor Area (sq ft)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=50
    )


with col3:

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=0,
        max_value=10,
        value=3,
        step=1
    )

    full_bath = st.number_input(
        "Full Bathrooms",
        min_value=0,
        max_value=5,
        value=2,
        step=1
    )

    fireplaces = st.number_input(
        "Fireplaces",
        min_value=0,
        max_value=5,
        value=1,
        step=1
    )


st.divider()


# ============================================================
# PREDICTION
# ============================================================

if st.button(
    "💰 Predict House Price",
    use_container_width=True
):

    st.info(
        "Preparing house information for the model..."
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Start with a real row from the training dataset so
    # that all 80 expected features are present.
    # --------------------------------------------------------

    data_path = PROJECT_ROOT / "data" / "train.csv"

    reference_data = pd.read_csv(data_path)

    input_data = reference_data.drop(
        columns=["SalePrice"]
    ).iloc[[0]].copy()


    # --------------------------------------------------------
    # Replace selected features with user input
    # --------------------------------------------------------

    input_data["OverallQual"] = overall_qual

    input_data["GrLivArea"] = gr_liv_area

    input_data["YearBuilt"] = year_built

    input_data["GarageCars"] = garage_cars

    input_data["TotalBsmtSF"] = total_bsmt_sf

    input_data["1stFlrSF"] = first_flr_sf

    input_data["BedroomAbvGr"] = bedrooms

    input_data["FullBath"] = full_bath

    input_data["Fireplaces"] = fireplaces


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(input_data)[0]


    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    st.success("Prediction completed!")

    st.metric(
        label="Estimated House Price",
        value=f"${prediction:,.0f}"
    )

    st.caption(
        "This is an ML estimate and should not be considered "
        "a professional property valuation."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built with Python, Scikit-learn, XGBoost and Streamlit"
)
