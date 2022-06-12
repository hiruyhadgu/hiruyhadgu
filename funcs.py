from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import streamlit as st
import pandas as pd
def ag_grid(data_set):

    gb = GridOptionsBuilder.from_dataframe(data_set)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    # sel_mode = st.radio('Selection Type', options=['single','multiple'])
    gb.configure_selection(selection_mode='multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridoptions = gb.build()

    grid_response = AgGrid(
        data_set,
        gridOptions=gridoptions,
        data_return_mode=DataReturnMode.AS_INPUT, 
        update_mode=GridUpdateMode.MODEL_CHANGED, 
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        #enable_enterprise_modules=True,
        height=450, 
        #width='100%',
        reload_data=False
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df_selected = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
    st.dataframe(df_selected)