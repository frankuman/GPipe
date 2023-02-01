#imports
import os
import pandas as pd
import pip._vendor.requests as requests
import json
from requests.auth import HTTPBasicAuth
from tkinter import *
import customtkinter
from datetime import date, datetime, timedelta
from IPython.display import display
from prettytable import PrettyTable
from PIL import Image


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("theme.json")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(0.9)
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

def get_df_str(JSON_response,error_Bool):
    if error_Bool == False:
        if JSON_response.status_code == 201:
            message = "Created"
        elif JSON_response.status_code == 204:
            message = "No Content"
        elif JSON_response.status_code == 400:
            message = "Bad Request"
        elif JSON_response.status_code == 401:
            message = "Unauthorized"
        elif JSON_response.status_code == 403:
            message = "Forbidden"
        elif JSON_response.status_code == 404:
            message = "Not Found"
        elif JSON_response.status_code == 500:
            message = "Internal Server Error"
        else:
            JSON_response.message = "Unknown HTTP status code"

        return(f"ERROR, Couldn't /crawl, ERROR\nHTTP status code: {JSON_response.status_code} ({message})")
    unique_ids = set()
    for item in JSON_response:
        unique_ids.add(item['id'])
    if len(unique_ids) == 0: return "Error, nothing returned from the search"
    new_status = [item for item in JSON_response if item["status"] == "NEW"]
    df = pd.DataFrame(JSON_response)
    df = df[['owner','project', 'branch', 'updated', 'insertions','deletions']]
    df['owner'] = df['owner'].apply(lambda x: x['_account_id']) #Removes unnecesary lines that makes the df way too long
    df['updated'] = df['updated'].apply(lambda x: x.split('.')[0])  
    df['project'] = df['project'].str.replace('chromium','...')
    table = PrettyTable()
    # Set the column names
    table.field_names = df.columns.tolist() #This works, i dont know why
    for row in df.itertuples(index=False):
        table.add_row(row)
    df = str(table)
    print("Unique IDs found: ",len(unique_ids))
    print("All NEW changes: ",len(new_status))
    return df

