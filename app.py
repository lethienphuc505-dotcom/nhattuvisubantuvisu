import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake . io",
    page_icon="🐍",
    layout="centered"
)

# Đọc nội dung từ file game.html độc lập bên ngoài để loại bỏ hoàn toàn lỗi cú pháp
with open("game.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=560)
