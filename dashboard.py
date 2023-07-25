import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# page configuration
st.set_page_config(page_title='Analytics', page_icon=':bar_chart:', layout='wide')

# document title with icon
st.title(':bar_chart: The Analyzer') 

# styling the title
st.markdown('<style>div.block-container{padding-top:1rem;}</div>', unsafe_allow_html=True)

# upload the data file
fl = st.file_uploader(':file_folder: Upload the file', type=(['csv', 'txt', 'xlsx', 'xls']))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = 'ISO-8859-1')
else:
    os.chdir(r'Home/PROJECTS/CLAU-HUB/Dashboard')
    df = pd.read_csv('Sample-Superstore.csv', encoding = 'ISO-8859-1')

col1, col2 = st.columns((2))
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Getting the min and max date
startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date', endDate))

# filtering the data based on the DATE
df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

# filtering the data based on: REGION, STATE & CITY
st.sidebar.header('Choose your filter: ')

region = st.sidebar.multiselect('Select Region', df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

# filtering the data based on: STATE
state = st.sidebar.multiselect('Select State', df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

# filtering the data based on: CITY
city = st.sidebar.multiselect('Select City', df3['City'].unique())
# if not city:
#     df4 = df3.copy()
# else:
#     df4 = df3[df3['City']isin(city)]

# Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]



category_df = filtered_df.groupby(by = ['Category'], as_index= False)['Sales'].sum()

with col1:
    st.subheader('Category wise Sales')
    fig = px.bar(category_df, x = 'Category', y = 'Sales', text = ['${:,.2f}'.format(x) for x in category_df['Sales']],
                 template= 'seaborn')
    st.plotly_chart(fig, use_container_width=True, height = 200)

with col2:
    st.subheader('Region wise Sales')
    fig = px.pie(filtered_df, values= 'Sales', names = 'Region', hole= 0.5)
    fig.update_traces(text = filtered_df['Region'], textposition = 'outside')
    st.plotly_chart(fig, use_container_width=True)


# visualize and download the data from the charts
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander('Category_View'):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index= False).encode('utf-8')
        st.download_button('Download Data', data = csv, file_name= 'Category.csv', mime= 'text/csv', 
                           help= 'Click here to download the data as a CSV file')

with cl2:
    with st.expander('Region_View'):
        region = filtered_df.groupby(by = 'Region', as_index = False)['Sales'].sum()
        st.write(region.style.background_gradient(cmap='Oranges'))
        csv = region.to_csv(index= False).encode('utf-8')
        st.download_button('Download Data', data = csv, file_name= 'Region.csv', mime= 'text/csv', 
                           help= 'Click here to download the data as a CSV file')