import pickle
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit import session_state as state
from datetime import datetime, timedelta
import mysql.connector
import os
import altair as alt

# from evadella_mysql import *
# import toml

import plotly.express as px
import base64


st.set_page_config(
    page_title="EvaDella App",
    page_icon=":ring:",
    layout="wide",  
    initial_sidebar_state="collapsed",
    # background_color = "green",
    # background_image = "Task\iStock.jpg"
)

# @st.cache_data
# def get_image_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# img = get_image_as_base64("Task\iStock.jpg")

# page_bg_img = """
#     <style>
#     [data-testid="stAppViewContainer"]{
#     # background-color: #cfe8eb;
#     background-image: url("data:image/png;base64,{img}");
#     background-size: cover;
#     }

#     [data-testid="stHeader"]{
#     background-color: rgba(0, 0, 0, 0);
#     }

#     </style>
#     """

# st.markdown(page_bg_img, unsafe_allow_html=True)

# user authentication
names = ["Giridhar", "Yerra"]
usernames = ["evadellagiri", "evadellayerra"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

    credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":hashed_passwords[1]
                }           
            }
        }
    

authenticator = stauth.Authenticate(credentials,
    "dashborad", "abcdefg", cookie_expiry_days = 30)

name, authentication_status, username = authenticator.login("login", "main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status: 
    state.authentication_status = True
    # st.balloons()
    # st.snow()

    page = st.sidebar.selectbox("Select a page", ["evadellaapp.py","evadellaapprawdata.py"])
    with st.sidebar:
        page_bg_img = """
                <style>
                div.css-6qob1r.e1akgbir3{
                    background-color: #e2f0af;

                }
                </style>
                """
        st.markdown(page_bg_img, unsafe_allow_html=True)

    if page == "evadellaapp.py":
        st.title('📊 EvaDella App Dashboard')   # :bar_chart:

        authenticator.logout("logout")

        # Navigation Bar

        selected = option_menu(
            menu_title = None,
            options = ["Summary", "Operations", "Sales", "Inventory", "Staff Metrics"],
            icons = ["house", "", "book", "building", "person"],
            orientation = "horizontal",
        )

        # # config = toml.load("config.toml")
        # mysql_host = os.environ.get('localhost')
        # mysql_user = os.environ.get('root')
        # mysql_password = os.environ.get('swapna2021')
        # mysql_database = os.environ.get('ecomm')

        # Establish the connection
        mydb = mysql.connector.connect(
            user = "root",
            host = "mysql-db",
            port = 3306,
            password = "swapna2021",
            database = "ecomm"
        )

        getOrderStatusDf = "SELECT * FROM ecomm.order_status"

        # todayOrdersDetails = "SELECT DATE(order_submit_dt_tm) as 'Date', order_id, total_amount FROM ecomm.orders WHERE DATE(order_submit_dt_tm) = CURDATE()"

        filterOrderStatusDf = "SElECT order_id, status_cd, estimated_time FROM ecomm.order_status"

        currentMonthOrders = "SELECT COUNT(order_id) as 'No Of Orders', order_id, coupon_applied, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders WHERE MONTH(order_submit_dt_tm) = MONTH(CURDATE() - INTERVAL 1 MONTH) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersWeekCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as Date, DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 WEEK)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersByDaysCount = "select DATE(order_submit_dt_tm) as 'Date', order_id, COUNT(order_id) as 'No Of Orders' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( CURDATE() - INTERVAL 10 DAY ) GROUP BY Date"

        ordersLastdaysCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from ecomm.orders where orders.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 10 DAY)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersMonthCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 MONTH)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedOrdersMonthCount1 = "select DATE(order_submit_dt_tm) as 'Date', status_cd, customer_id from orders o, order_status os WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') GROUP BY order_submit_dt_tm"

        ordersOfOneMonth= "SELECT os.order_id, os.status_cd, os.last_update_dt_tm as order_date_time, os.staff_cd FROM order_status os WHERE os.last_update_dt_tm >= CURRENT_DATE - INTERVAL 1 MONTH"


        if selected == "Summary":

            page_bg_img = """
                <style>
                div.css-keje6w.esravye1{
                    background-color: #aff0b4;
                    border: 1PX #02070f;
                    padding: 20px 20px 20px 20px; 
                    padding: 5% 5% 5% 7%;
                    border-radius: 20px;
                    text-align: center;
                }
                </style>"""
            
            st.markdown(page_bg_img, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                staffworking = pd.read_excel('Task\staffloginIOT.xlsx')

                st.subheader("Staff working analysis")

                # def stafftimings(intime, outtime):

                st.dataframe(staffworking)

        if selected == "Operations":

            # css applied
            page_bg_img = """
                <style>
                div.css-keje6w.esravye1{
                    background-color: #aff0b4;
                    border: 1PX #02070f;
                    padding: 20px 20px 20px 20px; 
                    padding: 5% 5% 5% 7%;
                    border-radius: 20px;
                    text-align: center;
                }
                </style>"""
            st.markdown(page_bg_img, unsafe_allow_html=True)

            # col1, col2, col3, col4 = st.columns(4)
            # with col1:
            #     st.subheader("heading for operations")
            #     st.table()

            # columns for partition
            col5, col6 = st.columns(2)

            with col5:

                st.subheader("Order Count By Status")

                orderCountByStatus = ("SELECT DATE(order_track_update_time) as 'Date', status_cd, order_id "
                                      "FROM ecomm.order_status "
                                      "WHERE order_status.order_track_update_time != 0")

                orderCountByStatusDf = pd.read_sql_query(orderCountByStatus, mydb)
                filteredOrderCountByStatusDf = orderCountByStatusDf.pivot_table(index='status_cd', columns='Date', values='Date', aggfunc='count')
                byStatusOrderCountDf = ((filteredOrderCountByStatusDf.replace(np.nan, 0)).astype(int)).iloc[:, ::-1]
                sumoforders = byStatusOrderCountDf.iloc[:, 3:].sum(axis=1)
                orderCountByStatusFinalDf = byStatusOrderCountDf.drop(byStatusOrderCountDf.iloc[:, 3:], axis=1)
                orderCountByStatusFinalDf['Prior period'] = sumoforders
                dfOrderCountByStatus = (pd.DataFrame(orderCountByStatusFinalDf)).reset_index()
                dfOrderCountByStatus.columns.values[0] = "Order Submit Date"

                st.dataframe(dfOrderCountByStatus)

            with col6:

                st.subheader("Today Orders/Average Orders - Count/Amount")

                todayOrdersDetails = ("SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)) as 'Count', ROUND(SUM(IFNULL(total_amount, 0))) as 'Amount' "
                                      "FROM ecomm.orders "
                                      "WHERE DATE(order_submit_dt_tm) = CURDATE()")

                todayOrdersDetailsDf = pd.read_sql_query(todayOrdersDetails, mydb)
                # convert_dict = {'Count': int, 'Amount' :int}
                # todayOrdersDetailsDf = todayOrdersDetailsDf.astype(convert_dict)
                todayOrdersDetailsDf.iloc[0, 0] = 'Today Orders'
                todayOrdersDetailsDf['Orders'] = todayOrdersDetailsDf['Date'].astype(str)
                todayOrdersDetailsDf = todayOrdersDetailsDf.drop('Date', axis=1)

                averageOrdersBy30Days = ("SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)/COUNT(DISTINCT DATE(order_submit_dt_tm))) as 'Count', "
                                        "ROUND(AVG(total_amount)) as 'Amount' "
                                        "FROM ecomm.orders "
                                        "WHERE DATE(order_submit_dt_tm) >= (CURDATE()- INTERVAL 1 MONTH)")

                averageOrdersBy30DaysDf = pd.read_sql_query(averageOrdersBy30Days, mydb)
                convert_dict = {'Count': int, 'Amount' :int}    
                averageOrdersBy30DaysDf = averageOrdersBy30DaysDf.astype(convert_dict) 
                averageOrdersBy30DaysDf.iloc[0, 0] = 'Daily Average Orders'
                averageOrdersBy30DaysDf['Orders'] = averageOrdersBy30DaysDf['Date'].astype(str)
                averageOrdersBy30DaysDf = averageOrdersBy30DaysDf.drop('Date', axis=1)

                todayOrdersAverageOrdersDF = (pd.concat([todayOrdersDetailsDf, averageOrdersBy30DaysDf]).reset_index())
                todayOrdersAverageOrdersDF = todayOrdersAverageOrdersDF.drop('index', axis=1)
                firstcolumn = todayOrdersAverageOrdersDF.pop('Orders')
                todayOrdersAverageOrdersDF.insert(0, 'Orders', firstcolumn)

                st.dataframe(todayOrdersAverageOrdersDF)

            # columns for partition
            col10, col11 = st.columns(2)

            with col10:
                st.subheader("Orders By OrderStatus By Week, Month, Year")

                option = st.selectbox(
                '',
                ('', 'Week', 'Month', 'Year'))

                def week():

                    ordersWithStatusWeek = (
                        "SELECT DATE(order_track_update_time) as Ordered_date, "
                        "order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd "
                        "FROM ecomm.order_status "
                        "WHERE order_track_update_time >= CURDATE() - INTERVAL 1 WEEK"
                    )

                    orderStatusWeekData = pd.read_sql_query(ordersWithStatusWeek, mydb)
                    def highlight_cell(val, column):
                        if column == column == 'status_cd' and val == 'PAID':
                            return 'color: blue'
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: green'
                        elif column == 'status_cd' and val == 'Shipped':
                            return 'color: yellow'
                        elif column =='status_cd' and val != 'Delivered':
                            return 'color: red'
                        else:
                            return ''

                    orderStatusWeekDataDF = orderStatusWeekData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                    st.dataframe(orderStatusWeekDataDF)
                    # st.write('You selected:', option)

                def month():

                    ordersWithStatusMONTH = ("SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, "
                                             "DATE(estimated_time) as Estimated_date, staff_cd "
                                             "FROM ecomm.order_status "
                                             "WHERE  order_track_update_time >= CURDATE() - INTERVAL 1 MONTH")

                    orderStatusMonthData = pd.read_sql_query(ordersWithStatusMONTH, mydb)
                    def highlight_cell(val, column):

                        if column == column == 'status_cd' and val == 'PAID':
                            return 'color: blue'
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: green'
                        elif column == 'status_cd' and val == 'SHIPPED':
                            return 'color: yellow'
                        elif column =='status_cd' and val != 'Delivered':
                            return 'color: red'
                        else:
                            return ''

                    orderStatusMonthDataDF = orderStatusMonthData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)
                    st.dataframe(orderStatusMonthDataDF)

                # def year():
                #     orderStatusYearData = pd.read_sql_query(ordersWithStatusYear, mydb)
                #     def highlight_cell(val, column):
                #         if column == 'status_cd' and val == 'PAID':
                #             return 'color: blue'
                #         elif column == 'status_cd' and val == 'Delivered':
                #             return 'color: green'
                #         elif column == 'status_cd' and val == 'Shipped':
                #             return 'color: yellow'
                #         elif column =='status_cd' and val != 'Delivered':
                #             return 'color: red'
                #         else:   
                #             return ''
                #     orderStatusYearDataDF = orderStatusYearData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                def year():
                    # Load the threshold data from Excel
                    thresholdData = pd.read_excel('Task/threshold_data.xlsx')

                    ordersWithStatusYear = ("SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, "
                                            "DATE(estimated_time) as Estimated_date, staff_cd "
                                            "FROM ecomm.order_status "
                                            "WHERE (order_track_update_time != 0 OR last_update_dt_tm != 0) "
                                            "AND order_track_update_time >= CURDATE() - INTERVAL 1 YEAR")

                    # Read the orders data from SQL query
                    orderStatusYearData = pd.read_sql_query(ordersWithStatusYear, mydb)

                    def highlight_cell(val, column):

                        if column == 'status_cd' and val == 'PAID':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "blue"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "green"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val == 'SHIPPED':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "yellow"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val != 'Delivered':
                            return 'color:red'

                        # elif column in thresholdData.columns:
                        #     threshold = thresholdData.loc[(thresholdData['Column'] == column), 'Threshold'].values[0]
                        #     if val >= threshold:
                        #         return 'color: ' + threshold
                        #     else:
                        #         return ''

                        else:
                            return ''

                    orderStatusYearDataDF = orderStatusYearData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                    st.dataframe(orderStatusYearDataDF)

                option_function_map = {
                    'Week' : week,
                    'Month' : month,
                    'Year' : year,
                }

                selected_function = option_function_map.get(option)
                if selected_function:
                    selected_function()

            with col11:

                st.subheader("Orders Delay")

                # orderstatusByThreshould = (
                #     "SELECT os.order_id, os.status_cd, os.last_update_dt_tm, os.staff_cd "
                #     "FROM order_status os "
                #     "JOIN orders o ON os.order_id = o.order_id "
                #     "JOIN thresholds tt ON tt.name = os.status_cd "
                #     "WHERE os.order_track_ref = (SELECT MAX(order_track_ref) FROM order_status WHERE order_id = os.order_id) "
                #     "AND DATEDIFF(CURRENT_DATE, os.last_update_dt_tm) > tt.value"
                # )

                # delayOrders = pd.read_sql(orderstatusByThreshould, mydb)

                # delayOrdersDf = pd.read_sql(ordersOfOneMonth, mydb)

                # def highlight_red(row):
                #     if row['order_date_time'] + timedelta(minutes=15) == delayOrdersDf.iloc[row.name]['order_date_time'] and row['status_cd'] == delayOrdersDf.iloc[row.name]['status_cd']:
                #         return ['background-color: red'] * len(row)
                #     return [''] * len(row)

                # styled_data = delayOrdersDf.style.apply(highlight_red, axis=1)

                # st.dataframe(styled_data)

        if selected == "Sales":

            # css applied
            page_bg_img = """

                <style>
                div.css-12w0qpk.esravye1{
                    background-color: #eebd90;
                    border: 3PX #02070f;
                    padding: 4px 1px 4px 3px;
                    border-radius: 10px;
                    /* padding: 5% 5% 5% 7%; */
                    text-align: center;
                }

                div.css-keje6w.esravye1{
                    background-color: #aff0b4;
                    border: 1PX #02070f;
                    padding: 20px 20px 20px 20px; 
                    # padding: 5% 5% 5% 7%;
                    border-radius: 20px;
                    text-align: center;
                }

                div.css-1r6slb0.esravye1 {
                    background-color: #96b7f3;
                    padding: 20px 20px 20px 20px;
                    text-align: center;
                    # /* padding: 5% 5% 5% 10%; */
                    border-radius: 10px;
                }

                div.css-keje6w.e1tzin5v2 {
                    background-color: #86dae4;
                    padding: 20px 20px 20px 20px;
                    text-align: center;
                    # /* padding: 5% 5% 5% 10%; */
                    border-radius: 10px;
                }
                </style>"""
            st.markdown(page_bg_img, unsafe_allow_html=True)

            # columns for partition
            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.subheader("Total No Of Orders")

                ordersCount = ("SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date',"
                            "DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name',"
                            "YEAR(order_submit_dt_tm) as 'Year'"
                            "FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" )

                ordersDf = pd.read_sql(ordersCount, mydb)
                totalOrders = sum(ordersDf['No Of Orders'])
                st.metric("", "")
                # st.markdown('<a href="http://localhost:8501/evadellaapprawdata" target="_self" >' + str(totalOrders) +'</a>',unsafe_allow_html = True)

            with col2:

                st.subheader("Input")

                st.metric(st.text_input(''),  value='')

            with col3:
                st.subheader("Total Amount")

                getOrdersDf = "SELECT * FROM ecomm.orders"

                ordersTable = pd.read_sql_query(getOrdersDf, mydb)
                totalAmount = sum(ordersTable['total_amount'])

                st.metric("", totalAmount, '0%')

            with col4:
                st.subheader("Number of sales")
                st.metric("", "25%", "-8%")

            # columns for partition
            col10, col11 = st.columns(2)

            with col10:
                st.subheader("Orders Count By Coupon Applied")

                ordersCountByCoupon = ("SELECT coupon_applied, COUNT(order_id) as 'No Of Orders' "
                                        "FROM ecomm.orders "
                                        "WHERE orders.coupon_applied <> '0' "
                                        "GROUP BY coupon_applied")

                ordersCountByCouponDf = pd.read_sql_query(ordersCountByCoupon, mydb)
                optionSelect = st.multiselect("Coupon Applied", options= ordersCountByCouponDf['coupon_applied'].unique(), 
                                            default = ordersCountByCouponDf['coupon_applied'].unique())
                appliedCoupon = ordersCountByCouponDf.query("coupon_applied == @optionSelect")

                st.table(appliedCoupon)

            with col11:

                st.subheader("Sales by categories")
 
                salesByCatagories = (
                    "SELECT o.order_id, DATE(o.order_submit_dt_tm) as ordered_date, ot.product_id, pc.catalog_id, "
                    "ct2.catalog_name as categories, ct1.catalog_name as cata_products, COUNT(ct1.catalog_name) as no_of_sales "
                    "FROM orders o "
                    "LEFT JOIN order_item ot ON o.order_id = ot.order_id "
                    "LEFT JOIN product_catalog_dir pc ON ot.product_id = pc.product_id "
                    "LEFT JOIN catalog_dir ct1 ON pc.catalog_id = ct1.catalog_id "
                    "LEFT JOIN catalog_dir ct2 ON ct1.parent_catalog_id = ct2.catalog_id "
                    "WHERE DATE(o.order_submit_dt_tm) >= DATE_SUB(CURRENT_DATE, INTERVAL 10 DAY) "
                    "GROUP BY cata_products ORDER BY cata_products")

                salesByCatagoriesDf = pd.read_sql_query(salesByCatagories, mydb)

                filterDf = salesByCatagoriesDf[['categories', 'no_of_sales']]

                salesByCatagoriesFilterDf1 = filterDf.groupby('categories')['no_of_sales'].agg(list).reset_index()

                salesByCatagoriesFilterDf1.columns = ['categories', 'sales']

                sales2 = salesByCatagoriesFilterDf1['sales']

                salesByCatagoriesFilterDf1['no of sales'] = sales2

                filterDf2 = salesByCatagoriesDf[['categories', 'cata_products']]

                salesByCatagoriesFilterDf2 = filterDf2.groupby('categories')['cata_products'].agg(list).reset_index()

                salesByCatagoriesFilterDf2.columns = ['categories', 'products']

                salesByCatagoriesFilterDf = pd.merge(salesByCatagoriesFilterDf2, salesByCatagoriesFilterDf1, on = 'categories')

                # salesByCatagoriesFilterDf1

                st.data_editor(
                salesByCatagoriesFilterDf,
                column_config={
                    "sales": st.column_config.BarChartColumn(
                        "sales",
                        width="small",
                        # help="The sales volume in the last 6 months",
                        y_min=0,
                        y_max=20,
                        # color ='green', 
                    )
                },
                hide_index=True,
            )

            # columns for partition
            col7, col8, col9 = st.columns(3)

            with col7:
                st.subheader("Orders By AmountRange")

                ordersCountByTotalAmount5 = ("select COUNT(order_id) as 'No Of Orders' "
                                             "from ecomm.orders "
                                             "where orders.total_amount > 1000")

                ordersCountByTotalAmount4 = ("select COUNT(order_id) as 'No Of Orders' "
                                             "from ecomm.orders "
                                             "where orders.total_amount > 500 and orders.total_amount >= 1000")

                ordersCountByTotalAmount3 = ("select COUNT(order_id) as 'No Of Orders' "
                                             "from ecomm.orders "
                                             "where orders.total_amount > 300 and orders.total_amount >= 500")

                ordersCountByTotalAmount2 = ("select COUNT(order_id) as 'No Of Orders' "
                                             "from ecomm.orders "
                                             "where orders.total_amount > 100 and orders.total_amount >= 300")

                ordersCountByTotalAmount1 = ("select COUNT(order_id) as 'No Of Orders' "
                                             "from ecomm.orders where orders.total_amount <= 100")

                ordersCountByTotalAmountDf1 =  pd.read_sql_query(ordersCountByTotalAmount1, mydb)
                ordersCountByTotalAmountDf2 =  pd.read_sql_query(ordersCountByTotalAmount2, mydb)
                ordersCountByTotalAmountDf3 =  pd.read_sql_query(ordersCountByTotalAmount3, mydb)
                ordersCountByTotalAmountDf4 =  pd.read_sql_query(ordersCountByTotalAmount4, mydb)
                ordersCountByTotalAmountDf5 =  pd.read_sql_query(ordersCountByTotalAmount5, mydb)

                filteringData = [list(ordersCountByTotalAmountDf1['No Of Orders']), list(ordersCountByTotalAmountDf2['No Of Orders']), 
                            list(ordersCountByTotalAmountDf3['No Of Orders']), list(ordersCountByTotalAmountDf4['No Of Orders']), list(ordersCountByTotalAmountDf5['No Of Orders'])]
                ordersCountByTotalAmountDf = pd.DataFrame(filteringData)
                ordersCountByTotalAmountDf.columns = ['Orders']
                amountRange = ['<100', '101 - 300', '301 - 500', '501 - 1000', '>1000']
                ordersCountByTotalAmountDf['AmountRange'] = amountRange

                st.table(ordersCountByTotalAmountDf)

            with col8:
                st.subheader('Orders Count By Month, By Year')

                ordersCount = ("SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', "
                               "DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', "
                               "MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' "
                               "FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" )

                ordersDf = pd.read_sql(ordersCount, mydb)

                totalOrderCount =ordersDf[['Year', 'Month Name', 'No Of Orders']]
                totalOrderCountDf = totalOrderCount.pivot_table(index = 'Month Name', columns = 'Year', values='No Of Orders', aggfunc = 'sum')
                totalOrderCountDf = (((totalOrderCountDf.replace(np.nan, 0)).astype(int)).iloc[:, ::-1]).reset_index()
                totalOrderCountDf.columns.values[0] = "Month Name/Year"

                st.table(totalOrderCountDf)

            with col9:

                st.subheader('No Of Orders By Year')

                ordersCount = ("SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', "
                               "DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', "
                               "MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' "
                               "FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" )

                ordersDf = pd.read_sql(ordersCount, mydb)

                def noOfOrders():   
                    noOfOrdersDf = (ordersDf.groupby(['Year'])['No Of Orders'].sum()).reset_index()
                    return noOfOrdersDf

                noOfOrdersCountDf = noOfOrders()

                optionSelect = st.multiselect('select year', options=noOfOrdersCountDf['Year'].unique(), 
                                            default = noOfOrdersCountDf['Year'].unique())
                ordersByYearDf = noOfOrdersCountDf.query("Year == @optionSelect")

                st.bar_chart(ordersByYearDf, x='Year', y='No Of Orders')

            # pie chart
            st.subheader("Last 30days Orders")

            ordersLastMonthCount = ("select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', "
                                    "DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', "
                                    "MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' "
                                    "from ecomm.orders "
                                    "where orders.order_submit_dt_tm >= ( CURDATE() - INTERVAL 1 MONTH) "
                                    "GROUP BY DATE(order_submit_dt_tm)")

            ordersLastMonthCountDf = pd.read_sql(ordersLastMonthCount, mydb)
            fig = px.pie(ordersLastMonthCountDf, values='No Of Orders', names='Date')

            st.plotly_chart(fig)


        if selected == "Inventory":

            # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            graph = st.selectbox("Select Graph:", ("Categories", "Products"))

            if graph == "Categories":

                st.subheader('Stock Quantity By Categories')

                productsStock = ("SELECT c2.catalog_name AS categories, c1.catalog_name AS products, p.product_name, ps.product_sku_id, "
                                "ps.product_sku_cd, ps.price, ps.status, SUM(ps.count) AS stock_count "
                                "FROM product_sku ps, product p, product_catalog_dir pc, catalog_dir c1, catalog_dir c2 "
                                "WHERE ps.product_id = p.product_id AND p.product_id = pc.product_id "
                                "AND pc.catalog_id = c1.catalog_id AND c1.parent_catalog_id = c2.catalog_id "
                                "GROUP BY categories ORDER BY categories")

                productsStockDF = pd.read_sql_query(productsStock, mydb)

                productsStockByCateDF = productsStockDF[["categories", "stock_count"]]

                target_value = 5
                high_level = 45

                # Create the line chart with tooltips
                chart = alt.Chart(productsStockByCateDF).mark_line().encode(
                    x='categories',
                    y='stock_count',
                    tooltip=['categories', 'stock_count'] # Adding 'tooltip' here will show these fields on hover
                ).properties(
                    width=600,  # Set the width of the chart
                    height=350  # Set the height of the chart
                )

                # Create the target line
                target_line = alt.Chart(pd.DataFrame({'target': [target_value]})).mark_rule(color='red').encode(
                    y='target:Q'
                )

                # Create the high-level line
                high_level_line = alt.Chart(pd.DataFrame({'target': [high_level]})).mark_rule(color='green').encode(
                    y='target:Q'
                )

                # Combine the line chart and the target line
                final_chart = chart + target_line + high_level_line

                # Show the chart using Streamlit
                st.altair_chart(final_chart, use_container_width=True)

            if graph == "Products":

                from bokeh.models import FactorRange
                from bokeh.plotting import figure
                from bokeh.models import ColumnDataSource

                st.subheader("Sales count by products")

                stockCountByProducts = ("SELECT c.catalog_name AS products, SUM(ps.count) AS stock_count "
                                        "FROM product_sku ps, product p, product_catalog_dir pc, catalog_dir c "
                                        "WHERE ps.product_id = p.product_id AND p.product_id = pc.product_id "
                                        "AND pc.catalog_id = c.catalog_id "
                                        " GROUP BY products; ")

                stockCountByProductsDf = pd.read_sql_query(stockCountByProducts, mydb)

                # Add a new column for color based on stock_count
                stockCountByProductsDf['color'] = ['red' if count < 10 else 'green' for count in stockCountByProductsDf['stock_count']]

                # Create a Bokeh ColumnDataSource
                source = ColumnDataSource(stockCountByProductsDf)

                # Define the Bokeh figure
                p = figure(x_range=stockCountByProductsDf['products'], plot_height=350, title="Sales count by products", tooltips=[("Product", "@products"), ("Stock Count", "@stock_count")])

                p.vbar(x='products', top='stock_count', source=source, width=0.5, color='color')
                p.line(x='products', y='stock_count', source=source, line_width=3)

                # Customize the plot
                p.xgrid.grid_line_color = None
                p.ygrid.grid_line_color = None
                p.y_range.start = 0
                p.xaxis.major_label_orientation = 1.2
                p.legend.title = 'Stock Count'
                p.legend.title_text_font_style = "bold"

                # Display the Bokeh plot in Streamlit
                st.bokeh_chart(p)

        if selected == "Staff Metrics":

            # css applied
            page_bg_img = """
                <style>
                div.css-keje6w.esravye1{
                    background-color: #aff0b4;
                    border: 1PX #02070f;
                    padding: 20px 20px 20px 20px; 
                    padding: 5% 5% 5% 7%;
                    border-radius: 20px;
                    text-align: center;
                }
                </style>"""
            st.markdown(page_bg_img, unsafe_allow_html=True)

            # columns for partition
            col1, col2 = st.columns(2)

            with col2:

                st.subheader("Target Orders Given To Staff")

                ordersByStaffAction = ("SELECT os.staff_cd, s.staff_name, DATE(os.last_update_dt_tm) as Date, "
                                       "COUNT(os.order_id) as orderscount, opr.staff_role "
                                       "FROM order_status os "
                                       "LEFT JOIN op_staff s ON os.staff_cd = s.staff_cd "
                                       "LEFT JOIN op_staff_role r ON s.op_staff_id = r.op_staff_id "
                                       "LEFT JOIN op_role opr ON r.role_id = opr.role_id "
                                       "GROUP BY os.staff_cd")

                # Read SQL data and Excel data
                ordersByStaffActionDf = pd.read_sql(ordersByStaffAction, mydb)
                thresholdData = pd.read_excel('Task/sample_data.xlsx')

                # Create a dictionary from the threshold table
                threshold_dict = dict(zip(thresholdData['Name'], thresholdData['Threshold Value']))

                # Apply the style to the 'staff_cd' column
                def color_status_cd(orderscount, staff_cd):
                    if staff_cd in threshold_dict and orderscount >= threshold_dict[staff_cd]:
                        return 'color: green'
                    else:
                        return 'color: red'

                styled_table = ordersByStaffActionDf.copy()
                styled_table['staff_cd'] = styled_table.apply(lambda row: color_status_cd(row['orderscount'], row['staff_cd']), axis=1)

                # Display the styled table in Streamlit
                st.dataframe(styled_table.style.applymap(lambda style: style, subset=['staff_cd']))

    if page == "evadellaapprawdata.py":

        st.title('Raw Data To Home Page')

        # authenticator.logout("logout")

        st.subheader('Total Orders Details')

        ordersCount = ("SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', "
                       "DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', "
                       "MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' "
                       "FROM ecomm.orders "
                       "GROUP BY DATE(order_submit_dt_tm)" )
 
        # unShippedOrdersMonthCountDf1
        ordersDf = pd.read_sql(ordersCount, mydb)

        totalOrders = sum(ordersDf['No Of Orders'])

        st.metric("Total No Of Orders", totalOrders)

        st.dataframe(ordersDf)
