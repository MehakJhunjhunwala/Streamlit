import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

st.set_page_config(page_title="UG Budget Tracker", layout="wide")

# Initialize storage
CSV_FILE = "expenses.csv"

# Load or create data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=['Date'])
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Sidebar navigation
st.sidebar.title("🎓 UG Budget Tracker")
nav = st.sidebar.radio("Navigate to", ["📝 Log Expense", "📋 View Table & Export", "📊 Visualize"])

# Session state initialization
if "income" not in st.session_state: st.session_state.income = 0
if "savings" not in st.session_state: st.session_state.savings = 0

# Tab 1: Log Expense + Set Goals
if nav == "📝 Log Expense":
    st.title("📝 Log Daily Expense")

    with st.form("log_form"):
        date = st.date_input("Select Date", datetime.date.today())
        category = st.selectbox("Select Category", ["Food", "Transport", "Utilities", "Entertainment", "Education", "Other"])
        amount = st.number_input("Enter Amount (₹)", min_value=1.0, step=0.5)
        submitted = st.form_submit_button("Add Expense")

    df = load_data()

    if submitted:
        new_entry = pd.DataFrame([[date, category, amount]], columns=["Date", "Category", "Amount"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.success(f"✅ ₹{amount} added under '{category}' on {date}")

    st.markdown("### 🎯 Set Monthly Goals")
    income = st.number_input("Monthly Income (₹)", min_value=0.0, value=st.session_state.income, step=500.0, key="income_input")
    savings = st.number_input("Savings Goal (₹)", min_value=0.0, value=st.session_state.savings, step=100.0, key="savings_input")

    st.session_state.income = income
    st.session_state.savings = savings

# Tab 2: View Table & Export
elif nav == "📋 View Table & Export":
    st.title("📋 View Logged Expenses")
    df = load_data()

    if df.empty:
        st.warning("No expenses logged yet.")
    else:
        st.dataframe(df, use_container_width=True)

        total = df["Amount"].sum()
        st.markdown(f"### 💰 Total Spent: ₹{total:.2f}")

        # Budget Feedback
        if st.session_state.income > 0:
            budget_limit = st.session_state.income - st.session_state.savings
            if total > budget_limit:
                st.error(f"⚠️ You have overspent by ₹{total - budget_limit:.2f} from your monthly budget!")
            else:
                st.success(f"🟢 You're within budget. ₹{budget_limit - total:.2f} remaining.")

        # Export CSV
        st.markdown("### 📤 Export Data")
        this_week = df[df["Date"] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
        csv = this_week.to_csv(index=False).encode('utf-8')
        st.download_button("Download This Week's Data", csv, "weekly_expenses.csv", "text/csv")

# Tab 3: Visualizations
elif nav == "📊 Visualize":
    st.title("📊 Spending Visualizations")
    df = load_data()

    if df.empty:
        st.warning("No data available for visualization.")
    else:
        # Aggregate
        cat_totals = df.groupby("Category")["Amount"].sum().reset_index()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧁 Pie Chart by Category")
            fig_pie = px.pie(cat_totals, names="Category", values="Amount", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("### 📦 Bar Chart by Category")
            fig_bar = px.bar(cat_totals, x="Category", y="Amount", text_auto=True, color="Category", color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("### 🗓️ Expense Timeline")
        timeline = df.groupby("Date")["Amount"].sum().reset_index()
        fig_line = px.line(timeline, x="Date", y="Amount", markers=True, title="Spending Over Time", line_shape="linear")
        st.plotly_chart(fig_line, use_container_width=True)
