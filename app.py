from email.policy import default
import os
from matplotlib.pyplot import plot
from numpy import disp
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import openpyxl
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from funcs import ag_grid

### --- SET UP THE PAGE

image = Image.open('combined.jpeg')
st.set_page_config(page_title='Howard County Council Candidate Contributions', 
            page_icon=image)
@st.cache
def get_data():
    foldername = choice.split(' ')[-1]
    data_file_folder = f'./{foldername}'
    df = []

    for file in os.listdir(data_file_folder):
        if file.endswith('.xlsx'):
            sheet_name, extension = file.split('.')
            file = f'{data_file_folder}/{file}'
            df.append(pd.read_excel(file, sheet_name = sheet_name, usecols = 'A:J'))
    return df
@st.cache
def get_csv(file):
    csv_data = pd.read_csv(file).drop_duplicates()
    return csv_data

header = st.container()
dataset = st.container()
crossref = st.container()

with header:
    st.title('Howard County Local Election Campagin Finance')
    st.write(
        'Howard County will hold its primary elections on July 19, 2022.\
        Council seats in District 1 and District 4 and the County Executive race.\
        This page provides a visual analysis of all-time campagin contributions for\
        candidates running for the County Council and County Executive.')
    st.markdown('[Click Here](https://data.howardcountymd.gov/DataExplorer/Search.aspx?Application=CouncilMember) to navigate to the county website to find your Councilmember \
        then pick the **District** and **Filing Period** to examine from the left sidebar.')
    
    st.write('__________________')
    
### --- LOAD DATAFRAME
with dataset:
    st.header('Explore The Selected Filings')
    
    menu = ['County Council D1', 'County Council D2', 'County Council D3', 'County Council D4', 'County Council D5', 'County Executive CE']
    st.sidebar.header('Choose Filter Criteria')
    choice = st.sidebar.selectbox('Pick Race:', menu)

    st.markdown(f'##### VIEWING: *{choice}* Filing')

    df_master = pd.concat(get_data(), axis=0)
    df_master['Employer Name']=df_master['Employer Name'].fillna('Not Reported')
    df_master['Employer Occupation']=df_master['Employer Occupation'].fillna('Not Reported')

    candidate_name = df_master['Receiving Committee'].unique().tolist()
    donor_name = df_master['Contributor Name'].unique().tolist()
    contributions = df_master['Contribution Amount'].unique().tolist()
    filing_period = df_master['Filing Period'].unique().tolist()

    selected_period = st.sidebar.selectbox('Filing Period:', filing_period)

    #selected_candidate = st.sidebar.selectbox('Candidate Name:', candidate_name)

    contributions_selection = st.slider('Contributions:', 
                                    min_value = min(contributions),
                                    max_value = max(contributions),
                                    value=(min(contributions), max(contributions)))

    candidate_selection = st.multiselect('Candidate Name:',
                                        candidate_name,
                                        default = candidate_name)

### --- LOAD DEVELOPER LIST TO CROSS REFERENCE
with crossref:
    developer_list = get_csv('developercrossreference.csv')
    developer_list = developer_list.dropna()
    developer_list['Developer/Developer Affiliated']=developer_list['Developer/Developer Affiliated'].str.lower()
    developer_id = developer_list['Developer/Developer Affiliated']=='yes'
    developer_list = developer_list[developer_id]
    developer_list=developer_list.reset_index()
    developer_list = developer_list.drop_duplicates(subset=['Contributor Name'])
    developer_list = developer_list.drop(columns = 'index')
    developer_filter=df_master['Contributor Name'].isin(developer_list['Contributor Name'])
    developer_contributions = df_master[developer_filter]
    developer = st.sidebar.checkbox('Display Developer Contributions Only')

    ### --- DEFINING THE FILTER CRITERIA. IF 'developer' IS SELECTED, THE FILTER WILL INCLUDE ONLY DEVELOPERS
    base_mask = (df_master['Filing Period']==selected_period) & (df_master['Contribution Amount'].between(*contributions_selection)) & (
                                    df_master['Receiving Committee'].isin(candidate_selection))
    if developer:
        mask =(developer_filter) & (base_mask)
    else:
        mask = base_mask

    number_of_results = df_master[mask].shape[0]
    sum_of_results = df_master[mask]['Contribution Amount'].sum()
    st.markdown('#### Campaign Finance Summary for Selected Criteria')
    st.text(f'Number of Contributions: {number_of_results} \nTotal Contribution: ${sum_of_results:,.2f}')

    df_master_copy = df_master[mask]
    df_master_copy['Contribution Amount']=df_master_copy['Contribution Amount'].astype(float).apply('${:,.2f}'.format)

display_options= ['Report by Filing Period', 'Summary Statistics', 'Show Figures']
display = st.sidebar.selectbox('Show Report', options=display_options, index=0)

if display == display_options[0]:
    display=ag_grid(df_master_copy)
    
df_grouped = df_master[mask].groupby(['Contributor Name', 'Receiving Committee']).agg({'Contribution Amount':["sum"], 'Contributor Name':["count"]})
df_grouped.columns=['Total Contribution', 'No of Contributions']
df_grouped_for_plot = df_grouped
df_grouped = df_grouped.sort_values(by=['No of Contributions'], ascending = False)
df_grouped['Total Contribution']=df_grouped['Total Contribution'].astype(float).apply('${:,.2f}'.format)
if display == display_options[1]:
    display = ag_grid(df_grouped.reset_index())

plot_data=False
if display==display_options[2]:
    plot_data = st.sidebar.checkbox('Show Plots for Selected Criteria', value=True)

if plot_data:

        plots = ['Top Ten Contributions', 'Developer Percent Contribution', 'By Filing Period']
        picked_plot = st.sidebar.selectbox('Pick a Plot', plots)
        #st.write(f'{len(picked_plot)}')
        if picked_plot == plots[1]:
            st.write('Select the "Display Developer Contributions" checkbox')
            data_set=['Developer Donations', 'Remaining']
            percent_dev = df_master[mask]['Contribution Amount'].sum()/df_master[base_mask]['Contribution Amount'].sum()
            values = [percent_dev, 1-percent_dev]
            fig = px.pie(df_master['Contribution Amount'], values=values, names=data_set)
            display = st.plotly_chart(fig)
        elif picked_plot == plots[0]:
            table_cols = df_grouped_for_plot.reset_index().sort_values(by=['Total Contribution'], ascending = False).head(10)
            #x_select=st.selectbox('Pick X Axis',table_cols)
           # y_select=st.selectbox('Pick Y Axis', table_cols)
            fig = px.bar(df_master_copy, x=table_cols['Contributor Name'], y=table_cols['Total Contribution'])
            display = st.plotly_chart(fig)