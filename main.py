# imports
import GUI
import API
import json
import pandas as pd
import customtkinter
from tkinter import *
from prettytable import PrettyTable
from datetime import date, datetime, timedelta


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "JSON/theme.json"
)  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(0.95)


# Different platforms
android = "https://android-review.googlesource.com"
opendev = "https://review.opendev.org"
chromium = "https://chromium-review.googlesource.com"

# Date stuff
current_date = date.today()
current_date_2 = current_date-timedelta(days=1)
time_1 = datetime.now()
time_2 = time_1
time_1 = time_1.strftime("%H:%M:%S")
time_2 = time_2.strftime("%H:%M:%S")
settings_dict_start = {
    "PLATFORM": chromium,
    "DATE_1": current_date.strftime("%Y-%m-%d"),
    "DATE_2": current_date_2.strftime("%Y-%m-%d"),
    "SET_TIME_1": time_1,
    "SET_TIME_2": time_2,
    "UTC": "0100", 
}


    
# I do not know if there is a better way to deal with settings,
# maybe loading and saving them in every function is not so great after all ┬─┬ノ( º _ ºノ)
# ------------------------Settings--------------------------------------------
def write_settings(settings):
    file_name = "JSON/settings.json"
    with open(file_name, "w") as settings_file:
        json.dump(settings, settings_file, indent=4)


def load_settings():
    file_name = "JSON/settings.json"
    with open(file_name, "r") as settings_file:
        settings_str = settings_file.read()
        settings_dict = json.loads(settings_str)
    return settings_dict


def get_df_str(error):
    if error != 200:
        if error == 201:
            message = "Created"
        elif error == 204:
            message = "No Content"
        elif error == 400:
            message = "Bad Request"
        elif error == 401:
            message = "Unauthorized"
        elif error == 403:
            message = "Forbidden"
        elif error == 404:
            message = "Not Found"
        elif error == 500:
            message = "Internal Server Error"
        else:
            message = "Unknown HTTP status code"

        return f"ERROR, Couldn't /crawl, ERROR\nHTTP status code: {error} ({message})"
    #Warning, spaghetti code
    ###OPEN FILE AND MAKES JSON_RESPONSE
    ###
    with open("JSON/out.json", "r") as f:
        data = json.load(f)

    unique_ids = set()
    unique_change = set()
    for item in data:
        unique_ids.add(item["id"])
    for item in data:
        unique_change.add(item["updated"])
    if len(unique_ids) == 0: #Dont know if this is best method
        return "Error, nothing returned from the search"
    #We just make the df pretty
    new_status = [item for item in data if item["status"] == "NEW"]
    df = pd.DataFrame(data)
    df = df[["owner", "project", "branch", "updated", "insertions", "deletions"]]
    df["owner"] = df["owner"].apply(
        lambda x: x["_account_id"]
    )  # Removes unnecesary lines that makes the df way too long
    df["updated"] = df["updated"].apply(lambda x: x.split(".")[0])
    df["project"] = df["project"].str.replace("chromium", "...")
    df['branch'] = df['branch'].apply(lambda x: '/'.join(x.split('/')[-2:])
                                       if len(x) > 10 else x)
    df['branch'] = df['branch'].apply(lambda x: '...' + x if len(x) > 10 else x)
    df['project'] = df['project'].apply(lambda x: '...' + x if len(x) > 10 else x)
    table = PrettyTable()
    # Set the column names
    table.field_names = df.columns.tolist()  # This works, i dont know why
    for row in df.itertuples(index=False):
        table.add_row(row)
    num_rows = df.shape[0]
    df = str(table)
    unique_ids = "All IDs found: " + str(len(unique_ids))
    unique_rows = "All changes found: " + str(num_rows)
    new_changes = ("All NEW changes: " + str(len(new_status)))
    df = unique_rows + "\n"+ new_changes + "\n"+ unique_ids + "\n" + df
    return df


def generateLink(
    PLATFORM,
    date1=current_date,
    date2=current_date,
    time1=time_1,
    time2=time_2,
    UTC="0100",
):
    """
    Generates a link that is used by the REST api, format is weird hopefully it doesn't break when
    more stuff is added
    """
    # The format is: since:"2023-01-26 21:18:00 +0100" before:"2023-01-26 21:18:30 +0100"
    since = f"%22{date2}%20{time2}%20%2B{UTC}%22"  # This took a long while to figure out, but thanks to
    before = f"%22{date1}%20{time1}%20%2B{UTC}%22"  # this stackoverflow person https://stackoverflow.com/questions/53589423/gerrit-rest-api-not-working-when-query-string-contains-hour-minute-second
    getLINK = f"{PLATFORM}/changes/?q=since:{since}+before:{before}"
    return getLINK

        #Only works for 2000 
# --------------------------------------------------------------------------

# ------------------------Changing Settings---------------------------------
def set_Time(date_1="",date_2="",time_1="",time_2="",utc_1=""):  # WIP
    """
    Sets the timeframe, i.e 2022-12-22 06:00:00 -> 2022-12-22 06:15:00
    """
    print(date_1,date_2,time_1,time_2)
    settings = load_settings()
    global settings_dict_start
    #We do this so when a Entry has changed, and then deleted so its empty
    #we can take the standard settings instead.
    if date_2 != "":
        settings["DATE_1"] = date_2
    else:
        settings["DATE_1"] = settings_dict_start["DATE_1"]
    if date_1 != "":
        settings["DATE_2"] = date_1
    else:
        settings["DATE_2"] = settings_dict_start["DATE_2"]
    if time_2 != "":
        settings["SET_TIME_1"] = time_2
    else:
        settings["SET_TIME_1"] = settings_dict_start["SET_TIME_1"]
    if time_1 != "":
        settings["SET_TIME_2"] = time_1
    else:
        settings["SET_TIME_2"] = settings_dict_start["SET_TIME_2"]
    if utc_1 != "":
        settings["UTC"] = utc_1
    else:
        settings["UTC"] = settings_dict_start["UTC"]
        
    print(settings)
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
    return current_settings


def run_GPipe(root, crawl = None):
    settings_dict = load_settings()
    PLATFORM = settings_dict["PLATFORM"]
    DATE_1 = settings_dict["DATE_1"]
    DATE_2 = settings_dict["DATE_2"]
    SET_TIME_1 = settings_dict["SET_TIME_1"]
    SET_TIME_2 = settings_dict["SET_TIME_2"]
    UTC = settings_dict["UTC"]
    
    error = API.Gerrit.requestAPICall(PLATFORM,DATE_1,DATE_2,SET_TIME_1,SET_TIME_2,root,crawl)
    return get_df_str(error)


platform_Options = {0: chromium, 1: opendev, 2: android}


def set_Platform(value=0):
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


if __name__ == "__main__":

    write_settings(settings_dict_start)
    app = GUI.App()
    app.mainloop()
