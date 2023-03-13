"""
GPipe main.py
"""
import json
from datetime import date, datetime, timedelta

import customtkinter
import pandas as pd
from prettytable import PrettyTable

import gpipe_api
import gpipe_gui


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(
    "src/JSON/theme.json"
)
customtkinter.set_widget_scaling(0.95)


# Different platforms
ANDROID = "https://android-review.googlesource.com"
OPENDEV = "https://review.opendev.org"
CHROMIUM = "https://chromium-review.googlesource.com"

# A standard date, which is from when you start the software to - 1 day.
current_date = date.today()
current_date_2 = current_date - timedelta(days=1)
time_1 = datetime.now()
time_2 = time_1
time_1 = time_1.strftime("%H:%M:%S")
time_2 = time_2.strftime("%H:%M:%S")
SETTING_DICT_START = {
    "PLATFORM": CHROMIUM,
    "DATE_1": current_date.strftime("%Y-%m-%d"),
    "DATE_2": current_date_2.strftime("%Y-%m-%d"),
    "SET_TIME_1": time_1,
    "SET_TIME_2": time_2,
    "UTC": "0100",
}

# ------------------------Settings--------------------------------------------
def write_settings(settings):
    """
    Writes the given settings dictionary to a JSON file located at 'src/JSON/settings.json'

    Parameters:
    settings (dict): A dictionary containing settings data to be written to the file.

    Returns:
    None
    """
    file_name = "src/JSON/settings.json"
    with open(file_name, "w", encoding="utf-8") as settings_file:
        json.dump(settings, settings_file, indent=4)


def load_settings():
    """
    Loads settings data from a JSON file located at 'src/JSON/settings.json'

    Returns:
    dict: A dictionary containing the loaded settings data.
    """
    file_name = "src/JSON/settings.json"
    with open(file_name, "r", encoding="utf-8") as settings_file:
        settings_str = settings_file.read()
        settings_dict = json.loads(settings_str)
    return settings_dict


def get_data_frame_str(error):
    """
    Generates a pretty table (as a string) from the data in a JSON file located at 
    'src/JSON/out.json'.

    Parameters:
    error (int): The HTTP error code returned by a server. If this is not equal to 
    200, the function will
    return an error message instead of the table.

    Returns:
    str: The pretty table, along with some additional information about the data.
    """
    with open("src/JSON/out.json", "r", encoding="utf-8") as out_file:
        data = json.load(out_file)
    if error != 200: #We check for errors
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
        #If there is a error, a context string should be attached
        message += ": " + data[0][2:].replace("b'", "").replace("\\n'", "")
        return f"ERROR, Couldn't /crawl, ERROR\nHTTP status code: {error} ({message})"

    # Warning, spaghetti code
    unique_ids = set()
    unique_change = set()
    for item in data:
        unique_ids.add(item["id"])
    for item in data:
        unique_change.add(item["updated"])
    if len(unique_ids) == 0:  # Dont know if this is best method
        return "Error, nothing returned from the search"
    # We just make the data_frame pretty
    new_status = [item for item in data if item["status"] == "NEW"]
    data_frame = pd.DataFrame(data)
    data_frame = data_frame[["owner", "project",
                             "branch", "updated", "insertions", "deletions"]]
    data_frame["owner"] = data_frame["owner"].apply(
        lambda x: x["_account_id"]
    )  # Removes unnecesary lines that makes the data_frame way too long
    data_frame["updated"] = data_frame["updated"].apply(
        lambda x: x.split(".")[0])
    data_frame["project"] = data_frame["project"].str.replace(
        "CHROMIUM", "...")
    data_frame["branch"] = data_frame["branch"].apply(
        lambda x: "/".join(x.split("/")[-2:]) if len(x) > 10 else x
    )

    data_frame["branch"] = data_frame["branch"].apply(
        lambda x: "..." + x if len(x) > 10 else x)
    data_frame["project"] = data_frame["project"].apply(
        lambda x: "..." + x if len(x) > 10 else x)
    data_frame["project"] = data_frame["project"].apply(shorten_path)
    num_unique_owners = data_frame["owner"].nunique()
    table = PrettyTable()
    # Set the column names
    table.field_names = data_frame.columns.tolist()  # This works, i dont know why
    for row in data_frame.itertuples(index=False):
        table.add_row(row)
    num_rows = data_frame.shape[0]
    data_frame = str(table)

    unique_ids = "All Unique IDs found: " + str((num_unique_owners))
    unique_rows = "All changes found: " + str(num_rows)
    new_changes = "All NEW changes: " + str(len(new_status))
    data_frame = unique_rows + "\n" + new_changes + \
        "\n" + unique_ids + "\n" + data_frame
    return data_frame


