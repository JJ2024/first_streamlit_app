import streamlit as st
import pandas as pd
import requests as rq

st.stop()

import snowflake.connector
from urllib.error import URLError



st.title('My Parents New Healthy Diner')
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Hard-Boiled Free-Range Egg")
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

#New section for Fruityvice API Response
st.header ('Fruityvice Fruit Advice!')

try:  
  fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
    
  else:
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)
    
except URLError as e:
  st.error()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
st.header("The fruit list contains:")
st.dataframe(my_data_row)

st.header('What fruit would you like to add?')
add_my_fruit = st.text_input('Input fruit')
y = my_cur.execute(f"insert into fruit_load_list values('{add_my_fruit}')")
