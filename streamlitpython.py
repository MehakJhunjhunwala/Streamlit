import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Student Expense Tracker", layout="wide")

st.sidebar.header("Monthly Budget Settings")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, value=10000, step=100)
goal = st.sidebar.number_input("Savings Goal (₹)", min_value=0, value=2000, step=100)
export_button = st.sidebar.button("Export Current Week to CSV")

if 'expenses' not in st.session_state:
    st.session_state['expenses'] = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

with st.form("entry_form", clear_on_submit=True):
    st.write("### Log New Expense")
    date = st.date_input("Date", value=datetime.date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Miscellaneous"])
    description = st.text_input("Description (optional)")
    amount = st.number_input("Amount (₹)", min_value=1, step=1)
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_row = {"Date": date, "Category": category, "Description": description, "Amount": amount}
        st.session_state['expenses'] = st.session_state['expenses'].append(new_row, ignore_index=True)
        st.success("Expense added!")

st.write("Expense Table")
df = st.session_state['expenses']
st.dataframe(df.style.format(subset=["Amount"], formatter="₹{:.2f}"))

# Weekly filter for exporting
today = datetime.date.today()
week_start = today - datetime.timedelta(days=today.weekday())
week_end = week_start + datetime.timedelta(days=6)
mask = (pd.to_datetime(df['Date']) >= pd.to_datetime(week_start)) & (pd.to_datetime(df['Date']) <= pd.to_datetime(week_end))
week_df = df[mask]

if export_button:
    csv = week_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"expenses_{week_start}_to_{week_end}.csv",
        mime='text/csv'
    )

total_spent = df["Amount"].sum()
remaining_budget = income - total_spent
max_spend = income - goal

# Warning logic
if total_spent > max_spend:
    st.error(f"Warning: You have exceeded your budgeted spending limit!\nTotal Spent: ₹{total_spent:.2f} / Allowed: ₹{max_spend:.2f}")
else:
    st.info(f"Total Spent: ₹{total_spent:.2f} / Allowed: ₹{max_spend:.2f}")

# Visualization
st.write("Expense Breakdown")
if not df.empty:
    cat_pivot = df.groupby('Category')['Amount'].sum()
    st.write("#### Pie Chart:")
    st.plotly_chart({
        "data": [
            {
                "values": cat_pivot.values,
                "labels": cat_pivot.index,
                "type": "pie"
            }
        ],
        "layout": {"title": "Spending by Category"}
    })

    st.write("Weekly Bar Chart:")
    if not week_df.empty:
        bar_df = week_df.groupby('Date')['Amount'].sum()
        st.bar_chart(bar_df)
    else:
        st.info("No expenses found for this week.")
else:
    st.info("No data to visualize yet. Add some expenses!")
