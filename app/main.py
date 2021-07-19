from flask import Flask, render_template
import requests
import json
import time

# the all-important app variable:
app = Flask(__name__)

cryptos =["ethereum", "bitcoin", "osmosis", "cosmos", "ion"]
currency = "USD"

actual_price = [0]*len(cryptos)

def price_extract(url_, crypto_, currency_):
    r = requests.get(url_)
    r_json = r.json()
    asset_price = round(float(r_json[crypto_][currency_]) , 3)
    return asset_price

def build_html():
    for i in range(len(cryptos)):
                url_price = "https://api.coingecko.com/api/v3/simple/price?ids="+cryptos[i]+"&vs_currencies="+currency
                try:
                    actual_price[i] = price_extract(url_price, cryptos[i], str.lower(currency))
                    
                except:
                    print("\nSomething went wrong while extracting prices from coingecko API\n")

    temp_html = " "
    #open('./templates/data.html', 'w').close()
    #time.strftime("%a %d %b %Y %H:%M:%S", time.localtime())
    temp_html += "<p>" + time.ctime()
    #print("\n\t<p>", time.ctime(), file=open('./templates/data.html', 'a'))
    temp_html += "<p>--------------------------------------------------------------------------------"
    #print("\n\n<p>--------------------------------------------------------------------------------", file=open('./templates/data.html', 'a'))
    for i in range(len(cryptos)):
        temp_html += "<p> " + str.upper(cryptos[i]) + "  Price: " + str(actual_price[i]) + "  " + currency
        #print("\n\t<p> {:15s} {:10s} {:4.2f} \t {}".format(str.upper(cryptos[i]),"Price: ", actual_price[i], currency), end=" ", file=open('./templates/data.html', 'a')) 
        #print("\t1H Change: ", percent, "%", end="")  
    temp_html += "<p>--------------------------------------------------------------------------------" 
    #print("\n\n<p>--------------------------------------------------------------------------------", file=open('./templates/data.html', 'a'))
    return temp_html

@app.route("/")
def index():
    html_data = build_html()
    print("donee at: ", time.ctime())
    return html_data #render_template('data.html')

@app.route("/hello")
def hello():
    return "Oh, Hello World"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)