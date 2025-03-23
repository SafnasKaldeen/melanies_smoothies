import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import when_matched
import pandas as pd

# Streamlit UI
st.title(":cup_with_straw: Pending Smoothie Orders! :cup_with_straw:")
st.write("Orders that need to be filled.")

# Snowflake session
session = get_active_session()

# Fetch data
my_dataframe = session.table("smoothies.public.orders").to_pandas()

# Check if the dataframe has data
if not my_dataframe.empty:
    # Allow inline editing of the ORDER_FILLED column
    edited_df = st.data_editor(
        my_dataframe,
        column_config={"ORDER_FILLED": st.column_config.CheckboxColumn("ORDER_FILLED")},
        disabled=["NAME_ON_ORDER", "INGREDIENTS"],  # Disable edits for other columns
        use_container_width=True
    )

    # Update the Snowflake table if changes were made
    if st.button("Submit"):
        # Convert updated dataframe back to Snowflake DataFrame
        edited_dataset = session.create_dataframe(edited_df)

        # Reference original Snowflake table
        og_dataset = session.table("smoothies.public.orders")
        try:
            # Perform a MERGE operation
            og_dataset.merge(
                edited_dataset,
                og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'],
                [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )

            st.success("Order(s) updated!", icon="👍")
        except:
            st.write("Something went wrong")
else:
    st.success("There are no pending orders right now!", icon="👍")
