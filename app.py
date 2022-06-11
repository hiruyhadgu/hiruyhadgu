import os
import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

### --- SET UP THE PAGE
st.set_page_config(page_title='Howard County Council Candidate Contributions')
st.markdown("<h1 style='text-align: center; color: #007af9;'>Howard County 2022 Elections \
for County Executive and County Council</h1>", unsafe_allow_html=True)
st.write('Howard County will hold its primary elections on July 19, 2022.\
            Council seats in District 1 and District 4 and the County Executive race.\
                This page show which candidates rely on contributions for developers.')

### --- LOAD DATAFRAME

menu = ['County Council D1', 'County Council D2', 'County Council D3', 'County Council D4', 'County Council D5', 'County Executive CE']
st.sidebar.header('Choose Election')
choice = st.sidebar.selectbox('Pick Race:', menu)
st.subheader(f'Viewing: {choice} Filing')

foldername = choice.split(' ')[-1]
data_file_folder = f'./{foldername}'
df = []

for file in os.listdir(data_file_folder):
    if file.endswith('.xlsx'):
        sheet_name, extension = file.split('.')
        file = f'{data_file_folder}/{file}'
        df.append(pd.read_excel(file, sheet_name = sheet_name, usecols = 'A:J'))
df_master = pd.concat(df, axis=0)

candidate_name = df_master['Receiving Committee'].unique().tolist()
donor_name = df_master['Contributor Name'].unique().tolist()
contributions = df_master['Contribution Amount'].unique().tolist()
filing_period = df_master['Filing Period'].unique().tolist()

selected_period = st.selectbox('Filing Period:', filing_period)

contributions_selection = st.slider('Contributions:', 
                                min_value = min(contributions),
                                max_value = max(contributions),
                                value=(min(contributions), max(contributions)))

candidate_selection = st.multiselect('Candidate Name:',
                                    candidate_name,
                                    default = candidate_name)

### --- LOAD DEVELOPER LIST TO CROSS REFERENCE

developer_list = pd.read_csv('developercrossreference.csv').drop_duplicates()
developer_list = developer_list.dropna()
developer_list['Developer/Developer Affiliated']=developer_list['Developer/Developer Affiliated'].str.lower()
developer_id = developer_list['Developer/Developer Affiliated']=='yes'
developer_list = developer_list[developer_id]
developer_list=developer_list.reset_index()
developer_list = developer_list.drop_duplicates(subset=['Contributor Name'])
developer_list = developer_list.drop(columns = 'index')
developer_filter=df_master['Contributor Name'].isin(developer_list['Contributor Name'])
developer_contributions = df_master[developer_filter]
developer = st.checkbox('Display Developer Contributions Only')


### --- DEFINING THE FILTER CRITERIA. IF 'developer' IS SELECTED, THE FILTER WILL INCLUDE ONLY DEVELOPERS

if developer:
     mask =(df_master['Contributor Name'].isin(developer_list['Contributor Name']))&(df_master['Filing Period']==selected_period) & (df_master['Contribution Amount'].between(*contributions_selection)) & (
                                    df_master['Receiving Committee'].isin(candidate_selection))
else:
    mask = (df_master['Filing Period']==selected_period) & (df_master['Contribution Amount'].between(*contributions_selection)) & (
                                    df_master['Receiving Committee'].isin(candidate_selection)) 
number_of_results = df_master[mask].shape[0]
sum_of_results = df_master[mask]['Contribution Amount'].sum()
st.markdown(f'*Number of Contributions: {number_of_results}*')
st.markdown(f'*Total Contribution for Selected Range: ${sum_of_results:,.2f}*')

df_master_copy = df_master[mask]
df_master_copy['Contribution Amount']=df_master_copy['Contribution Amount'].astype(float).apply('${:,.2f}'.format)

gb = GridOptionsBuilder.from_dataframe(df_master_copy)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    df_master_copy,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    #enable_enterprise_modules=True,
    height=450, 
    #width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

df_filtered = df_master[mask]


df_grouped1 = df_master[mask].groupby(['Contributor Name', 'Receiving Committee'])
df_grouped = df_grouped1.agg(
    TotalContribution = ("Contribution Amount","sum"),
     NoofContribution=("Contribution Amount","count")).reset_index()
df_grouped = df_grouped.sort_values(by=['NoofContribution'], ascending = False)

df_grouped_copy = df_grouped
df_grouped_copy['TotalContribution']=df_grouped_copy['TotalContribution'].astype(float).apply('${:,.2f}'.format)

gb = GridOptionsBuilder.from_dataframe(df_grouped_copy)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(df_grouped_copy,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
 #   enable_enterprise_modules=True,
    height=450, 
    #width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df_selected = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
st.dataframe(df_selected)