import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Streamlit App")
streamlit.header("MENU 🍞 🥑")
streamlit.text("🍞 BREAD")
streamlit.text("🥑 AVOCADO")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please enter a fruit name to get info")
    
  else:  
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
    streamlit.error()

def get_fruit_load_list():
  with my_cnx_cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")  
    return my_cur.fetchall()
  
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

def insert_row_sf(fruit_name):
  with my_cnx_cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('FROM STREAMLIT')")  
    return "Thanks for adding"+fruit_name
  
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_sf(fruit_name)
  streamlit.text(back_from_function)
  
  


