import pandas as pd
import numpy as np
import missingno as msno
import plotly.express as px
import unidecode

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# navegador = webdriver.Chrome()

# navegador.get('https://opendatasus.saude.gov.br/dataset/febre-amarela-em-humanos-e-primatas-nao-humanos/resource/8e98b4e8-90e0-417b-b921-20653fb538cb')

# navegador.maximize_window()

# botao = '//*[@id="content"]/div[3]/section/div/div[1]/ul/li/div'

# dados = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/Febre+Amarela/fa_casoshumanos_1994-2024.csv'

# import pandas as pd

# import shutil

# origem = r"../../../Downloads/fa_casoshumanos_1994-2024.csv"

# destino = r"../../Documentos/BD/WEB DATA/AP2_projeto/Bases_originais/fa_casoshumanos_1994-2024.csv"

# shutil.copy(origem, destino)

# print("Arquivo CSV copiado com sucesso!")

# df = pd.read_csv("../Bases_originais/fa_casoshumanos_1994_2024.csv", sep=';', encoding='latin1')
# print(df.columns)

# df['OBITO'] = df['OBITO'].str.upper().str.strip()

# import pandas as pd

# df = pd.read_csv("../Bases_originais/fa_casoshumanos_1994_2024.csv", sep=';', encoding='latin1')

# df['obito'] = df['OBITO'].apply(lambda x: x.count('SIM'))
# df['vivo'] = df['OBITO'].apply(lambda x: x.count('NÃO'))
# df['ignorado'] = df['OBITO'].apply(lambda x: x.count('IGN'))

# df = df.drop(columns=['OBITO'])

# df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('latin1')

# import os
# if not os.path.exists('Bases_tratadas'):
#     os.makedirs('Bases_tratadas')

# df.to_csv('../Bases_tratadas/fa_casoshumanos_1994_2024_corrigido.csv', sep=';', index=False, encoding='latin1')

# print("Arquivo CSV corrigido e salvo em 'Bases_tratadas'.")

# import pandas as pd
# import unicodedata

# def remover_acentos(txt):
#     if isinstance(txt, str):
#         return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
#     return txt

# df_raw = pd.read_csv("../Bases_originais/fa_casoshumanos_1994_2024.csv", sep=';', encoding='latin1')

# linhas_corrigidas = []

# for _, linha in df_raw.iterrows():
#     uf = remover_acentos(linha['UF_LPI'])
#     obitos_str = remover_acentos(str(linha['OBITO']).upper().replace('', '').strip())

#     obitos = [obitos_str[i:i+3] for i in range(0, len(obitos_str), 3)]

#     for ob in obitos:
#         linhas_corrigidas.append({
#             'UF': uf,
#             'OBITO': ob
#         })

# df_corrigido = pd.DataFrame(linhas_corrigidas)

# df_corrigido.columns = [remover_acentos(col) for col in df_corrigido.columns]

# df_corrigido['OBITO'] = df_corrigido['OBITO'].str.upper().str.strip()

# tabela_final = df_corrigido.groupby('UF')['OBITO'].value_counts().unstack(fill_value=0).reset_index()

# tabela_final = tabela_final.rename(columns={
#     'SIM': 'obito',
#     'NAO': 'vivo',
#     'IGN': 'ignorado'
# })

# for col in ['obito', 'vivo', 'ignorado']:
#     if col not in tabela_final.columns:
#         tabela_final[col] = 0

# tabela_final.to_csv('../Bases_upload/tabela1_obitos_por_estado.csv', sep=';', index=False, encoding='latin1')

# print("Tabela salva em 'Bases_upload/tabela1_obitos_por_estado.csv'")
# print(tabela_final)

# import pandas as pd
# import os

# caminho_csv_corrigido = '../Bases_tratadas/fa_casoshumanos_1994_2024_corrigido.csv'

# df = pd.read_csv(caminho_csv_corrigido, sep=';', encoding='latin1')

# if 'UF_LPI' in df.columns and 'ANO_IS' in df.columns:
#     tabela_estado_ano = df.groupby(['UF_LPI', 'ANO_IS'])[['obito', 'vivo', 'ignorado']].sum().reset_index()

#     tabela_estado_ano['ID'] = tabela_estado_ano[['obito', 'vivo', 'ignorado']].sum(axis=1)

