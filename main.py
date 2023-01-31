#imports
import pandas as pd
import pip._vendor.requests as requests
import json
from requests.auth import HTTPBasicAuth
from tkinter import *
import customtkinter
from datetime import date, datetime, timedelta
from IPython.display import display
from prettytable import PrettyTable



customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

#Date stuff
current_date = date.today()
time_1 = datetime.now()
time_2 = time_1 - timedelta(minutes=5)
time_1 = time_1.strftime("%H:%M:%S")
time_2 = time_2.strftime("%H:%M:%S")

#Different platforms
android = "https://android-review.googlesource.com"
opendev = "https://review.opendev.org"
chromium = "https://chromium-review.googlesource.com"


#I do not know if there is a better way to deal with settings, 
# maybe loading and saving them in every function is not so great after all ┬─┬ノ( º _ ºノ)
#------------------------Settings--------------------------------------------
def write_settings(settings):
    file_name = "settings.json"
    with open(file_name, "w") as settings_file:
        json.dump(settings, settings_file,indent=4)

def load_settings():
    file_name = "settings.json"
    with open(file_name, "r") as settings_file:
        settings_str = settings_file.read()
        settings_dict = json.loads(settings_str)
    return settings_dict

def show_Results(JSON_response):
    unique_ids = set()
    for item in JSON_response:
        unique_ids.add(item['id'])
    if len(unique_ids) == 0: return "Error, nothing returned from the search"
    new_status = [item for item in JSON_response if item["status"] == "NEW"]
    df = pd.DataFrame(JSON_response)
    #df = df[['subject', 'owner','project', 'branch', 'updated', 'insertions', 'deletions','status']]
    df = df[['owner','project', 'branch', 'updated', 'insertions','deletions']]

    print("Unique IDs found: ",len(unique_ids))
    print("All NEW changes: ",len(new_status))
    return df

def requestAPICall(url):
    """
    does API stuff
    """
    response = requests.get(url)
    JSON_response = json.loads(response.text[4:])
    if(response.status_code == 200):
        generateJSON(JSON_response)
        #JSON_response = response.json()
        unique_ids = set()

    else:
        print(response)
        print("Error occured")
    return JSON_response



def generateJSON(JSON_response):
    """
    Generates and saves the data as a JSON names out.json
    """

    file_name = "out.json"
    with open(file_name, "w") as json_file:
        json.dump(JSON_response, json_file, indent=4)
    return

def generateLink(PLATFORM,date1 = current_date,date2=current_date,time1=time_1,time2=time_2,UTC="0100"):
    """
    Generates a link that is used by the REST api, format is weird hopefully it doesn't break when
    more stuff is added
    """
    #The format is: since:"2023-01-26 21:18:00 +0100" before:"2023-01-26 21:18:30 +0100"
    since = f"%22{date2}%20{time2}%20%2B{UTC}%22" #This took a long while to figure out, but thanks to 
    before = f"%22{date1}%20{time1}%20%2B{UTC}%22"#this stackoverflow person https://stackoverflow.com/questions/53589423/gerrit-rest-api-not-working-when-query-string-contains-hour-minute-second
    getLINK = f"{PLATFORM}/changes/?q=since:{since}+before:{before}"
    return getLINK
#--------------------------------------------------------------------------

#------------------------Changing Settings---------------------------------
def set_Time(): #WIP
    """
    Sets the timeframe, i.e 2022-12-22 06:00:00 -> 2022-12-22 06:15:00
    """
    settings = load_settings()
    date_1 = str(input("Select a START date [FORMAT:2022-12-22]:"))
    date_2 = str(input("Select a END date [FORMAT:2022-12-22]:"))
    time_1 = str(input("Select a START time in the format of [FORMAT:23:39:00]:"))
    time_2 = str(input("Select a END time in the format of [FORMAT:23:39:00]"))
    UTC2 = str(input("Select a END time in the format of [0100]:"))
    settings["DATE_1"] = date_2
    settings["DATE_2"] = date_1
    settings["SET_TIME_1"] = time_2
    settings["SET_TIME_2"] = time_1
    settings["UTC"] = UTC2
    write_settings(settings)
    return
  
def quit_GPipe():
    """
    Function is used to quit GPipe
    """
    print("Quitting GPipe...")
    quit()



