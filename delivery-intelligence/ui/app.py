import streamlit as st
import requests

# st.title("Delivery Intelligence")

project = st.text_input(
    "Project",
    "SCRUM"
)

sprint = st.number_input(
    "Sprint",
    value=2
)

question = st.text_input(
    "Ask Question"
)

if st.button("Ask"):

    response = requests.get(
        "http://127.0.0.1:8000/ask",
        params={
            "question": question,
            "project_key": project,
            "sprint_id": sprint
        }
    )

    st.json(response.json())