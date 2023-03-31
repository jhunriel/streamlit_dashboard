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

# CSS to inject contained in a string
hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_excel("Bindaree History.xlsx")
df['Period'] = df['Date'].dt.strftime("%b%Y")
df['YearStr'] = df['Date'].dt.strftime("%Y")
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['MonthName'] = df['Date'].dt.strftime("%B")

#Measure
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

#MAIN
st.markdown(f'''<h1 style="color:#294C89; font-weight:bold; margin:0;font-size:45px;">Bindaree Beef Dashboard </h1>
                <p style="font-style:italic; margin:0;font-size:20px;">GST Filing Period : {selected_month} {selected_year}</p>
                <span style="display:inline-block; vertical-align:middle; margin:0 0 26px; border-bottom:1px solid #cecece; width:100%;">
                </span>
                <p><br></p>
''', unsafe_allow_html=True)

entity = st.multiselect("Select Entity",df["Entity"].unique().tolist())


if len(entity) == 0:
    selected_entity = df["Entity"].unique().tolist()
else:
    selected_entity = entity

#SELECTED

period_selected = datetime.strptime(str(selected_year)+str(selected_month),"%Y%B")
previous_month = datetime(period_selected.year,period_selected.month-1,1) if period_selected.month != 1 else datetime(period_selected.year-1,12,1)
previous_year = datetime.strptime(str(selected_year-1)+str(selected_month),"%Y%B")

amount_selected = df[(df['Bas Category']==item_selected)&
                     (df['Date']==period_selected)&
                     (df["Entity"].isin(selected_entity))]['Amount'].sum()
amount_prev_month = df[(df['Bas Category']==item_selected)&
                       (df['Date']==previous_month)&
                        (df["Entity"].isin(selected_entity))]['Amount'].sum()
amount_prev_year = df[(df['Bas Category']==item_selected)&
                      (df['Date']==previous_year)&
                     (df["Entity"].isin(selected_entity))]['Amount'].sum()
delta_prev_month = f"{(abs(amount_selected)-abs(amount_prev_month))/abs(amount_prev_month) :,.2f}%"
delta_prev_year = f"{(abs(amount_selected)-abs(amount_prev_year))/abs(amount_prev_year) :,.2f}%"

def gst_net(amount,item_selected):
    if item_selected == "Net GST":
        if amount < 0:
            return " GST Refund"
        return " GST Payable"
    return ""



amount_selected_1a = df[(df['Bas Code']=='1A')&
                        (df['Date']==period_selected)&
                        (df["Entity"].isin(selected_entity))]['Amount'].sum()
amount_selected_1a_f = f"{amount_selected_1a:,.2f}"
amount_selected_1b = df[(df['Bas Code']=='1B')&
                        (df['Date']==period_selected)&
                        (df["Entity"].isin(selected_entity))]['Amount'].sum()
amount_selected_1b_f = f"{amount_selected_1b:,.2f}"
amount_prev_year_1a = df[(df['Bas Code']=='1A')&
                         (df['Date']==previous_year)&
                         (df["Entity"].isin(selected_entity))]['Amount'].sum()
amount_prev_year_1a_f = f"{amount_prev_year_1a:,.2f}"
amount_prev_year_1b = df[(df['Bas Code']=='1B')&
                         (df['Date']==previous_year)&
                         (df["Entity"].isin(selected_entity))]['Amount'].sum()
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


m1, m2, m3 = st.columns(3)

with m1:
    m1.metric(f"Amount{gst_net(amount_selected,item_selected)}",f"{abs(amount_selected) :,.2f}")
with m2:
    m2.metric(f"Prev Month{gst_net(amount_prev_month,item_selected)}",f"{abs(amount_prev_month) :,.2f}",delta_prev_month)

with m3:
    m3.metric(f"Prev Year{gst_net(amount_prev_year,item_selected)}",f"{abs(amount_prev_year) :,.2f}",delta_prev_year)


df_selected_bas_item = df[(df['Bas Category']==item_selected)&
                          (df["Entity"].isin(selected_entity))].groupby(['Date','Bas Category','Bas Code'])[["Amount"]].sum().reset_index()
df_selected_bas_item["GST"] = abs(df_selected_bas_item["Amount"])
df_selected_bas_period = df.loc[(df['Date']==period_selected)&
                                (df["Entity"].isin(selected_entity)),:].groupby(['Period','Bas Category','Bas Code'])[["Amount"]].sum().reset_index()
df_selected_bas_period["GST"] = abs(df_selected_bas_period["Amount"])
df_selected_bas_period_item = df.loc[(df['Date']==period_selected)&
                                     (df['Bas Category']==item_selected),:].groupby(['Client','Entity'])[["Amount"]].sum().reset_index()
