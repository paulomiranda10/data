import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from decimal import Decimal

from pandas.io.json import json_normalize  
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go


import pandas_datareader.data as web
import yfinance as yf
from pandas_datareader._utils import RemoteDataError
from pathlib import Path

from bokeh.plotting import figure
import matplotlib.image as mpimg
import altair as alt
import mplfinance as fplt

from bokeh.io import output_file, show
from bokeh.models import CustomJS, ColumnDataSource



import warnings
warnings.filterwarnings('ignore')

################################################################################
### Stocks Robot
################################################################################
# Lê parâmetros de entrada
def inputParameters(my_bar):
    image=mpimg.imread('tradder_icon.jpg')
    st.image(image, width=200, caption="Stock's Bot")

    #st.title("Stock's Robot")
    
    #set number of weeks in which you want to see return
    #return_period_weeks = 4
    return_period_weeks = st.sidebar.number_input("Weeks: ", 1, 12, 4, 1)

    #start date for simulation. 
    #Further back means more training data but risk of including patterns that no longer exist
    #More recent means less training data but only using recent patterns

    #start_date, end_date = datetime(2019,1,1), datetime.now().date()
    start_date = st.sidebar.date_input('Start Date: ', datetime(2019,1,1))
    end_date = datetime.now().date()

    values_return = st.sidebar.slider('Select a range of return:', -100.0, 400.0, (-100.0,400.0), 1.0, '%f')

    values_dev = st.sidebar.slider('Select a range of std deviation:', 0.0, 200.0, (0.0,200.0), 10.0, '%f')

    tickerSymbol = st.sidebar.text_input('Ticker to forecast: ', '')

    show_sim = st.sidebar.checkbox("Show Simulation")

    initial_invest = st.sidebar.number_input("Initial Investiment $: ", 1000, 500000, 10000, 1000)

    increase_days = st.sidebar.number_input("Increasing days: ", 1, 20, 1, 1)
    decrease_days = st.sidebar.number_input("Decreasing days: ", 1, 20, 1, 1)

    circuit_breaker = st.sidebar.number_input("Circuit Breaker (%): ", 0, 50, 6, 1)

    increase_breaker = st.sidebar.number_input("CB waitting days: ", 0, 90, 5, 1)


    #st.markdown(type(start_date))
    #st.markdown(end_date)


    # The goals to peak are: 
    # Conservative: High avg return and Low deviation/volatility
    # Aggresive:    High avg return and High deviation/volatility
    #
    my_bar.progress(0)
    return start_date, end_date, return_period_weeks, values_return, values_dev, tickerSymbol, show_sim, initial_invest, increase_days, decrease_days, circuit_breaker, increase_breaker


def perform_analysis_for_stock(ticker, start_date, end_date, return_period_weeks, verbose=False):
    #st.markdown("ticker ___ = " + ticker)
#    Inputs:
#        ticker: the ticker symbol to analyze
#        start_date: the first date considered in simulation
#        end_date: the last date considered in simulation
#        return_period_weeks: the number of weeks in which to calculate returns
#        verbose: True if you want to print simulation steps
#        
#    Outputs:
#        average and standard deviation of returns for simulated runs of this ticker within the given date range
    
    #get the data for this ticker
    try:
        prices = web.DataReader(ticker, 'yahoo', start=start_date, end=end_date).Close
        #st.markdown(str(len(prices)))
        #st.markdown('Lenght of data from yahoo finance: ' + str(len(prices)))
        if (len(prices) < 30):
            #print('There is few data for this ticher: ' + ticker)
            #st.warning("There is few data for this ticher: " + ticker)
            st.markdown("There is not enough data for this ticher: ** " + ticker + "**")
            return -np.inf, np.inf, None
        #prices = web.get_data_yahoo(ticker)
    #could not find data on this ticker
    except (RemoteDataError, KeyError):
        #return default values
        st.markdown("Could not find data for this ticher: ** " + ticker + "**")
