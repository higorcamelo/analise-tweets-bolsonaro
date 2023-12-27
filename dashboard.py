import streamlit as st
import pandas as pd

# Carregar os dados
data = pd.read_csv('data/bolsonaro_tweets_preprocessado.csv')

# Título do dashboard
st.markdown("<h1 style='text-align: center; color: black; font-size: 36px;'>BolsoInsights - Análise de Comunicação (2019-2020)</h1>", unsafe_allow_html=True)
# Exibir os primeiros registros do DataFrame
st.subheader('Dados:')
st.dataframe(data.head())

# Visualizar a contagem de sentimentos
st.subheader('Contagem de Sentimentos:')
sentimento_count = data['sentimento'].value_counts()
st.bar_chart(sentimento_count)

# Visualizar os emojis mais frequentes
st.subheader('Emojis Mais Frequentes:')
emoji_count = data['emojis'].explode().value_counts()
st.bar_chart(emoji_count.head(10))

# Visualizar um gráfico de linhas da quantidade de likes e retweets ao longo do tempo
st.subheader('Likes e Retweets ao Longo do Tempo:')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['date'], data['likes'], label='Likes')
ax.plot(data['date'], data['retweets'], label='Retweets')
ax.set_xlabel('Data')
ax.set_ylabel('Quantidade')
ax.legend()
st.pyplot(fig)