def update_current_settings():
    settings_dict = load_settings()
    platform = settings_dict.get("PLATFORM", "chromium")
    date_2 = settings_dict.get("DATE_2", "")
    date_1 = settings_dict.get("DATE_1", "")
    time_2 = settings_dict.get("SET_TIME_2", "")
    time_1 = settings_dict.get("SET_TIME_1", "")
    current_settings = f"""
---------------------------------------------------------
Current settings
Platform: {platform}
Time:  {date_2} {time_2} -> {date_1} {time_1}
    """
    return(current_settings)
def run_GPipe():
    settings_dict = load_settings()
    PLATFORM = settings_dict["PLATFORM"]
    DATE_1 = settings_dict["DATE_1"]
    DATE_2 = settings_dict["DATE_2"]
    SET_TIME_1 = settings_dict["SET_TIME_1"]
    SET_TIME_2 = settings_dict["SET_TIME_2"]
    UTC = settings_dict["UTC"]
    getOPEN = generateLink(PLATFORM,DATE_1, DATE_2,SET_TIME_1,SET_TIME_2,UTC)
    JSON_response = requestAPICall(getOPEN)
    return show_Results(JSON_response)



platform_Options = {0: chromium, 1: opendev, 2: android}
def set_Platform(value = 0):
    """
    Sets the platform the user wants to use. Only one can be selected.
    """

    settings = load_settings()
    choice = value
    if choice in platform_Options:
        print(platform_Options[choice])
        settings["PLATFORM"] = platform_Options[choice]
        write_settings(settings)
    else:
        print("ERROR! Platform could not be set.")
        

class App(customtkinter.CTk):
    root = customtkinter.CTk()
    def __init__(root):
        super().__init__()
        """
        Simple and easy menu that loads the function needed to set different things.
        """
        root.geometry("1400x600+25+25")
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure((2, 3), weight=0)
        root.grid_rowconfigure((0, 1, 2), weight=1)

        settings_dict = {"PLATFORM": chromium, "DATE_1": current_date.strftime("%Y-%m-%d"), "DATE_2": current_date.strftime("%Y-%m-%d"), "SET_TIME_1": time_1, "SET_TIME_2":time_2,"UTC":"0100"}
        write_settings(settings_dict)

        root.title("Menu")
        
        #Platform, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.radiobutton_frame = customtkinter.CTkFrame(root)
        root.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        root.radio_var = IntVar(value=0)
        root.label_radio_group = customtkinter.CTkLabel(master=root.radiobutton_frame, text="Platform")
        root.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        root.radio_button_1 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=0, text="Chromium")
        root.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        root.radio_button_2 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=1, text="OpenDEV")
        root.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        root.radio_button_3 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=2, text="Android")
        root.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create textbox
        root.textbox = customtkinter.CTkTextbox(root, width=1000)
        root.textbox.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        #Sidebar, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
        root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
        root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        root.sidebar_frame.grid_rowconfigure(4, weight=1)
        root.logo_label = customtkinter.CTkLabel(root.sidebar_frame, text="GPipe", font=customtkinter.CTkFont(size=35, weight="bold"))
        root.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        root.run_button = customtkinter.CTkButton(root.sidebar_frame,text="Run",command=root.run_GPipe_event)
        root.run_button.grid(row=1, column=0, padx=20, pady=10)
        root.quit_button = customtkinter.CTkButton(root.sidebar_frame, text="Quit",command=quit_GPipe)
        root.quit_button.grid(row=5, column=0, padx=20, pady=(10, 0))

    def run_GPipe_event(root):
        platform = root.radio_var.get()

        set_Platform(platform)
        df = run_GPipe()


        df['owner'] = df['owner'].apply(lambda x: x['_account_id'])
        df['updated'] = df['updated'].apply(lambda x: x.split('.')[0])  

        # Create a prettytable instance
        table = PrettyTable()

        # Set the column names
        table.field_names = df.columns.tolist()
        for row in df.itertuples(index=False):
            table.add_row(row)
        textbox_string = str(table)
        #df.columns = ['owner ', 'project ', 'branch ', 'updated ', 'insertions ', 'deletions ']
        #df.style.set_properties(subset=pd.IndexSlice[:, :], **{'width': '50px'})

        #textbox_string = df.to_string(index=True, justify='center')
        print(textbox_string)
        root.textbox.configure(font=("Consolas", 12))
        
        root.textbox.insert("1.0",textbox_string)

        #root.textbox.insert("0.0",)

if __name__ == "__main__":  
    app = App()
    app.mainloop()