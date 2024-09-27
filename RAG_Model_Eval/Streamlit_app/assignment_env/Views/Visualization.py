import streamlit as st
import psycopg2
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def get_validation_data():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        query = "SELECT validated, validated_with_help, not_validated FROM gaia_validation_dashboard"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data from database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

def create_visualizations(df):
    try:
        validated_count = df['validated'].sum()
        validated_with_help_count = df['validated_with_help'].sum()
        not_validated_count = df['not_validated'].sum()
        total_count = validated_count + validated_with_help_count + not_validated_count

        labels = ['Validated', 'Validated with Help', 'Not Validated']
        counts = [validated_count, validated_with_help_count, not_validated_count]
        colors = ['green', 'orange', 'red']

        if total_count > 0:
            # Display summary metrics
            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Validations", total_count)
            col2.metric("Validated", f"{validated_count} ({validated_count/total_count:.1%})")
            col3.metric("Not Validated", f"{not_validated_count} ({not_validated_count/total_count:.1%})")

            # Create two columns for charts
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Bar Chart of Validation Results")
                fig_bar, ax_bar = plt.subplots()
                ax_bar.bar(labels, counts, color=colors)
                ax_bar.set_ylabel('Count')
                ax_bar.set_title('Validation Status')
                st.pyplot(fig_bar)

            with col2:
                st.subheader("Pie Chart of Validation Results")
                fig_pie, ax_pie = plt.subplots()
                ax_pie.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors)
                ax_pie.axis('equal')
                st.pyplot(fig_pie)

            # Display data table
            st.subheader("Data Table")
            st.table(pd.DataFrame({'Category': labels, 'Count': counts, 'Percentage': [f"{c/total_count:.1%}" for c in counts]}))
        else:
            st.warning("No validation data available to display.")
    except Exception as e:
        st.error(f"Error displaying visualizations: {e}")

def visualization_page():
    st.title("Validation Dashboard Visualization")
    df = get_validation_data()
    if df.empty:
        st.warning("No data available to display.")
    else:
        create_visualizations(df)

if __name__ == "__main__":
    visualization_page()