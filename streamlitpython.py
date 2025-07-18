import streamlit as st
import pandas as pd

st.title("CSV File Uploader and Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display the dataframe
        st.subheader("CSV File Contents:")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to view its content.")
