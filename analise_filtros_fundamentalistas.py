import pandas as pd
from pprint import pprint

ARQUIVO_DADOS = 'dados_oceans_status.csv'
ARQUIVO_DADOS = 'https://raw.githubusercontent.com/lucasHashi/coleta-dados-fundamentalistas/master/dados_oceans_status.csv'

def somar_posicoes(df_rank, list_indicadores):
    linhas_posi = []
    for tick, linha in df_rank.iterrows():
        soma_posi = 0
        for i in range(1, len(linha), 1):
            soma_posi += linha[i]
        linhas_posi.append([tick, soma_posi])
    
    df_posi = pd.DataFrame(linhas_posi, columns=['tick', 'soma_posi'])
    df_posi.set_index('tick', inplace=True)
    return df_rank.join(df_posi).copy()

def calcular_ranking(df_completo, list_indicadores, ano):
    ''' Para cada indicador selecionado, rankeia e gera a coluna de soma das posicoes
    Recebe:
    DataFrame - dados completos
    list_indicadores - [['TICKER', bool (O primeiro lugar é o menor valor?)], [Ticker, bool], ...]
    int - ano

    Retorna:
    DataFrame - com: tick, soma das posicoes, posicao em cada indicador
    '''
    df_rankings = df_completo[df_completo['ano'] == ano][['tick', 'ano']].copy()
    df_rankings.set_index('tick', inplace=True)

    for indicador, asc in list_indicadores:
        if(not indicador == 'liq_media_diaria'):
            df_indicador = df_completo[df_completo['ano'] == ano][['tick', indicador]].copy()
            df_indicador.set_index('tick', inplace=True)

            df_indicador['rank_'+indicador] = df_indicador[indicador].rank(ascending=asc, na_option='bottom')
            df_indicador.drop(indicador, axis=1, inplace=True)

            df_rankings = df_rankings.join(df_indicador)
    
    df_rankings = somar_posicoes(df_rankings, list_indicadores)
    return df_rankings.sort_values('soma_posi').copy()

def analisar_indicadores(lista_indicadores, ano):
    ''' A partir de uma lista de indicadores e um ano, retorna uma dataframe com o ranking de cada empresa
    recebe:
    dict - 'indicador': [min, max]
    int - ano

    retorna
    DataFrame - tabela com: tick, posicao geral, posicao normalizada, posicao no indicador 1, 2, 3, ..., n
    '''
    DICT_ASC = {
        'divida_liq_EBITDA': ['divida_liq_EBITDA', True],
        'DY': ['DY', False],
        'ROA': ['ROA', False],
        'ROE': ['ROE', False],
        'ROIC': ['ROIC', False],
        'P_L': ['P_L', True],
        'P_VP': ['P_VP', True],
        'LPA': ['LPA', False],
        'VPA': ['VPA', True],
        'PSR': ['PSR', False],
        'P_EBIT': ['P_EBIT', True],
        'P_EBITDA': ['P_EBITDA', True],
        'P_ativos': ['P_ativos', True],
        'P_cap_giro': ['P_cap_giro', False],
        'P_cirulante_liq': ['P_cirulante_liq', False],
        'margem_EBITDA': ['margem_EBITDA', False],
        'margem_EBIT': ['margem_EBIT', False],
        'margem_liq': ['margem_liq', False],
        'margem_bruta': ['margem_bruta', False],
        'EV_EBITDA': ['EV_EBITDA', True],
        'EV_EBIT': ['EV_EBIT', True],
        'liq_corrente': ['liq_corrente', False],
        'liq_imediata': ['liq_imediata', False],
        'receitas_5anos': ['receitas_5anos', False],
        'lucros_5anos': ['lucros_5anos', False],
        'divida_liq_EBIT': ['divida_liq_EBIT', False],
        'divida_liq_patrimonio': ['divida_liq_patrimonio', False],
        'patrimonio_ativos': ['patrimonio_ativos', False],
        'passivos_ativos': ['passivos_ativos', False],
        'giro_ativos': ['giro_ativos', False],
        'liq_media_diaria': ['liq_media_diaria', False]
    }

    lista_duplas = []
    for indicador in lista_indicadores:
        lista_duplas.append(DICT_ASC[indicador])
    
    #df_indicadores = pd.read_csv(ARQUIVO_DADOS)
    df_indicadores = filtrar_indicadores(lista_indicadores)
    
    df_final = calcular_ranking(df_indicadores, lista_duplas, ano)

    df_final['posi_normalizada'] = round((100*df_final['soma_posi'])/(len(df_final)*len(lista_indicadores)),2)

    colunas_certas = list(df_final.columns)
    colunas_certas.remove('ano')
    colunas_certas.remove('soma_posi')
    colunas_certas.remove('posi_normalizada')
    colunas_certas = ['soma_posi', 'posi_normalizada'] + colunas_certas

    return df_final[colunas_certas].copy()

def analisar_anos_anteriores(indicadores, tamanho_carteira, ano_inicial):
    ''' Analisar a melhor carteira de tamanho (tamanho_carteira) ao longo dos ultimos anos
    Recebe:
    dict - 'indicador': [min, max]
    int - quantidade de ativos
    int - ano inicial

    Retorna:
    dict - 'ano': [ativo1, ativo2, ..., ativoN]
    '''
    ativos_por_ano = {}

    for ano in range(ano_inicial, 2021, 1):
        df_ano_atual = analisar_indicadores(indicadores, ano)
        df_ano_atual = df_ano_atual.head(10).copy()
        #melhores_empresas = list(df_ano_atual['tick'])
        melhores_empresas = list(df_ano_atual.index)
        ativos_por_ano[str(ano)] = melhores_empresas
    
    for ano in ativos_por_ano:
        ativos_por_ano[ano] = ativos_por_ano[ano] + ([''] * (tamanho_carteira - len(ativos_por_ano[ano])))
    
    return ativos_por_ano

def filtrar_indicadores(dict_indicadores):
    df_indicadores = pd.read_csv(ARQUIVO_DADOS)

    for indicador in dict_indicadores:
        minimo, maximo = dict_indicadores[indicador]
        df_indicadores = df_indicadores[(df_indicadores[indicador] >= minimo) & (df_indicadores[indicador] <= maximo)].copy()

    return df_indicadores.copy()












