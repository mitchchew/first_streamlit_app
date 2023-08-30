import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'] )
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

#new section
streamlit.header('Fruityvice Fruit Advice!')
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else: 
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)

except URLError as e: 
streamlit.error()

streamlit.write('The user entered ', fruit_choice)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#import requests
streamlit.header('What fruit would you like to add!')
add_my_fruit = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('Thanks for adding ', add_my_fruit)

add_my_fruit = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

streamlit.stop()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_rows)

#this will not work correctly but just go with it 
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
