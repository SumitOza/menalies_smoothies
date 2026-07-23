# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_smoothie = st.text_input('Name on Smoothie:')

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ' '

    for fruits_choosen in ingredients_list:
        ingredients_string += ' '+fruits_choosen+' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
                values ('""" + ingredients_string + """','"""+name_on_smoothie+"""')"""
    
    time_to_insert = st.button("Place Order")
    
    if time_to_insert:
        st.write('Name on the Cup will be :', name_on_smoothie)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
