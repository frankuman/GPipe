import main  # We're going to use circular dependancy until we fix spaghetti
import os
import GUI
import json
import pyglet
import pandas as pd
import customtkinter
from tkinter import *
from PIL import Image
from prettytable import PrettyTable
from IPython.display import display
from requests.auth import HTTPBasicAuth
import pip._vendor.requests as requests
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime, timedelta


class App(customtkinter.CTk):
    # Set window size
    width = 1600
    height = 800

    def __init__(root):

        """
        Simple and easy menu that loads the function needed to set different things.
        """
        super().__init__()

        root.geometry(f"{root.width}x{root.height}")

        root.grid_columnconfigure((1, 2, 3), weight=1)
        root.grid_rowconfigure((1, 2), weight=2)
        root.grid_rowconfigure((0), weight=1)
        root.attributes('-alpha',0.99)
        root.resizable(False, False)  # Optional, but the UI is made for this size

        root.title("gpipe")
        current_path = os.path.dirname(os.path.realpath(__file__))
        #Load a font :)
        customtkinter.FontManager.load_font(current_path+'/font/Poppins-SemiBold.ttf')

 

        # Platform, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.right_top_frame()

        # Search button - WIP, doesnt do anything right now
        root.entry = customtkinter.CTkEntry(
            root,
            placeholder_text="Enter ID/Project name/Branch",
            height=50,
            corner_radius=24,
            fg_color="white",
            text_color="black",
        )
        root.entry.grid(
            row=3, column=4, columnspan=1, padx=(10, 10), pady=(20, 20), sticky="nsew"
        )

        root.main_button_1 = customtkinter.CTkButton(
            master=root,
            fg_color="transparent",
            border_width=2,
            text="/  Crawl",
            font=customtkinter.CTkFont(size=15, weight="bold", family="Poppins SemiBold"),
            hover_color="#181818",
        )
        root.main_button_1.grid(
            row=3, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        #Settings tab
        #root.date1 = tk
        root.radiobutton_frame_3 = customtkinter.CTkTabview(root, width=150,fg_color="#181818",height=40,border_width=0)
        root.radiobutton_frame_3.grid(row=1, column=4, padx=(10, 10), pady=(10, 0), sticky="nsew")
        root.radiobutton_frame_3.add("Time settings")
        root.radiobutton_frame_3.add("Special settings")
        root.radiobutton_frame_3.add("Other settings")
        root.radiobutton_frame_3.tab("Time settings").grid_columnconfigure(0, weight=0)# configure button of individual tabs
        root.radiobutton_frame_3._segmented_button.grid(padx = 20)  
        for root.button in root.radiobutton_frame_3._segmented_button._buttons_dict.values():# configure button of individual tabs
                root.button.configure(width=150, height=50,font=customtkinter.CTkFont(size=15, weight="bold", family="Poppins SemiBold"),corner_radius=12)
 

        root.date_text_1 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="Time settings",
            font=customtkinter.CTkFont(size=24, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.date_text_1.grid(
            row=1, column=3, columnspan=1, padx=10, pady=(5,1), sticky="nsew"
        )

        root.settings_text_1 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="From",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.settings_text_1.grid(
            row=2, column=3, columnspan=1, padx=10, pady=(10, 1), sticky="nsew"
        )
        
        root.date_entry_1 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=110,
            height=40,
            border_width=0,
            placeholder_text=root.load_start_date(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.date_entry_1.grid(row=3, column=3, padx=10, pady=(5, 1), sticky="nsew")

        root.settings_text_2 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="To",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.settings_text_2.grid(
            row=4, column=3, columnspan=1, padx=(10, 5), pady=1, sticky="nsew"
        )

        root.date_entry_2 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            placeholder_text=root.load_end_date(),
            border_width=0,
            border_color="#3E454A",
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.date_entry_2.grid(row=5, column=3, padx=10, pady=1, sticky="nsew")

        root.time_entry_1 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            border_width=0,
            placeholder_text=root.load_start_time(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.time_entry_1.grid(row=3, column=4, padx=10, pady=(5, 1), sticky="nsew")

        root.time_entry_2 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            border_width=0,
            placeholder_text=root.load_end_time(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.time_entry_2.grid(row=5, column=4, padx=10, pady=(5, 1), sticky="nsew")

        root.settings_text_3 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="Age",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.settings_text_3.grid(
            row=2, column=5, columnspan=1, padx=10, pady=(10, 5), sticky="nsew"
        )
        #Age
        root.age_entry_1 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=110,
            height=40,
            border_width=0,
            placeholder_text="Not needed",
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.age_entry_1.grid(row=3, column=5, padx=10, pady=(5, 1), sticky="nsew")

        root.settings_text_age = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="Timeframe",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.settings_text_age.grid(
            row=4, column=5, columnspan=1, padx=10, pady=(10, 5), sticky="nsew"
        )

        root.optionmenu_1 = customtkinter.CTkOptionMenu(
            master=root.radiobutton_frame_3.tab("Time settings"),
            width=110,
            height=40,
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
            values=["min", "hours", "days","months","years"]
        )
        root.optionmenu_1.grid(row=5, column=5, padx=10, pady=(5, 1), sticky="nsew")


        


        #Special settings
        root.tab_2_text = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Special settings"),
            text="Special settings",
            font=customtkinter.CTkFont(size=24, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.tab_2_text.grid(
            row=1, column=3, columnspan=2, padx=10, pady=(5,1), sticky="nsew"
        )

        root.tab_2_subtext_1 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Special settings"),
            text="From",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.tab_2_subtext_1.grid(
            row=2, column=3, columnspan=1, padx=10, pady=(10, 1), sticky="nsew"
        )

        root.tab_2_settings_1 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=110,
            height=40,
            border_width=0,
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.tab_2_settings_1.grid(row=3, column=3, padx=10, pady=(5, 1), sticky="nsew")

        root.tab_2_subtext_2 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Special settings"),
            text="To",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.tab_2_subtext_2.grid(
            row=4, column=3, columnspan=1, padx=(10, 5), pady=1, sticky="nsew"
        )

        root.tab_2_settings_2 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=90,
            height=40,
            border_width=0,
            border_color="#3E454A",
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.tab_2_settings_2.grid(row=5, column=3, padx=10, pady=1, sticky="nsew")

        root.tab_2_settings_3 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=90,
            height=40,
            border_width=0,
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.tab_2_settings_3.grid(row=3, column=4, padx=10, pady=(5, 1), sticky="nsew")

        root.tab_2_settings_4 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=90,
            height=40,
            border_width=0,
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.tab_2_settings_4.grid(row=5, column=4, padx=10, pady=(5, 1), sticky="nsew")

        root.tab_2_settings_5 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Special settings"),
            text="Age",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.tab_2_settings_5.grid(
            row=2, column=5, columnspan=1, padx=10, pady=(10, 5), sticky="nsew"
        )

        root.tab_2_settings_6 = customtkinter.CTkEntry(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=110,
            height=40,
            border_width=0,
            placeholder_text="Not needed",
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        root.tab_2_settings_6.grid(row=3, column=5, padx=10, pady=(5, 1), sticky="nsew")

        root.tab_2_settings_7 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Special settings"),
            text="Timeframe",
            font=customtkinter.CTkFont(size=18, weight="bold", family="Poppins SemiBold"),
            anchor="w",
        )
        root.tab_2_settings_7.grid(
            row=4, column=5, columnspan=1, padx=10, pady=(10, 5), sticky="nsew"
        )

        root.optionmenu_2 = customtkinter.CTkOptionMenu(
            master=root.radiobutton_frame_3.tab("Special settings"),
            width=110,
            height=40,
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
            values=["min", "hours", "days","months","years"]
        )
        root.optionmenu_2.grid(row=5, column=5, padx=10, pady=(5, 1), sticky="nsew")
 

        # check - WIP
        root.checkbox_slider_frame = customtkinter.CTkFrame(root)
        root.checkbox_slider_frame.grid(
            row=1, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )

        root.checkbox_slider_group_2 = customtkinter.CTkLabel(
            master=root.checkbox_slider_frame, text="is:", anchor="n",font=customtkinter.CTkFont(size=16, weight="bold", family="Poppins SemiBold")
        )
        root.checkbox_slider_group_2.grid(row=0, column=0, padx=5, pady=5, sticky="")

        root.checkbox_1 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="open"
        )
        root.checkbox_1.grid(row=1, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_2 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="watched"
        )
        root.checkbox_2.grid(row=2, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_3 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="unassigned"
        )
        root.checkbox_3.grid(row=3, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_4 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="reviewed"
        )
        root.checkbox_4.grid(row=4, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_4 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="closed"
        )
        root.checkbox_4.grid(row=5, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_4 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="merged"
        )
        root.checkbox_4.grid(row=6, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_4 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="pending"
        )
        root.checkbox_4.grid(row=7, column=0, pady=(5, 5), padx=20, sticky="n")

        # create textbox
        root.textbox = customtkinter.CTkTextbox(
            root,
            width=1100,
            corner_radius=8,
            border_width=2,
        )

        root.textbox.grid(row=0, column=3,columnspan=2, padx=(0, 10), pady=(20, 0), sticky="nsew")
  

        # create sidebox next to textbox
        root.radiobutton_frame_2 = customtkinter.CTkFrame(root, corner_radius=8)
        root.radiobutton_frame_2.grid(
            row=0, column=1, padx=(10,10), pady=(20, 0), sticky="nsew"
        )
        root.radiobutton_frame_3 = customtkinter.CTkFrame(root, corner_radius=8)
        root.radiobutton_frame_3.grid(
            row=1, column=3, padx=(10, 10), pady=(20, 0), sticky="nsew"
        )
        
        

        # Sidebar, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.logo_image = customtkinter.CTkImage(
            Image.open(current_path + "/images/gpipe.png"), size=(140, 50)
        )

        root.sidebar_frame = customtkinter.CTkFrame(
            root, width=140, corner_radius=0, fg_color="#000000"
        )
        root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        root.sidebar_frame.grid_rowconfigure(4, weight=1)
        root.logo_image_label = customtkinter.CTkLabel(
            root.sidebar_frame,
            image=root.logo_image,
            text="",
            height=0,
            fg_color="#000000",
        )
        root.logo_image_label.grid(row=0, column=0, sticky="n", padx=10, pady=(10, 0))
    
        root.run_button = customtkinter.CTkButton(
            root.sidebar_frame,
            height=50,
            text="/      Run",
            anchor="w",
            command=root.run_GPipe_event,
            font=customtkinter.CTkFont(size=20, weight="bold", family="Poppins SemiBold"),
        )
        root.run_button.grid(row=1, column=0, padx=0, pady=10)

        root.quit_button = customtkinter.CTkButton(
            root.sidebar_frame,
            height=50,
            anchor="w",
            text="/      Quit",
            command=main.quit_GPipe,
            font=customtkinter.CTkFont(size=20, weight="bold", family="Poppins SemiBold"),
        )
        root.quit_button.grid(row=5, column=0, padx=0, pady=(20, 20))
    def right_top_frame(root):
        root.radiobutton_frame = customtkinter.CTkFrame(root)

        root.radiobutton_frame.grid(
            row=0, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        root.radio_var = IntVar(value=0)
        root.label_radio_group = customtkinter.CTkLabel(
            master=root.radiobutton_frame, text="Platform:",font=customtkinter.CTkFont(size=16, weight="bold", family="Poppins SemiBold")
        )
        root.label_radio_group.grid(
            row=0, column=4, columnspan=1, padx=10, pady=(5, 5), sticky="nsew"
        )
        root.radio_button_1 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var,
            value=0,
            text="Chromium",
        )
        root.radio_button_1.grid(row=1, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_2 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var,
            value=1,
            text="OpenDEV",
        )
        root.radio_button_2.grid(row=2, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_3 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var,
            value=2,
            text="Android",
        )
        root.radio_button_3.grid(row=3, column=4, pady=10, padx=20, sticky="n")
        # More radio buttons, doesnt do anything rn

        root.radio_var_2 = IntVar(value=0)

        root.label_radio_group_2 = customtkinter.CTkLabel(
            master=root.radiobutton_frame, text="Chungite:",
            font=customtkinter.CTkFont(size=16, weight="bold", family="Poppins SemiBold")
        )
        root.label_radio_group_2.grid(
            row=4, column=4, columnspan=1, padx=10, pady=10, sticky=""
        )
        root.radio_button_4 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var_2,
            value=0,
            text="Yes",
        )
        root.radio_button_4.grid(row=5, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_5 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var_2,
            value=1,
            text="Tomorrow",
        )
        root.radio_button_5.grid(row=6, column=4, pady=10, padx=20, sticky="n")
        root.radio_button_6 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame,
            variable=root.radio_var_2,
            value=2,
            text="Ooga",
        )
        root.radio_button_6.grid(row=7, column=4, pady=10, padx=20, sticky="n")
    def run_GPipe_event(root):
        platform = root.radio_var.get()

        main.set_Platform(platform)
        st = root.date_entry_1.get()
        print("hello?"+st)

        main.set_Time(root.date_entry_1.get(),root.date_entry_2.get(),root.time_entry_1.get(),root.time_entry_2.get())

        df = main.run_GPipe()
        print(df)
        settings = main.update_current_settings()
        # Credit to help at https://stackoverflow.com/questions/75295073/tkinter-textbox-does-not-look-the-same-as-terminal-print/75295357?noredirect=1#comment132864739_75295357
        root.textbox.configure(
            font=("Consolas", 14)
        )  # Only works with consolas, no matter
        root.textbox.delete("0.0",END)
        root.textbox.insert("0.0", settings + "\n" + df + "\n\n")

    def load_start_date(root):

        settings_dict = main.load_settings()
        date_2 = settings_dict["DATE_2"]
        return date_2

    def load_end_date(root):

        settings_dict = main.load_settings()
        date_1 = settings_dict["DATE_1"]

        return date_1

    def load_start_time(root):

        settings_dict = main.load_settings()
        time_2 = settings_dict["SET_TIME_2"]
        return time_2

    def load_end_time(root):

        settings_dict = main.load_settings()
        time_1 = settings_dict["SET_TIME_1"]
        return time_1
