import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.markdown(
    """
    <style>
        css-j7qwjs e1fqkh3o7 {display: none;}
    </style>
    """,unsafe_allow_html=True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_excel("Bindaree History.xlsx")
df['Period'] = df['Date'].dt.strftime("%b%Y")
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['MonthName'] = df['Date'].dt.strftime("%B")

#Measure
# max_dt = ''.join(df.loc[df['Date']==max(df['Date']),'Period'].unique().tolist())
date_list = df['Period'].unique().tolist()
date_list = sorted(date_list, key=lambda x : datetime.strptime(x,"%b%Y"),reverse=True)
bas_cat_list = df['Bas Category'].unique().tolist()
bas_code_list = df['Bas Code'].unique().tolist()


#SIDE BAR
st.sidebar.markdown(f'''<span style="display:inline-block; vertical-align:middle; margin:0 0 26px; border-bottom:1px solid #cecece; width:100%;">
                </span>
''', unsafe_allow_html=True)
st.sidebar.markdown(f'Latest Period : `{max(df["Date"]).strftime("%B %Y")}`')
st.sidebar.markdown(f'Minimum Period : `{min(df["Date"]).strftime("%B %Y")}`')
st.sidebar.markdown(f'''<span style="display:inline-block; vertical-align:middle; margin:0 0 26px; border-bottom:1px solid #cecece; width:100%;">
                </span>
''', unsafe_allow_html=True)

item_selected = st.sidebar.selectbox("Filter BAS Item",bas_cat_list,key='item_selected',index=len(bas_cat_list)-1)
st.sidebar.markdown(f'''<span style="display:inline-block; vertical-align:middle; margin:0 0 26px; border-bottom:1px solid #cecece; width:100%;">
                </span>
''', unsafe_allow_html=True)
st.sidebar.markdown(f'''<p style="color:#294C89; font-weight:bold; margin:0;font-size:15px;">Select Period</p><br>''', unsafe_allow_html=True)

months_choice = ['January','February','March','April','May','June','July',
                 'August','September','October','November','December']

y,m = st.sidebar.columns(2)
with y:
   selected_year = y.selectbox("Year",set(df['Year']),key='year_selected',index=len(set(df['Year']))-1)
with m:
   selected_month = m.selectbox("Month",months_choice,key='month_selected')

period_selected = datetime.strptime(str(selected_year)+str(selected_month),"%Y%B")
previous_month = datetime(period_selected.year,period_selected.month-1,1) if period_selected.month != 1 else datetime(period_selected.year-1,12,1)
previous_year = datetime.strptime(str(selected_year-1)+str(selected_month),"%Y%B")

# period_selected = st.sidebar.selectbox("Year",date_list,key='period_selected')

#SELECTED
amount_selected = df[(df['Bas Category']==item_selected)&(df['Date']==period_selected)]['Amount'].sum()
amount_prev_month = df[(df['Bas Category']==item_selected)&(df['Date']==previous_month)]['Amount'].sum()
amount_prev_year = df[(df['Bas Category']==item_selected)&(df['Date']==previous_year)]['Amount'].sum()
delta_prev_month = f"{(abs(amount_selected)-abs(amount_prev_month))/abs(amount_prev_month) :,.2f}%"
delta_prev_year = f"{(abs(amount_selected)-abs(amount_prev_year))/abs(amount_prev_year) :,.2f}%"



amount_selected_1a = df[(df['Bas Code']=='1A')&(df['Date']==period_selected)]['Amount'].sum()
amount_selected_1a_f = f"{amount_selected_1a:,.2f}"
amount_selected_1b = df[(df['Bas Code']=='1B')&(df['Date']==period_selected)]['Amount'].sum()
amount_selected_1b_f = f"{amount_selected_1b:,.2f}"
amount_prev_year_1a = df[(df['Bas Code']=='1A')&(df['Date']==previous_year)]['Amount'].sum()
amount_prev_year_1a_f = f"{amount_prev_year_1a:,.2f}"
amount_prev_year_1b = df[(df['Bas Code']=='1B')&(df['Date']==previous_year)]['Amount'].sum()
amount_prev_year_1b_f = f"{amount_prev_year_1b:,.2f}"

if amount_selected_1a>=amount_prev_year_1a:
    _hex_1a = "#228B22"
    _url_1a = "https://assets.dryicons.com/uploads/icon/preview/1325/large_1x_up.png"
else:
    _hex_1a = "#C70039"
    _url_1a = "https://assets.dryicons.com/uploads/icon/preview/554/large_1x_down.png"

if amount_selected_1b>=amount_prev_year_1b:
    _hex_1b = "#228B22"
    _url_1b = "https://assets.dryicons.com/uploads/icon/preview/1325/large_1x_up.png"
else:
    _hex_1b = "#C70039"
    _url_1b = "https://assets.dryicons.com/uploads/icon/preview/554/large_1x_down.png"




#MAIN
st.markdown(f'''<h1 style="color:#294C89; font-weight:bold; margin:0;font-size:45px;">Bindaree Beef Dashboard </h1>
                <p style="font-style:italic; margin:0;font-size:20px;">{selected_month} {selected_year}</p>
                <span style="display:inline-block; vertical-align:middle; margin:0 0 26px; border-bottom:1px solid #cecece; width:100%;">
                </span>
                <p><br></p>
''', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)

with m1:
    m1.metric("Amount",f"{amount_selected :,.2f}")
with m2:
    m2.metric("Prev Month",f"{amount_prev_month :,.2f}",delta_prev_month)

with m3:
    m3.metric("Prev Year",f"{amount_prev_year :,.2f}",delta_prev_year)


df_selected_bas_item = df[(df['Bas Category']==item_selected)]
df_selected_bas_period = df.loc[(df['Date']==period_selected),['Period','Bas Category','Bas Code','Amount']]
df_yoy = df.loc[(df['Date']>=datetime(previous_year.year,1,1))&
                (df['Date']<=period_selected)&
                (df['Bas Category']==item_selected),:]
df_yoy_payable_receivable = df.loc[(df['Date']>=previous_year)&
                (df['Date']<=period_selected)&
                (df['Bas Code'].isin(['1A','1B'])),:]


# Trend Analysis
fig = px.line(df_selected_bas_item, 
              x="Date", 
              y="Amount",
              title=f'Trend Analysis by {item_selected}')
for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ''
st.plotly_chart(fig,theme="streamlit",use_container_width=True)


fig2 = px.line(df_yoy, 
               x="MonthName",
               y="Amount", 
               color='Year',
               title=f'GST Group BAS Summary by {item_selected}',
               category_orders={"MonthName": ["January", "February", "March", "April", "May", "June",
                                          "July", "August", "September", "October", "November", "December"]})
for axis in fig2.layout:
    if type(fig2.layout[axis]) == go.layout.XAxis:
        fig2.layout[axis].title.text = ''
st.plotly_chart(fig2,theme="streamlit",use_container_width=True)

fig3 = px.line(df_yoy_payable_receivable, x="Date", y="Amount", color='Bas Category',markers=True,title=f'GST Payable vs GST Receivable {selected_month} {selected_year-1} - {selected_month} {selected_year}')
for axis in fig3.layout:
    if type(fig3.layout[axis]) == go.layout.XAxis:
        fig3.layout[axis].title.text = ''
st.plotly_chart(fig3,theme="streamlit",use_container_width=True)

st.markdown(f"""
<table>
  <tr>
    <th>Metric</th>
    <th>{period_selected.strftime("%B %Y")}</th>
    <th>{previous_year.strftime("%B %Y")}</th>
  </tr>
  <tr style="font-size:15px;">
    <td>GST Payable</td>
    <td style="color:{_hex_1a};">{amount_selected_1a_f} <img src="{_url_1a}" height='18' width='18'/></td>
    <td>{amount_prev_year_1a_f}</td>
  </tr>
  <tr style="font-size:15px;">
    <td>GST Receivable</td>
    <td style="color:{_hex_1b};" >{amount_selected_1b_f} <img src="{_url_1b}" height='18' width='18'/</td>
    <td>{amount_prev_year_1b_f}</td>
  </tr>
</table>
""",unsafe_allow_html=True)

st.markdown(f'''<h1 style="font-weight:bold; margin:0;font-size:15px;"><br>BAS Info</h1>''', unsafe_allow_html=True)
st.dataframe(df_selected_bas_period)
