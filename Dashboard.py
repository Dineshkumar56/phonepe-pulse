# Required Library

import  streamlit as st

import streamlit_option_menu

from streamlit_option_menu import *

import numpy as np

import pandas as pd

import psycopg2 as pg2

import matplotlib.pyplot as plt

from  plotly.subplots import make_subplots

import plotly_express as px

import plotly.graph_objects as go

from streamlit_vertical_slider import vertical_slider

from streamlit_extras import *

from streamlit_extras.metric_cards import style_metric_cards

import math

from streamlit_card import card

from streamlit_extras.colored_header import colored_header

from streamlit_extras.switch_page_button import switch_page

from streamlit_extras.stoggle import stoggle

import json as js

import time

import pymongo as pm

from st_keyup import st_keyup

from streamlit_extras.streaming_write import write

from streamlit_extras.buy_me_a_coffee import button

from streamlit_extras.keyboard_url import keyboard_to_url

from streamlit_lottie import st_lottie

from streamlit_extras.stateful_button import button

import requests as rs

#____________________________________________________________________________________________________________________________________________________________________________


class Phonepe_pulse:

            def  dashboard(self):

                    # POSTGRESQL CONNECTIVITY
                    dinesh = pg2.connect(host='localhost', user='postgres', password='dinesh', database='phonepe')
                    cursor = dinesh.cursor()
                    # _____________________________________________________________________________________________________________________________________________________________________________
                    # PAGE CONFIGURATION
                    st.set_page_config(page_title='Phonepe Project', layout="wide")
                  # ______________________________________________________________________________________________________________________________________________________________________________
                                                                                                     # PROGRAMS INITIATED
                    with st.sidebar:     # Navbar
                        selected = option_menu(
                                                   menu_title="Phonepe Pulse",
                                                   options=['Transaction Type Analysis',"Mobile Brand Analysis","Location-Wise Analysis",'Time-Based Analysis','GeoPlot Pulse Analysis'],
                                                   icons = ['cash-stack','phone-flip','geo-alt-fill','clock-fill','globe-central-south-asia'],
                                                   menu_icon='alexa',
                                                   default_index=0,
                                               )
                    #__________________________________________________________________________________________________________________________________________________________________________________________---
                                                                                     #________________________________________Condition_____________________________________#
                    if selected == "Transaction Type Analysis":

                        st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

                        explore = option_menu(
                            menu_title="",
                            options=[ 'Explore Dashboard'],
                            icons=[ 'eye-fill'],
                            menu_icon='',
                            default_index=0,
                            orientation='horizontal'
                        )

                        
                        if explore =='Explore Dashboard':

                            st.write("")
                            st.write("")

                            colored_header(
                                label="Transaction Type Analysis",
                                description="",
                                color_name="blue-green-70", )

                            st.write("")
                            st.write("")

                            col1, col2 ,col3 , col4  ,col6= st.columns([8,8,8,8,8])
                            st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                            # FILTERS

                            # 1) state

                            cursor.execute('select distinct(state) from public.map_transaction order by state desc')
                            state_names = [i[0] for i in cursor.fetchall()]  # State Names

                            # 2) year

                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 3) Quater

                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            # Year , Quater Combined
                            with col6.expander("FILTER"):
                                year = st.select_slider('CHOOSE YEAR', options=y_values)
                                q = st.select_slider('CHOOSE QUATER', options=q_values)
                                query = "select distinct(agg_transaction_type) from public.aggregated_transaction"
                                cursor.execute(query)
                                res = [i[0] for i in cursor.fetchall()]
                                type_selected = st.selectbox("Choose Transaction Type", res)

                            with col6.expander("FILTER"):
                                state_selected = st.selectbox('CHOOSE STATE', state_names)
                                option = st.selectbox("CHOOSE VALUE", ['Transaction Amount', 'Transaction Count'])

                                st.write("")
                                order = st.selectbox('CHOOSE ORDER',['Top 10','Bottom 10'])


                            #____________________________________________________________________________________________________________________________________________

                            #_______________________________________________________________________________________________________________________________________________________________

                                                                                          #__________METRICS __________#

                            # Metrics 1 : Total Transaction Count
                            query_1 = f"select sum(agg_transaction_count) from  public.aggregated_transaction where year = '{year}' and quater = {q} and agg_transaction_type = '{type_selected}'   group by agg_transaction_type"
                            cursor.execute(query_1)
                            total_transaction_count = [int(i[0]) for i in cursor.fetchall()]
                            col1.metric(label="Transaction count", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
                                          delta=total_transaction_count[0])
                            #________________________________________________________________________________________________________________________________________________________________

                            # Metrics 2 : Total Transaction Amount
                            query_2 = f"select sum(agg_transaction_amount) from  public.aggregated_transaction where year = '{year}' and quater = {q} and agg_transaction_type = '{type_selected}'   group by agg_transaction_type"
                            cursor.execute(query_2)
                            total_transaction_amount = [int(i[0]) for i in cursor.fetchall()]
                            col2.metric(label="Transaction Amount", value=f"{round(((total_transaction_amount[0]/100000)/10),2)}M",
                                        delta=total_transaction_amount[0])
                            #__________________________________________________________________________________________________________________________________________________________________

                            # Metrics 3 : Avg Transaction Amount

                            query_1 = f"select avg(agg_transaction_amount) from  public.aggregated_transaction where year = '{year}' and quater = {q} and agg_transaction_type = '{type_selected}'   group by agg_transaction_type"
                            cursor.execute(query_1)
                            total_transaction_count = [int(i[0]) for i in cursor.fetchall()]

                            col4.metric(label="Average Transaction Amount", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
                                        delta=total_transaction_count[0]/100)

                            #_________________________________________________________________________________________________________________________________________________
                            # Metrics 4 : Avg Transaction count

                            query_1 = f"select avg(agg_transaction_count) from  public.aggregated_transaction where year = '{year}' and quater = {q} and agg_transaction_type = '{type_selected}'   group by agg_transaction_type"
                            cursor.execute(query_1)
                            total_transaction_count = [int(i[0]) for i in cursor.fetchall()]

                            col3.metric(label="Average Transaction Count", value=f"{round(((total_transaction_count[0] / 100000) / 10), 2)}M",
                                        delta=total_transaction_count[0] / 100)
                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")
                    #___________________________________________________________________________________________________________________________________________________________________

                                                                                          #____________CHARTS___________#
                            #______________________________________________________________________________________________________________________________________________________________________

                            col1 , col2 = st.columns([10,10])

                            # PIE Chart : Total Transaction Type By Count

                            # Pie 1 : Total Transaction Type By Count

                            query_3 = f"select  agg_transaction_type , sum(agg_transaction_count)as Total_Transaction from public.aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by agg_transaction_type;"
                            cursor.execute(query_3)
                            total_transaction_type_by_amount = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction Count"])
                            pie = px.pie(df, names='Transaction Type', values='Transaction Count', hole=0.6,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")
                            with col1.expander(f"Total Transaction Count By Transaction Type In {state_selected} "):

                                 st.plotly_chart(pie, theme=None, use_container_width=True)
                            #______________________________________________________________________________________________________________________________________________________________________

                            # Pie 2 : Total Transaction Type By Amount

                            query_3 = f"select  agg_transaction_type , sum(agg_transaction_amount)as Total_Transaction from public.aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by agg_transaction_type;"
                            cursor.execute(query_3)
                            total_transaction_type_by_amount = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction Amount"])
                            pie = px.pie(df, names='Transaction Type', values='Transaction Amount', hole=0.6,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")
                            with col2.expander(f"Total Transaction Amount By Transaction Type In {state_selected}"):

                                 st.plotly_chart(pie, theme=None, use_container_width=True)


                            #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                            # 3D - Charts :

                            # col1, col2, col3 = st.columns([1, 200, 1])
                            if option == 'Transaction Count':
                                query = f"select state , agg_transaction_type , agg_transaction_count,year ,quater from public.aggregated_transaction where state = '{state_selected}'order by year"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['State','Transaction Type', 'Transaction Count', 'Year','Quater'])

                                fig = px.bar(df, x="Transaction Type", y="Transaction Count", animation_frame="Year",hover_name='State',
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                                with st.expander(f"{option} Of {state_selected} From 2018 To 2022"):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)
                            elif option == 'Transaction Amount':
                                query = f"select state , agg_transaction_type , agg_transaction_amount,year ,quater from public.aggregated_transaction where state = '{state_selected}'order by year"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['State','Transaction Type', 'Transaction Amount', 'Year','Quater'])

                                fig = px.bar(df, x="Transaction Type", y="Transaction Amount", animation_frame="Year",hover_name='State',
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                                with st.expander(f"{option} Of {state_selected} From 2018 TO 2022"):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                            #________________________________________________________________________________________________________________________________________________________________________

                            # # Top / Bottom 10 states By transaction Type filter year option
                            if option == "Transaction Count":
                                if order  == 'Top 10':
                                    query = f"select state , sum(agg_transaction_count) as val,agg_transaction_type   from public.aggregated_transaction where  year = '{year}' and quater = {q} and agg_transaction_type ='{type_selected}' group by state,agg_transaction_type order by val desc limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Count',"Transaction Type"])

                                    fig = px.bar(df, x="State", y="Transaction Count",hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"{order} States By {option} Q{4} In year {year} of {type_selected} Transaction Type"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                                elif order == 'Bottom 10':
                                    query = f"select state , sum(agg_transaction_count) as val,agg_transaction_type   from public.aggregated_transaction where  year = '{year}' and quater = {q} and agg_transaction_type ='{type_selected}' group by state,agg_transaction_type order by val limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Count', "Transaction Type"])

                                    fig = px.bar(df, x="State", y="Transaction Count", hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"{order} States By {option} Q{4} In year {year} of {type_selected} Transaction Type"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                            elif option == "Transaction Amount":
                                if order  == 'Top 10':
                                    query = f"select state , sum(agg_transaction_amount) as val,agg_transaction_type   from public.aggregated_transaction where  year = '{year}' and quater = {q} and agg_transaction_type ='{type_selected}' group by state,agg_transaction_type order by val desc limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Amount',"Transaction Type"])

                                    fig = px.bar(df, x="State", y="Transaction Amount",hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"{order} States By {option} Q{4} In year {year} of {type_selected} Transaction Type"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                                elif order == 'Bottom 10':
                                    query = f"select state , sum(agg_transaction_amount) as val,agg_transaction_type   from public.aggregated_transaction where  year = '{year}' and quater = {q} and agg_transaction_type ='{type_selected}' group by state,agg_transaction_type order by val limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Amount', "Transaction Type"])

                                    fig = px.bar(df, x="State", y="Transaction Amount", hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"{order} States By {option} Q{q} In year {year} of {type_selected} Transaction Type"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                            # #_______________________________________________________________________________________________________________________________________________________________________________________
                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")  # #262730

                            colored_header(
                                label="CONCLUSION",
                                description="Financial and Other services had lower level in Both Transaction Count and Amount",
                                color_name="blue-green-70",
                            )
                            #____________________________________________________________________________________________________________________________________________________________________'

                            if st.button("Click Me!"):
                                if option == "Transaction Count":
                                    query = f"select sum(agg_transaction_count) as val,agg_transaction_type   from public.aggregated_transaction  group by agg_transaction_type order by val "
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Transaction Count', 'Transaction Type'])

                                    fig = px.bar(df, x="Transaction Type", y="Transaction Count", hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"Which Transaction Type  had  lower {option}?"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                                elif option == 'Transaction Amount':
                                    query = f"select sum(agg_transaction_amount) as val,agg_transaction_type   from public.aggregated_transaction  group by agg_transaction_type order by val "
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Transaction Amount', 'Transaction Type'])

                                    fig = px.bar(df, x="Transaction Type", y="Transaction Amount", hover_name='Transaction Type',
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    with st.expander(f"Which  Transaction Type had  lower {option}?"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)


                            #__________________________________________________________________________________________________________________________________________
                            col1,col2,col3 = st.columns([10,5,10])
                            col2.write("")
                            col2.write("")
                            col2.write("")

                            # with col2:
                            #     if st.button("Go To Mobile  Brand Analysis"):
                            #        switch_page(selected)
                    #_______________________________________________________________________________________________________________________________________________________________________________________________
                    elif selected == "Mobile Brand Analysis":

                        st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

                        explore_1 = option_menu(
                            menu_title="",
                            options=[ 'Explore Dashboard'],
                            icons=[ 'eye-fill'],
                            menu_icon='',
                            default_index=0,
                            orientation='horizontal'
                        )


                        if explore_1 == 'Explore Dashboard':

                                st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)
                                st.write('')
                                st.write("")
                                st.write("")
                                colored_header(
                                label="Mobile Brand Analysis",
                                description="",
                                color_name="blue-green-70", )
                                st.write("")
                                st.write("")

                                col1, col2, col3,col4,col5,col6 = st.columns([8,9,8,8,8,8])

                                                                                                         #__________FILTERS___________#

                                # 1) Brand

                                cursor.execute(f"select agg_users_brand from public.aggregated_user where agg_users_brand not in  ('Not Mentioned') group by agg_users_brand order by sum(agg_users_count) desc")
                                brand_values = [i[0] for i in cursor.fetchall()]

                                # 3) State
                                cursor.execute('select distinct(state) from public.map_transaction order by state desc')
                                state_names = [i[0] for i in cursor.fetchall()]  # State Names

                                with col6.expander("FILTER"):
                                    state_selected = st.selectbox('CHOOSE STATE',state_names)
                                    selected_brand = st.selectbox('CHOOSE MOBILE BRAND', brand_values)
                                    option = st.selectbox('CHOOSE OPTION',['Registered Users','App Opens'])
                                    order = st.selectbox('CHOOSE ORDER',['Top 10','Bottom 10'])

                                # 1) Year
                                cursor.execute(f"select distinct(year) from public.aggregated_user where agg_users_brand = '{selected_brand}' order  by year asc ;")
                                y_values = [i[0] for i in cursor.fetchall()]

                                with col6.expander("FILTER"):
                                    year = st.selectbox('CHOOSE YEAR',y_values)
                                    # 2) Quater
                                    cursor.execute(f"select distinct(quater) from public.aggregated_user where agg_users_brand = '{selected_brand}'  and year = '{year}' order  by quater asc ;")
                                    q_values = [i[0] for i in cursor.fetchall()]
                                    quater = st.selectbox('CHOOSE QUATER',q_values)









                            #_____________________________________________________________________________________________________________________________________________________________________________

                                                                #_____________________________METRICS______________________#


                                # Brand selected
                                # col1.write("")
                                col1.write("")
                                col1.metric(label="Mobile Brand", value=selected_brand)

                                style_metric_cards(
                                    border_left_color='#08EED2',
                                    background_color='#0E1117', border_color="#0E1117")

                            #___________________________________________________________________________________________________________________________________________________________________________________

                                # metrics 2: Total User Registered of selected brand :

                                query_5 = f"select  sum(agg_users_count) from public.aggregated_user where agg_users_brand = '{selected_brand}' group by agg_users_brand"
                                cursor.execute(query_5)
                                total_reg_user = [i[0] for i in cursor.fetchall()]

                                col2.metric(label="Overall Registered User", value=f'{round(((total_reg_user[0]/100000)/10),2)}M',delta=int(total_reg_user[0]))

                               #_____________________________________________________________________________________________________________________________________________________________________

                                # Metrices 3 : Appopens

                                query_6 = f"select  sum(agg_users_percentage) from public.aggregated_user where agg_users_brand = '{selected_brand}' group by agg_users_brand"
                                cursor.execute(query_6)

                                total_app_opens = [i[0] for i in cursor.fetchall()]
                                col3.metric(label="Overall User Engagement", value=f'{round(((total_app_opens[0]/611.9999999999987)*100),2)}%',delta=(total_app_opens[0]/611.9999999999987)*100)



                               #_______________________________________________________________________________________________________________________________________________________________________________________

                                # metrics 4: Total User Registered of selected brand with filter :

                                query_5 = f"select  sum(agg_users_count) from public.aggregated_user where agg_users_brand = '{selected_brand}' and year = '{year}' and quater = {quater} group by agg_users_brand"
                                cursor.execute(query_5)
                                total_reg_user = [i[0] for i in cursor.fetchall()]
                                val = f'{round(((total_reg_user[0] / 100000) / 10), 2)}M' if total_reg_user != None else 0
                                col4.metric(label=f"Registered User In Q{quater} of {year}", value=val,delta=int(total_reg_user[0]))

                               #__________________________________________________________________________________________________________________________________________________________________________________________________

                                # Metrices 3 : Appopens with filter

                                query_6 = f"select  sum(agg_users_percentage) from public.aggregated_user where agg_users_brand = '{selected_brand}' and year = '{year}' and quater = {quater} group by agg_users_brand"
                                cursor.execute(query_6)

                                total_app_opens = [i[0] for i in cursor.fetchall()]
                                col5.metric(label=f"Overall UE In Q{quater} of {year}", value=f'{round(((total_app_opens[0] / 611.9999999999987) * 100), 2)}%',
                                            delta=(total_app_opens[0] / 611.9999999999987) * 100)



                            #______________________________________________________________________________________________________________________________________________________________________________
                                                                                                             #_______CHARTS_______#


                                col1,col2 ,col3= st.columns([8,8,8])

                                # 1 ) Quater  and appopens and RU in (filter year , state , year )

                                if option == "Registered Users":
                                    query = f"select quater , sum(agg_users_count) from public.aggregated_user where year = '{year}' and agg_users_brand = '{selected_brand}' and state = '{state_selected}'group by quater order by quater asc"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res,columns=['Quater','Registered Users'])
                                    fig = px.bar(df, x="Quater", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with st.expander(f"In {state_selected} {selected_brand} Brand {option} In The Year Of {year}   (Quater Wise COMPARISON)"):
                                         st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif option == "App Opens":
                                    query = f"select quater , sum(agg_users_appopens) from public.aggregated_user where year = '{year}' and agg_users_brand = '{selected_brand}' and state = '{state_selected}' group by quater order by quater asc"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res,columns=['Quater','App Opens'])
                                    pie = px.pie(df, names='Quater', values='App Opens', hole=0.7,
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])  # change color


                                    pie.update_traces(textposition='outside')
                                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")
                                    with st.expander(f"In {state_selected} {selected_brand} Brand {option} In The Quaters Of {year} "):
                                         st.plotly_chart(pie, theme=None, use_container_width=True)
                               #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                # 3) State - wise Brand Engagement of Ao/Ru

                                col1,col2,col3,col4,col5 = st.columns([10,8,2,8,2])

                                if order == 'Top 10':
                                    if option == "Registered Users":
                                        query = f"select state , sum(agg_users_count) as val from public.aggregated_user where year = '{year}' and quater = {quater} and agg_users_brand = '{selected_brand}' group by state order by val desc limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res,columns=['State','Registered Users'])

                                        fig = px.bar(df, x="State", y="Registered Users")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} India States of {selected_brand} Brand {option} Over The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                                    elif option == 'App Opens':

                                        query = f"select state , sum(agg_users_appopens) as val from public.aggregated_user where year = '{year}' and quater = {quater} and agg_users_brand = '{selected_brand}' group by state order by val desc limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['State', 'App opens'])

                                        fig = px.bar(df, x="State", y="App opens")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} India States of {selected_brand} Brand {option} Over The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif order == 'Bottom 10':
                                    if option == "Registered Users":
                                        query = f"select state , sum(agg_users_count) as val from public.aggregated_user where year = '{year}' and quater = {quater} and agg_users_brand = '{selected_brand}' group by state order by val  limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res,columns=['State','Registered Users'])

                                        fig = px.bar(df, x="State", y="Registered Users")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} India States of {selected_brand} Brand {option} Over The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                                    elif option == 'App Opens':

                                        query = f"select state , sum(agg_users_appopens) as val from public.aggregated_user where year = '{year}' and quater = {quater} and agg_users_brand = '{selected_brand}' group by state order by val  limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['State', 'App opens'])

                                        fig = px.bar(df, x="State", y="App opens")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} India States of {selected_brand} Brand {option} Over The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                #________________________________________________________________________________________________________________________________________________________________________

                                # Top 10 / bottom 10 Brand in each state

                                if order == 'Top 10':
                                    if option == "Registered Users":
                                        query = f"select agg_users_brand  , sum(agg_users_count) as val from public.aggregated_user where year = '{year}' and quater = {quater} and state = '{state_selected}' group by state , agg_users_brand  order by val desc limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res,columns=['Mobile Brand','Registered Users'])

                                        fig = px.bar(df, x="Mobile Brand", y="Registered Users")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} {option} Brands In {state_selected} In The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)


                                elif order == 'Bottom 10':

                                    if option == "Registered Users":
                                        query = f"select agg_users_brand  , sum(agg_users_count) as val from public.aggregated_user where year = '{year}' and quater = {quater} and state = '{state_selected}' group by state , agg_users_brand  order by val  limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res,columns=['Mobile Brand','Registered Users'])

                                        fig = px.bar(df, x="Mobile Brand", y="Registered Users")
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        fig.update_traces(marker_color='#1BD4BD')
                                        with st.expander(f"{order} {option} Brands In {state_selected} In The Year {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)


                                #_____________________________________________________________________________________________________________________________________________________________________
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")  # #262730

                                colored_header(
                                    label="CONCLUSION",
                                    description="The Mobile Brands Xiaomi,Samsung,Vivo,Oppo,Others,Realme,Apple,Motorola,Oneplus,Huawei Has Higher User Engagement",
                                    color_name="blue-green-70",
                                )
                                # ____________________________________________________________________________________________________________________________________________________________________'

                                if st.button("Click Me!"):
                                    if order == "Top 10":
                                        query = f"select agg_users_brand , sum(agg_users_count) val from public.aggregated_user where agg_users_brand != 'Not Mentioned' group by agg_users_brand order by val desc limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Mobile Brand', 'User Engagement'])

                                        fig = px.pie(df, names="Mobile Brand", values="User Engagement",
                                                     color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        with st.expander(f"What are the Mobile Brands has Higher User Engagement ?"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                                    elif order == "Bottom 10":
                                        query = f"select agg_users_brand , sum(agg_users_count) val from public.aggregated_user where agg_users_brand != 'Not Mentioned' group by agg_users_brand order by val limit 10;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Mobile Brand', 'User Engagement'])

                                        fig = px.pie(df, names="Mobile Brand", values="User Engagement",
                                                     color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        with st.expander(f"What are the Mobile Brands has Lower User Engagement ?"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                    #_______________________________________________________________________________________________________________________________________________________________________________________________
                    elif selected == "Location-Wise Analysis":



                        st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)


                        selected_1 = option_menu(
                                menu_title="",
                                options=['CHOOSE OPTION', 'TRANSACTION', "USER"],
                                icons=['arrow-right-circle-fill', 'cash-coin', 'people-fill'],
                                default_index=0,
                                orientation ='horizontal'
                            )
                        st.write("")
                        st.write("")



                        if selected_1 == 'CHOOSE OPTION':
                            def lottie(filepath):
                                with open(filepath, 'r') as file:
                                    return js.load(file)

                            # Spinner:
                            col1, col2, = st.columns([10, 8])
                            col1.write("")
                            col1.write("")
                            with col1:
                                file = lottie('p2.json')
                                st_lottie(
                                    file,
                                    speed=1,
                                    reverse=False,
                                    loop=True,
                                    quality='low',
                                    # renderer='svg',
                                    height=600,
                                    width=600,
                                    key=None
                                )
                            with col2:
                                file = lottie('u1.json')
                                st_lottie(
                                    file,
                                    speed=1,
                                    reverse=False,
                                    loop=True,
                                    quality='low',
                                    # renderer='svg',
                                    height=600,
                                    width=600,
                                    key=None
                                )



                        elif selected_1 == 'TRANSACTION':



                            colored_header(
                                    label="STATE TRANSACTION ANALYSIS",
                                    description="",
                                    color_name="blue-green-70",
                                )

                            st.write("")

                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")



                        #_____________________________________________________________________________________________________________________________

                                                                             #____________FILTERS___________#

                            col1,col2,col3,col4,col5 = st.columns([10,7,8,8,7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]


                            # 3) State
                            cursor.execute('select distinct(state) from public.map_transaction order by state desc')
                            state_names = [i[0] for i in cursor.fetchall()]  # State Names


                            with col5.expander("FILTER"):
                                st.write("")
                                state_selected = st.selectbox('CHOOSE STATE', state_names)
                            with col5.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('CHOOSE YEAR', options=y_values)
                                st.write("")
                                q = st.select_slider('CHOOSE QUATER', options=q_values)
                                st.write("")
                                order = st.selectbox("CHOOSE ORDER",['Top','Bottom'])


                            st.write("")
                            st.write('')
                            #_________________________________________________________________________________________________________________________________

                                                                              #________________METRICS__________________#

                            # 1) Metric  : Top State By Amount
                            query = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1=[i[1] for i in cursor.fetchall()]
                            col1.metric(label="Top State By Transaction Amount",
                                        value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            #________________________________________________________________________________________________________________________________________________________________________________________

                            # 2) Metric  : Top State By Count

                            Query = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
                            cursor.execute(Query)
                            res = [i[0] for i in cursor.fetchall()]    # Name
                            cursor.execute(Query)
                            res1 = [i[1] for i in cursor.fetchall()]   # Count

                            col2.metric(label='Top State By Transaction Count',value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            #______________________________________________________________________________________________________________________________________________________________________________________________

                            # 3) Metric  : Current State By Amount

                            Query_1 = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"
                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]  # Name
                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]  # Count
                            col3.metric(label="Current State By Transaction Amount",
                                            value=res[0],
                                            delta=f"{round(((res1[0]/100000)/10),2)}M")

                            #_______________________________________________________________________________________________________________________________________________________________________________________________________

                            # 4) Metric  : Current State By Count

                            Query_1 = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"

                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]  # Name
                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]  # Count
                            col4.metric(label="Current State By Transaction Count",
                                        value=res[0],
                                        delta=f"{round(((res1[0] / 100000) / 10), 2)}M")

                            #____________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                                          #___________CHARTS___________#

                            col1,col2 = st.columns([7,7])

                            #_____________________________________________________________________________________________________________________________________________________________________________

                            # 1) Bar : Top/Bottom  10 States By Count

                            if order == 'Bottom':
                                query=f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
                                fig = px.bar(df, x="State", y="Transaction Count")
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")

                                fig.update_traces(marker_color='#1BD4BD')
                                with col1.expander(f"Bottom 10 State By Transaction Count "):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                            elif order == "Top":
                                    query = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
                                    fig = px.bar(df, x="State", y="Transaction Count")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col1.expander(f"Top 10 State By Transaction Count "):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                            #____________________________________________________________________________________________________________________________________________________________________________________________________

                            # 1) Bar : Top/Bottom  1o States By Count

                            if order == 'Bottom':
                                query=f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
                                fig = px.bar(df, x="State", y="Transaction Amount")
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")

                                fig.update_traces(marker_color='#1BD4BD')
                                with col2.expander(f"Bottom 10 State By Transaction Amount "):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                            elif order == "Top":
                                    query = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
                                    fig = px.bar(df, x="State", y="Transaction Amount")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander(f"Top 10 State By Transaction Amount "):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")


                        #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                      #_______DISTRICTS-WISE ANALYSIS___________#


                            col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

                            colored_header(
                                    label="DISTRICT TRANSACTION ANALYSIS",
                                    description="",
                                    color_name="blue-green-70")
                            st.write("")
                            st.write("")

                            #___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                             #__________FILTERS____________#\

                            col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])


                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            # 3) State
                            cursor.execute('select distinct(top_transaction_district) from public.top_transaction_district_state order by top_transaction_district;')
                            dist_names = [i[0] for i in cursor.fetchall()]  # dist Names


                            with col5.expander("FILTER"):
                                st.write("")
                                dist_selected = st.selectbox('CHOOSE DISTRICT', dist_names)
                            with col5.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('YEAR', options=y_values)
                                st.write("")
                                q = st.select_slider('QUATER', options=q_values)
                                st.write("")
                                order = st.selectbox("ORDER", ['Top', 'Bottom'])

                            #_________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                              #_____________METRICS___________#

                            # 1) Metric  : Top District By Amount
                            query = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col1.metric(label="Top District By Transaction Amount",
                                        value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            # ________________________________________________________________________________________________________________________________________________________________________________________

                            # 2) Metric  : Top district  By Count

                            Query = f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 1;"
                            cursor.execute(Query)
                            res = [i[0] for i in cursor.fetchall()]  # Name
                            cursor.execute(Query)
                            res1 = [i[1] for i in cursor.fetchall()]  # Count

                            col2.metric(label="Top State By Transaction Count",
                                        value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            # ______________________________________________________________________________________________________________________________________________________________________________________________

                            # 3) Metric  : Current State By Amount

                            Query_1 = f"select  top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater = {q} and  top_transaction_district = '{dist_selected}' group by  top_transaction_district;"

                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]  # Name

                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]  # Count
                            col3.metric(label="Current District By  Amount",
                                        value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            # _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                            # # 4) Metric  : Current State By Count

                            Query_1 = f"select  top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state  where year= '{year}' and quater = {q} and  top_transaction_district = '{dist_selected}' group by  top_transaction_district;"

                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]  # Name
                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]  # Count

                            col4.metric(label="Current District By  Count",
                                        value=res[0],
                                        delta=f"{round(((res1[0]/100000)/10),2)}M")

                            st.write("")
                            st.write("")

                            #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________



                                                                                                          #___________CHARTS___________#

                            col1,col2 = st.columns([7,7])

                            #_____________________________________________________________________________________________________________________________________________________________________________

                            # 1) Bar : Top/Bottom  1o districts By Count

                            if order == 'Bottom':
                                query=f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val asc limit 10;"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['District', 'Transaction Count'])
                                fig = px.bar(df, x="District", y="Transaction Count")
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")

                                fig.update_traces(marker_color='#1BD4BD')
                                with col1.expander(f"Bottom 10 District By Transaction Count "):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                            elif order == "Top":
                                    query = f"select top_transaction_district, sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
                                    fig = px.bar(df, x="State", y="Transaction Count")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col1.expander(f"Top 10 District By Transaction Count "):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                            #____________________________________________________________________________________________________________________________________________________________________________________________________

                            # 2) Bar : Top/Bottom  1o districts By amount

                            if order == 'Bottom':
                                query=f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district  order by val asc limit 10;"
                                cursor.execute(query)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
                                fig = px.bar(df, x="District", y="Transaction Amount")
                                fig.update_layout(title_x=1)
                                fig.update_layout(
                                    plot_bgcolor='#0E1117',
                                    paper_bgcolor='#0E1117',
                                    xaxis_title_font=dict(color='#0DF0D4'),
                                    yaxis_title_font=dict(color='#0DF0D4')
                                )
                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")

                                fig.update_traces(marker_color='#1BD4BD')
                                with col2.expander(f"Bottom 10 Districts By Transaction Amount "):
                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                            elif order == "Top":
                                    query = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
                                    fig = px.bar(df, x="District", y="Transaction Amount")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander(f"Top 10 District By Transaction Amount "):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                            st.write("")
                            st.write("")
                            st.write("")


                            #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                          # ________PINCODE TRANSACTION ANALYSIS___________#


                            col1, col2, col3, = st.columns([4, 10, 1])

                            colored_header(
                                label="PINCODE TRANSACTION ANALYSIS",
                                description="",
                                color_name="blue-green-70")

                            st.write("")
                            st.write("")

                            #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                            #_____________FILTER_____________________#

                            col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('SELECT YEAR', options=y_values)
                                st.write("")
                                q = st.select_slider('SELECT QUATER', options=q_values)
                            with col2.expander("FILTER"):

                                st.write("")
                                order = st.selectbox("SELECT ORDER", ['Top', 'Bottom'])

                           #______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                                  #____________CHARTS____________#


                            col1,col2 = st.columns([7,7])


                             # 1)  Top 10 Pincode By Transaction Amount


                            if order == "Top":
                                query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val desc limit 10;"
                                cursor.execute(query_pin)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
                                pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])  # change color

                                pie.update_traces(textposition='outside')
                                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")
                                with col1.expander("Top 10 Pincode By Transaction Amount"):
                                     st.plotly_chart(pie, theme=None, use_container_width=True)

                            elif order == "Bottom":
                                query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val asc limit 10;"
                                cursor.execute(query_pin)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
                                pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])
                                pie.update_traces(textposition='outside')
                                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")
                                with col1.expander("Bottom 10 Pincode By Transaction Amount"):
                                   st.plotly_chart(pie, theme=None, use_container_width=True)


                            #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                            # 2) Top 10 Pincode By Transaction Count

                            if order == 'Top':
                                query_pin_1 = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val desc limit 10;"
                                cursor.execute(query_pin_1)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['Pincode', 'Transaction Count'])
                                pie = px.pie(df, names='Pincode', values='Transaction Count', hole=0.7,
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                                pie.update_traces(textposition='outside')
                                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")
                                with col2.expander("Top 10 Pincode By Transaction Count"):
                                     st.plotly_chart(pie, theme=None, use_container_width=True)

                            if order == 'Bottom':
                                query_pin_1 = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val asc limit 10;"
                                cursor.execute(query_pin_1)
                                res = [i for i in cursor.fetchall()]
                                df = pd.DataFrame(res, columns=['Pincode', 'Transaction Count'])
                                pie = px.pie(df, names='Pincode', values='Transaction Count', hole=0.7,
                                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                                pie.update_traces(textposition='outside')
                                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")
                                with col2.expander("Bottom 10 Pincode By Transaction Count"):
                                      st.plotly_chart(pie, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")
                            #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                             #_____________SDP Transaction Amount Concentration________________________#



                            colored_header(
                                label="SDP TRANSACTION AMOUNT CONCENTRATION ANALYSIS",
                                description="",
                                color_name="blue-green-70")

                            st.write("")
                            st.write("")

                            #___________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                                            #_______________FILTERS___________________#

                            col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):

                                year = st.select_slider('Pick YEAR', options=y_values)

                            with col2.expander("FILTER"):
                                q = st.select_slider('Pick QUATER', options=q_values)




                           #__________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                                          #__________CHARTS_______________#


                            col1,col2,col3 = st.columns([7,7,7])

                                                                                                                                        #_________State_Level__________#

                            querys_top = f"select sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
                            cursor.execute(querys_top)
                            res = [i for i in cursor.fetchall()]
                            df_1 = pd.DataFrame(res, columns=['Amount Top'])

                            querys_bottom = f"select  sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater ={q} and state not in (select state  from public.top_transaction_district_state where year = '{year}' and quater ={q}  group by state order by  sum(top_transaction_amount) desc limit 10) group by state order by val desc ;"

                            cursor.execute(querys_bottom)
                            res = [i for i in cursor.fetchall()]
                            df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

                            state_last = {"Names": [], 'value': []}
                            state_last['Names'].append("Top 10 States")
                            state_last['Names'].append("Other States")

                            state_last['value'].append(int(sum(df_1['Amount Top'])))
                            state_last['value'].append(int(sum(df_2['Amount Bottom'])))

                            df = pd.DataFrame(state_last)

                            pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Transaction Amount'},
                                         hole=0.7,
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                            with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
                                st.plotly_chart(pie, theme=None, use_container_width=True)

                            #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                                  #______________Districts Level__________#

                                # Metrics 3 : District Transaction Concentration :

                            query_top = f"select sum(top_transaction_amount) as val  from public.top_transaction_district_state where year = '{year}' and quater = {q} group by top_transaction_district order by val desc limit 10;"
                            cursor.execute(query_top)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Top'])
                            last = {'Names': [], 'value': []}
                            last['Names'].append("Top 10 Districts")
                            last['value'].append(int(sum(df['Amount Top'])))

                            query_bottom = f"select  sum(top_transaction_amount)  from public.top_transaction_district_state where year = '{year}' and quater ={q} and top_transaction_district not in (select top_transaction_district   from public.top_transaction_district_state where year = '{year}' and quater ={q}  group by top_transaction_district order by sum(top_transaction_amount) desc limit 10) group by top_transaction_district order by sum(top_transaction_amount) desc ;"
                            cursor.execute(query_bottom)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Bottom'])


                            last['Names'].append("Other Districts")
                            last['value'].append(int(sum(df['Amount Bottom'])))

                            df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
                            pie = px.pie(df, names='Names', values='value', hole=0.7,
                                         labels={'Names': 'District Type', 'value': 'Transaction Amount'},
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                            with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
                                  st.plotly_chart(pie, theme=None, use_container_width=True)

                            #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                       #____________PINCODE_____________#

                            query_top = f"select sum(top_transaction_amount) as val  from public.top_transaction_pincode where year = '{year}' and quater = {q} group by top_transaction_pincode order by val desc limit 10;"
                            cursor.execute(query_top)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Top'])
                            last = {'Names': [], 'value': []}
                            last['Names'].append("Top 10 Pincodes")
                            last['value'].append(int(sum(df['Amount Top'])))

                            query_bottom = f"select  sum(top_transaction_amount)  from public.top_transaction_pincode where year = '{year}' and quater ={q} and top_transaction_pincode not in (select top_transaction_pincode   from public.top_transaction_pincode where year = '{year}' and quater ={q} group by top_transaction_pincode  order by sum(top_transaction_amount) desc limit 10) group by top_transaction_pincode order by sum(top_transaction_amount) ;"
                            cursor.execute(query_bottom)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Bottom'])

                            last['Names'].append("Other Pincodes")
                            last['value'].append(int(sum(df['Amount Bottom'])))

                            df = pd.DataFrame(last)
                            pie = px.pie(df, names='Names', values='value', hole=0.7,
                                         labels={'Names': 'Pincode Type', 'value': 'Transaction Amount'},
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                            with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
                                st.plotly_chart(pie, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                          #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                   #___________________Top 10 DP In State By Transaction Amount_______________#

                            col1,col2,col3 = st.columns([2,8,1])



                            colored_header(
                                label="TOP 10 DISTRICTS AND PINCODES IN EACH STATE",
                                description="",
                                color_name="blue-green-70")
                            st.write("")
                            st.write("")

                        #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                              #___________FILTERS_______________#

                            col1, col2, col3 ,col4, col5,col6 = st.columns([5,5,5,5,5,5])

                        #_____________________________________________________________________________________________________________________________________________________
                        # 1) State
                            query="select distinct(state) from public.top_transaction_district_state order by state desc"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            with col1.expander("FILTER"):
                                state_selected =  st.selectbox("PICK STATE",res)
                                st.write("")

                        # 2) Districts and Pincodes

                            with col2.expander("FILTER"):
                                vary = st.selectbox('PICK OPTION',['District','Pincode'])
                                st.write("")

                        # 3) Amount and Count

                            with col3.expander("FILTER"):
                                Choice = st.selectbox('PICK CHOICE', ['Amount', 'Count'])
                                st.write("")

                        # 4) Year and Quater

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):
                                year = st.select_slider("PICK YEAR", options=y_values)

                            with col5.expander('FILTER'):
                                q = st.select_slider('PICK QUATER', options=q_values)


                        # 5) Top / Bottom 10

                            with col6.expander("FILTER"):
                                order = st.selectbox("PICK ORDER",['desc','asc'])
                                st.write("")

                    #____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                               #_____CONDITION METRICS_____#
                            col1,col2,col3  = st.columns([1,100,1])

                            if vary == "District":
                                     if Choice == "Amount":
                                         query_1 = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_district order by val {order} limit 10;"
                                         cursor.execute(query_1)
                                         res = [i for i in cursor.fetchall()]
                                         df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
                                         fig = px.bar(df, x="District", y="Transaction Amount")

                                         fig.update_layout(title_x=1,
                                                           plot_bgcolor='#0E1117',
                                                           paper_bgcolor='#0E1117',
                                                           xaxis_title_font=dict(color='#0DF0D4'),
                                                           yaxis_title_font=dict(color='#0DF0D4')
                                                           )
                                         fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                           hoverlabel_font_color="#0DF0D4",
                                                           marker_color='#1BD4BD')
                                         with col2.expander("Top 10 District By Transaction Amount"):
                                             st.plotly_chart(fig, theme=None, use_container_width=True)

                                     elif Choice == "Count":
                                         query_1 = f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_district order by val {order} limit 10;"
                                         cursor.execute(query_1)
                                         res = [i for i in cursor.fetchall()]
                                         df = pd.DataFrame(res, columns=['District', 'Transaction Count'])
                                         fig = px.bar(df, x="District", y="Transaction Count",)
                                         fig.update_layout(title_x=1,
                                                           plot_bgcolor='#0E1117',
                                                           paper_bgcolor='#0E1117',
                                                           xaxis_title_font=dict(color='#0DF0D4'),
                                                           yaxis_title_font=dict(color='#0DF0D4')
                                                           )
                                         fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                           hoverlabel_font_color="#0DF0D4",
                                                           marker_color='#1BD4BD')
                                         with col2.expander("Top 10 District By Transaction Count"):
                                             st.plotly_chart(fig, theme=None, use_container_width=True)





                            elif vary == "Pincode":
                                    if Choice == "Amount":
                                        query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_pincode order by val {order} limit 10;"
                                        cursor.execute(query_pin)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res,columns=["Pincode","Transaction Amount"])
                                        pie = px.pie(df, names='Pincode', values="Transaction Amount", hole=0.7,
                                                     color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                                        pie.update_traces(textposition='outside')
                                        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                           hoverlabel_font_color="#0DF0D4")


                                        with col2.expander("Top 10 Pincode By Transaction Amount"):
                                            st.plotly_chart(pie, theme=None, use_container_width=True)

                                    elif Choice == "Count":
                                        query_pin = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_pincode order by val {order} limit 10;"
                                        cursor.execute(query_pin)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=["Pincode", "Transaction Count"])
                                        pie = px.pie(df, names='Pincode', values="Transaction Count", hole=0.7,
                                                     color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ', '#51B9A3 '])
                                        pie.update_traces(textposition='outside')
                                        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                           hoverlabel_font_color="#0DF0D4")

                                        with col2.expander("Top 10 Pincode By Transaction Count"):
                                            st.plotly_chart(pie, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                            st.write("")

                        #_________________________________________________________________________________CONCLUSION__________________________________________________________________________-
                            colored_header(
                                label="CONCLUSION",
                                description="State: Telangana , District : Bengaluru urban , Pincode : 500001 has got more Transaction Amount Moreover In Transaction Count Pincode : 500034 , State : Maharashtra, District : Bengaluru urban",
                                color_name="blue-green-70", )


                        elif selected_1 == "USER":


                            #_________________________________________________________________________________________________________________________________________________________________

                                                                                                                  #____State Registered Users Analysis____#


                            st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

                            colored_header(
                                label="STATE USERS ANALYSIS",
                                description="",
                                color_name="blue-green-70",
                            )

                            st.write("")

                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")

                            # __________________________________________________________________________________________________________________________________________________________________

                                                                                                                   # ____________FILTERS___________#

                            col1, col2,col3, col4,col6 = st.columns([8, 10, 9, 9, 7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year desc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            # 3) State
                            cursor.execute('select distinct(state) from public.top_user_district order by state desc')
                            state_names = [i[0] for i in cursor.fetchall()]  # State Names




                            with col6.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('CHOOSE YEAR', options=y_values)

                                q = st.select_slider('CHOOSE QUATER', options=q_values)

                            with col6.expander('FILTER'):
                                state_selected = st.selectbox('CHOOSE STATE', state_names)
                                st.write("")
                                order = st.selectbox("CHOOSE ORDER", ['Top', 'Bottom'])
                                st.write("")
                                option = st.selectbox('CHOOSE OPTION',['Regsitered Users','App Opens'])
                        #_____________________________________________________________________________________________________________________________________________________________________________

                                                                                        # ________________METRICS__________________#

                        # 1) Metric  : Top State By RU

                            query = f"select state , sum(map_registered_users) as val from public.map_user where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col1.metric(label='Top State By Registered Users',value=res[0],delta=f"{round((res1[0]/100000)/10,2)}M")

                        # ________________________________________________________________________________________________________________________________________________________________________________________
                        # 2) Metric  : Top State By Ap

                            query = f"select state , sum(map_appopens) as val from public.map_user where year= '{year}' and quater = {q} group by state order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col2.metric(label='Top State By App Opens', value=res[0], delta=f"{round((res1[0] / 100000) / 10, 2)}M")

                        #_________________________________________________________________________________________________________________________________________________________________
                        # 3) Metric  : Current State By RU

                            Query_1 = f"select state , sum(map_registered_users) as val from public.map_user where year={year} and quater= {q} and state = '{state_selected}' group by state ;"
                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]

                            col3.metric(label='Current State By Registered Users', value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

                        #________________________________________________________________________________________________________________________________________________________________________________
                            # 2) Metric: current State by ap

                            query = f"select state , sum(map_appopens) as val from public.map_user where year= '{year}' and quater = {q} and state = '{state_selected}' group by state ;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col4.metric(label='Top State By App Opens', value=res[0], delta=f"{round((res1[0] / 100000) / 10, 2)}M")

                            st.write("")
                            st.write("")

                            #_______________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                        # ___________CHARTS___________#

                            col1, col2,col3 = st.columns([1, 100,1])

                        # _____________________________________________________________________________________________________________________________________________________________________________

                        # 1) Bar : Top/Bottom  1o States By (RU)
                            if option == 'Regsitered Users':
                                if order == 'Bottom':
                                    query = f"select state , sum(map_registered_users) as val from  public.map_user where year= '{year}' and quater= {q} group by state order by val  limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Bottom 10 State By Registered Users"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif order == "Top":
                                    query = f"select state , sum(map_registered_users) as val from  public.map_user where year= '{year}' and quater= {q} group by state order by val  desc limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Top 10 State By Registered Users"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                        #___________________________________________________________________________________________________________________________________________________________________________________________________________________
                                # 1) Bar : Top/Bottom  1o States By (RU)
                            if option == 'App Opens':  #
                                if order == 'Bottom':
                                    query = f"select state , sum(map_appopens) as val from  public.map_user where year= '{year}' and quater= {q} group by state order by val   limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Bottom 10 States By App Opens"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif order == "Top":
                                    query = f"select state , sum(map_appopens) as val from  public.map_user where year= '{year}' and quater= {q} group by state order by val desc  limit 10;"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Top 10 States By App Opens"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")


                    # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                             # _______DISTRICTS-WISE ANALYSIS___________#


                            colored_header(
                                label="DISTRICT USERS ANALYSIS",
                                description="",
                                color_name="blue-green-70",
                            )

                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")
                            col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)


                        # ___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                             # __________FILTERS____________#\

                            col1, col3, col4, col5,col6 = st.columns([8,  9, 10, 10,6])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year desc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            # 3) State
                            cursor.execute('select distinct(map_user_district) from public.map_user order by map_user_district;')
                            dist_names = [i[0] for i in cursor.fetchall()]  # dist Names



                            with col6.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('PICK YEAR', options=y_values)
                                st.write("")
                                q = st.select_slider('PICK QUATER', options=q_values)
                            with col6.expander("FILTER"):
                                dist_selected = st.selectbox('PICK DISTRICT', dist_names)
                                st.write("")
                                order = st.selectbox("PICK ORDER", ['Top 10', 'Bottom 10'])
                                st.write("")
                                option = st.selectbox('PICK OPTION', ['Registered Users', 'App Opens'])

                            # _________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                      # _____________METRICS___________#

                            # 1) Metric  : Top District By RU
                            query = f"select map_user_district , sum(map_registered_users) as val from  public.map_user where year= '{year}' and quater= {q} group by  map_user_district  order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col1.metric("Top District By Registered Users", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

                            # ______________________________________________________________________________________________________________________________________________________________________________________________
                            # 1) Metric  : Top District By APPopens
                            query = f"select map_user_district , sum(map_appopens) as val from  public.map_user where year= '{year}' and quater= {q} group by  map_user_district  order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col3.metric("Top District By App Opens", value=res[0], delta=f"{round((res1[0] / 100000) / 10, 2)}M")


                            #___________________________________________________________________________________________________________________________________________________________________________________________________________
                            # 3) Metric  : Current State By RU

                            Query_1 = f"select map_user_district , sum(map_registered_users) as val from  public.map_user where year= '{year}' and  quater= {q} and map_user_district = '{dist_selected}' group by  map_user_district"

                            cursor.execute(Query_1)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(Query_1)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col4.metric("Current District By Registered Users", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")
                            #____________________________________________________________________________________________________________________________________________________________________________________________________
                            # 1) Metric  : Top District By APPopens
                            query = f"select map_user_district , sum(map_appopens) as val from  public.map_user where year= '{year}' and quater= {q} and map_user_district = '{dist_selected}'group by  map_user_district  order by val desc limit 1;"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            cursor.execute(query)
                            res1 = [i[1] for i in cursor.fetchall()]
                            col5.metric("Current District By App Opens", value=res[0], delta=f"{round((res1[0] / 100000) / 10, 2)}M")

                            # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                             # ___________CHARTS___________#

                            st.write("")
                            col1, col2 ,col3= st.columns([1,100 ,1])

                            #_____________________________________________________________________________________________________________________________________________________________________________

                            # 1) Bar : Top/Bottom  1o districts By RU

                            if option=="Registered Users":  #
                                if order == 'Bottom 10':
                                    query = f"select map_user_district , sum(map_registered_users) as val from public.map_user where year= '{year}' and quater= {q} group by map_user_district order by val  limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['District', 'Registered Users'])
                                    fig = px.bar(df, x="District", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Bottom 10 District By Registered Users"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif order == "Top 10":
                                    query = f"select map_user_district , sum(map_registered_users) as val from public.map_user where year= '{year}' and quater= {q} group by map_user_district order by val desc  limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander("Top 10 District By Registered Users"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                            #_______________________________________________________________________________________________________________________________________________________________________

                            if option=="App Opens":
                                if order == 'Bottom 10':
                                    query = f"select map_user_district , sum(map_appopens) as val from public.map_user  where year= '{year}' and quater= {q} group by map_user_district order by val  limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['District', 'App Opens'])
                                    fig = px.bar(df, x="District", y="App Opens")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander(f"Bottom 10 District By {option}"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif order == "Top 10":
                                    query = f"select map_user_district , sum(map_appopens) as val from public.map_user  where year= '{year}' and quater= {q} group by map_user_district order by val desc limit 10"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
                                    fig = px.bar(df, x="State", y="Registered Users")
                                    fig.update_layout(title_x=1)
                                    fig.update_layout(
                                        plot_bgcolor='#0E1117',
                                        paper_bgcolor='#0E1117',
                                        xaxis_title_font=dict(color='#0DF0D4'),
                                        yaxis_title_font=dict(color='#0DF0D4')
                                    )
                                    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")

                                    fig.update_traces(marker_color='#1BD4BD')
                                    with col2.expander(f"Top 10 District By {option}"):
                                        st.plotly_chart(fig, theme=None, use_container_width=True)
                      #______________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                    # ________PINCODE TRANSACTION ANALYSIS___________#

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")

                            colored_header(
                                label="PINCODE USERS ANALYSIS",
                                description="",
                                color_name="blue-green-70",
                            )


                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")


                            # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                     # _____________FILTER_____________________#

                            col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year desc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):
                                year = st.select_slider('SELECT YEAR', options=y_values)

                                q = st.select_slider('SELECT QUATER', options=q_values)
                            with col2.expander("FILTER"):
                                option = st.selectbox('SELECT OPTION', ['Registered Users', 'App Opens'])
                                st.write("")
                                order = st.selectbox("SELECT ORDER", ['Top', 'Bottom'])
                                st.write("")

                            # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                                           # ____________CHARTS____________#

                            col1, col2 ,col3= st.columns([1,100,1])

                            # 1)  Top 10 Pincode By Transaction Amount
                            if option == 'Registered Users':
                                if order == "Top":
                                    query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val desc limit 10;"
                                    cursor.execute(query_pin)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
                                    pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
                                    pie.update_traces(textposition='outside')
                                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")
                                    with col2.expander("Top 10 Pincode By Registered Users"):
                                        st.plotly_chart(pie, theme=None, use_container_width=True)

                                elif order == "Bottom":
                                    query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val  limit 10;"
                                    cursor.execute(query_pin)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
                                    pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
                                    pie.update_traces(textposition='outside')
                                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                  hoverlabel_font_color="#0DF0D4")
                                    with col2.expander("Bottom 10 Pincode By Registered Users"):
                                        st.plotly_chart(pie, theme=None, use_container_width=True)
                            elif option =="App Opens":
                                if order == "Top":
                                    query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val desc limit 10;"
                                    cursor.execute(query_pin)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Pincode', 'App Opens"'])
                                    pie = px.pie(df, names='Pincode', values='App Opens"', hole=0.7,
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                          '#51B9A3 '])  # change color
                                    pie.update_traces(textposition='outside')
                                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")
                                    with col2.expander(f"Top 10 Pincode By {option}"):
                                        st.plotly_chart(pie, theme=None, use_container_width=True)

                                elif order == "Bottom":
                                    query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val desc limit 10;"
                                    cursor.execute(query_pin)
                                    res = [i for i in cursor.fetchall()]
                                    df = pd.DataFrame(res, columns=['Pincode', 'App Opens"'])
                                    pie = px.pie(df, names='Pincode', values='App Opens"', hole=0.7,
                                                 color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                          '#51B9A3 '])  # change color
                                    pie.update_traces(textposition='outside')
                                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                      hoverlabel_font_color="#0DF0D4")
                                    with col2.expander(f"Bottom 10 Pincode By {option}"):
                                        st.plotly_chart(pie, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")
                            # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                       # _____________SDP Registered User  Concentration________________________#



                            colored_header(
                                label="SDP REGISTERED USER CONCENTRATION ANALYSIS",
                                description="",
                                color_name="blue-green-70",
                            )


                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")



                            # ___________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                    # _______________FILTERS___________________#

                            col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):
                                st.write("")
                                year = st.select_slider('Pick YEAR', options=y_values)

                            with col2.expander("FILTER"):
                                st.write("")
                                q = st.select_slider('Pick QUATER', options=q_values)


                            # __________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                          # __________CHARTS_______________#

                            col1, col2, col3 = st.columns([7, 7, 7])

                                                                                                                           # _________State_Level__________#

                            querys_top = f"select sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
                            cursor.execute(querys_top)
                            res = [i for i in cursor.fetchall()]
                            df_1 = pd.DataFrame(res, columns=['Amount Top'])

                            querys_bottom = f"select  sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater ={q} and state not in (select state  from  public.top_user_district where year = '{year}' and quater ={q}  group by state order by  sum(top_registered_users) desc limit 10) group by state order by val desc ;"

                            cursor.execute(querys_bottom)
                            res = [i for i in cursor.fetchall()]
                            df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

                            state_last = {"Names": [], 'value': []}
                            state_last['Names'].append("Top 10 States")
                            state_last['Names'].append("Other States")

                            state_last['value'].append(int(sum(df_1['Amount Top'])))
                            state_last['value'].append(int(sum(df_2['Amount Bottom'])))

                            df = pd.DataFrame(state_last)

                            pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Registered Users'},
                                         hole=0.7,
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                  '#51B9A3 '])  # change color
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                            with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
                                st.plotly_chart(pie, theme=None, use_container_width=True)

                            # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                           # ______________Districts Level__________#

                            # Metrics 3 : District Transaction Concentration :

                            query_top = f"select  sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater = {q}  group by top_user_district order by val desc limit 10"
                            cursor.execute(query_top)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Top'])
                            last = {'Names': [], 'value': []}
                            last['Names'].append("Top 10 Districts")
                            last['value'].append(int(sum(df['Amount Top'])))

                            query_bottom = f"select  sum(top_registered_users)  from public.top_user_district where year = '{year}' and quater ={q} and top_user_district not in (select top_user_district  from public.top_user_district where year = '{year}' and quater ={q} group by top_user_district  order by sum(top_registered_users) desc limit 10) group by top_user_district  order by sum(top_registered_users) desc ;"
                            cursor.execute(query_bottom)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Bottom'])

                            last['Names'].append("Other Districts")
                            last['value'].append(int(sum(df['Amount Bottom'])))

                            df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
                            pie = px.pie(df, names='Names', values='value', hole=0.7,
                                         labels={'Names': 'District Type', 'value': 'Registered Users'},
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                  '#51B9A3 '])  # change color
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")
                            with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
                                st.plotly_chart(pie, theme=None, use_container_width=True)

                            # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                     #_____________PINCODE_____________#

                            query_top = f"select sum(top_registered_users) as val  from public.top_user_pincode where year = '{year}' and quater = {q} group by top_user_pincode order by val desc limit 10"
                            cursor.execute(query_top)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Top'])
                            last = {'Names': [], 'value': []}
                            last['Names'].append("Top 10 Pincodes")
                            last['value'].append(int(sum(df['Amount Top'])))

                            query_bottom = f"select  sum(top_registered_users)  from  public.top_user_pincode where year = '{year}' and quater ={q} and top_user_pincode not in (select top_user_pincode  from public.top_user_pincode where year = '{year}' and quater ={q} group by top_user_pincode  order by sum(top_registered_users) desc limit 10) group by top_user_pincode order by sum(top_registered_users) desc;"
                            cursor.execute(query_bottom)
                            res = [i for i in cursor.fetchall()]
                            df = pd.DataFrame(res, columns=['Amount Bottom'])

                            last['Names'].append("Other Pincodes")
                            last['value'].append(int(sum(df['Amount Bottom'])))

                            df = pd.DataFrame(last)
                            pie = px.pie(df, names='Names', values='value', hole=0.7,
                                         labels={'Names': 'Pincode Type', 'value': 'Registered Userst'},
                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                  '#51B9A3 '])  # change color
                            pie.update_traces(textposition='outside')
                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                              hoverlabel_font_color="#0DF0D4")

                            with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
                                st.plotly_chart(pie, theme=None, use_container_width=True)

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")


                            # _______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                     # ___________________Top 10 DP In State By Transaction Amount_______________#

                            colored_header(
                                label="TOP 10 DISTRICTS AND PINCODES IN EACH STATE",
                                description="",
                                color_name="blue-green-70",
                            )


                            style_metric_cards(
                                border_left_color='#08EED2',
                                background_color='#0E1117', border_color="#0E1117")



                            # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                                                            # ___________FILTERS_______________#

                            col1, col2, col3, col4, col5 ,col6 = st.columns([10, 10, 10, 10, 10,10])

                            # ________________________________________________________________________________________________________________________________________________________________________________________
                            # 1) State

                            query = "select distinct(state) from public.top_transaction_district_state order by state desc"
                            cursor.execute(query)
                            res = [i[0] for i in cursor.fetchall()]
                            with col1.expander("FILTER"):
                                st.write("")

                                state_selected = st.selectbox("PICK STATE", res)

                            # 2) Districts and Pincodes

                            with col2.expander("FILTER"):
                                st.write("")
                                vary = st.selectbox('PICK OPTION', ['District', 'Pincode'])



                            # 1) Year
                            cursor.execute('select distinct(year) from public.top_user_pincode order by year desc')
                            y_values = [i[0] for i in cursor.fetchall()]

                            # 2) Quater
                            cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater desc')
                            q_values = [i[0] for i in cursor.fetchall()]

                            with col4.expander("FILTER"):
                                year = st.select_slider("Choose Year", options=y_values)

                            with col3.expander("FILTER"):
                                q = st.select_slider('Choose Quater', options=q_values)


                            # 5) Top / Bottom 10

                            with col5.expander("FILTER"):
                                st.write("")
                                order = st.selectbox("Choose Order", ['Top 10', 'Bottom 10'])

                            with col6.expander("FILTER"):
                                st.write("")
                                option = st.selectbox("Choose Option",['Registered Users','App Opens'])


                            # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                               # _____CONDITION METRICS_____#
                            col1, col2, col3 = st.columns([1, 100, 1])

                            if option == 'Registered Users':
                                if order == 'Top 10':
                                    if vary == "District":

                                        query_1 = f"select map_user_district , sum(map_registered_users) as val from public.map_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by map_user_district order by val desc  limit 10;"
                                        cursor.execute(query_1)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['District', 'Registered Users'])
                                        fig = px.bar(df, x="District", y="Registered Users")

                                        fig.update_layout(title_x=1,
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#0DF0D4'),
                                            yaxis_title_font=dict(color='#0DF0D4')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4",
                                                          marker_color='#1BD4BD')

                                        with col2.expander(f"{order} District By Registered User"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)





                                    elif vary == "Pincode":

                                            query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_user_pincode order by val desc  limit 10;"
                                            cursor.execute(query_pin)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=["Pincode", "Registered Users"])
                                            pie = px.pie(df, names='Pincode', values="Registered Users", hole=0.7,
                                                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                                  '#51B9A3 '])  # change color
                                            pie.update_traces(textposition='outside')
                                            pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#0DF0D4")

                                            with col2.expander(f"{order} Pincode By Registered Users"):
                                                st.plotly_chart(pie, theme=None, use_container_width=True)

                                elif order == 'Bottom 10':
                                    if vary == "District":

                                        query_1 = f"select map_user_district , sum(map_registered_users) as val from public.map_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by map_user_district order by val   limit 10;"
                                        cursor.execute(query_1)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['District', 'Registered Users'])
                                        fig = px.bar(df, x="District", y="Registered Users")

                                        fig.update_layout(title_x=1,
                                                          plot_bgcolor='#0E1117',
                                                          paper_bgcolor='#0E1117',
                                                          xaxis_title_font=dict(color='#0DF0D4'),
                                                          yaxis_title_font=dict(color='#0DF0D4')
                                                          )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4",
                                                          marker_color='#1BD4BD')

                                        with col2.expander(f"{order} District By Registered User"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)





                                    elif vary == "Pincode":

                                        query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_user_pincode order by val  limit 10;"
                                        cursor.execute(query_pin)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=["Pincode", "Registered Users"])
                                        pie = px.pie(df, names='Pincode', values="Registered Users", hole=0.7,
                                                     color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ',
                                                                              '#51B9A3 '])  # change color
                                        pie.update_traces(textposition='outside')
                                        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4")

                                        with col2.expander(f"{order} Pincode By Registered Users"):
                                            st.plotly_chart(pie, theme=None, use_container_width=True)
                        #____________________________________________________________________________________________________________________________________________________________________

                            elif option == 'App Opens':
                                if order == 'Top 10':
                                    if vary == "District":

                                        query_1 = f"select map_user_district , sum(map_appopens) as val from public.map_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by map_user_district order by val desc  limit 10;"
                                        cursor.execute(query_1)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['District', 'App Opens'])
                                        fig = px.bar(df, x="District", y="App Opens")

                                        fig.update_layout(title_x=1,
                                                          plot_bgcolor='#0E1117',
                                                          paper_bgcolor='#0E1117',
                                                          xaxis_title_font=dict(color='#0DF0D4'),
                                                          yaxis_title_font=dict(color='#0DF0D4')
                                                          )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4",
                                                          marker_color='#1BD4BD')

                                        with col2.expander(f"{order} District By {option}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                                    elif vary == 'Pincode':
                                        st.code('Phonepe  has  not  provided  Appopens  Data  for  Pincode')

                                elif order == 'Bottom 10':
                                    if vary == "District":

                                        query_1 = f"select map_user_district , sum(map_appopens) as val from public.map_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by map_user_district order by val   limit 10;"
                                        cursor.execute(query_1)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['District', 'App Opens'])
                                        fig = px.bar(df, x="District", y="App Opens")

                                        fig.update_layout(title_x=1,
                                                          plot_bgcolor='#0E1117',
                                                          paper_bgcolor='#0E1117',
                                                          xaxis_title_font=dict(color='#0DF0D4'),
                                                          yaxis_title_font=dict(color='#0DF0D4')
                                                          )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#0DF0D4",
                                                          marker_color='#1BD4BD')

                                        with col2.expander(f"{order} District By {option}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)
                                    elif vary == 'Pincode':
                                        st.code('Phonepe  has  not  provided  Appopens  Data  for  Pincode')

                            st.write("")
                            st.write("")
                            st.write("")

                            colored_header(
                                label="CONCLUSION",
                                description= "State : maharashtra , District : bengaluru urban , Pincode : 201301 has higher user engagement",
                                color_name="blue-green-70")
                    #---------------------------------------------------------------------------------------------------------------------------_____________________________________________________________________________________________________________________________________________________________________________________________
                    elif selected == "Time-Based Analysis":

                        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                        explore_1 = option_menu(
                            menu_title="",
                            options=[ 'Explore Dashboard'],
                            icons=['arrow-right-circle-fill', 'eye-fill'],
                            menu_icon='',
                            default_index=0,
                            orientation='horizontal'
                        )

                        

                        col1, col2, col3 = st.columns([6, 10, 5])
                        col2.markdown(
                                "<h1 style='font-size: 50px;'><span style='color: cyan;'>Time</span> <span style='color: white;'>Series</span> <span style='color: cyan;'>Analysis</span></h1>",
                                unsafe_allow_html=True)

                        if explore_1 == 'Explore Dashboard':

                                st.write("")
                                st.write("")

                                colored_header(
                                    label="TIME-BASED ANALYSIS",
                                    description="",
                                    color_name="blue-green-70", )

                                st.write("")
                                st.write("")
                                #______________________________________________________________________________________________________________________________________________________________________

                                                                                                     #________FILTER____________#

                                col1, col2, col3,col4 ,col5,col6= st.columns([8,10,10,8,8,10])

                                # Select State or District
                                with col1.expander("FILTER"):
                                    select = st.selectbox('PICK OPTION',['State','District','Pincode'])

                                # State
                                query = "select distinct(state) from public.map_transaction  order by state asc"
                                cursor.execute(query)
                                res = [i[0] for i in cursor.fetchall()]
                                with col2.expander("FILTER"):
                                    state_selected = st.selectbox("CHOOSE STATE",res)

                                # District

                                query_1 = f"select distinct(map_transaction_district) from public.map_transaction  where state = '{state_selected}' order by map_transaction_district asc"

                                cursor.execute(query_1)
                                res_1 = [i[0] for i in cursor.fetchall()]
                                with col3.expander("FILTER"):
                                    dist_selected  = st.selectbox("CHOOSE DISTRICT", res_1)

                                # Year

                                query_2 = "select distinct(year) from public.map_transaction  order by year desc"

                                cursor.execute(query_2)
                                res_2 = [i[0] for i in cursor.fetchall()]
                                with col5.expander("FILTER"):
                                    year = st.selectbox("CHOOSE YEAR", res_2)

                                # pincode

                                query =f"select distinct(top_transaction_pincode) from public.top_transaction_pincode where top_transaction_pincode is not null and state = '{state_selected}' order by top_transaction_pincode"
                                cursor.execute(query)
                                res_2 = [int(i[0]) for i in cursor.fetchall()]
                                with col4.expander("FILTER"):
                                    pincode = st.selectbox("CHOOSE PINCODE", res_2)


                                # Option

                                with col6.expander('FILTER'):
                                   option =  st.selectbox("CHOOSE OPTION",['Transaction Amount',"Transaction Count","Registered Users",'App Opens'])
                                st.write("")
                                st.write("")



                                #__________________________________________________________________________________________________________________________________________________________________________________________

                                c1, c2, c3 = st.columns([18, 10, 18])

                                with c2:
                                    colored_header(
                                        label="QUATER-WISE ANALYSIS",
                                        description="",
                                        color_name="blue-green-70", )


                                st.write("")

                                #________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                        #_______CHARTS_______#
                                #
                                c1, c2, c3 = st.columns([1, 100, 1])



                                # # 1)  Total Amount , Count , RU By state , year , District

                                if select == "State":

                                    if option == 'Transaction Amount':

                                            query = f"select quater , sum(map_transaction_amount) from public.map_transaction where state = '{state_selected}' and year = '{year}' group by quater order by quater asc"

                                            cursor.execute(query)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=['Quater', 'Transaction Amount'])
                                            fig = px.line(df, x="Quater", y="Transaction Amount", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                            fig.update_layout(title_x=1)
                                            fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                            fig.update_traces(marker_color='#FFFFFF')
                                            with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                                                st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "Transaction Count":

                                           query = f"select quater , sum(map_transaction_count) from public.map_transaction where state = '{state_selected}' and year = '{year}' group by quater order by quater asc;"
                                           cursor.execute(query)
                                           res = [i for i in cursor.fetchall()]
                                           df = pd.DataFrame(res, columns=['Quater', 'Transaction Count'])
                                           fig = px.line(df, x="Quater", y="Transaction Count", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                           fig.update_layout(title_x=1)
                                           fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                           fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                           fig.update_traces(marker_color='#FFFFFF')
                                           with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                                               st.plotly_chart(fig, theme=None, use_container_width=True)



                                    elif option == "Registered Users":

                                        query = f"select quater , sum(map_registered_users)  from public.map_user where year ='{year}' and state = '{state_selected}' group by quater order by quater asc"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
                                        fig = px.line(df, x="Quater", y="Registered Users", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "App Opens":

                                        query = f"select quater , sum(map_appopens)  from public.map_user where year ='{year}' and state = '{state_selected}' group by quater order by quater asc"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Quater', 'App Opens'])
                                        fig = px.line(df, x="Quater", y="App Opens", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                #________________________________________________________________________________ Quaters In District Wise__________________________________________________________________________

                                elif select == "District":

                                        if option == 'Transaction Amount':

                                                query = f"select quater , sum(map_transaction_amount) from public.map_transaction where map_transaction_district = '{dist_selected}' and year = '{year}' group by quater order by quater asc"

                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Quater', 'Transaction Amount'])
                                                fig = px.line(df, x="Quater", y="Transaction Amount", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                                        elif option == "Transaction Count":

                                                query = f"select quater , sum(map_transaction_count) from public.map_transaction where map_transaction_district = '{dist_selected}' and year = '{year}' group by quater order by quater asc;"
                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Quater', 'Transaction Count'])
                                                fig = px.line(df, x="Quater", y="Transaction Count", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                                                   st.plotly_chart(fig, theme=None, use_container_width=True)



                                        elif option == "Registered Users":

                                            query = f"select quater , sum(map_registered_users)  from public.map_user where year ='{year}' and map_user_District = '{dist_selected}' group by quater order by quater asc"

                                            cursor.execute(query)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
                                            fig = px.line(df, x="Quater", y="Registered Users", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                            fig.update_layout(title_x=1)
                                            fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                            fig.update_traces(marker_color='#FFFFFF')
                                            with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                                                st.plotly_chart(fig, theme=None, use_container_width=True)

                                        elif option == 'App Opens':

                                                query = f"select quater , sum(map_appopens) from public.map_user where map_user_district = '{dist_selected}' and year = '{year}' group by quater order by quater asc"

                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Quater', 'App Opens'])
                                                fig = px.line(df, x="Quater", y="App Opens", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)


                                                                         #_____________________PINCODE QUATERS_______________________________#

                                elif select == "Pincode":

                                        if option == 'Transaction Amount':

                                                query = f"select quater , sum(top_transaction_amount) from public.top_transaction_pincode where top_transaction_pincode = {pincode} and year = '{year}' group by quater order by quater asc"

                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Quater', 'Transaction Amount'])
                                                fig = px.line(df, x="Quater", y="Transaction Amount", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in pincode {pincode} Over the quaters of {year}"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                                        elif option == "Transaction Count":

                                                query = f"select quater , sum(top_transaction_count) from public.top_transaction_pincode where top_transaction_pincode = {pincode} and year = '{year}' group by quater order by quater asc"
                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Quater', 'Transaction Count'])
                                                fig = px.line(df, x="Quater", y="Transaction Count", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in pincode {pincode} Over the quaters of {year}"):
                                                   st.plotly_chart(fig, theme=None, use_container_width=True)



                                        elif option == "Registered Users":

                                            query = f"select quater , sum(top_registered_users) from public.top_user_pincode where top_user_pincode = {pincode} and year = '{year}' group by quater order by quater asc"

                                            cursor.execute(query)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
                                            fig = px.line(df, x="Quater", y="Registered Users", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                            fig.update_layout(title_x=1)
                                            fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                            fig.update_traces(marker_color='#FFFFFF')
                                            with c2.expander(f"{option} in pincode {pincode} Over the quaters of {year}"):
                                                st.plotly_chart(fig, theme=None, use_container_width=True)

                                        elif option == 'App Opens':
                                            st.code('Phonepe has not provided app opens data for pincode')

                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")

                               #_____________________________________________________________________________________________________________________________________________________________________________________________________________


                                st.write("")

                                c1, c2, c3 = st.columns([17, 10,17])

                                with c2:
                                    colored_header(
                                        label="OVERALL YEAR ANALYSIS",
                                        description="",
                                        color_name="blue-green-70", )

                                #__________________________________________________________________________________________________________________________________________________________________________________________________________________
                                st.write("")
                                c1, c2, c3 = st.columns([1, 100, 1])

                                # # 1)  Total Amount , Count , RU By state , year , District

                                if select == "State":

                                    if option == 'Transaction Amount':

                                        query = f"select year , sum(map_transaction_amount) from public.map_transaction where state = '{state_selected}'  group by year order by year asc"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Year', 'Transaction Amount'])
                                        fig = px.line(df, x="Year", y="Transaction Amount", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "Transaction Count":

                                        query = f"select year , sum(map_transaction_count) from public.map_transaction where state = '{state_selected}'  group by year order by year asc;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Year', 'Transaction Count'])
                                        fig = px.line(df, x="Year", y="Transaction Count", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)



                                    elif option == "Registered Users":

                                        query = f"select year , sum(map_registered_users)  from public.map_user where state = '{state_selected}'  group by year order by year asc;"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Year', 'Registered Users'])
                                        fig = px.line(df, x="Year", y="Registered Users", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "App Opens":

                                            query = f"select year , sum(map_appopens)  from public.map_user where  state = '{state_selected}' group by year order by year asc"

                                            cursor.execute(query)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=['Year', 'App Opens'])
                                            fig = px.line(df, x="Year", y="App Opens", markers='D',
                                                          color_discrete_sequence=['#1BD4BD', '#0AD6CD'])
                                            fig.update_layout(title_x=1)
                                            fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                            fig.update_traces(marker_color='#FFFFFF')
                                            with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                                                st.plotly_chart(fig, theme=None, use_container_width=True)

                                #___________________________________________________________________________DISTRICT YEAR WISE _____________________________________________________________________
                                elif select == "District":

                                    if option == 'Transaction Amount':

                                        query = f"select year , sum(map_transaction_amount) from public.map_transaction where map_transaction_district = '{dist_selected}'  group by year order by year asc"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Year', 'Transaction Amount'])
                                        fig = px.line(df, x="Year", y="Transaction Amount", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "Transaction Count":

                                        query = f"select year , sum(map_transaction_count) from public.map_transaction where  map_transaction_district = '{dist_selected}'  group by year order by year asc;"
                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Year', 'Transaction Count'])
                                        fig = px.line(df, x="Year", y="Transaction Count", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)



                                    elif option == "Registered Users":

                                        query = f"select year , sum(map_registered_users)  from public.map_user where  map_user_district = '{dist_selected}'  group by year order by year asc;"

                                        cursor.execute(query)
                                        res = [i for i in cursor.fetchall()]
                                        df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
                                        fig = px.line(df, x="Quater", y="Registered Users", markers='D',color_discrete_sequence=['#1BD4BD','#0AD6CD'])
                                        fig.update_layout(title_x=1)
                                        fig.update_layout(
                                            plot_bgcolor='#0E1117',
                                            paper_bgcolor='#0E1117',
                                            xaxis_title_font=dict(color='#1BD4BD'),
                                            yaxis_title_font=dict(color='#1BD4BD')
                                        )
                                        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                          hoverlabel_font_color="#1BD4BD")
                                        fig.update_traces(marker_color='#FFFFFF')
                                        with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                                            st.plotly_chart(fig, theme=None, use_container_width=True)

                                    elif option == "App Opens":

                                            query = f"select year , sum(map_appopens) from public.map_user where map_user_district = '{dist_selected}'  group by year order by year asc"

                                            cursor.execute(query)
                                            res = [i for i in cursor.fetchall()]
                                            df = pd.DataFrame(res, columns=['Year', 'App Opens'])
                                            fig = px.line(df, x="Year", y="App Opens", markers='D',
                                                          color_discrete_sequence=['#1BD4BD', '#0AD6CD'])
                                            fig.update_layout(title_x=1)
                                            fig.update_layout(
                                                plot_bgcolor='#0E1117',
                                                paper_bgcolor='#0E1117',
                                                xaxis_title_font=dict(color='#1BD4BD'),
                                                yaxis_title_font=dict(color='#1BD4BD')
                                            )
                                            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                              hoverlabel_font_color="#1BD4BD")
                                            fig.update_traces(marker_color='#FFFFFF')
                                            with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                                                st.plotly_chart(fig, theme=None, use_container_width=True)

                                elif select == "Pincode":

                                            if option == 'Transaction Amount':

                                                query = f"select year , sum(top_transaction_amount) from public.top_transaction_pincode where top_transaction_pincode = {pincode}  group by year order by year asc"

                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Year', 'Transaction Amount'])
                                                fig = px.line(df, x="Year", y="Transaction Amount", markers='D',
                                                              color_discrete_sequence=['#1BD4BD', '#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {pincode}  Over The Years From 2018 To 2022"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)

                                            elif option == "Transaction Count":

                                                query = f"select year , sum(top_transaction_count) from public.top_transaction_pincode where top_transaction_pincode = {pincode}  group by year order by year asc"
                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Year', 'Transaction Count'])
                                                fig = px.line(df, x="Year", y="Transaction Count", markers='D',
                                                              color_discrete_sequence=['#1BD4BD', '#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {pincode}  Over The Years From 2018 To 2022"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)



                                            elif option == "Registered Users":

                                                query = f"select year , sum(top_registered_users) from public.top_user_pincode where top_user_pincode = {pincode}  group by year order by year asc"

                                                cursor.execute(query)
                                                res = [i for i in cursor.fetchall()]
                                                df = pd.DataFrame(res, columns=['Year', 'Registered Users'])
                                                fig = px.line(df, x="Year", y="Registered Users", markers='D',
                                                              color_discrete_sequence=['#1BD4BD', '#0AD6CD'])
                                                fig.update_layout(title_x=1)
                                                fig.update_layout(
                                                    plot_bgcolor='#0E1117',
                                                    paper_bgcolor='#0E1117',
                                                    xaxis_title_font=dict(color='#1BD4BD'),
                                                    yaxis_title_font=dict(color='#1BD4BD')
                                                )
                                                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                                  hoverlabel_font_color="#1BD4BD")
                                                fig.update_traces(marker_color='#FFFFFF')
                                                with c2.expander(f"{option} in {pincode}  Over The Years From 2018 To 2022"):
                                                    st.plotly_chart(fig, theme=None, use_container_width=True)
                                            elif option == 'App Opens':
                                                st.code('Phonepe has not provided app opens data for pincode')
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")

                                colored_header(
                                    label="CONCLUSION",
                                    description="Using This Dashboard User Can Anlaysis The Specific State or District or Pincode in Over the Specific Time Period To Get Insights About Transactions And User Engagement",
                                    color_name="blue-green-70", )
                    #________________________________________________________________________________________________________________________________________________________________________________________________________________________
                    elif selected == 'GeoPlot Pulse Analysis':

                        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                        explore_1 = option_menu(
                            menu_title="",
                            options=[ 'Explore Dashboard'],
                            icons=[ 'eye-fill'],
                            menu_icon='',
                            default_index=0,
                            orientation='horizontal'
                        )


                        col1, col2, col3 = st.columns([7, 10, 5])
                        col2.markdown("<h1 style='font-size: 50px;'><span style='color: cyan;'>Geo</span> <span style='color: white;'>Plot</span> <span style='color: cyan;'>Analysis</span></h1>",unsafe_allow_html=True)

                        if explore_1 == 'Explore Dashboard':

                                st.write("")
                                st.write("")

                                colored_header(
                                    label="GeoPlot Pulse Analysis",
                                    description="",
                                    color_name="blue-green-70", )






                                style_metric_cards(
                                    border_left_color='#08EED2',
                                    background_color='#0E1117', border_color="#0E1117")

                                st.write("")
                                st.write("")

                                col1,col2,col3 = st.columns([5,10,5])


                                with col2.expander('Filter'):
                                    option = st.selectbox('OPTION',['Transaction Amount','Transaction Count','Registered Users','App Opens'])


                                st.write('')
                                st.write('')

                                if option == 'Transaction Amount':


                                    query = f"select state , sum(map_transaction_amount) from public.map_transaction   group by state"

                                    cursor.execute(query)

                                    res = [i for i in cursor.fetchall()]

                                    Map_transaction_df = pd.DataFrame(res,columns=['state','Total Transaction Amount'])


                                    a_t2 = Map_transaction_df[['state', 'Total Transaction Amount']]
                                    a_t2 = a_t2.sort_values(by='state')
                                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                                    response = rs.get(url)
                                    data1 = js.loads(response.content)
                                    print(data1)
                                    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                                    state_names_tra.sort()

                                    df_state_names_tra = pd.DataFrame({'state': state_names_tra})

                                    a_t2['state'] = a_t2['state'].str.replace('-', ' ')
                                    a_t2['state'] = a_t2['state'].str.replace('Dadra & Nagar Haveli & Daman & Diu',
                                                                              'Dadra and Nagar Haveli and Daman and Diu')
                                    a_t2['state'] = a_t2['state'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
                                    a_t2['state'] = a_t2['state'].str.title()

                                    merge_df = df_state_names_tra.merge(a_t2, on='state')

                                    trans_fig = px.choropleth_mapbox(merge_df,
                                                                     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                                     featureidkey='properties.ST_NM', locations='state', color='Total Transaction Amount',
                                                                     color_continuous_scale=['#C8E2E3 ', '#12F6FF'], range_color=(0, 20000000000000),
                                                                     height=1000, zoom=4, center={"lat": 20.5937, "lon": 78.9629}
                                                                     )

                                    trans_fig.update_geos(fitbounds="locations", visible=False)
                                    trans_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7',
                                                            coloraxis_colorbar_title="Total Transaction Amount",  # Set plot background color to black
                                                            paper_bgcolor='black',width=800

                                                            )

                                    trans_fig.update_layout(mapbox_style="open-street-map")
                                    trans_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                                    trans_fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                            hoverlabel_font_color="#12F6FF")
                                    st.plotly_chart(trans_fig,use_container_width=True, width=450)

                                elif option == 'Transaction Count':


                                    query = f"select state , sum(map_transaction_count) from public.map_transaction group by state "

                                    cursor.execute(query)

                                    res = [i for i in cursor.fetchall()]

                                    Map_transaction_df = pd.DataFrame(res,columns=['state','Total Transaction Count'])

                                    Map_transaction_df['Total Transaction Count'] = Map_transaction_df['Total Transaction Count'].apply(lambda x: f'{round((x/1000),2)}T' )

                                    a_t2 = Map_transaction_df[['state', 'Total Transaction Count']]
                                    a_t2 = a_t2.sort_values(by='state')
                                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                                    response = rs.get(url)
                                    data1 = js.loads(response.content)
                                    print(data1)
                                    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                                    state_names_tra.sort()

                                    df_state_names_tra = pd.DataFrame({'state': state_names_tra})

                                    a_t2['state'] = a_t2['state'].str.replace('-', ' ')
                                    a_t2['state'] = a_t2['state'].str.replace('Dadra & Nagar Haveli & Daman & Diu',
                                                                              'Dadra and Nagar Haveli and Daman and Diu')
                                    a_t2['state'] = a_t2['state'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
                                    a_t2['state'] = a_t2['state'].str.title()

                                    merge_df = df_state_names_tra.merge(a_t2, on='state')

                                    trans_fig = px.choropleth_mapbox(merge_df,
                                                                     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                                     featureidkey='properties.ST_NM', locations='state', color='Total Transaction Count',
                                                                     color_continuous_scale=['#C8E2E3 ', '#12F6FF'], range_color=(0, 20000000000),
                                                                     height=1000, zoom=4, center={"lat": 20.5937, "lon": 78.9629}
                                                                     )

                                    trans_fig.update_geos(fitbounds="locations", visible=False)
                                    trans_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7',
                                                            coloraxis_colorbar_title="Total Transaction Count",  # Set plot background color to black
                                                            paper_bgcolor='black',width=800

                                                            )

                                    trans_fig.update_layout(mapbox_style="open-street-map")
                                    trans_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                                    trans_fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                            hoverlabel_font_color="#12F6FF")
                                    st.plotly_chart(trans_fig,use_container_width=True, width=450)

                                elif option == 'Registered Users':

                                    query = f"select state , sum(map_registered_users) from public.map_user group by state"

                                    cursor.execute(query)

                                    res = [i for i in cursor.fetchall()]

                                    Map_transaction_df = pd.DataFrame(res, columns=['state', 'Registered Users'])
                                    Map_transaction_df['Registered Users'] = Map_transaction_df['Registered Users'].apply(lambda x: f'{round((x/1000),2)}T' )


                                    a_t2 = Map_transaction_df[['state', 'Registered Users']]
                                    a_t2 = a_t2.sort_values(by='state')
                                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                                    response = rs.get(url)
                                    data1 = js.loads(response.content)
                                    print(data1)
                                    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                                    state_names_tra.sort()

                                    df_state_names_tra = pd.DataFrame({'state': state_names_tra})

                                    a_t2['state'] = a_t2['state'].str.replace('-', ' ')
                                    a_t2['state'] = a_t2['state'].str.replace('Dadra & Nagar Haveli & Daman & Diu',
                                                                              'Dadra and Nagar Haveli and Daman and Diu')
                                    a_t2['state'] = a_t2['state'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
                                    a_t2['state'] = a_t2['state'].str.title()

                                    merge_df = df_state_names_tra.merge(a_t2, on='state')

                                    trans_fig = px.choropleth_mapbox(merge_df,
                                                                     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                                     featureidkey='properties.ST_NM', locations='state',
                                                                     color='Registered Users',
                                                                     color_continuous_scale='blues',
                                                                     range_color=(0, 200000000000000000),
                                                                     height=1000, zoom=4,
                                                                     center={"lat": 20.5937, "lon": 78.9629},


                                                                     )

                                    trans_fig.update_geos(fitbounds="locations", visible=False)
                                    trans_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7',
                                                            coloraxis_colorbar_title="Registered Users",
                                                            # Set plot background color to black
                                                            paper_bgcolor='black', width=800

                                                            )

                                    trans_fig.update_layout(mapbox_style="open-street-map")
                                    trans_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                                    trans_fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                            hoverlabel_font_color="#12F6FF")
                                    st.plotly_chart(trans_fig, use_container_width=True, width=450)

                                elif option == 'App Opens':

                                    query = f"select state, sum(map_appopens) from public.map_user group by state"
                                    cursor.execute(query)
                                    res = [i for i in cursor.fetchall()]
                                    Map_transaction_df = pd.DataFrame(res, columns=['state', 'App Opens'])
                                    Map_transaction_df['App Opens'] = Map_transaction_df['App Opens'].apply(lambda x: f'{round((x/1000),2)}T' )

                                    a_t2 = Map_transaction_df[['state', 'App Opens']]
                                    a_t2 = a_t2.sort_values(by='state')
                                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                                    response = rs.get(url)
                                    data1 = js.loads(response.content)
                                    print(data1)
                                    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                                    state_names_tra.sort()

                                    df_state_names_tra = pd.DataFrame({'state': state_names_tra})


                                    a_t2['state'] = a_t2['state'].str.replace('-', ' ')
                                    a_t2['state'] = a_t2['state'].str.replace('Dadra & Nagar Haveli & Daman & Diu',
                                                                              'Dadra and Nagar Haveli and Daman and Diu')
                                    a_t2['state'] = a_t2['state'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
                                    a_t2['state'] = a_t2['state'].str.title()

                                    merge_df = df_state_names_tra.merge(a_t2, on='state')

                                    trans_fig = px.choropleth_mapbox(merge_df,
                                                                     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                                     featureidkey='properties.ST_NM', locations='state',
                                                                     color='App Opens',
                                                                     color_continuous_scale=['#C8E2E3 ', '#12F6FF'],
                                                                     range_color=(0, 200000000000000000),
                                                                     height=1000, zoom=4,
                                                                     center={"lat": 20.5937, "lon": 78.9629},

                                                                     )

                                    trans_fig.update_geos(fitbounds="locations", visible=False)
                                    trans_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7',
                                                            coloraxis_colorbar_title="App Opens",
                                                            # Set plot background color to black
                                                            paper_bgcolor='black', width=800

                                                            )

                                    trans_fig.update_layout(mapbox_style="open-street-map")
                                    trans_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                                    trans_fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                                            hoverlabel_font_color="#12F6FF")
                                    st.plotly_chart(trans_fig, use_container_width=True, width=450)

                                colored_header(
                                    label="",
                                    description="",
                                    color_name="blue-green-70", )
                    #____________________________________________________________________________________________________________________________________________________________________________________________________________
                   
                   
#_________________________________________________________________________________________________________________________________________________________________________________

# Creation Object for Class Phonepe Pulse

object = Phonepe_pulse()

object.dashboard()
#_______________________________________________________________________FINISHED_______________________________________________________________________________________________________________________________________________________________________________________________________________________________
