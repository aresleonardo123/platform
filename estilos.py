# estilos.py
import streamlit as st

def aplicar_estilos():
    with open("assets/estilos_base.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    with open("assets/estilos_input.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Cursor tipo "manito" para selectbox y radio */
        .stSelectbox div[role="button"],
        .stSelectbox div[role="option"],
        .stSelectbox div[data-baseweb="select"] * {
            cursor: pointer !important;
        }

        .stRadio div[role="radiogroup"] > div,
        .stRadio label,
        .stRadio input[type="radio"] + div {
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)


