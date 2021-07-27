import pandas as pd
import streamlit as st

#web title
st.markdown('''
# **CSV FILE MERGER**

This website can **append, merge, and sort** CSV files from **Heedzy**

---
''')
#Upload CSV data
with st.sidebar.header('1.Upload CSV data'):
    app_file = st.sidebar.file_uploader("Upload App Store Reviews file", type=['csv'])
    play_file = st.sidebar.file_uploader("Upload Play Store Reviews file", type=['csv'])

#CSV data handling
if app_file and play_file is not None:
    def load_app():
        csv= pd.read_csv(app_file)
        return csv
    def load_play():
        csv = pd.read_csv(play_file)
        return csv
    df_app = load_app()
    df_app.loc[:, 'Source'] = 'CenturyLink App Store'
    df_play = load_play()
    df_play.loc[:, 'Source'] = 'CenturyLink Play Store'
    df = pd.concat([df_app, df_play], ignore_index=True)

    st.write(df)
else:
    st.info('Awaiting CSV file upload...')
