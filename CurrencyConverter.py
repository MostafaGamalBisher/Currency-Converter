import tkinter as tk  #importing the tkinter module for GUI creation
import requests  #importing the requests module to make API requests
from dotenv import load_dotenv 
import os 

load_dotenv() 
apikey = os.getenv("MY_SECRET_KEY") #API key for authentication

def exchange():
    
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={apikey}"
    
    response = requests.get(url)

    status_code = response.status_code 
    if(status_code != 200):  # checking if the response is valid
        print("Sorry, there was a problem. Please try again later.")
        quit()
        
    data = response.json()

    rates = data["rates"]


    initcurrancy = initcurrancytextarea.get().upper()  #getting the initial currency from the entry area
    targtedcurrancy = targtedcurrancytextarea.get().upper()  #getting the targeted currency from the entry area
    amount = float(amounttextarea.get())  #getting the amount to be converted from the entry
    
    if initcurrancy not in rates or targtedcurrancy not in rates:
        resultlabel.config(text="Invalid currency code.")
        return
    init_rate = float(rates[initcurrancy])
    target_rate = float(rates[targtedcurrancy])
    usd_amount = amount / init_rate
    converted_amount = usd_amount * target_rate
    resultlabelvalue.config(text=f"{amount} {initcurrancy} = {converted_amount:.2f} {targtedcurrancy}")
    ratevaluelabel.config(text=f"1 {initcurrancy} = {(target_rate / init_rate):.4f} {targtedcurrancy}")

#Creating the main window

window = tk.Tk()
window.title("Currancy Exchange App")
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(0 , weight=1)
window.rowconfigure(1 , weight=1)
window.rowconfigure(2 , weight=1)

#Creating the exchange button and entry areas

exchangebtt = tk.Button(window , text= "Exchange" , relief="raised" ,command= exchange)
exchangebtt.grid(column=2, row=0 , padx=10, pady=10, sticky="ew")

initcurrancytextarea = tk.Entry(window , text = "Initial Currancy")
initcurrancytextarea.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

targtedcurrancytextarea = tk.Entry(window , text= "Targeted Currancy")
targtedcurrancytextarea.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

amounttextarea = tk.Entry(window , text= "Amount")
amounttextarea.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

#Creating labels to display the results

fromlabel = tk.Label(window , text="From:")
fromlabel.grid(column=0, row=0, padx=10, pady=10, sticky="e")

tolabel = tk.Label(window , text="To:")
tolabel.grid(column=0, row=1, padx=10, pady=10, sticky="e")

amountlabel = tk.Label(window , text= "Amount:")
amountlabel.grid(column=0, row=2, padx=10, pady=10, sticky="e")

ratelabel = tk.Label(window , text="Rate:")
ratelabel.grid(column=0, row=3, padx=10, pady=10, sticky="e")
ratevaluelabel = tk.Label(window , text="N/A")
ratevaluelabel.grid(column=1, row=3, padx=10, pady=10, sticky="w")

resultlabel = tk.Label(window , text="Result:")
resultlabel.grid(column=0, row=4, padx=10, pady=10, sticky="e")

resultlabelvalue = tk.Label(window , text="N/A")
resultlabelvalue.grid(column=1, row=4, padx=10, pady=10, sticky="w")

window.mainloop()  #Running the main event loop