#        print('Could not find data for this ticker !')
        return -np.inf, np.inf, None
    
    prices.index = [d.date() for d in prices.index]
    
    #this will store all simulated returns
    pct_return_after_period = []
    buy_dates = []

    #assume we buy the stock on each day in the range
    for buy_date, buy_price in prices.iteritems():
        #get price of the stock after given number of weeks
        sell_date = buy_date + timedelta(weeks=return_period_weeks)
        
        try:
            sell_price = prices[prices.index == sell_date].iloc[0]
        #trying to sell on a non-trading day, skip
        except IndexError:
            continue
        
        #compute the percent return
        pct_return = ((sell_price - buy_price)/buy_price)*100
        pct_return_after_period.append(pct_return)
        buy_dates.append(buy_date)
        
        if verbose:
            st.markdown('Date Buy : %s, Price Buy : %s'%(buy_date,round(buy_price,2)))
            st.markdown('Date Sell: %s, Price Sell: %s'%(sell_date,round(sell_price,2)))
            st.markdown('Return: %s%%'%round(pct_return*100,1))
            st.markdown('-------------------')

    #if no data collected return default values
    if len(pct_return_after_period) == 0:
        return -np.inf, np.inf, None
    
    #report average and deviation of the percent returns
    return np.round(np.mean(pct_return_after_period), 2), np.round(np.std(pct_return_after_period), 2), [buy_dates, pct_return_after_period]


def analyze(my_bar, start_date, end_date, return_period_weeks, values_return, values_dev, tickerSymbol):
    priceData = []
    df_stock = pd.read_csv('B3_new.csv', encoding= 'unicode_escape')

    classes_in = ['ON','PN','PN Resg','PNA','PNB','PNC','PND','PNE','PNF','PNG','PNAB','PNAE','PNAG']
    df_stock = df_stock[df_stock.Classe.isin(classes_in)]
    
    # To take out banks 
#    seg_out = ['Bancos']
#    df_stock = df_stock[df_stock.Classe.isin(classes_in) & 
#                        ~df_stock.Classe.isin(seg_out)
#                    ]

#    df_stock.drop(['Classe', 'Setor',  'Segmento', 'Codigo_old'], axis='columns', inplace=True)
    df_stock.drop(['Classe', 'Codigo_old'], axis='columns', inplace=True)

    my_file = Path("stocks_returns_std.csv")
    there_is_file = my_file.exists()
    #there_is_file =  False

    #st.markdown("Tem arquivo = " + str(there_is_file))

    if there_is_file:
        stock_matrix = pd.read_csv('stocks_returns_std.csv', encoding= 'unicode_escape')
    else:
        stock_matrix = pd.DataFrame(columns=['Ticker', 'Return', 'Deviation'])


        size = len(df_stock)
        #st.markdown("Size = " + str(size))
        #st.warning(" Tamanho ==> " + str(size))
        #st.warning(" Tamanho ==> " + str(size))
        #st.error(" == Erro == ")
        #st.info(" == info == ")
        #st.success(" == success == ")
        #st.exception(e)
        for i in range(0, size): 
            progress = int(i+1/size)
            #st.warning(str(progress))
            if (progress > 100):
                progress = 100
            my_bar.progress(progress)
            try:
                #ticker = df_stock.Codigo[i] + '.SA'
                ticker = df_stock.Codigo[i]
                name   = df_stock.Empresa[i]
                #ticker = 'WEGE3.SA'
                st.markdown("Getting data for : ** " + ticker + "**")

                avg_return, dev_return, all_returns = perform_analysis_for_stock(ticker, start_date, end_date, return_period_weeks, False)
#                avg_return = Decimal(avg_return)
#                avg_return = round(avg_return,2)

                stock_matrix = stock_matrix.append({'Ticker': ticker, 'Return': avg_return, 'Deviation': dev_return}, ignore_index=True)
            except :
                continue
        #st.info(" == Loading finished == ")
        stock_matrix.to_csv (r'stocks_returns_std.csv', index = False, header=True)

    stock_matrix = stock_matrix[~stock_matrix.Return.isin(["-inf"])]
    my_bar.progress(100)

    filter = 'Return >= ' + str(values_return[0]) + ' & Return <= ' + str(values_return[1]) + ' & Deviation >= ' + str(values_dev[0]) + ' & Deviation <= ' + str(values_dev[1])
    #st.info(" == Filtro ==> " + filter)

    'Filtered Tickers', stock_matrix.query(filter)

#    if (len(stock_matrix) > 0):
#        if st.checkbox("Show Analysis Results"):
#            'Results', stock_matrix

    #tickerSymbol = st.sidebar.text_input('Ticker to forecast: ', 'CNTO3.SA')

#    'Return vs Std Deviation Map'

