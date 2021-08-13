import pandas as pd
import streamlit as st
import base64
from langdetect import detect


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV File</a>'
    return href


def load_app():
    csv = pd.read_csv(app_file)
    csv.loc[:, 'Source'] = 'App Store'
    csv.drop_duplicates(subset=['Content', 'Name'], keep='first', inplace=True)
    csv.drop(columns=['Title', 'Name', 'Rating', 'Version'], inplace=True)
    mask = (csv['Content'].str.len() >= 10)
    csv = csv.loc[mask]
    csv['Date'] = pd.to_datetime(csv['Date']).dt.date
    return csv


def load_play():
    csv = pd.read_csv(play_file)
    csv.loc[:, 'Source'] = 'Play Store'
    csv.drop_duplicates(subset=['Content', 'Name'], keep='first', inplace=True)
    csv.drop(columns=['Title', 'Name', 'Rating', 'Version'], inplace=True)
    mask = (csv['Content'].str.len() >= 10)
    csv = csv.loc[mask]
    csv['Date'] = pd.to_datetime(csv['Date']).dt.date
    return csv


def load_sprinklr():
    csv = pd.read_csv(sprinklr_file)
    csv.drop_duplicates(subset=['SenderListedName', 'Message'], keep='first', inplace=True)
    final_columns = ['SocialNetwork', 'CreatedTime', 'Message', 'MessageType', 'Permalink']
    csv.drop(columns=csv.columns.difference(final_columns), inplace=True)
    # csv['MessageType'] = csv['Message'].astype('str')
    # csv['Permalink'] = csv['Permalink'].astype('str')
    mask = (csv['Message'].str.len() >= 10) & (csv['Message'].str.len() <= 1000)
    csv = csv.loc[mask]
    csv.loc[:, 'CreatedTime'] = pd.to_datetime(csv['CreatedTime']).dt.date
    cols = csv.columns.tolist()
    final_col = [0, 3, 1, 2, 4]
    cols = [cols[i] for i in final_col]
    csv = csv[cols]
    csv.columns = ['Source', 'Date', 'Content', 'MessageType', 'Permalink']
    return csv


@st.cache
def det(x):
    try:
        lang = detect(x)
    except:
        lang = 'Other'
    return lang


# Upload CSV data
page_names = ['About', 'Application']
page = st.sidebar.radio('Navigation', page_names, index=1)
if page == 'Application':
    with st.sidebar.header('Upload CSV data'):
        app_file = st.sidebar.file_uploader("Upload App Store Reviews file", type=['csv'], accept_multiple_files=False)
        play_file = st.sidebar.file_uploader("Upload Play Store Reviews file", type=['csv'],
                                             accept_multiple_files=False)
        sprinklr_file = st.sidebar.file_uploader('Upload Sprinklr Reviews file', type=['csv'],
                                                 accept_multiple_files=False)
    if app_file and play_file and sprinklr_file is not None:
        df_app = load_app()
        df_app = df_app.reindex(columns=df_app.columns.tolist() + ['MessageType', 'Permalink'])
        df_play = load_play()
        df_play = df_play.reindex(columns=df_play.columns.tolist() + ['MessageType', 'Permalink'])
        df_sprinklr = load_sprinklr()
        df_merged = pd.concat([df_app, df_play, df_sprinklr], ignore_index=True)
        if st.button('Add Language Detection'):
            df_merged['Lang code'] = df_merged['Content'].apply(det)
        st.dataframe(df_merged)
        st.markdown(filedownload(df_merged), unsafe_allow_html=True)

    else:
        st.info('Awaiting CSV file upload...')
else:
    st.markdown('''
    # **Project Scythe**

    This website can **append, merge, and translate** CSV files from **Heedzy & Sprinklr**

    ---
    The application's tab generates a sidebar to upload .csv files and a download preview.

    Use "Add Language Detection" button to reload the data with ISO language codes

    **Heedzy cleaning rules**: 

        1. Drop duplicates based on "Name" & "Content" 

        2. Drop "Name", "Title" , "Rating", & "Version" columns

        3. Drop "Content" column rows that are less than 10 characters

    **Sprinklr cleaning rules**: 

        1. Drop duplicates based on "SenderListedName" & "Message"

        2. Keep only "SocialNetwork", "CreatedTime", "Message", "MessageType", "Permalink" 

        3. Drop "Message" column rows that are less than 10 and more than 1000 characters  
    ''')
