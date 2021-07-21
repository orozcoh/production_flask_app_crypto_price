from flask import Flask, send_file, render_template
import requests
import json
import time
import threading

# the all-important app variable:
app = Flask(__name__)

API_Request_Lock = threading.Lock()
print_lock = threading.Lock()

cryptos =["ethereum", "bitcoin", "osmosis", "cosmos", "ion"]
currency = "USD"

actual_price = [0]*len(cryptos)

API_call_permit = 1     # 0 -> API call cannot be made (already has whitin user time range)
                        # 1 -> API call can be made 

temp_html = " "


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
    open('./templates/data.html', 'w').close()
    #time.strftime("%a %d %b %Y %H:%M:%S", time.localtime())
    temp_html += "" + time.ctime()
    print("\n\t<p>", time.ctime(), file=open('./templates/data.html', 'a'))
    temp_html += "<p>--------------------------------------------------------------------------------"
    print("\n\n<p>--------------------------------------------------------------------------------", file=open('./templates/data.html', 'a'))
    for i in range(len(cryptos)):
        temp_html += "<p> " + str.upper(cryptos[i]) + "  Price: " + str(actual_price[i]) + "  " + currency
        print("\n\t<p> {:15s} {:10s} {:4.2f} \t {}".format(str.upper(cryptos[i]),"Price: ", actual_price[i], currency), end=" ", file=open('./templates/data.html', 'a')) 
        #print("\t1H Change: ", percent, "%", end="")  
    temp_html += "<p>--------------------------------------------------------------------------------" 
    print("\n\n<p>--------------------------------------------------------------------------------", file=open('./templates/data.html', 'a'))
    return temp_html

def reset_API_request_timer():
    global API_call_permit

    # print_lock.acquire()
    # print("\nEnter to thread: ", end=" ")
    # print("\tTime: ", time.ctime())
    # print_lock.release()

    time.sleep(60)
    API_Request_Lock.acquire()
    API_call_permit = 1
    API_Request_Lock.release()

    # print_lock.acquire()
    # print("\nExit from thread: ", end=" ")
    # print("\tTime: ", time.ctime())
    # print_lock.release()


t_reset_api_permit = threading.Thread(target=reset_API_request_timer)

@app.route("/")
def index():
    global API_call_permit
    global temp_html
    global t_reset_api_permit

    # print_lock.acquire()
    # print("\nPERMIT: ", API_call_permit)
    # print_lock.release()

    API_Request_Lock.acquire()

    if API_call_permit == 1:
        API_call_permit = 0
        html_data = build_html()
        temp_html = "<p>LAST TIME UPDATED: " + html_data

        if not t_reset_api_permit.is_alive():
            try:
                t_reset_api_permit.start()
            except RuntimeError: #occurs if thread is dead
                t_reset_api_permit = threading.Thread(target=reset_API_request_timer) #create new instance if thread is dead
                t_reset_api_permit.start()

    API_Request_Lock.release()

    # print_lock.acquire()
    # print("html sent: ", time.ctime()) 
    # print_lock.release()

    
    return temp_html #render_template('data.html')

@app.route('/download_file')
def download_file():

	path = "./templates/data.html"

	return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)