#    c = alt.Chart(stock_matrix.query(filter)).mark_circle().encode(
#        x='Return', 
#        y='StdDeviation', 
#        color='Return', tooltip=['Return', 'Ticker', 'StdDeviation'] ).interactive()

#    st.altair_chart(c, use_container_width=True)

    source = stock_matrix.query(filter).sort_values(by=['Return'], ascending=True)
    'Return per Ticker'
    bars = alt.Chart(source).mark_bar().encode(
        x='Return',
        y="Ticker",
        color=alt.condition(
            alt.datum.Return > 0,
            alt.value("steelblue"),  # The positive color
            alt.value("orange")  # The negative color
        )
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Return'
    )
    
#    st.altair_chart((bars + text).properties(height=900), use_container_width=True)
    st.altair_chart((bars + text), use_container_width=True)


    if (len(tickerSymbol) > 0):
        #get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        #get the historical prices for this ticker
        tickerDf = tickerData.history(interval='1d', start=start_date, end=end_date)
    #        tickerDf = tickerData.history(interval='1d', start='2019-1-1', end='2020-10-28')

        #st.markdown("Size = " + str(len(tickerDf)))

        'Historical Positions for: ' + tickerSymbol, tickerDf

        #current_stock_value = tickerDf.Close.iloc[len(tickerDf)-1]

        priceData = tickerDf.Open


#        'priceData.index', priceData.index
#        'tickerDf.Open', tickerDf.Open

        p = figure(
            title = "%s Price Data"%tickerSymbol, 
            x_axis_label='Date',
            x_axis_type='datetime',
            y_axis_label='Price' )

        p.line(priceData.index, tickerDf.Open, legend='Trend', line_width=2)

        st.bokeh_chart(p, use_container_width=True)

