import streamlit as st
import pandas as pd
import requests as rq
import snowflake.connector


st.title('My Parents New Healthy Diner')
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Hard-Boiled Free-Range Egg")
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

#New section to display fruityvice api response

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered', fruit_choice)
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

#output it to the screen as a table
st.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
st.header("The fruit list contains:")
st.dataframe(my_data_row)

st.header('What fruit would you like to add?')
add_my_fruit = st.text_input('Input fruit')
st.header(f"insert into fruit_load_list values({add_my_fruit})")

