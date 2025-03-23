# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the Fruits you want in your custom Smoothie!")

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Bananas", "Strawberries", "Peaches"),
# )

# st.write("Your favourite fruits is: ", option)


from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie list will be: ",name_on_order)


ingredients_list = st.multiselect('choose upto 5 ingredients: ', my_dataframe ,max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)
        # st.write(fruit_chosen)

    # st.write(ingredients_string)

    my_insert_stmt = f""" 
    INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""


    # st.write(my_insert_stmt)
    
    submit_button = st.button('Submit Order')

    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success(f"""Your Smoothie is ordered, {name_on_order}!""", icon="✅")
    