#        'Candlestick for: ' + tickerSymbol

        source = tickerDf.copy()
        source.reset_index(level=0, inplace=True)

        my_file = Path("candle-web.html")
        there_is_file = my_file.exists()

        #st.markdown("Tem arquivo = " + str(there_is_file))

        if not there_is_file:
            # First instance
            trace1 = {
                'x': tickerDf.index,
                'open': tickerDf.Open,
                'close': tickerDf.Close,
                'high': tickerDf.High,
                'low': tickerDf.Low,
                'type': 'candlestick',
                'name': tickerSymbol,
                'showlegend': False
            }

            # Calculate and define moving average of 30 periods
            avg_30 = tickerDf.Close.rolling(window=30, min_periods=1).mean()

            # Calculate and define moving average of 50 periods
            avg_50 = tickerDf.Close.rolling(window=50, min_periods=1).mean()

            # Second instance - avg_30
            trace2 = {
                'x': tickerDf.index,
                'y': avg_30,
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 1,
                    'color': 'blue'
                        },
                'name': 'Moving Average of 30 periods'
            }

            # Third instance - avg_50
            trace3 = {
                'x': tickerDf.index,
                'y': avg_50,
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 1,
                    'color': 'red'
                },
                'name': 'Moving Average of 50 periods'
            }

            # Aggregate all instances and define 'data' variable
            data = [trace1, trace2, trace3]
    #        data = [trace1]

            # Config graph layout
            layout = go.Layout({
                'title': {
                    'text': tickerSymbol,
                    'font': {
                        'size': 15
                    }
                }
            })

            # Create Figure and plot
            fig = go.Figure(data=data, layout=layout)
            path_and_file = "./candle-web.html" 
            fig.write_html(path_and_file)


        HtmlFile = open("candle-web.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 450)

    return priceData


#####
##### Buy and Sell Portion
#####
#################################################################################

def get_buying_selling_days(price_data, b, s):
    
    #get the percent change day after day
    pct_change = price_data.pct_change()[1:]

    #'pct_change', pct_change
    
    #this function checks the buying condition
    def buying_condition(sub_series):
        return (sub_series > 0).all()
    
    #this function checks the selling condition
    def selling_condition(sub_series):
        return (sub_series < 0).all()
    
    #get all buying days in the data
    buying_days = pct_change.rolling(b).apply(buying_condition)
    
    #get all potential selling days in the data
    potential_selling_days = pct_change.rolling(s).apply(selling_condition)
    
    #return a dictionary
    return {'buying_days': buying_days, 'potential_selling_days': potential_selling_days, 'pct_change': pct_change}

def check_cumulative_percent_change(price_data, buy_date, potential_sell_date):
    """
    This helper function will check if the cumulative percent change
    between a buying and potential selling day yields overall growth
    """
    
    #get the percent change day after day
    pct_change = price_data.pct_change()[1:]
    
    sub_series = 1 + pct_change[buy_date + timedelta(hours=1): potential_sell_date]

    return sub_series.product() > 1

def get_investing_result(df_stocks, starting_funds, verbose, increase_breaker):
    price_data = df_stocks.price
    
    #at start, not holding any shares
    holding = False
    
    #init vars
    current_funds = starting_funds
    current_shares = 0
    last_buy_date = None
    
    #init dict of buying and selling dates
    events_list = []
    
    increase_breaker_cnt = 0
#    yesterday_price = -1

    first_buy_stock_amt = 0

    df_stocks.reset_index(level=0, inplace=True)

    #'Buy/Sell Conditions', df_stocks

    #for each buying day and potential selling day...
    for i in range(0, len(df_stocks)):
        data = df_stocks.iloc[i]
        # Check for Circuit Breaker Condition
        if (data['pct_change']==True and increase_breaker_cnt==0 and holding==True):
            #check to make sure we're making a profit
            if check_cumulative_percent_change(price_data, last_buy_date, data['Date']):
                current_funds += current_shares * data['price']
                if verbose:
                    msg_text = '**Sold..CB:** {:0,.0f} shares at ${:0,.2f} on {} totaling ${:0,.2f}'.format(current_shares, data['price'], data['Date'].date(), round(num_shares_to_buy*data['price'],2))
                    html_temp = '<font color="red">' + msg_text + '</font>'
                    st.markdown(html_temp, unsafe_allow_html=True)

                    #html_temp = '<div style ="background-color:yellow;padding:8px"><h1 style ="color:black;text-align:left;">' + msg_text + '</h1></div>'
                    #st.markdown('--------------------------------------------------------------------')
                    #st.markdown('**Sold..CB:** {:0,.0f} shares at ${:0,.2f} on {} totaling ${:0,.2f}'.format(current_shares, data.price, date.date(), round(num_shares_to_buy*data.price,2)))
                    #st.markdown('--------------------------------------------------------------------')
                    
                #reset current shares
                current_shares = 0
                #we are no longer holding shares
                holding = False
                # Start the quarentine before buy again
                increase_breaker_cnt = increase_breaker
                events_list.append(('s', data['Date']))


    #if not currently holding shares, and this is a buying day..., and not under circuit breaker quarentine
#        if (not holding) and data.buying_day:
        if (not holding) and data['buying_day'] and increase_breaker_cnt==0:
            # In case of Circuit Breaker Condition,  sell all stocks

            #calculate the number of shares we can buy
            num_shares_to_buy = int(current_funds / data['price'])
            
            #update number of shares
            current_shares += num_shares_to_buy
            
            #decrease current funds
            current_funds -= num_shares_to_buy * data['price']
            
            #set last buy date
            last_buy_date = data['Date']
            events_list.append(('b', data['Date']))
            
            #we are now holding shares
            holding = True
            
            if verbose:
                st.markdown('**Bought:** {:0,.0f} shares at ${:0,.2f} on {} totaling ${:0,.2f}'.format(num_shares_to_buy, data['price'], data['Date'].date(), round(num_shares_to_buy*data['price'],2)))

            if (first_buy_stock_amt == 0):
                first_buy_stock_amt = num_shares_to_buy

        #if you are holding shares, and this is a potential selling day...
        elif holding and data['potential_selling_day']:
            #check to make sure we're making a profit
            if check_cumulative_percent_change(price_data, last_buy_date, data['Date']):
                #add to our current funds
                current_funds += current_shares * data['price']
                
                if verbose:
                    st.markdown('**Sold....:** {:0,.0f} shares at ${:0,.2f} on {} totaling ${:0,.2f}'.format(current_shares, data['price'], data['Date'].date(), round(num_shares_to_buy*data['price'],2)))
                    #st.markdown('--------------------------------------')
                    
                #reset current shares
                current_shares = 0
                
                #we are no longer holding shares
                holding = False
                
                events_list.append(('s', data['Date']))

        #yesterday_price = data.price
        if (increase_breaker_cnt > 0):
            increase_breaker_cnt -= 1


    #get the stock price at the end of the time span
    final_stock_price = price_data[-1]
        
    #get the final total value of all assets (funds + stock value)
    final_value = current_funds + final_stock_price * current_shares
    
    #return the percent change in value
    return round((final_value - starting_funds) / starting_funds,2), events_list, holding, final_stock_price, current_shares, current_funds, first_buy_stock_amt

def calculateReturn(tickerSymbol, priceData, initial_invest, increase_days, decrease_days, circuit_breaker, increase_breaker):
    info_dict = get_buying_selling_days(priceData, increase_days, decrease_days)

    #'info_dict', pd.DataFrame(info_dict)

    buying_days = info_dict['buying_days']
    potential_selling_days = info_dict['potential_selling_days']
    pct_change = info_dict['pct_change']

    #create dataframe to store information
    df_stocks = pd.DataFrame(index = buying_days.index)

    #populate df with buying days, possible selling days, and price
    df_stocks['buying_day'] = (buying_days == 1)
    df_stocks['potential_selling_day'] = (potential_selling_days == 1)
    if (circuit_breaker <= 0):
        df_stocks['pct_change'] = 0
    else:
        df_stocks['pct_change'] = ((pct_change*-1) >= (circuit_breaker/100))

    df_stocks['price'] = priceData
    #df_stocks['vai'] = (buying_days == 1) or (potential_selling_days == 1) or ((pct_change*-1) >= (circuit_breaker/100))
    df_stocks['aux'] = df_stocks['buying_day'] + df_stocks['potential_selling_day'] + df_stocks['pct_change']


    #'df_stocks 1', df_stocks 

    df_stocks = df_stocks[df_stocks.aux == 1]

    #'df_stocks 2', df_stocks
    df_stocks.drop(['aux'], axis='columns', inplace=True)

    #Apagar
    #df_au = df_stocks.copy()
    #df_au.reset_index(level=0, inplace=True)
    #df_au.to_csv (r'df_stocks.csv', index = False, header=True)

    percent_change, events_list, holding, final_stock_price, current_shares, current_funds, first_buy_stock_amt = get_investing_result(df_stocks, initial_invest, True, increase_breaker)

    if holding:
        cur_amt = round(final_stock_price * current_shares,2)
        st.markdown("Estimated current amount (stock value: ${:0,.2f}) : ** ${:0,.2f} **".format(final_stock_price, cur_amt))
    else:
        st.markdown("Estimated value in cash is : ** ${:0,.2f} **".format(current_funds))
#        st.markdown("Estimated value in cash is: **$ " + str(round(current_funds,2))+ "**")

    estimate_return = percent_change * 100
    st.markdown("Estimated return is :       ** " + str(round(estimate_return,2)) + "%**")

    st.markdown("Estimated amount if you bought and holded is : ** ${:0,.2f} **".format(first_buy_stock_amt * final_stock_price))

    ### Graph
#    fig = plt.figure(figsize=(10,4))
#    plt.plot(priceData)
#
#    y_lims = (int(priceData.min()*.95), int(priceData.max()*1.05))
#    shaded_y_lims = int(priceData.min()*.5), int(priceData.max()*1.5)
#
#    for idx, event in enumerate(events_list):
#        color = 'blue' if event[0] == 'b' else 'red'
#        plt.axvline(event[1], color=color, linestyle='--', alpha=0.4)
#        if event[0] == 's':
#            plt.fill_betweenx(range(*shaded_y_lims), 
#                            event[1], events_list[idx-1][1], color='k', alpha=0.1)
#
#    plt.title("%s Price Data"%tickerSymbol, fontsize=20)
#    plt.ylim(*y_lims)
#
#    st.pyplot(fig)


##### 
##### MAIN()
##### 
################################################################################ 
def main():
    #termo, registros, api1, api2, nomeAPI1, nomeAPI2 = readParameters()
    #pd.options.display.float_format = '{:.2f}'.format   

    my_bar = st.sidebar.progress(0)

    start_date, end_date, return_period_weeks, values_return, values_dev, tickerSymbol, show_sim, initial_invest, increase_days, decrease_days, circuit_breaker, increase_breaker = inputParameters(my_bar)

    #submit = st.sidebar.button('Execute')
    #submit2 = False

    #if submit:
    priceData = analyze(my_bar, start_date, end_date, return_period_weeks, values_return, values_dev, tickerSymbol)

    if show_sim:
        calculateReturn(tickerSymbol, priceData, initial_invest, increase_days, decrease_days, circuit_breaker, increase_breaker)
        #st.sidebar.balloons()

main() 