def shorten_path(path):  # This is truly some chatgpt stuff
    """
    returns a shorter path part of the dataframe
    """
    return "/".join(path.split("/")[-2:])


# ------------------------Changing Settings---------------------------------
def set_time(set_date_1="", set_date_2="", set_time_1="", set_time_2="", utc_1=""):  # WIP
    """
    Sets the timeframe, i.e 2022-12-22 06:00:00 -> 2022-12-22 06:15:00
    """
    print(set_date_1, set_date_2, set_time_1, set_time_2)
    settings = load_settings()
    # We do this so when a Entry has changed, and then deleted so its empty
    # we can take the standard settings instead.
    if set_date_2 != "":
        settings["DATE_1"] = set_date_2
    else:
        settings["DATE_1"] = SETTING_DICT_START["DATE_1"]
    if set_date_1 != "":
        settings["DATE_2"] = set_date_1
    else:
        settings["DATE_2"] = SETTING_DICT_START["DATE_2"]
    if set_time_2 != "":
        settings["SET_TIME_1"] = set_time_2
    else:
        settings["SET_TIME_1"] = SETTING_DICT_START["SET_TIME_1"]
    if set_time_1 != "":
        settings["SET_TIME_2"] = set_time_1
    else:
        settings["SET_TIME_2"] = SETTING_DICT_START["SET_TIME_2"]
    if utc_1 != "":
        settings["UTC"] = utc_1
    else:
        settings["UTC"] = SETTING_DICT_START["UTC"]

    print(settings)
    write_settings(settings)
    return


def quit_gpipe():
    """
    Function is used to quit GPipe
    """

    print("Quitting GPipe...")
    quit()


def update_current_settings():
    """
    Function is used to update the JSON settings file with the settings from the global dict.
    """
    #I truly don't remember if this is different from the set_time function
    settings_dict = load_settings()
    update_platform = settings_dict.get("PLATFORM", "CHROMIUM")
    update_date_2 = settings_dict.get("DATE_2", "")
    update_date_1 = settings_dict.get("DATE_1", "")
    update_time_2 = settings_dict.get("SET_TIME_2", "")
    update_time_1 = settings_dict.get("SET_TIME_1", "")
    current_settings = f"""
Platform: {update_platform}
Time:  {update_date_2} {update_time_2} -> {update_date_1} {update_time_1}
    """
    return current_settings


def run_gpipe(root, crawl=None):
    """
    Function is used to run GPipe, takes in the root and crawl, 
    if user wants to crawl it takes a crawl argument aswell
    """
    settings_dict = load_settings() #We load the current settings
    run_platform = settings_dict["PLATFORM"]
    date_1 = settings_dict["DATE_1"]
    date_2 = settings_dict["DATE_2"]
    set_time_1 = settings_dict["SET_TIME_1"]
    set_time_2 = settings_dict["SET_TIME_2"]
    #We start the requests
    error = gpipe_api.request_api_call(
        run_platform, date_1, date_2, set_time_1, set_time_2, root, crawl
    )
    return get_data_frame_str(error)


platform_Options = {0: CHROMIUM, 1: OPENDEV, 2: ANDROID}

def set_platform(value=0):
    """
    Sets the platform the user wants to use. Only one can be selected.
    """
    #We change the platform by updating the settings.json
    settings = load_settings()
    choice = value
    if choice in platform_Options:
        print(platform_Options[choice])
        settings["PLATFORM"] = platform_Options[choice]
        write_settings(settings)
    else:
        print("ERROR! Platform could not be set.")


if __name__ == "__main__":

    write_settings(SETTING_DICT_START)
    app = gpipe_gui.App()
    app.mainloop()
