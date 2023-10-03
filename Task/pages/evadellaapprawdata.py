import pandas as pd
import numpy as np
import streamlit as st
# import mysql.connector
from evadellaapp import *
from evadella_mysql import *
# from evadellalogin import *
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="EvaDella App",
    page_icon=":ring:", 
    layout="wide",  
    initial_sidebar_state="collapsed"
)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "swapna2021",
    database = "ecomm"
)

# css applied
with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

if not hasattr(state, "authentication_status"):
    state.authentication_status = True

if not state.authentication_status:
    st.error("Please login with username/password")
    
else:
    st.title('Raw Data To Home Page')

    authenticator.logout("logout")

    col15, col16 = st.columns(2)

    with col15:

        st.subheader('Total Orders Details')

        ordersCount = "SELECT COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" 

        # unShippedOrdersMonthCountDf1
        ordersDf = pd.read_sql(ordersCount, mydb)

        totalOrders = sum(ordersDf['No Of Orders'])

        st.metric("Total No Of Orders", totalOrders)

        st.dataframe(ordersDf)
        
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.BarChartColumn(
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
        ),
    },
    hide_index=True,
)

sample_data = pd.DataFrame({
    "products": [
        'pulses', 'vagetables', 'fruits', 'pickels'
    ]
})

sample_data["sales"] = data_df
st.data_editor(
    sample_data,
    column_config={
        "sales": st.column_config.BarChartColumn(
            "Sales",
            # width="medium",
            # help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
        )
    }
)



        # import streamlit as st
        # from streamlit_modal import Modal

        # modal = Modal(key="Demo Key", title="test")
        # for col1 in st.columns(2):
        #     with col1:
        #         open_modal = st.button('button')
        #         if open_modal:
        #             with modal.container():
        #                 st.markdown('Hi This is Giridhar')



# Function to fetch data from the MySQL database based on selected filters
def fetch_data(category_filter, date_filter, vendor_filter):
    # MySQL connection configuration
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='swapna2021',
        database='ecomm'
    )

    # Build the SQL query based on the selected filters
    query = "SELECT * FROM product_sku WHERE 1=1"
    if category_filter:
        query += f" AND product_id = '{category_filter}'"
    if date_filter:
        query += " AND product_sku_cd = '{date_filter}'"
    if vendor_filter:
        query += " AND status = '{vendor_filter}'"

    # Fetch data from the database using the query and filters
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data

# Streamlit app
def main():
    st.title('inventory stock')

    # Fetch unique values for each filter from the database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='swapna2021',
        database='ecomm'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT product_id FROM product_sku")
    categories = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT product_sku_cd FROM product_sku")
    dates = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT status FROM product_sku")
    vendors = [row[0] for row in cursor.fetchall()]

    # Sidebar filters
    col1, col2, col3 = st.columns(3)
    category_filter = col1.selectbox('Select id', categories)
    date_filter = col2.selectbox('Select sku', dates)
    vendor_filter = col3.selectbox('Select status', vendors)

    # Display data based on filters
    if st.button('Apply Filters'):

        data = fetch_data(category_filter, date_filter, vendor_filter)

        if data:
            columns=[['product_id', 'product_sku_cd', 'status', 'list_price']]
            df = pd.DataFrame(data, columns=columns)

            st.dataframe(df)
        else:
            st.write("No data found with the selected filters.")
    else:
        # Initialize df with None outside the if block
        df = None        
        
if __name__ == '__main__':
    main()

