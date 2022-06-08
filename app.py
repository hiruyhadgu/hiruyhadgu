import os
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import openpyxl


st.set_page_config(page_title='Howard County Council Candidate Contributions')
st.header('2022 Primary Elections')
st.subheader('Know who is contributing in your local elections')

### --- LOAD DATAFRAME
data_file_folder = './'
df = []

for file in os.listdir(data_file_folder):
    if file.endswith('.xlsx'):
        sheet_name, extension = file.split('.')
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

developer_list = pd.read_csv('developercrossreference.csv').drop_duplicates()
developer_list = developer_list.dropna()
developer_list['Developer/Developer Affiliated']=developer_list['Developer/Developer Affiliated'].str.lower()
developer_id = developer_list['Developer/Developer Affiliated']=='yes'
developer_list = developer_list[developer_id]
developer_list=developer_list.reset_index()
developer_list = developer_list.drop(columns = 'index')
developer_filter=df_master['Contributor Name'].isin(developer_list['Contributor Name'])
developer_contributions = df_master[developer_filter]
developer = st.checkbox('Display Developer Contributions Only')

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
st.dataframe(df_master[mask])


st.dataframe(developer_contributions)

df_contribution_sum = df_master[mask].groupby(by = ['Contributor Name', 'Receiving Committee']).sum()[['Contribution Amount']]
df_contribution_count = df_master[mask].groupby(by = ['Contributor Name','Receiving Committee']).count()[['Contribution Amount']]
df_contribution_count = df_contribution_count.rename(columns = {'Contribution Amount':'No of Contributions'})
df_grouped = [df_contribution_sum, df_contribution_count]
df_grouped = pd.concat(df_grouped, axis = 1)
df_grouped = df_grouped.sort_values(by=['No of Contributions'], ascending = False)
#df_grouped.columns = df_grouped.columns.astype('str')
# df_grouped = df_grouped.unstack()
#st.sidebar.selectbox("Select Candidate Name:", candidate_name)
st.dataframe(df_grouped.reset_index())