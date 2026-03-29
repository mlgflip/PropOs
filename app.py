import streamlit as st
import pickle
import numpy as np
import pandas as pd

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("encoder.pkl", "rb") as f:
    le = pickle.load(f)

df = pd.read_csv("miami_rentals.csv")

st.set_page_config(page_title="PropOS", page_icon="🏠", layout="centered")
st.title("PropOS — Miami Rent Predictor")
st.subheader("Enter property details to get a rent estimate")

col1, col2 = st.columns(2)

with col1:
    beds = st.number_input("Bedrooms", min_value=0, max_value=10, value=2)
    baths = st.number_input("Bathrooms", min_value=1.0, max_value=10.0, value=1.0, step=0.5)
    sqft = st.number_input("Square Footage", min_value=100, max_value=10000, value=900)

with col2:
    year_built = st.number_input("Year Built", min_value=1900, max_value=2025, value=2000)
    zip_code = st.selectbox("Zip Code", [33131, 33137, 33138, 33130, 33129, 33132, 33133, 33143])
    property_type = st.selectbox("Property Type", le.classes_)

st.markdown("---")
st.subheader("Investment Analyzer")
st.caption("Optional — fill in to see ROI breakdown")

col3, col4 = st.columns(2)
with col3:
    purchase_price = st.number_input("Purchase Price ($)", min_value=0, max_value=5000000, value=400000, step=10000)
with col4:
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, max_value=10000, value=800, step=50,
                                help="Mortgage, taxes, insurance, maintenance")

if st.button("Predict Rent", type="primary"):
    property_type_enc = le.transform([property_type])[0]
    features = np.array([[beds, baths, sqft, year_built, zip_code, property_type_enc]])
    prediction = model.predict(features)[0]
    low = round(prediction * 0.90 / 50) * 50
    high = round(prediction * 1.10 / 50) * 50

    # neighborhood context
    zip_avg = df[df["zip"] == zip_code]["price"].median()
    diff = prediction - zip_avg
    diff_pct = (diff / zip_avg) * 100

    # investment calcs
    monthly_cashflow = prediction - expenses
    annual_cashflow = monthly_cashflow * 12
    cap_rate = (annual_cashflow / purchase_price) * 100 if purchase_price > 0 else 0
    gross_yield = ((prediction * 12) / purchase_price) * 100 if purchase_price > 0 else 0

    st.markdown("---")
    st.subheader("Results")

    # rent prediction
    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated Rent", f"${prediction:,.0f}/mo")
    c2.metric("Likely Range", f"${low:,} — ${high:,}")
    if diff >= 0:
        c3.metric("vs Zip Avg", f"+${diff:,.0f}", f"{diff_pct:.1f}% above median")
    else:
        c3.metric("vs Zip Avg", f"-${abs(diff):,.0f}", f"{diff_pct:.1f}% below median", delta_color="inverse")

    st.markdown("---")
    st.subheader("Investment Breakdown")

    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Monthly Cash Flow", f"${monthly_cashflow:,.0f}")
    i2.metric("Annual Cash Flow", f"${annual_cashflow:,.0f}")
    i3.metric("Cap Rate", f"{cap_rate:.2f}%")
    i4.metric("Gross Yield", f"{gross_yield:.2f}%")

    if cap_rate >= 6:
        st.success(f"Strong investment — {cap_rate:.1f}% cap rate is above the 6% threshold for Miami.")
    elif cap_rate >= 4:
        st.warning(f"Moderate investment — {cap_rate:.1f}% cap rate. Viable but tight margins.")
    elif purchase_price > 0:
        st.error(f"Weak investment — {cap_rate:.1f}% cap rate. Consider a lower purchase price or higher rent area.")

    st.markdown("---")
    st.subheader(f"Neighborhood Context — Zip {zip_code}")
    zip_data = df[df["zip"] == zip_code]["price"]
    st.write(f"Based on {len(zip_data)} active listings in this zip code:")

    n1, n2, n3 = st.columns(3)
    n1.metric("Median Rent", f"${zip_data.median():,.0f}")
    n2.metric("Lowest", f"${zip_data.min():,.0f}")
    n3.metric("Highest", f"${zip_data.max():,.0f}")