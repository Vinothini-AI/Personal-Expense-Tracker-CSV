
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Tracker")
st.write("Track your daily expenses easily.")

FILE = "expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Amount"]

# Create the CSV file if it does not exist
if not os.path.exists(FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)

# Load expense records
df = pd.read_csv(FILE)

# Ensure the required columns exist
if not all(column in df.columns for column in COLUMNS):
    df = pd.DataFrame(columns=COLUMNS)

# Add a new expense
st.header("➕ Add New Expense")

with st.form("expense_form"):
    expense_date = st.date_input("Date", value=date.today())

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills",
         "Education", "Health", "Other"]
    )

    description = st.text_input("Description")
    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.error("Enter an amount greater than zero.")
        else:
            new_expense = pd.DataFrame([{
                "Date": str(expense_date),
                "Category": category,
                "Description": description,
                "Amount": amount
            }])

            df = pd.concat([df, new_expense], ignore_index=True)
            df.to_csv(FILE, index=False)
            st.success("Expense added successfully!")
            st.rerun()

# Prepare data for display
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

st.header("📊 Expense Summary")

total = df["Amount"].sum()
col1, col2 = st.columns(2)

col1.metric("Total Expenses", f"₹{total:,.2f}")
col2.metric("Number of Expenses", len(df))

if not df.empty:
    st.header("📈 Category-wise Spending")
    chart_data = df.groupby("Category")["Amount"].sum()
    st.bar_chart(chart_data)

    st.header("📋 All Expenses")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Expenses CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )
else:
    st.info("No expenses yet. Add your first expense above!")