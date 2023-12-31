import streamlit as st
import pandas as pd
from collections import Counter
import emoji
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv('./data/bolsonaro_tweets_preprocessado.csv')

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black; font-size: 36px;'>BolsoInsights - Análise de Comunicação (2019-2020)</h1>", unsafe_allow_html=True)

# Função para extrair emojis
def extract_emojis(text):
    return [char for char in text if char in emoji.UNICODE_EMOJI]

def info_card(title, value, color):
    card_html = f"""
    <div style="background-color: {color}; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: white;">{title}</h3>
        <p style="font-size: 24px; font-weight: bold; color: white;">{value}</p>
    </div>
    """
    st.sidebar.markdown(card_html, unsafe_allow_html=True)
    
# Média de likes por tweet
media_likes = df['likes'].mean().round(0)
# Média de retweets por tweet, removendo as casas decimais
media_retweets = df['retweets'].mean().round(0)
    
# Calcular emojis mais frequentes
df['emojis'] = df['emojis'].apply(lambda x: [] if pd.isna(x) else eval(x))
emojis_presentes = df[df['emojis'].apply(lambda x: len(x) > 0)]
all_emojis = emojis_presentes['emojis'].explode()
emoji_counts = Counter(all_emojis)
top_emojis = emoji_counts.most_common(3)

# Calcular hashtags mais frequentes não nulas
df['hashtags'] = df['hashtags'].apply(lambda x: [] if pd.isna(x) else eval(x))
hashtags_presentes = df[df['hashtags'].apply(lambda x: len(x) > 0 and x[0] is not None)]
hashtag_counts = Counter(hashtags_presentes['hashtags'].explode())
top_hashtags = hashtag_counts.most_common(3)

# Lista de ministérios mais mencionados
ministerios_list = [
    'MInfraestrutura',
    'MinEconomia',
    'minsaude',
    'mdregional_br',
    'MEC_Comunicacao',
]

# Lista de ministros mais mencionados
ministros_list = [
    'tarcisiogdf',
    'SF_Moro',
    'ernestofaraujo',
    'TerezaCrisMS',
    'DamaresAlves'
]

# Lista de filhos mais mencionados
filhos_list = [
    'CarlosBolsonaro', 
    'FlavioBolsonaro',
    'BolsonaroSP',
]

# Função para contar menções
def contar_mencoes(df, lista):
    return Counter([m for mencao in df['mencoes'] for m in (eval(mencao) if isinstance(mencao, str) else mencao) if m in lista])

# Filtrar menções aos ministérios, ministros e filhos
df_ministerios = df[df['mencoes'].apply(lambda x: any(m in eval(x) if isinstance(x, str) else m in x for m in ministerios_list))]
df_ministros = df[df['mencoes'].apply(lambda x: any(m in eval(x) if isinstance(x, str) else m in x for m in ministros_list))]
df_filhos = df[df['mencoes'].apply(lambda x: any(m in eval(x) if isinstance(x, str) else m in x for m in filhos_list))]

# Contar menções aos ministérios, ministros e filhos
ministerios_counts = contar_mencoes(df_ministerios, ministerios_list)
ministros_counts = contar_mencoes(df_ministros, ministros_list)
filhos_counts = contar_mencoes(df_filhos, filhos_list)

# Criar dataframes com os dados
df_ministerios = pd.DataFrame.from_dict(ministerios_counts, orient='index').reset_index()
df_ministerios.columns = ['ministerio', 'count']

df_ministros = pd.DataFrame.from_dict(ministros_counts, orient='index').reset_index()
df_ministros.columns = ['ministro', 'count']

df_filhos = pd.DataFrame.from_dict(filhos_counts, orient='index').reset_index()
df_filhos.columns = ['filho', 'count']

# Grafico de pizza com as menções aos filhos
fig_filhos = px.pie(df_filhos, values='count', names='filho', title='Menções aos Filhos', 
                    hover_data=['filho', 'count'],
                    labels={'count': 'Número de Menções'},
                    )

# Adicionando dica de ferramenta personalizada
fig_filhos.update_traces(
    hovertemplate='<b>%{label}</b><br>Número de Menções: %{value}<br>'
                  '<i>Insight:</i> Maior prevalência de menções ao filho Eduardo, indicando que este é o mais ativo nas redes sociais e o administrador do perfil do pai no Twitter.'
)

# Criar gráfico de barras clusterizado
fig_minis = px.bar(df_ministerios, x='count', y='ministerio', orientation='h',
             title='Menções aos Ministérios e Ministros Mais Frequentes',
             labels={'count': 'Número de Menções'},
             color_discrete_sequence=['#1f77b4'] * len(df_ministerios),
             width=800, height=600)

# Adicionar cluster para ministros
fig_minis.add_trace(px.bar(df_ministros, x='count', y='ministro',
                     color_discrete_sequence=['#ff7f0e'] * len(df_ministros)).data[0])

# Atualizar layout do gráfico
fig_minis.update_layout(barmode='group', yaxis_categoryorder='total ascending')

# Adicionar tooltip
fig_minis.update_traces(hovertemplate='%{x} menções', textposition='outside')

# Adicionar dica de ferramenta personalizada
fig_minis.update_traces(
    hovertemplate='<b>%{y}</b><br>Número de Menções: %{x}<br>'
                  '<i>Insight:</i> Grande número de menções ao min. da infraestrutura e nominalmente ao ministro Tarcísio, indicando um foco do ex-presidente em um possível sucessor político.'
)

# Juntar todas as palavras dos tokens em uma única string
all_tokens = ''.join(df['tokens'].explode().dropna())

# Criar a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_tokens)

# Exibir a WordCloud usando matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Palavras Mais Citadas nos Tweets')

likes = df['likes']
retweets = df['retweets']

# Criar um gráfico de dispersão
fig_lik_ret = px.scatter(df, x='likes', y='retweets', trendline='ols', 
                         title='Correlação entre Likes e Retweets com Linha de Tendência',
                         labels={'likes': 'Likes', 'retweets': 'Retweets'}
                         )

# Adicionar rótulos
fig_lik_ret.update_layout(xaxis_title='Likes', yaxis_title='Retweets')

# Adicionar dica de ferramenta personalizada
fig_lik_ret.update_traces(
    hovertemplate='<b>Likes:</b> %{x}<br><b>Retweets:</b> %{y}<br>'
                  '<i>Insight:</i> Relativa facilidade dos tweets do ex-presidente beirar os 100 mil likes e 15 mil retweets, indicando uma grande base de apoiadores e propagação de suas ideias.'
)
col1, col2 = st.columns(2)

col1.plotly_chart(fig_minis, use_container_width=True)
col1.pyplot(plt)
st.sidebar.header("Informações Gerais")
info_card("Emojis mais frequentes", f"1º {top_emojis[0][0]}     2º {top_emojis[1][0]}   3º {top_emojis[2][0]} " , "#4CAF50")
info_card("Hashtags mais frequentes", f"#{top_hashtags[0][0]}" , "#F44336")
info_card("Média de Likes por Tweet", f"aprox. {media_likes}", "#2196F3")
info_card("Retweets Totais", f"aprox. {media_retweets}", "#FF9800")
col2.plotly_chart(fig_filhos, use_container_width=True)
col2.plotly_chart(fig_lik_ret, use_container_width=True)