def requestAPICall(url):
    """
    does API stuff
    """
    response = requests.get(url)
    if(response.status_code == 200):
        JSON_response = json.loads(response.text[4:])
        generateJSON(JSON_response)
        return (JSON_response,True)
    print("Error Occured")
    return (response,False)    



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
    JSON_response,error_Bool = requestAPICall(getOPEN)
    return get_df_str(JSON_response,error_Bool)



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
    #Set window size
    width = 1600    
    height = 800
    def __init__(root):
        
        """
        Simple and easy menu that loads the function needed to set different things.
        """
        super().__init__() 
    
        root.geometry(f"{root.width}x{root.height}")
        #root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure((1, 2, 3), weight=1)
        root.grid_rowconfigure((1, 2), weight=2)
        root.grid_rowconfigure((0), weight=1)

        root.resizable(False, False) #Optional, but the UI is made for this size
        #root.wm_attributes("-transparentcolor", "white")
        root.wm_attributes('-alpha', 0.99)
        #root.wm_attributes('-transparentcolor','#2f3136')
        #root.wm_attributes('-topmost', True)
        settings_dict = {"PLATFORM": chromium, "DATE_1": current_date.strftime("%Y-%m-%d"),
         "DATE_2": current_date.strftime("%Y-%m-%d"), "SET_TIME_1": time_1, "SET_TIME_2":time_2,"UTC":"0100"}
        write_settings(settings_dict)
        root.title("gpipe")
        current_path = os.path.dirname(os.path.realpath(__file__))
        root.bg_image = customtkinter.CTkImage(Image.open(current_path + "/images/bg.png"),size=(root.width/2+25, root.height/2+200))
        root.bg_image_label = customtkinter.CTkLabel(master = root, image=root.bg_image,text="")
        
        root.bg_image_label.grid(row=0, column=1,columnspan=6,rowspan=6,sticky='',padx=(0,0),pady=(200,0))
        
        
        #Platform, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.radiobutton_frame = customtkinter.CTkFrame(root)
       
        root.radiobutton_frame.grid(row=0, column=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        root.radio_var = IntVar(value=0)
        root.label_radio_group = customtkinter.CTkLabel(master=root.radiobutton_frame, text="/ Platform")
        root.label_radio_group.grid(row=0, column=4, columnspan=1, padx=10, pady=(5, 5), sticky="")
        root.radio_button_1 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=0, text="Chromium")
        root.radio_button_1.grid(row=1, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_2 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=1, text="OpenDEV")
        root.radio_button_2.grid(row=2, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_3 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var, value=2, text="Android")
        root.radio_button_3.grid(row=3, column=4, pady=10, padx=20, sticky="n")
        #More radio buttons, doesnt do anything rn
        
        root.radio_var_2 = IntVar(value=0)

        root.label_radio_group_2 = customtkinter.CTkLabel(master=root.radiobutton_frame, text="Chungite?")
        root.label_radio_group_2.grid(row=4, column=4, columnspan=1, padx=10, pady=10, sticky="")
        root.radio_button_4 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var_2, value=0, text="Yes")
        root.radio_button_4.grid(row=5, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_5 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var_2, value=1, text="Tomorrow")
        root.radio_button_5.grid(row=6, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_6 = customtkinter.CTkRadioButton(master=root.radiobutton_frame, variable=root.radio_var_2, value=2, text="Ooga")
        root.radio_button_6.grid(row=7, column=4, pady=10, padx=20, sticky="n")
        #Search button - WIP, doesnt do anything right now
        root.entry = customtkinter.CTkEntry(root, placeholder_text="Enter ID/Project name/Branch", height=50)
        root.entry.grid(row=3, column=2, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        root.main_button_1 = customtkinter.CTkButton(master=root, fg_color="transparent", border_width=2, text="/  Crawl")
        root.main_button_1.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        #check - WIP
   
        root.checkbox_slider_frame = customtkinter.CTkFrame(root)
        root.checkbox_slider_frame.grid(row=1, column=4, padx=(20, 20), pady=(20, 0), sticky="nsew")

        root.checkbox_slider_group_2 = customtkinter.CTkLabel(master=root.checkbox_slider_frame, text="/ is:",anchor="n")
        root.checkbox_slider_group_2.grid(row=0, column=0, padx=5, pady=5, sticky="")

        root.checkbox_1 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="open")
        root.checkbox_1.grid(row=1, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_2 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="watched")
        root.checkbox_2.grid(row=2, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_3 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="unassigned")
        root.checkbox_3.grid(row=3, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_4 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="reviewed")
        root.checkbox_4.grid(row=4, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_4 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="closed")
        root.checkbox_4.grid(row=5, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_4 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="merged")
        root.checkbox_4.grid(row=6, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_4 = customtkinter.CTkCheckBox(master=root.checkbox_slider_frame,text="pending")
        root.checkbox_4.grid(row=7, column=0, pady=(5, 5), padx=20, sticky="n")
        # create textbox
        root.textbox = customtkinter.CTkTextbox(root, width=1100,corner_radius=8,fg_color="transparent", border_width=2,)
        #root.bg_image_label.lift()
        root.textbox.grid(row=0, column=3, padx=(10, 10), pady=(20, 0), sticky="nsew")
        # create sidebox next to textbox
        root.radiobutton_frame_2 = customtkinter.CTkFrame(root,corner_radius=8)
        root.radiobutton_frame_2.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        #Sidebar, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py

        root.logo_image = customtkinter.CTkImage(Image.open(current_path + "/images/gpipe.png"),size=(140, 50))

        root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
        root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        root.sidebar_frame.grid_rowconfigure(4, weight=1)
        root.logo_image_label = customtkinter.CTkLabel(root.sidebar_frame, image=root.logo_image,text="",height=0,fg_color="#2f3136")
        root.logo_image_label.grid(row=0, column=0,sticky='n',padx=10,pady=(10,0))
        #root.logo_label = customtkinter.CTkLabel(root.sidebar_frame, text="GPipe", font=customtkinter.CTkFont(size=35, weight="bold",family="Uni Sans"))
        #root.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        root.run_button = customtkinter.CTkButton(root.sidebar_frame,height = 50,text="/      Run",anchor="w",command=root.run_GPipe_event,font=customtkinter.CTkFont(size=15, weight="bold",family="Uni Sans"))
        root.run_button.grid(row=1, column=0, padx=10, pady=10)
        root.quit_button = customtkinter.CTkButton(root.sidebar_frame,height = 50, anchor="w", text="/      Quit",command=quit_GPipe,font=customtkinter.CTkFont(size=15, weight="bold",family="Uni Sans"))
        root.quit_button.grid(row=5, column=0, padx=10, pady=(20, 20))

    def run_GPipe_event(root):
        platform = root.radio_var.get()

        set_Platform(platform)
        df = run_GPipe()
        

        print(df)
        settings = update_current_settings()
        #Credit to help at https://stackoverflow.com/questions/75295073/tkinter-textbox-does-not-look-the-same-as-terminal-print/75295357?noredirect=1#comment132864739_75295357
        root.textbox.configure(font=("Consolas", 15)) #Only works with consolas, no matter
        root.textbox.insert("0.0",settings + "\n" + df + "\n\n")
        

        #root.textbox.insert("0.0",)

if __name__ == "__main__":  
    app = App()
    app.mainloop()