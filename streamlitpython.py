import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Student Budget Manager", layout="wide")

# Session State for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "income" not in st.session_state:
    st.session_state.income = 0

if "savings_goal" not in st.session_state:
    st.session_state.savings_goal = 0

# Sidebar navigation
st.sidebar.title("📊 Student Budget Manager")
page = st.sidebar.radio("Choose Option", ["➕ Input Expense", "📁 Table & Export", "📈 Visualize"])

# Monthly Income & Savings Setup
st.sidebar.header("💰 Monthly Setup")
st.session_state.income = st.sidebar.number_input("Monthly Income (₹)", value=10000)
st.session_state.savings_goal = st.sidebar.number_input("Monthly Savings Goal (₹)", value=2000)

# Calculate Monthly Budget
budget = st.session_state.income - st.session_state.savings_goal
total_spent = sum([x['Amount'] for x in st.session_state.expenses])
remaining_budget = budget - total_spent

# TAB 1: INPUT EXPENSE
if page == "➕ Input Expense":
    st.header("➕ Log a New Expense")

    with st.form("expense_form", clear_on_submit=True):
        date_input = st.date_input("Date", value=date.today())
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Stationery", "Other"])
        description = st.text_input("Description")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=1.0)

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            st.session_state.expenses.append({
                "Date": date_input,
                "Category": category,
                "Description": description,
                "Amount": amount
            })
            st.success("Expense added!")

            # Alerts
            total_spent = sum([x['Amount'] for x in st.session_state.expenses])
            remaining_budget = budget - total_spent

            if total_spent > st.session_state.income:
                st.warning("⚠️ You have exceeded your income!")
            elif remaining_budget < 0:
                st.warning("⚠️ You're overspending and hitting your savings!")
            elif remaining_budget < st.session_state.savings_goal:
                st.info("💡 Your remaining budget is less than your savings goal.")

# TAB 2: TABLE & EXPORT
elif page == "📁 Table & Export":
    st.header("📁 View All Expenses")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Weekly Expenses", csv, "weekly_expenses.csv", "text/csv")
    else:
        st.info("No expenses added yet.")

# TAB 3: VISUALIZATION
elif page == "📈 Visualize":
    st.header("📊 Expense Visualizations")

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Pie Chart - Expense by Category")
            pie_data = df.groupby("Category")["Amount"].sum()
            fig1, ax1 = plt.subplots()
            ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.subheader("📅 Bar Chart - Daily Spending")
            bar_data = df.groupby("Date")["Amount"].sum()
            st.bar_chart(bar_data)
    else:
        st.info("No expenses to visualize yet.")
