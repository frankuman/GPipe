WELCOME ="""
  .oooooo.    ooooooooo.    o8o                       
 d8P'  `Y8b   `888   `Y88.  `"'                       
888            888   .d88' oooo  oo.ooooo.   .ooooo.  
888            888ooo88P'  `888   888' `88b d88' `88b 
888     ooooo  888          888   888   888 888ooo888 
`88.    .88'   888          888   888   888 888    .o 
 `Y8bood8P'   o888o        o888o  888bod8P' `Y8bod8P' 
                                  888                 
                                 o888o
                    A Gerrit Analysis Pipeline
                    Made by Oliver Bölin                                                                      """



import pip._vendor.requests as requests
import json
from requests.auth import HTTPBasicAuth
from datetime import date, datetime, timedelta


#Date stuff
current_date = date.today()
time_1 = datetime.now()
time_2 = time_1 - timedelta(minutes=5)
time_1 = time_1.strftime("%H:%M:%S")
time_2 = time_2.strftime("%H:%M:%S")

#Menu stuff
MENU = f"""
1. Choose platform [Standard chromium]
2. Sort by time [Standard {current_date} {time_2} -> {current_date} {time_1} (UTC +01)]
8. Run with current settings
9. Quit GPipe
"""

#Different platforms
android = "https://android-review.googlesource.com"
opendev = "https://review.opendev.org"
chromium = "https://chromium-review.googlesource.com"

#Globals

def write_settings(settings):
    file_name = "settings.json"
    print(settings)
    with open(file_name, "w") as settings_file:
        json.dump(settings, settings_file,indent=4)

def load_settings():
    file_name = "settings.json"
    with open(file_name, "r") as settings_file:
        settings_str = settings_file.read()
        settings_dict = json.loads(settings_str)
    return settings_dict

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
        for item in JSON_response:
            unique_ids.add(item['id'])
        print("Unique IDs found: ",len(unique_ids))
    else:
        print(response)
        print("Error occured")
    return JSON_response

def generateJSON(json_response):
    """
    Generates and saves the data as a JSON names out.json
    """

    file_name = "out.json"
    with open(file_name, "w") as json_file:
        json.dump(json_response, json_file, indent=4)

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

def set_Time(): #WIP
    """
    Sets the timeframe, i.e 2022-12-22 06:00:00 -> 2022-12-22 06:15:00
    """
    settings = load_settings()
    date_1 = str(input("Select a START date [FORMAT:2022-12-22]:"))
    date_2 = str(input("Select a END date [FORMAT:2022-12-22]:"))
    time_1 = str(input("Select a START time in the format of [FORMAT:23:39:00]:"))
    time_1 = str(input("Select a END time in the format of [FORMAT:23:39:00]"))
    UTC2 = str(input("Select a END time in the format of [0100]:"))
    settings["DATE_2"] = date_1
    settings["DATE_1"] = date_2
    settings["SET_TIME_2"] = time_1
    settings["SET_TIME_1"] = time_2
    settings["UTC"] = UTC2
    write_settings(settings)
    menu()


platform_Options = {1: android, 2: opendev, 3: chromium}
def set_Platform():
    settings = load_settings()
    """
    Sets the platform the user wants to use. Only one can be selected.
    """
    #global PLATFORM
    print("These platforms are available (standard is chromium)")
    print("1. " + android)
    print("2. " + opendev)
    print("3. " + chromium)
    print("9. Return to menu")
    choice = int(input("Enter your choice: "))
    if choice in platform_Options:
        print(platform_Options[choice])
        settings["PLATFORM"] = platform_Options[choice]
        write_settings(settings)
        menu()
    if choice == 9:
        menu()
    else:
        print("Option not found in menu, try again!")
        set_Platform()
    
def run_GPipe():
    settings_dict = load_settings()
    PLATFORM = settings_dict["PLATFORM"]
    DATE_1 = settings_dict["DATE_1"]
    DATE_2 = settings_dict["DATE_2"]
    SET_TIME_1 = settings_dict["SET_TIME_1"]
    SET_TIME_2 = settings_dict["SET_TIME_2"]
    UTC = settings_dict["UTC"]
    getOPEN = generateLink(PLATFORM,DATE_1, DATE_2,SET_TIME_1,SET_TIME_2,UTC)
    requestAPICall(getOPEN)


    menu()
def quit_GPipe():
    """
    Function is used to quit GPipe
    """
    print("Quitting GPipe...")
    quit()

menu_Options = {1: set_Platform, 2: set_Time, 9: quit_GPipe}
def menu():
    """
    Simple and easy menu that loads the function needed to set different things.
    """
    print(update_current_settings())
    print(MENU)
    choice = int(input("Enter your choice: "))
    if choice in menu_Options:
        menu_Options[choice]()
    if choice == 8:
        run_GPipe()
    else:
        print("Option not found in menu, try again!")
        menu()

def main():
    #Dict with settings, and all in strings
    settings_dict = {"PLATFORM": chromium, "DATE_1": current_date.strftime("%Y-%m-%d"), "DATE_2": current_date.strftime("%Y-%m-%d"), "SET_TIME_1": time_1, "SET_TIME_2":time_2,"UTC":"0100"}
    write_settings(settings_dict)
    print(WELCOME)
    menu()

if __name__ == "__main__":
    main()