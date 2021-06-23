from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd


def load_webdriver():

    driver = webdriver.Chrome(ChromeDriverManager().install())
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
        df = pd.read_html(element.get_attribute("outerHTML"), decimal=",", flavor='bs4', thousands='')
        result[index] = df #trocando elemento por um dataframe na lista result
    return result

def clean_indicators_tables(tables):
    indicators = pd.DataFrame()
    for df in tables[:-1]: #para cada item na tabela
        x = 0 #variaveis para consultar blocaos de colunas
        y = 2
        data_frame = df[0].iloc[1:].T #puxa 1o elemento da lista df, todas linhas, - a 1a e faz transpose da tabela
        while True:
            if data_frame.shape[0]-1 >= y: #se y é menor que a quantidade de linhas, tá no fim da tabela?
                df1 = data_frame.iloc[x:y].reset_index(drop = True) #busca par de linhas (título e valores)
                df1.columns = df1.iloc[0] 
                df1 = df1.iloc[1]
                indicators.append(df1) #jogando para uma lista essa tabeça
            else:
                df1 = data_frame.iloc[x:].reset_index(drop = True)
                df1.columns = df1.iloc[0]
                df1 = df1.iloc[1]
                indicators.append(df1)
                break
            x += 2
            y += 2
    print(indicators)
    indicators.to_csv('indicadores.csv', index=False, sep='|')

    #to-do: conectar tudo
    - vou ter um método controlador: precisa abrri um driver, passar pro outro lado
    - o scraping_single_indicators (passar como parametro o driver também)