#     tabela_estado_ano = tabela_estado_ano[['UF_LPI', 'ANO_IS', 'ID', 'obito', 'vivo', 'ignorado']]

#     os.makedirs('Bases_upload', exist_ok=True)
#     tabela_estado_ano.to_csv('../Bases_upload/tabela3_casos_por_estado_ano.csv', sep=';', index=False, encoding='utf-8')

#     print("Tabela 3 corrigida e salva em '../Bases_upload/tabela3_casos_por_estado_ano.csv'.")

# else:
#     print("As colunas 'UF_LPI' e 'ANO_IS' não foram encontradas no DataFrame.")

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../bases_upload/tabela1_obitos_por_estado.csv', sep=',')

colunas_alvo = ['ignorado','vivo','obito']
for col in colunas_alvo:
    df[col] = pd.to_numeric(df[col], errors = 'coerce')

st.title('Analise de Dados - Febre Amarela - 30 anos')
st.write('Visualização da Tabela:')
st.dataframe(df)

st.subheader('Análise de nulos')
nulos = df.isnull().sum()
st.dataframe(nulos)

aux = pd.DataFrame({'variavel': nulos.index, 'qtd_miss':nulos.values})
st.dataframe(aux)

st.subheader('Análises univariadas')
st.write('Medidas resumo')
st.dataframe(df.describe())

coluna_escolhida = st.selectbox('Escolha a coluna para analise:', df.columns)

df.loc[df[coluna_escolhida] >999, coluna_escolhida] = 999
df.loc[df[coluna_escolhida] <0, coluna_escolhida] = 100

lista_de_colunas = df.columns
coluna_escolhida = st.selectbox('selecione a coluna',lista_de_colunas)
media = round(df[coluna_escolhida].mean(),2)
desvio = round(df[coluna_escolhida].std(),2)
mediana = round(df[coluna_escolhida].quantile(0.5),2)
maximo = round(df[coluna_escolhida].max(),2)

st.write(f'A coluna escolhida foi {coluna_escolhida}. Média = {media}. Desvio = {desvio}. Mediana = {mediana} e Máximo = {maximo}')
st.write('Histograma')
fig = px.histogram(df,x='ignorado')
st.plotly_chart(fig)
st.write('Boxplot')
fig2 = px.box(df,x='ignorado')
st.plotly_chart(fig2)

st.subheader('Análises Multivariadas')
lista_de_escolha = st.multiselect('Escolha até 3 variaveis:',['ignorado', 'obito', 'vivo'])
st.markdown('Gráfico de dispersão')
if len(lista_de_escolha) != 3:
    st.warning('Selecione exatamente 3 colunas para gerar os gráficos.')
else:
    fig3 = px.scatter(df, x=lista_de_escolha[0], y=lista_de_escolha[1], color=lista_de_escolha[2])
    st.plotly_chart(fig3)

    st.markdown('Gráfico de Caixa')
    fig4 = px.box(df, x=lista_de_escolha[0], y=lista_de_escolha[1], color=lista_de_escolha[2])
    st.plotly_chart(fig4)   

col1, col2 = st.columns(2)
with col1:
    st.subheader('Histograma')
    fig = px.histogram(df, x=coluna_escolhida)
    st.plotly_chart(fig, use_container_width=True, key = 'histograma')
with col1:
    st.subheader('Boxplot')
    fig2 = px.box(df, x=coluna_escolhida)
    st.plotly_chart(fig, use_container_width=True, key = 'boxplot')

    media = round(df[coluna_escolhida].mean(), 2)
mediana = round(df[coluna_escolhida].median(), 2)
desvio = round(df[coluna_escolhida].std(), 2)
maximo = round(df[coluna_escolhida].max(), 2)
minimo = round(df[coluna_escolhida].min(), 2)

st.markdown(f"""
### Resumo Estatístico da Coluna *{coluna_escolhida}*

- *Média:* {media}  
- *Mediana:* {mediana}  
- *Desvio Padrão:* {desvio}  
- *Valor Máximo:* {maximo}  
- *Valor Mínimo:* {minimo}

Esses valores representam o comportamento dos dados da coluna escolhida.  
Use os gráficos acima para analisar a distribuição dos dados escolhidos e identificar possíveis outliers, comparando a dispersão em relação a media e media.
""")