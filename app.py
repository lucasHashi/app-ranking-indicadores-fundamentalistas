import streamlit as st
import pandas as pd
import altair as alt

import analise_filtros_fundamentalistas as analises

URL_DADOS_COMPLETOS = 'https://raw.githubusercontent.com/lucasHashi/coleta-dados-fundamentalistas/master/dados_oceans_status.csv'

COLUNAS_OCEANS = ['Dívida líq./EBITDA', 'ROA', 'LPA',
                'Margem EBITDA', 'ROE', 'P/VP', 'EV/EBITDA',
                'DY', 'P/Ativos', 'ROIC', 'Margem liquida',
                'PSR', 'EV/EBIT', 'Liquidez imediata',
                'Liquidez corrente', 'P/EBIT', 'P/EBITDA', 'P/L', 'VPA']

TRADUDOR_INDICADORES = {
    'DY': 'DY',
    'ROA': 'ROA',
    'ROE': 'ROE',
    'ROIC': 'ROIC',
    'P/L': 'P_L',
    'P/VP': 'P_VP',
    'LPA': 'LPA',
    'VPA': 'VPA',
    'PSR': 'PSR',
    'P/EBIT': 'P_EBIT',
    'P/EBITDA': 'P_EBITDA',
    'P/Ativos': 'P_ativos',
    'P/Cap. Giro': 'P_cap_giro',
    'Preço sobre Ativo Circ. Líq.': 'P_cirulante_liq',
    'Margem EBITDA': 'margem_EBITDA',
    'Margem EBIT': 'margem_EBIT',
    'Margem liquida': 'margem_liq',
    'Margem bruta': 'margem_bruta',
    'EV/EBITDA': 'EV_EBITDA',
    'EV/EBIT': 'EV_EBIT',
    'Liquidez corrente': 'liq_corrente',
    'Liquidez imediata': 'liq_imediata',
    'CAGR Receitas 5 Anos': 'receitas_5anos',
    'CAGR Lucros 5 Anos': 'lucros_5anos',
    'Dívida líq./EBIT': 'divida_liq_EBIT',
    'Dívida líq./EBITDA': 'divida_liq_EBITDA',
    'Dívida líq/Patrimônio': 'divida_liq_patrimonio',
    'Patrimônio / Ativos': 'patrimonio_ativos',
    'Passivos / Ativos': 'passivos_ativos',
    'Giro Ativos': 'giro_ativos',
    'Liquidez diaria': 'liq_media_diaria'
}

df_dados = pd.read_csv(URL_DADOS_COMPLETOS)
df_dados.sort_values('tick', inplace=True)
df_dados.reset_index(drop=True, inplace=True)

ano_min = df_dados['ano'].min()
ano_max = df_dados['ano'].max()
ano_selecionado = st.selectbox('Ano de analise', list(range(ano_min, ano_max+1, 1)))
st.write('Alguns filtros são exclusivos de 2020 pela falta de dados.')

filtros_validos = list(TRADUDOR_INDICADORES.keys()) if(ano_selecionado == 2020) else COLUNAS_OCEANS

filtros_validos.sort()
indicadores_escolhidos_bruto = st.multiselect('Indicadores para filtrar', filtros_validos)

indicadores_escolhidos = [TRADUDOR_INDICADORES[indicador] for indicador in indicadores_escolhidos_bruto]

dict_filtros = {}
for i, indicador in enumerate(indicadores_escolhidos):
    indicador_user = indicadores_escolhidos_bruto[i]
    dict_filtros[indicador] = st.slider('Limites: '+indicador_user, df_dados[indicador].min(), df_dados[indicador].max(), (df_dados[indicador].min(), df_dados[indicador].max()))

st.write('## Analisar carteiras')
if(len(dict_filtros) > 0):
    st.write('### Carteira para {}'.format(ano_selecionado))
    df_ano_selecionado = analises.analisar_indicadores(dict_filtros, ano_selecionado)
    st.write(df_ano_selecionado)

    ano_inicial = st.slider('Ano inicial da analise', int(ano_min), int(ano_max))

    tamanho_carteira = 10
    melhores_por_ano = analises.analisar_anos_anteriores(dict_filtros, tamanho_carteira, ano_inicial)
    #pprint(melhores_por_ano)
    df_melhores_por_ano = pd.DataFrame(melhores_por_ano)
    st.write('### Carteiras ideias de {} até 2020'.format(ano_inicial))
    st.write(df_melhores_por_ano)
else:
    st.write('Selecione os indicadores para analisar carteiras')
