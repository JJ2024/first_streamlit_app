import streamlit as st
import pandas as pd
import requests as rq


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
st.header('Fruityvice Fruit Advice!')
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/watermelon" + "kiwi")

#take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

#output it to the screen as a table
st.dataframe(fruityvice_normalized)