if item_selected == "Net GST":
    df_selected_bas_period_item["GST Payable/Refund"] = df_selected_bas_period_item["Amount"].apply(lambda x : gst_net(x,item_selected))
    # df_selected_bas_period_item["GST Payable/Refund"] = df_selected_bas_period_item["Amount"].apply(lambda x : "GST Refund" if x<0 else "GST Payable")
    df_selected_bas_period_item["Amount"] = abs(df_selected_bas_period_item["Amount"])
df_yoy = df.loc[(df['Date']>=datetime(previous_year.year,1,1))&
                (df['Date']<=period_selected)&
                (df['Bas Category']==item_selected)&
                (df["Entity"].isin(selected_entity)),:].groupby(['MonthName','Year','YearStr','Date','Bas Category','Bas Code'])[["Amount"]].sum().reset_index().sort_values("Date")
df_yoy["GST"] = abs(df_yoy["Amount"])
df_yoy_payable_receivable = df.loc[(df['Date']>=previous_year)&
                (df['Date']<=period_selected)&
                (df['Bas Code'].isin(['1A','1B','7D']))&
                (df["Entity"].isin(selected_entity)),:].groupby(['MonthName','Year','Date','Bas Category','Bas Code'])[["Amount"]].sum().reset_index().sort_values("Date")
df_yoy_payable_receivable["GST"] = abs(df_yoy_payable_receivable["Amount"])

st.markdown(f"<h1 style='text-align: center; font-weight:bold; margin:0;font-size:30px;;'>Total {item_selected}</h1>", unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    st.markdown(f'''<h1 style="font-weight:bold; margin:0;font-size:18px;"><br></h1>''', unsafe_allow_html=True)
    st.table(df_selected_bas_period_item.style.format({"Amount": "{:,.2f}"}))
    

with p2:
    #Pie Chart
    figpie = px.pie(df_selected_bas_period_item, values='Amount', names='Entity')

    st.plotly_chart(figpie,theme="streamlit",use_container_width=True)

chart_type = st.radio("Chart Type",["Line","Bar"],horizontal=True)

if chart_type == "Line":
# Line Chart
    # Trend Analysis
    fig = px.line(df_selected_bas_item, 
                x="Date", 
                y="Amount",
                title=f'Trend Analysis by {item_selected}')
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    st.plotly_chart(fig,theme="streamlit",use_container_width=True)

    #YoY
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

    #GST Payable vs Recievable vs Net
    fig3 = px.line(df_yoy_payable_receivable, 
                   x="Date", 
                   y="Amount", 
                   color='Bas Category',
                   markers=True,
                   title=f'GST Payable vs GST Receivable {selected_month} {selected_year-1} - {selected_month} {selected_year}')
    for axis in fig3.layout:
        if type(fig3.layout[axis]) == go.layout.XAxis:
            fig3.layout[axis].title.text = ''
    st.plotly_chart(fig3,theme="streamlit",use_container_width=True)

if chart_type == "Bar":
#Bar Chart
    # Trend Analysis
    figbar = px.bar(df_selected_bas_item, 
                    x='Date', 
                    y='Amount',
                    title=f'Trend Analysis by {item_selected}')
    for axis in figbar.layout:
        if type(figbar.layout[axis]) == go.layout.XAxis:
            figbar.layout[axis].title.text = ''
    st.plotly_chart(figbar,theme="streamlit",use_container_width=True)

    #YoY
    figbar2 = px.bar(df_yoy, 
                    x="MonthName", 
                    y="Amount",
                    color='YearStr',
                    barmode="group",
                    title=f'GST Group BAS Summary by {item_selected}')
    
    for axis in figbar2.layout:
        if type(figbar2.layout[axis]) == go.layout.XAxis:
            figbar2.layout[axis].title.text = ''
    st.plotly_chart(figbar2,theme="streamlit",use_container_width=True)

    #GST Payable vs Recievable vs Net

    figbar3 = px.bar(df_yoy_payable_receivable, 
                    x="Date", 
                    y="Amount",
                    color='Bas Category',
                    barmode="group",
                    title=f'GST Payable vs GST Receivable {selected_month} {selected_year-1} - {selected_month} {selected_year}')

    for axis in figbar3.layout:
        if type(figbar3.layout[axis]) == go.layout.XAxis:
            figbar3.layout[axis].title.text = ''
    st.plotly_chart(figbar3,theme="streamlit",use_container_width=True)

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

# st.markdown(f'''<h1 style="font-weight:bold; margin:0;font-size:15px;"><br>BAS Info</h1>''', unsafe_allow_html=True)
# st.dataframe(df_selected_bas_period)
