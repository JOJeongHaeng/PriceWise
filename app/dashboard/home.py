import streamlit as st

from app.components.queries import build_overview_query


st.set_page_config(page_title="PriceWise", layout="wide")
st.title("PriceWise Dashboard")
st.caption("Consumer price insights built from the Korean Consumer Agency OpenAPI.")

st.code(build_overview_query().strip(), language="sql")
