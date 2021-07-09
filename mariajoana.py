from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome #,ChromeOptions
from pandas import DataFrame, read_html 
from datetime import datetime
import psycopg2


now = datetime.now
de_para_colunas = {
        'Papel' : 'papel',
        'Cotação': 'cotacao',
        'Tipo' : 'tipo',
        'Empresa' : 'empresa',
        'Setor' : 'setor',
        'Subsetor' : 'subsetor',
        'Data últ cot' : 'data_ult_cot',
        'Min 52 sem' : 'min_52_sem',
        'Max 52 sem' : 'max_52_sem',
        'Vol $ méd (2m)' : 'vol_med_2m',
        'Valor da firma' : 'valor_da_firma',
        'Nro. Ações' : 'nro_acoes',
        'Dia' : 'dia%',
        'Mês' : 'mes%',
        '30 dias' : 'var_30_dias%',
        '12 meses' : 'var_12_meses%',
        '2021' : 'var_2021%',
        '2020' : 'var_2020%',
        '2019' : 'var_2019%',
        '2018' : 'var_2018%',
        '2017' : 'var_2017%',
        '2016' : 'var_2016%',
        'P/L' : 'p_l',
        'P/VP' : 'p_vp',
        'P/EBIT' : 'p_ebit',
        'PSR' : 'psr',
        'P/Ativos' : 'p_ativos',
        'P/Cap. Giro' : 'p_cap_giro',
        'P/Ativ Circ Liq' : 'p_ativ_circ_liq',
        'Div. Yield' : 'div_yield%',
        'EV / EBITDA' : 'ev_ebitda',
        'EV / EBIT' : 'ev_ebit',
        'Cres. Rec (5a)' : 'cres_rec_5a%',
        'LPA' : 'lpa',
        'VPA' : 'vpa',
        'Marg. Bruta' : 'marg_bruta%',
        'Marg. EBIT' : 'marg_ebit%',
        'Marg. Líquida' : 'marg_liquida%',
        'EBIT / Ativo' : 'ebit_ativo%',
        'ROIC' : 'roic%',
        'ROE' : 'roe%',
        'Liquidez Corr' : 'liquidez_corr',
        'Div Br/ Patrim' : 'div_br_patrim',
        'Giro Ativos' : 'giro_ativos',
        'Ativo' : 'ativo',
        'Disponibilidades' : 'disponibilidades',
        'Ativo Circulante' : 'ativo_circulante',
        'Dív. Bruta' : 'div_bruta',
        'Dív. Líquida' : 'div_liquida',
        'Patrim. Líq' : 'patrim_liq',
        }

def load_webdriver():

    driver = Chrome(ChromeDriverManager().install())
    return driver

    # def open_browser(self, download_path):
    #         try:
    #             print(' - Abrindo Navegador')
    #             options = webdriver.ChromeOptions()
    #             prefs = {"download.default_directory": download_path}
    #             options.add_argument("--disable-gpu")
    #             options.add_argument("--headless")
    #             options.add_argument("--disable-logging")
    #             options.add_argument("--log-level=3")
    #             options.add_argument("--output=/dev/null")
    #             options.add_experimental_option("prefs", prefs)
    #             driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #             return Response(code=0, data=driver)
    #         except Exception as e:
    #             return Response(code=1, message=f'open_browser Error: {e}, lineno: {sys.exc_info()[2].tb_lineno}')


def scraping_single_indicators(tick, driver):
    url = f'http://fundamentus.com.br/detalhes.php?papel={tick}'
    driver.get(url)
    result = driver.find_elements_by_tag_name('table') #criei lista de tabelas

    for index, element in enumerate(result): #element é cada tabela e index é posição
        df = read_html(element.get_attribute("outerHTML"), decimal=",", flavor='bs4', thousands='.')
        result[index] = df #trocando elemento por um dataframe na lista result

    return result


def clean_indicators_tables(tables):
    indicators = {}
    for num_tabela, df in enumerate(tables[:-1]): #para cada item na tabela
        df = df[0]
        x = 0 #variaveis para consultar blocaos de colunas
        y = 2
        df.fillna('', inplace=True)
        #df = df.applymap(lambda x: str(x).replace('?', ''))
        df = df.replace('\?', '', regex=True)
        df = df.replace(de_para_colunas)
        if num_tabela == 0:
            data_frame = df.T #puxa 1o elemento da lista df, todas linhas, - a 1a e faz transpose da tabela
        else:
            data_frame = df.iloc[1:].T #puxa 1o elemento da lista df, todas linhas, - a 1a e faz transpose da tabela
        while True:
            if data_frame.shape[0]-1 >= y: #se y é menor que a quantidade de linhas, tá no fim da tabela?
                df1 = data_frame.iloc[x:y].reset_index(drop = True) #busca par de linhas (título e valores)
                df1.columns = df1.iloc[0]
                df1 = df1.iloc[1]
                indicators.update(df1.to_dict()) #jogando para uma lista essa tabela
            else:
                df1 = data_frame.iloc[x:].reset_index(drop = True)
                df1.columns = df1.iloc[0]
                df1 = df1.iloc[1]
                indicators.update(df1.to_dict())
                break
            x += 2
            y += 2

    # for key, value in indicators.items():
    #     print(key)
    #     indicators[key] = [value]
    
    indicators.pop('')

    #indicators = DataFrame(indicators)
    # print(indicators)
    # indicators.to_csv('indicadores.csv', index=False, sep='|')
    return indicators


    #to-do: conectar tudo
    # - vou ter um método controlador: precisa abrir um driver, passar pro outro lado
    # - o scraping_single_indicators vai retornar uma lista de tables


def controller(tickers):
    driver = load_webdriver()
    #all_indicators = DataFrame()
    tables_list = []
    
    for tick in tickers:
        tables = scraping_single_indicators(tick, driver)
        tables_list.append(tables)

    driver.close()

    for tables in tables_list:
        result = clean_indicators_tables(tables)
        #all_indicators = all_indicators.append(result)
    
    return result


def convert_values(value:str):
    # not working - TO FIX
    try:
        if '%' in value:
            return float(value.strip('%').replace(',','.')) / 100
        elif '.'  in value or ',' in value: # elif any([True if x in value else False for x in ['.', ',']])  
            x = float(value.replace(',', "").replace('.', ",")) # 2,999,999.00
            print(x)
            return x
        else:
            return value
    except Exception as e:
        print(e)
        return value


def query_editor(indicators):
    columns = ''
    values = ''
    for key, value in indicators.items():
        value = convert_values(str(value))
        columns += f'"{key}",'
        values += f"'{value}'," 
    columns = columns.rstrip(',')
    values = values.rstrip(',')

    query = f'INSERT INTO public.indicators_raw ({columns}) VALUES ({values})'
    print(query)
    db_controller(query)


def db_controller(query):
    con = psycopg2.connect(database="DB", user=db_user, password=db_pwd, host="127.0.0.1", port="5432")
    cur = con.cursor()
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()
    con.close()


tickers = ['AZUL4']#, 'ITSA4', 'RNEW4', 'TRPL4', 'TRPL3', 'WEGE3', 'VVAR3']


t0 = now()

indicators = controller(tickers)
print(f'Tempo de execução 1: {now()-t0}')

query_editor(indicators)

print(f'Tempo de execução 2: {now()-t0}')
