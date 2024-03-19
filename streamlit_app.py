# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie!"
)

title = st.text_input('Name on Smoothie', '')
st.write('The name on your Smoothie will be: ', title)

name_on_order = title
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)
#if ingredients_list is not null: then do everything below this line that is indented. 

if ingredients_list:
    ingredients_string =''  #para transformar la lista en un string tenemos que pasarle esto vacio a python

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    varbool = False;
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_witdh=True)
