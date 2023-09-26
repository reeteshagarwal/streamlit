
import streamlit
import pandas
import requests

#streamlit.stop()
import snowflake.connector
from urllib.error import URLError



streamlit.title('My Parents New Healty Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text ('🥗 Kale ')
streamlit.text('🐔  Hard-Bolied Eggs')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import Pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#Create a repetable code block
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  


#New section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select fruit to get information.")
  else:
    back_from_function=get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function);
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()


#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")

#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()

#streamlit.text("Hello from Snowflake:")
streamlit.text("The fruit load list:")

#streamlit.text(my_data_row)
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.text('Thanks for adding ' + add_my_fruit)
my_cur.execute("Insert into pc_rivery_db.public.fruit_load_list values('From streamlit');" )
my_cur.execute("commit;")
