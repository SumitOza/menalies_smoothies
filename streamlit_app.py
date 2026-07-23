# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests  
import pandas as pd

name_on_smoothie = st.text_input('Name on Smoothie:')

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)
if ingredients_list:
    ingredients_string = ' '
    
    for fruit_choosen in ingredients_list:
        ingredients_string += ' '+fruit_choosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
                values ('""" + ingredients_string + """','"""+name_on_smoothie+"""')"""
    
    time_to_insert = st.button("Place Order")
    
    if time_to_insert:
        st.write('Name on the Cup will be :', name_on_smoothie)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
