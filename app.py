import pandas as pd
from cv_calc import cv_calc
import streamlit as st
import matplotlib.pyplot as plt
import datetime

# -- Set page config
apptitle = 'Colateral Value Calculator'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

#Header
st.markdown("""
**Collateral Value (CV) Calculator**

Based on the following rules, below we can check out the CV at any given point in time.
""")

#Data Transforms
st.image('collateral_value_formula.png')

data = pd.read_csv('cryptopunks_01-14-2022_13-55-22_downloaded.csv')

cv_data_eth = cv_calc(data,'eth_price','utc_timestamp')['col_value']
cv_data_usd = cv_calc(data,'usd_price','utc_timestamp')['col_value']

out = cv_calc(data,'eth_price','utc_timestamp')[['eth_price','usd_price']]
out['cv_eth'] = cv_calc(data,'eth_price','utc_timestamp')['col_value']
out['cv_usd'] = cv_calc(data,'usd_price','utc_timestamp')['col_value']
out.index.name = 'UTC Time'

#Date filter
st.markdown(''' **Visualizing CV Data** ''')

start_date = st.date_input('Start Date:',value=datetime.datetime(2018,11,1))
end_date = st.date_input('End Date:',value=datetime.datetime.now())

mask = (out.index >= pd.to_datetime(start_date)) & (out.index <= pd.to_datetime(end_date))
filter_data = out.loc[mask]

#Plot
st.text('')
st.markdown(""" **Time plot**  """)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('CV (ETH)', color=color)
ax1.plot(filter_data.index,filter_data['cv_eth'],color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels(ax1.get_xticklabels(),rotation=45,ha='right',va='top')

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('CV (USD)', color=color)
ax2.plot(filter_data.index,filter_data['cv_usd'],color=color)
ax2.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('ETH Price (USD)', color=color)
ax2.plot(filter_data.index,filter_data['usd_price']/filter_data['eth_price'],color=color,alpha=0.3)
ax2.tick_params(axis='y', labelcolor=color, pad=75, width=0)

fig.set_figheight(3)
fig.set_figwidth(5)

st.pyplot(fig)

#Table
st.dataframe(filter_data.dropna(),width=1000,height=400)