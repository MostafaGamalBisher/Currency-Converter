# Currency Converter with Autocomplete + Error Handling + pycountry

import tkinter as tk
import requests
import pycountry
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
apikey = os.getenv("MY_SECRET_KEY")


# ------------------- AUTOCOMPLETE FUNCTION ------------------- #

def get_currency_suggestions(text):
    """Return list of currency codes matching user input."""
    if not text:
        return []
    text = text.upper()
    suggestions = []
    for currency in pycountry.currencies:
        if currency.alpha_3.startswith(text) or currency.alpha_3 == text:
            suggestions.append(currency.alpha_3)
    return suggestions[:8]   # Max 8 suggestions


def show_suggestions(entry_widget, listbox_widget, event):
    """Display suggestions under the entry box."""
    text = entry_widget.get()
    suggestions = get_currency_suggestions(text)

    listbox_widget.delete(0, tk.END)

    if suggestions:
        for s in suggestions:
            listbox_widget.insert(tk.END, s)
        listbox_widget.place(x=entry_widget.winfo_x(),
                             y=entry_widget.winfo_y() + entry_widget.winfo_height())
    else:
        listbox_widget.place_forget()


def fill_currency(entry_widget, listbox_widget, event):
    """Fill selected currency from listbox into entry."""
    try:
        selected = listbox_widget.get(listbox_widget.curselection())
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected)
    except:
        pass
    listbox_widget.place_forget()


# ---------------------- EXCHANGE FUNCTION ---------------------- #

def exchange(event=None):
    """Main currency conversion function."""
    try:
        url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={apikey}"
        response = requests.get(url)

        if response.status_code != 200:
            resultlabelvalue.config(text="API Error. Try again later.")
            return

        data = response.json()
        rates = data["rates"]

        initc = initcurrancytextarea.get().upper()
        targetc = targtedcurrancytextarea.get().upper()
        amount = float(amounttextarea.get())

        if initc not in rates or targetc not in rates:
            resultlabelvalue.config(text="Invalid currency code.")
            return

        init_rate = float(rates[initc])
        target_rate = float(rates[targetc])

        usd_amount = amount / init_rate
        converted = usd_amount * target_rate

        resultlabelvalue.config(text=f"{amount} {initc} = {converted:.2f} {targetc}")
        ratevaluelabel.config(text=f"1 {initc} = {(target_rate/init_rate):.4f} {targetc}")

    except ValueError:
        resultlabelvalue.config(text="Enter a valid amount.")
    except Exception as e:
        resultlabelvalue.config(text=f"Error: {str(e)}")


# ---------------------------- UI ---------------------------- #

window = tk.Tk()
window.title("Currency Exchange App")
window.geometry("430x320")

# Grid expand
for i in range(3):
    window.columnconfigure(i, weight=1)
for i in range(5):
    window.rowconfigure(i, weight=1)


# ENTRY FIELDS
initcurrancytextarea = tk.Entry(window)
initcurrancytextarea.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

targtedcurrancytextarea = tk.Entry(window)
targtedcurrancytextarea.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

amounttextarea = tk.Entry(window)
amounttextarea.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

# LABELS
tk.Label(window, text="From:").grid(column=0, row=0, sticky="e")
tk.Label(window, text="To:").grid(column=0, row=1, sticky="e")
tk.Label(window, text="Amount:").grid(column=0, row=2, sticky="e")

tk.Label(window, text="Rate:").grid(column=0, row=3, sticky="e")
ratevaluelabel = tk.Label(window, text="N/A")
ratevaluelabel.grid(column=1, row=3, sticky="w")

tk.Label(window, text="Result:").grid(column=0, row=4, sticky="e")
resultlabelvalue = tk.Label(window, text="N/A")
resultlabelvalue.grid(column=1, row=4, sticky="w")


# EXCHANGE BUTTON
exchangebtt = tk.Button(window, text="Exchange", command=exchange)
exchangebtt.grid(column=2, row=0, padx=10, pady=10, sticky="ew")

# ENTER KEY triggers exchange
window.bind("<Return>", exchange)


# ------------------- AUTOCOMPLETE BOXES ------------------- #

init_listbox = tk.Listbox(window, height=5)
target_listbox = tk.Listbox(window, height=5)

# Bind typing events
initcurrancytextarea.bind("<KeyRelease>",
                          lambda event: show_suggestions(initcurrancytextarea, init_listbox, event))
targtedcurrancytextarea.bind("<KeyRelease>",
                             lambda event: show_suggestions(targtedcurrancytextarea, target_listbox, event))

# Bind selection from listbox
init_listbox.bind("<<ListboxSelect>>",
                  lambda event: fill_currency(initcurrancytextarea, init_listbox, event))
target_listbox.bind("<<ListboxSelect>>",
                    lambda event: fill_currency(targtedcurrancytextarea, target_listbox, event))


window.mainloop()
