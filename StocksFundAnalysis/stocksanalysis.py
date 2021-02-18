import pandas as pd
import numpy as np

# for web scraping
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

################################################################################
### Get Stikers Codes
################################################################################
def get_tickers():
#    tickers = []
    tickers = pd.DataFrame(columns=['ticker'])
    for page in range(1, 3):
        page_url = "https://investidor10.com.br/acoes/?page=" + str(page)

        # opens the connection and downloads html page from url
        #uClient = uReq(page_url)

        r = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        page_soup = soup(urlopen(r).read(), "html.parser")
        #uClient.close()

        # finds each product from the store page
        #containers = page_soup.findAll("div", {"class": "card-text d-flex align-items-center"})
        #grid = page_soup.findAll("div", {"class": "grid"})
        containers = page_soup.findAll("div", {"class": "actions-codes"})

        for container in containers:
            #ticker = container.findAll("div", {"class": "tag-ticker"})[0].text
            #print(container)
            tickers_units = container.findAll("a", {"class": "actions-code"})

            for unit in tickers_units:
                ticker = unit.text
                print("ticket: " + ticker)
                tickers = tickers.append({ 'ticker': ticker }, ignore_index=True)

    return tickers    

################################################################################
### Get the metrics for one ticker
################################################################################
def get_metrics(ticker):
    #print(" ===> Entrei get_metrics <=== ")
    metrics = []

    print("Ticker Inside ===> " + ticker)
    page_url = "https://investidor10.com.br/acoes/" + str(ticker)

    # opens the connection and downloads html page from url
    #uClient = uReq(page_url)
    try:

        r = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        try:
            page_soup = soup(urlopen(r, timeout=100).read(), "html.parser")
        except:
            print("Timeout Error !")
        #uClient.close()

        # finds each ticker indicator from the top of the page
        #containers = page_soup.findAll("div", {"class": "col-6 col-xl-2"})

        #cotacao
        #indicator = (containers[0].find("div", {"class": "card-body d-flex align-items-center justify-content-center"}).div.span.text).replace("\n", "")
        #indicator = (containers[0].find("div", {"class": "_card-body"}).div.span.text).replace("\n", "")
        tk_resume = page_soup.findAll("div", {"class": "_card cotacao"})
        indicator = (tk_resume[0].find("div", {"class": "_card-body"}).div.span.text).replace("\n", "")
        metrics.append(indicator)
        #valorizacao
        tk_resume = page_soup.findAll("div", {"class": "_card pl"})
        indicator = (tk_resume[0].find("div", {"class": "_card-body"}).div.span.text).replace("\n", "")
        metrics.append(indicator)
        #P/L
        tk_resume = page_soup.findAll("div", {"class": "_card val"})
        indicator = (tk_resume[0].find("div", {"class": "_card-body"}).span.text).replace("\n", "")
        metrics.append(indicator)
        #P/VP
        tk_resume = page_soup.findAll("div", {"class": "_card vp"})
        indicator = (tk_resume[0].find("div", {"class": "_card-body"}).span.text).replace("\n", "")
        metrics.append(indicator)
        #DY
        tk_resume = page_soup.findAll("div", {"class": "_card dy"})
        indicator = (tk_resume[0].find("div", {"class": "_card-body"}).span.text).replace("\n", "")
        metrics.append(indicator)

        #ROE
        #indicator = (containers[5].find("div", {"class": "card-body d-flex align-items-center justify-content-center"}).span.text).replace("\n", "")
        tk_resume = page_soup.findAll("div", {"class": "table table-bordered outter-borderless"})
        #print(tk_resume)
        tk_indicators = tk_resume[0].findAll("div", {"class": "value"})
        indicator = (tk_indicators[19].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)

        # finds each ticker indicator from the middle of the page
        containers = page_soup.findAll("div", {"class": "d-flex justify-content-between align-items-center"})
        #Payout
        indicator = (tk_indicators[3].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #Margem Liquida
        indicator = (tk_indicators[4].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #Margem Bruta
        indicator = (tk_indicators[5].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #Margem Ebit
        indicator = (tk_indicators[6].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #Margem Ebitda
        indicator = (tk_indicators[7].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #ev/ebitda
        indicator = (tk_indicators[8].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #ev/ebit
        indicator = (tk_indicators[9].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #p/ebitda
        indicator = (tk_indicators[10].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #p/ebit
        indicator = (tk_indicators[11].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #p/ativo
        indicator = (tk_indicators[12].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #p/cap.giro
        indicator = (tk_indicators[13].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #p/ativ.circ.liq
        indicator = (tk_indicators[14].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #psr
        indicator = (tk_indicators[15].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #vpa
        indicator = (tk_indicators[16].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #lpa
        indicator = (tk_indicators[17].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #giro ativos
        indicator = (tk_indicators[18].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #roe -> pulei pq já havia pego antes
        #roic
        indicator = (tk_indicators[20].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #roa
        indicator = (tk_indicators[21].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #divida liquida/patrimonio
        indicator = (tk_indicators[22].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #divida liquida/ebitda
        indicator = (tk_indicators[23].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #divida liquida/ebit
        indicator = (tk_indicators[24].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #divida bruta/patrimonio
        indicator = (tk_indicators[25].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #patrimonio/ativos
        indicator = (tk_indicators[26].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #passivos/ativos
        indicator = (tk_indicators[27].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #liquidez corrente
        indicator = (tk_indicators[28].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #cagr receitas 5 anos
        indicator = (tk_indicators[29].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        #cagr lucros 5 anos
        indicator = (tk_indicators[30].span.text).replace("\n", "")
        #print(indicator)
        metrics.append(indicator)
        
        # finds each ticker sector/subsector/segment
    #    containers = page_soup.findAll("li")
    #    containers = page_soup.findAll("ul", {"class": "segment-breadcrumb"})
    #    print(" ===================== ========================= ======================")
    #    print(containers[29])
    #    print(" ===================== ========================= ======================")
    #    print(containers[30])
        
    #    print(" ____________________________________________________________________________ ")
    #    print(ticker)
    #    print(containers)
    #    print(containers[29])
    #    print(" ____________________________________________________________________________ ")

        #setor
    #    indicator = containers[29].find("div").h2.text
    #    metrics.append(indicator)
        #subsetor
    #    indicator = containers[30].find("div").h2.text
    #    metrics.append(indicator)
        #segmento
    #    indicator = containers[31].find("div").h2.text
    #    metrics.append(indicator)

    #    for container in containers:
    #        indicator = container.find("div", {"class": "card-body d-flex align-items-center justify-content-center"}).div.span.text
    #        metrics.append(indicator)
    except:
        print("There is no data for the ticker " + ticker)
        return metrics
    #print(" ===> Sai get_metrics <=== ")
    return metrics


################################################################################ 
##### 
##### MAIN()
##### 
################################################################################ 
def main():
    my_file = Path("tickers.csv")
    there_is_file = my_file.exists()
    #there_is_file =  False
    #st.markdown("Tem arquivo = " + str(there_is_file))
    if there_is_file:
        tickers = pd.read_csv('tickers.csv', encoding= 'unicode_escape')
    else:
        tickers = pd.DataFrame(columns=['ticker'])
        tickers = get_tickers()
        tickers.to_csv (r'tickers.csv', index = False, header=True)

    size = len(tickers)
    print("Tickers read : " + str(size))

    my_file = Path("metrics.csv")
    there_is_file = my_file.exists()
    if there_is_file:
        df_metrics = pd.read_csv('metrics.csv', encoding= 'unicode_escape')
    else:
        df_metrics = pd.DataFrame(columns=['ticker', 'cotacao', 'valorizacao', 'pl', 'pvp', 'dy', 'roe', 'payout', 'mrg_liquida', 
        'mrg_bruta', 'margem_ebit', 'margem_ebitda', 'ev_ebitda', 'ev_ebit', 'p_ebitda', 'p_ebit', 'p_ativo', 'p_cap_giro', 
        'p_ativ_circ_liq', 'psr', 'vpa', 'lpa', 'giro_ativos', 'roic', 'roa', 'div_liq_patr', 'div_liq_ebitda', 'div_liq_ebit', 
        'div_bruta_patr', 'patr_ativos', 'passivos_ativos', 'liquidez_corrente', 'cagr_rec_5_anos', 'cagr_lucros_5_anos'])

    df_metrics_index = df_metrics.copy()
    df_metrics_index.reset_index(level=0, inplace=True)
    df_metrics_index = df_metrics_index[['ticker']]

    df_metrics_index.set_index('ticker', inplace=True)
    tickers.set_index('ticker', inplace=True)

    tickers = tickers.drop(df_metrics_index.index.values.tolist())

    package_size = 25
    size = len(tickers)
    row = 1
    tickers.reset_index(level=0, inplace=True)
    print(tickers)

    for i in range (0, size):
        data = tickers.iloc[i]
        ticker =  data['ticker']
        metrics = get_metrics(ticker)
        if metrics != []:
            perc = ( (i+1) / size) * 100
            print(ticker)
            #print(" Executing: " +  str(perc))
            print(" Executing: {:.2f}".format(perc) + "%")
            
            cotacao             = float( metrics[0][3:].replace(".", "").replace(",", ".")) 
            valorizacao         = float( metrics[1].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[1].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            pl                  = float( metrics[2].replace(".", "").replace(",", ".")) if metrics[2].replace(",", ".") != '-' else ""
            pvp                 = float( metrics[3].replace(".", "").replace(",", ".")) if metrics[3].replace(",", ".") != '-' else ""
            dy                  = float( metrics[4].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[4].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            roe                 = float( metrics[5].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[5].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            payout              = float( metrics[6].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[6].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            mrg_liquida         = float( metrics[7].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[7].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            mrg_bruta           = float( metrics[8].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[8].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            margem_ebit         = float( metrics[9].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[9].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""

            margem_ebitda       = float(metrics[10].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[10].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            ev_ebitda           = float(metrics[11].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[11].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            ev_ebit             = float(metrics[12].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[12].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            p_ebitda            = float(metrics[13].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[13].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            p_ebit              = float(metrics[14].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[14].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            p_ativo             = float(metrics[15].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[15].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            p_cap_giro          = float(metrics[16].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[16].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            p_ativ_circ_liq     = float(metrics[17].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[17].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            psr                 = float(metrics[18].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[18].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            vpa                 = float(metrics[19].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[19].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            lpa                 = float(metrics[20].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[20].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            giro_ativos         = float(metrics[21].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[21].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            roic                = float(metrics[22].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[22].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            roa                 = float(metrics[23].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[23].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            div_liq_patr        = float(metrics[24].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[24].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            div_liq_ebitda      = float(metrics[25].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[25].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            div_liq_ebit        = float(metrics[26].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[26].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            div_bruta_patr      = float(metrics[27].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[27].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            patr_ativos         = float(metrics[28].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[28].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            passivos_ativos     = float(metrics[29].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[29].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            liquidez_corrente   = float(metrics[30].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[30].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            cagr_rec_5_anos     = float(metrics[31].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[31].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""
            cagr_lucros_5_anos  = float(metrics[32].replace(".", "").replace(",", ".").replace("%","").replace(" ","")) if metrics[32].replace(".", "").replace(",", ".").replace("%","").replace(" ","") != '-' else ""

    #        setor = metrics[33]
    #        subsetor = metrics[34]
    #        segmento = metrics[35]

            df_metrics = df_metrics.append({'ticker': ticker, 
                                            'cotacao': cotacao, 
                                            'valorizacao': valorizacao,
                                            'pl': pl,
                                            'pvp' : pvp, 
                                            'dy': dy,
                                            'roe': roe,
                                            'payout': payout,
                                            'mrg_liquida': mrg_liquida,
                                            'mrg_bruta': mrg_bruta,
                                            'margem_ebit': margem_ebit,
                                            'margem_ebitda': margem_ebitda,
                                            'ev_ebitda': ev_ebitda,
                                            'ev_ebit': ev_ebit,
                                            'p_ebitda': p_ebitda,
                                            'p_ebit': p_ebit,
                                            'p_ativo': p_ativo,
                                            'p_cap_giro': p_cap_giro,
                                            'p_ativ_circ_liq': p_ativ_circ_liq,
                                            'psr': psr,
                                            'vpa': vpa, 
                                            'lpa': lpa,
                                            'giro_ativos': giro_ativos,
                                            'roic': roic,
                                            'roa': roa,
                                            'div_liq_patr': div_liq_patr,
                                            'div_liq_ebitda': div_liq_ebitda,
                                            'div_liq_ebit': div_liq_ebit,
                                            'div_bruta_patr': div_bruta_patr,
                                            'patr_ativos': patr_ativos,
                                            'passivos_ativos': passivos_ativos,
                                            'liquidez_corrente': liquidez_corrente,
                                            'cagr_rec_5_anos': cagr_rec_5_anos,
                                            'cagr_lucros_5_anos': cagr_lucros_5_anos
                                        }, ignore_index=True)        
        i+=1
        if (row < package_size):
            row+=1
        else: 
            row=1
            df_metrics.to_csv(r'metrics.csv', index = False, header=True)
                    
    print(df_metrics)
    df_metrics.to_csv(r'metrics.csv', index = False, header=True)
    df_metrics.set_index('ticker', inplace=True)
    print(df_metrics)

    df_dy_roe = pd.read_csv('dy_roe.csv', encoding= 'unicode_escape')
    print(df_dy_roe)
    df_dy_roe.set_index('ticker', inplace=True)
    print(df_dy_roe)
    
    df_metrics = df_metrics.join(df_dy_roe, lsuffix='_metr', rsuffix='_dyroe')
    df_metrics.reset_index(inplace=True)
    df_metrics = df_metrics.rename(columns = {'index':'ticker'})

    print(df_metrics)

    df_metrics.to_csv(r'metrics_final.csv', index = False, header=True)

#    if show_custom:
        #calculateReturn(tickerSymbol, priceData, initial_invest, increase_days, decrease_days, circuit_breaker, increase_breaker, allow_loss)
#        'Tickers', tickers
#        st.sidebar.balloons()
main()        