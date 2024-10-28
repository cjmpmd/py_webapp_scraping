
import requests, json, os
import tkinter as tk
from ady_func import printer
from tkinter import messagebox
from dotenv import load_dotenv
load_dotenv()


def web_api(case):
    url = url(os.getenv('API_ENDPOINT'))
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(case), headers=headers)

    if response.status_code == 200:
        printer('--- Connected with webapp...')
        printer('--- JSON sent successfully')
    else:
        printer('Failed to send JSON')
    printer('Connection ended: webapp...')

def dashboard(fid,vitals,case_data,details,full_notes,meds,main_location,mode):
    case = {}
    case['fid'] = fid
    case['vitals'] = vitals
    case['case_data'] = case_data
    case['details'] = details
    if(mode == 1):
        case['full_notes'] = full_notes
    if(meds != ''):
        case['meds'] = meds

    file_name = 'full_case_'
    web_api(case)
    

def show_alert():
    messagebox.showinfo("Alert", "This is a pop-up alert!")

# Create the main window
    root = tk.Tk()
    root.title("Pop-up Alert Example")

    # Create a button to trigger the alert
    alert_button = tk.Button(root, text="Show Alert", command=show_alert)
    alert_button.pack(padx=20, pady=10)

    # Start the GUI event loop
    root.mainloop()