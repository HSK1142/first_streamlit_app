import streamlit
import pandas

streamlit.title("Streamlit App")
streamlit.header("MENU 🍞 🥑")
streamlit.text("🍞 BREAD")
streamlit.text("🥑 AVOCADO")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.dataframe(my_fruit_list)
