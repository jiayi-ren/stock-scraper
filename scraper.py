import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
import datetime,os,sys,pandas
import bokeh
from bokeh.plotting import figure,show,save,output_file


API_Key = pandas.read_csv("Alpha Vantage API key.txt")

ts = TimeSeries(key='API_Key', output_format = 'pandas')
################### Stock data scraper ############
def intraday(stock,interval,size):
    data, meta_data = ts.get_intraday(symbol=stock,interval=interval, outputsize=size)

def daily(stock,size):
    data, meta_data = ts.get_daily(symbol=stock, outputsize=size)
    return data

def weekly(stock,size):
    data, meta_data = ts.get_weekly(symbol=stock, outputsize=size)

def monthly(stock,size):
    data, meta_data = ts.get_weekly(symbol=stock, outputsize=size)
################### User Input ####################
try:
    stock = input("Enter Stock Symbol: ") #stock symbol e.g. SPY
    duration = input("Choose Time Frame (intraday/daily/weekly/monthly): ")
    if duration == "intraday" :
        interval = input("Choose interval (1min, 5min, 15min, 30min) :") #1min,5min, 15min, 30min, 60min
    size = input("Choose data size (compact, full)\n" +
    "##compact:latest 100 data points##\n##full:all available datapoints##\ncompact or full? ") #compact:latest 100 data points, full:all available datapoints
    if size != ("compact" or "full"):
        size = input("Re-choose compact or full: ")
    df=daily(stock,size)
####### Invalid stock symbol check ###############
except ValueError:
    print("\nInvalid stock symbol")
    sys.exit()

df.columns=['open','high','low','close','volume']
df.index =pandas.to_datetime(df.index, format='%Y-%m-%d')
########### stock data output file ###################
datafile = input("Enter a output data file name: ")
df.to_csv(datafile +".csv")

################## Bokeh Graph saved to HTML file ##############
htmlfilename=input("Enter graph file name otherwise N/A: ")


def inc_dec(c, o):
    if c > o:
        value="Up"
    elif c < o:
        value="Down"
    else:
        value="Equal"
    return value

def bokeh_graph(htmlfile= "N/A"): 
    df["Status"]=[inc_dec(c, o) for c, o in zip(df.close,df.open)]
    df["Middle"]=(df.open+df.close)/2
    df["Height"]=abs(df.open-df.close)

    p=figure(x_axis_type='datetime',plot_width=500,plot_height=300, sizing_mode="scale_width")
    p.title.text="Candlestick chart"
    p.grid.grid_line_alpha=0
    p.segment(df.index,df.high,df.index,df.low,color="Black")

    hours_12=12*60*60*1000

    p.rect(df.index[df.Status=='Up'],df.Middle[df.Status=="Up"], hours_12, 
        df.Height[df.Status=='Up'],fill_color="green",line_color="black")

    p.rect(df.index[df.Status=='Down'],df.Middle[df.Status=="Down"], hours_12, 
        df.Height[df.Status=='Down'],fill_color="red",line_color="black")
    
    if  "N/A" in htmlfile.upper():
        pass
    else:
        output_file(htmlfile+".html")
        save(p)

bokeh_graph(htmlfilename)
