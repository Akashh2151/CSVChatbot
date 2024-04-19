import os
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from apikey import apikey

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = apikey

# Define Streamlit app
def app():
    st.title("CSV Query App")
    st.write("Connect to a MySQL database and enter a query or request a summary.")

    # Database connection parameters
    db_config = {
        'host': '127.0.0.1',
        'database': 'test',
        'user': 'root',
        'password': 'roott'
    }

    # Connect to the MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            st.write('Successfully connected to the database')
            query = "SELECT * FROM hotel_bookings" 
            data = pd.read_sql(query, conn)
            st.write("Data Preview:")
            st.dataframe(data.head())

            agent = create_pandas_dataframe_agent(OpenAI(temperature=0), data, verbose=True)
            query_input = st.text_input("Enter a query or summary request (e.g., 'summarize data in 2 lines'):")

            if st.button("Execute"):
                # Check if the query is a summarization request
                if 'summarize data in' in query_input:
                    lines = int(query_input.split()[-2])  # Assuming the format is always correct
                    summary_response = agent.run(f"summarize the data in {lines} lines")
                    st.write("Summary:")
                    st.write(summary_response)
                else:
                    # Process as a normal query
                    answer = agent.run(query_input)
                    st.write("Answer:")
                    st.write(answer)
    except Error as e:
        st.write('Error while connecting to MySQL', str(e))
    finally:
        if conn.is_connected():
            conn.close()
            st.write('Database connection closed')

if __name__ == "__main__":
    app()
