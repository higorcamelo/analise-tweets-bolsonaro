# BolsoInsights - Análise de Comunicação (2019-2020)

**Este projeto é puramente educacional, profissional e de análise de dados. Não reflete opiniões políticas ou pessoais.**

Este projeto realiza uma análise da comunicação do ex-presidente Jair Bolsonaro por meio de seus tweets, explorando insights e padrões ao longo do período de 2019-2020. O dashboard resultante destaca visualizações interativas e informações úteis sobre os dados.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **Streamlit**: Biblioteca para a criação de dashboards interativos.
- **Pandas**: Manipulação e análise de dados.
- **Plotly Express e Matplotlib**: Geração de gráficos e visualizações.
- **NLTK**: Processamento de linguagem natural para pré-processamento de texto.
- **Demoji**: Extração de emojis a partir do texto.

## Pré-processamento dos Dados
O código responsável pelo pré-processamento dos dados realiza as seguintes etapas:

1. Carregamento do conjunto de dados de tweets do ex-presidente Bolsonaro.
2. Conversão da coluna 'date' para o formato datetime.
3. Remoção de links e tweets com likes/retweets igual a zero.
4. Tokenização e pré-processamento do texto, removendo pontuações, stopwords e aplicando stemming.
5. Extração de menções, hashtags e emojis de cada tweet.
6. Contagem das menções mais frequentes.
7. Exportação do DataFrame resultante para um arquivo CSV contendo colunas relevantes.

## Insights Obtidos
Após a análise exploratória dos dados, alguns insights notáveis incluem:

- **Menções Mais Frequentes:** Destaque para a presença maior de menções ao ministro Tarcísio, talvez indicando uma prefência do ex-presidente e investindo no titular da infraestrutura um futuro sucessor ou aliado chave
- **Hashtags Relevantes:** Destaque para hashtags de confrontação a opositores.
- **Emojis Mais Utilizados:** Observação de emojis com a bandeira do Brasil e de comunicação informal com o uso do "joinha", além de destaque para a frequência da bandeira dos EUA.

