import streamlit as st
import pandas as pd

data = pd.read_csv('bolsonaro_tweets_preprocessado.csv')

st.title('Bolsonaro Tweets Dashboard')

st.dataframe(data)

if __name__ == '__main__':
    st.run()
