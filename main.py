import pandas as pd
import streamlit as st
import base64

# web title
st.markdown('''
# **CSV FILE MERGER**

This website can **append, merge, and sort** CSV files from **Heedzy & Sprinklr**

---
''')
# Upload CSV data
with st.sidebar.header('1.Upload CSV data'):
    app_file = st.sidebar.file_uploader("Upload App Store Reviews file", type=['csv'])
    play_file = st.sidebar.file_uploader("Upload Play Store Reviews file", type=['csv'])
    sprinklr_file = st.sidebar.file_uploader('Upload Sprinklr Reviews file', type=['csv'])


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV File</a>'
    return href


# CSV data handling
if app_file and play_file and sprinklr_file is not None:

    def load_app():
        csv = pd.read_csv(app_file)
        csv.loc[:, 'Source'] = 'App Store'
        csv.drop(columns=['Title', 'Name', 'Rating', 'Version'], inplace=True)
        csv['Date'] = pd.to_datetime(csv['Date']).dt.date
        csv.drop_duplicates(subset=['Content'], keep='first', inplace=True)
        return csv


    def load_play():
        csv = pd.read_csv(play_file)
        csv.loc[:, 'Source'] = 'Play Store'
        csv.drop(columns=['Title', 'Name', 'Rating', 'Version'], inplace=True)
        csv['Date'] = pd.to_datetime(csv['Date']).dt.date
        csv.drop_duplicates(subset=['Content'], keep='first', inplace=True)
        return csv


    def load_sprinklr():
        csv = pd.read_csv(sprinklr_file)
        final_columns = ['SocialNetwork', 'CreatedTime', 'Message',]
        csv.drop(columns=csv.columns.difference(final_columns), inplace=True)
        csv['Message'] = csv['Message'].astype('str')
        mask = (csv['Message'].str.len() >= 16) & (csv['Message'].str.len() <= 300)
        csv = csv.loc[mask]
        csv['CreatedTime'] = pd.to_datetime(csv['CreatedTime']).dt.date
        cols = csv.columns.tolist()
        final_col = [0, 2, 1]
        cols = [cols[i] for i in final_col]
        csv = csv[cols]
        csv.columns = ['Source', 'Date', 'Content']
        return csv


    df_app = load_app()
    df_play = load_play()
    df_sprinklr = load_sprinklr()
    df_merged = pd.concat([df_app, df_play, df_sprinklr], ignore_index=True)
    df_merged = df_merged.sample(frac=1).reset_index(drop=True)
    st.dataframe(df_merged)
    st.markdown(filedownload(df_merged), unsafe_allow_html=True)

else:
    st.info('Awaiting CSV file upload...')
