import json
import os
import threading
from tkinter import *

import customtkinter
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
from PIL import Image

import main  # We're going to use circular dependancy until we fix spaghetti

welcome = """ __          __  _                            _           _____ _____ _            
 \ \        / / | |                          | |         / ____|  __ (_)           
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |  __| |__) | _ __   ___ 
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | | |_ |  ___/ | '_ \ / _ \\
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |__| | |   | | |_) |  __/
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____|_|   |_| .__/ \___|
                                                                       | |         
                                                                       |_|"""
text = """
GPipe is a Gerrit Analysis Pipeline
GPipe was made by Oliver Bölin during a university course at Blekinge Tekniska University (BTH)
Usage:
(Warning!) Searching all users for about a month timeframe takes around 5 minutes, so try to filter your search!
Since this was made within 3 months it is prone to crashing if abused (◕‿-)

Time settings - Here you can set the time for your search, default is current time-1 day
Graph settings - Here you can choose the X-axis and if you want to popout pyplot
Generate graph - If you have made a run you can now generate a graph on that data, you can also change the x-axis in graph settings
Generate PDF - If you have made a run you can now generate a PDF on that data, you can also change the x-axis in graph settings
Generate EXCEL - If you have made a run you can now generate an EXCEL on that data
Platform picker - Here you choose one of the platforms. I have not added authentication but it could probably be done easily, chromium and android is a bit slower than OpenDEV
is: - Choose a metric, or none, if none it searches all changes.
/ Crawl - Input a username or similar stuff and crawl by that
/ Run - Run GPipe with current settings
/ Quit - Quit GPipe"""


class App(customtkinter.CTk):
    """GUI

    Args:
        customtkinter
    """    
    # Set window size
    width = 1600
    height = 800

    def __init__(root):
        """        Simple and easy menu that loads the function needed to set different things.

        Args:
            root
        """
        
        super().__init__()

        root.geometry(f"{root.width}x{root.height}")

        root.grid_columnconfigure((1, 2, 3), weight=1)
        root.grid_rowconfigure((1, 2), weight=2)
        root.grid_rowconfigure((0), weight=1)
        root.attributes("-alpha", 1)
        root.resizable(False, False)  # Optional, but the UI is made for this size

        root.title("gpipe")
        root.current_path = os.path.dirname(os.path.realpath(__file__))
        # Load a font :)
        customtkinter.FontManager.load_font(
            root.current_path + "/assets/font/Poppins-SemiBold.ttf"
        )

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
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
            hover_color="#181818",
            command=root.run_Crawl_event,
        )
        root.main_button_1.grid(
            row=3, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        # Settings tab
        # root.date1 = tk
        root.radiobutton_frame_3 = customtkinter.CTkTabview(
            root, width=150, fg_color="#171717", height=40, border_width=0
        )
        root.radiobutton_frame_3.grid(
            row=1, column=4, padx=(10, 10), pady=(10, 0), sticky="nsew"
        )
        root.radiobutton_frame_3.add("Time settings")
        root.radiobutton_frame_3.add("Graph settings")
        root.radiobutton_frame_3.tab("Time settings").grid_columnconfigure(
            0, weight=0
        )  # configure button of individual tabs
        root.radiobutton_frame_3._segmented_button.grid(padx=20)
        for (
            root.button
        ) in (
            root.radiobutton_frame_3._segmented_button._buttons_dict.values()
        ):  # configure button of individual tabs
            root.button.configure(
                width=150,
                height=50,
                font=customtkinter.CTkFont(
                    size=15, weight="bold", family="Poppins SemiBold"
                ),
                corner_radius=12,
            )

        root.date_text_1 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="Time settings",
            font=customtkinter.CTkFont(
                size=24, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        root.date_text_1.grid(
            row=1, column=3, columnspan=1, padx=10, pady=(5, 1), sticky="nsew"
        )

        root.settings_text_1 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Time settings"),
            text="From",
            font=customtkinter.CTkFont(
                size=18, weight="bold", family="Poppins SemiBold"
            ),
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
            font=customtkinter.CTkFont(
                size=18, weight="bold", family="Poppins SemiBold"
            ),
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

        # Graph settings
        ##Popout
        root.tab_2_text = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            text="Graph settings",
            font=customtkinter.CTkFont(
                size=24, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        root.tab_2_text.grid(
            row=1, column=1, columnspan=2, padx=5, pady=(5, 1), sticky="nsew"
        )
        root.popout = IntVar(value=0)
        root.label_radio_group_2 = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            text="Popout PyPlot?",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.label_radio_group_2.grid(
            row=2, column=1, columnspan=1, padx=(5, 1), pady=10, sticky="n"
        )
        root.radio_button_4 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.popout,
            value=0,
            text="No",
        )
        root.radio_button_4.grid(row=3, column=1, pady=5, padx=(5, 1), sticky="n")
        root.radio_button_5 = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.popout,
            value=1,
            text="Yes",
        )
        root.radio_button_5.grid(row=4, column=1, pady=5, padx=(5, 1), sticky="n")
        ##Dayweekmonth
        root.sortby_label = customtkinter.CTkLabel(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            text="X-axis",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.sortby_label.grid(
            row=2, column=2, columnspan=1, padx=(10, 1), pady=10, sticky="n"
        )
        root.time = IntVar(value=0)
        root.hour_radio_button = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.time,
            value=0,
            text="Hour",
        )
        root.hour_radio_button.grid(row=3, column=2, pady=5, padx=(35, 1), sticky="n")

        root.day_radio_button = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.time,
            value=1,
            text="Day",
        )
        root.day_radio_button.grid(row=4, column=2, pady=5, padx=(35, 1), sticky="n")

        root.week_radio_button = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.time,
            value=2,
            text="Week",
        )
        root.week_radio_button.grid(row=5, column=2, pady=5, padx=(35, 1), sticky="n")
        root.month_radio_button = customtkinter.CTkRadioButton(
            master=root.radiobutton_frame_3.tab("Graph settings"),
            variable=root.time,
            value=3,
            text="Month",
        )
        root.month_radio_button.grid(row=6, column=2, pady=5, padx=(35, 1), sticky="n")
        # check - WIP
        root.checkbox_slider_frame = customtkinter.CTkFrame(root)
        root.checkbox_slider_frame.grid(
            row=1, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )

        root.checkbox_slider_group_2 = customtkinter.CTkLabel(
            master=root.checkbox_slider_frame,
            text="is:",
            anchor="n",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.checkbox_slider_group_2.grid(row=0, column=0, padx=5, pady=5, sticky="")
        root.open_v = IntVar(value=0)
        root.watched_v = IntVar(value=0)
        root.unassigned_v = IntVar(value=0)
        root.reviewed_v = IntVar(value=0)
        root.closed_v = IntVar(value=0)
        root.merged_v = IntVar(value=0)
        root.pending_v = IntVar(value=0)
        root.abandoned_v = IntVar(value=0)
        root.checkbox_1 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="open", variable=root.open_v
        )
        root.checkbox_1.grid(row=1, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_2 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="watched", variable=root.watched_v
        )
        root.checkbox_2.grid(row=2, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_3 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame,
            text="unassigned",
            variable=root.unassigned_v,
        )
        root.checkbox_3.grid(row=3, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_4 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="reviewed", variable=root.reviewed_v
        )
        root.checkbox_4.grid(row=4, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_5 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="closed", variable=root.closed_v
        )
        root.checkbox_5.grid(row=5, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_6 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="merged", variable=root.merged_v
        )
        root.checkbox_6.grid(row=6, column=0, pady=(5, 5), padx=20, sticky="n")

        root.checkbox_7 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame, text="pending", variable=root.pending_v
        )
        root.checkbox_7.grid(row=7, column=0, pady=(5, 5), padx=20, sticky="n")
        root.checkbox_8 = customtkinter.CTkCheckBox(
            master=root.checkbox_slider_frame,
            text="abandonded",
            variable=root.abandoned_v,
        )
        root.checkbox_8.grid(row=8, column=0, pady=(5, 5), padx=20, sticky="n")
        # create textbox
        root.textbox = customtkinter.CTkTextbox(
            root,
            width=1100,
            corner_radius=8,
            border_width=2,
        )

        root.textbox.grid(
            row=0, column=1, columnspan=4, padx=(10, 10), pady=(20, 0), sticky="nsew"
        )
        root.textbox.configure(
            font=("Consolas", 13)
        )  # Only works with consolas, no matter

        # Credit to help at https://stackoverflow.com/questions/75295073/tkinter-textbox-does-not-look-the-same-as-terminal-print/75295357?noredirect=1#comment132864739_75295357

        root.textbox.delete("0.0", END)
        root.textbox.insert("0.0", welcome + "\n" + text + "\n")
        # create graphbox

        root.graph_frame = customtkinter.CTkFrame(
            root, width=700, corner_radius=8, fg_color="#121212", border_width=0
        )
        root.graph_frame.grid(
            row=1,
            column=2,
            columnspan=1,
            rowspan=3,
            padx=(10, 5),
            pady=(20, 0),
            sticky="nsew",
        )
        root.graph_label = customtkinter.CTkLabel(
            root.graph_frame, text="", width=700, height=400
        )
        root.graph_label.grid(sticky="n", pady=(0, 40), padx=(10, 0))
        root.graph_button_frame = customtkinter.CTkFrame(
            root, width=100, corner_radius=8, fg_color="#181818", border_width=0
        )
        root.graph_button_frame.grid(
            row=1, column=1, rowspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        root.Generation = customtkinter.CTkLabel(
            root.graph_button_frame,
            text="Generate",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
            anchor="center",
        )
        root.Generation.grid(row=0, column=0, padx=(25, 0), pady=(5, 1), sticky="n")
        root.graph_button = customtkinter.CTkButton(
            root.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=root.graph_button_frame._current_width,
            text="Graph",
            hover_color="#121212",
            command=root.run_Graph_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.graph_button.grid(row=2, column=0, padx=(30, 0), pady=10, sticky="n")
        root.pdf_button = customtkinter.CTkButton(
            root.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=root.graph_button_frame._current_width,
            text="PDF",
            hover_color="#121212",
            command=root.run_PDF_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.pdf_button.grid(row=3, column=0, padx=(30, 0), pady=10, sticky="n")
        root.XCEL_button = customtkinter.CTkButton(
            root.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=root.graph_button_frame._current_width,
            text="EXCEL",
            hover_color="#121212",
            command=root.run_EXCEL_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.XCEL_button.grid(row=4, column=0, padx=(30, 0), pady=10, sticky="n")
        # Sidebar, https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
        root.logo_image = customtkinter.CTkImage(
            Image.open(root.current_path + "/assets/images/gpipe.png"), size=(140, 50)
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
            font=customtkinter.CTkFont(
                size=20, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.run_button.grid(row=1, column=0, padx=0, pady=10)

        root.quit_button = customtkinter.CTkButton(
            root.sidebar_frame,
            height=50,
            anchor="w",
            text="/      Quit",
            command=root.quit_gpipe_event,
            font=customtkinter.CTkFont(
                size=20, weight="bold", family="Poppins SemiBold"
            ),
        )
        root.quit_button.grid(row=5, column=0, padx=0, pady=(20, 20))

    def right_top_frame(root):
        """right top frame

        Args:
            root
        """        
        root.radiobutton_frame = customtkinter.CTkFrame(root)

        root.radiobutton_frame.grid(
            row=0, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        root.radio_var = IntVar(value=0)
        root.label_radio_group = customtkinter.CTkLabel(
            master=root.radiobutton_frame,
            text="Platform:",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
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
            master=root.radiobutton_frame,
            text="Chungite:",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
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

    def run_GPipe_event(root, crawl=None):
        """Threading is used within this event
        to create faster running time and no crashing for the GUI

        Args:
            root
            crawl: Defaults to None.
        """        
       
        platform = root.radio_var.get()

        main.set_Platform(platform)

        main.set_Time(
            root.date_entry_1.get(),
            root.date_entry_2.get(),
            root.time_entry_1.get(),
            root.time_entry_2.get(),
        )
        if crawl == None:
            x = threading.Thread(target=root.thread_start)
        else:
            x = threading.Thread(target=root.thread_start(crawl=crawl))
        x.setDaemon(
            True
        )  # We create a Daemon so when we quit all other threads this one also
        # quits. Meaning quit_gpipe_event still works
        x.start()

        root.textbox.configure(
            font=("Consolas", 15),
        )

        if x.is_alive() == True:

            root.textbox.delete("0.0", END)
            root.textbox.insert(
                "0.0", "GPipe is loading... \nYou should probably grab a coffee\n"
            )

    def thread_start(root, crawl=None):
        """starts the thread

        Args:
            root
            crawl Defaults to None.
        """
        if crawl == None:
            root.df = main.run_GPipe(root)
        else:
            root.df = main.run_GPipe(root, crawl)

        root.textbox.configure(
            font=("Consolas", 13)
        )  # Only works with consolas, no matter
        print(root.df)
        settings = main.update_current_settings()
        # Credit to help at https://stackoverflow.com/questions/75295073/tkinter-textbox-does-not-look-the-same-as-terminal-print/75295357?noredirect=1#comment132864739_75295357

        root.textbox.delete("0.0", END)
        root.textbox.insert("0.0", settings + "\n" + root.df + "\n\n")

    def quit_gpipe_event(root):
        """quits gpipe as a event

        Args:
            root
        """        
        main.quit_GPipe()

    def run_Graph_event(root):
        """starts gpipe as a event

        Args:
            root
        """        
        root.graph_data(root.time.get(), root.popout.get())
        root.load_graph()

    def run_Crawl_event(root):
        """runs the search engine

        Args:
            root
        """        
        root.run_GPipe_event(crawl=root.entry.get())

    def graph_data(root, time=0, popout=0):
        """Reads a JSON file and converts it to a Pandas dataframe.
        It then groups the data based on a specified time interval and generates
        a bar chart using Matplotlib:

        Args:
            root _
            time (int, optional): Defaults to 0.
            popout (int, optional): Defaults to 0.
        """        
        
        with open("src/JSON/out.json", "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df = df[["updated"]]
        df["updated"] = df["updated"].apply(lambda x: x.split(".")[0])
        df["updated"] = pd.to_datetime(df["updated"])
        plt.style.use("dark_background")

        if time == 0:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1H")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Hour")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Hour")
            plt.savefig(
                "generations/plot.jpg", bbox_inches="tight", facecolor="#121212", dpi=150
            )
        elif time == 1:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1D")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Day")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Day")
            plt.savefig(
                "generations/plot.jpg", facecolor="#121212", bbox_inches="tight", dpi=150
            )
        elif time == 2:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1W")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Week")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Week")
            plt.savefig(
                "generations/plot.jpg", facecolor="#121212", bbox_inches="tight", dpi=150
            )
        elif time == 3:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1M")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Month")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Month")
            plt.savefig(
                "generations/plot.jpg", facecolor="#121212", bbox_inches="tight", dpi=150
            )
        if popout == 1:
            plt.ion()
            plt.show()
        root.textbox.insert(
            "0.0", "PNG generated at " + root.current_path + "/generations\n"
        )

    def run_EXCEL_event(root):
        """generates a excel of the dataframe

        Args:
            root
        """        
        with open("src/JSON/out.json", "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        # We just make the df pretty

        df = df[["owner", "project", "branch", "updated", "insertions", "deletions"]]
        df["owner"] = df["owner"].apply(
            lambda x: x["_account_id"]
        )  # Removes unnecesary lines that makes the df way too long
        df["updated"] = df["updated"].apply(lambda x: x.split(".")[0])
        df["project"] = df["project"].str.replace("chromium", "...")
        df["branch"] = df["branch"].apply(
            lambda x: "/".join(x.split("/")[-2:]) if len(x) > 10 else x
        )
        df["branch"] = df["branch"].apply(lambda x: "..." + x if len(x) > 10 else x)
        df["project"] = df["project"].apply(lambda x: "..." + x if len(x) > 10 else x)
        df.to_excel(excel_writer="generations/excelGPipe.xlsx", sheet_name="excelGPipe")
        root.textbox.insert(
            "0.0", "Excel generated at " + root.current_path + "/generations\n"
        )

    def run_PDF_event(root):
        """generates a PDF of the graph

        Args:
            root
        """        
        time = root.time.get()
        with open("src/JSON/out.json", "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df = df[["updated"]]
        df["updated"] = df["updated"].apply(lambda x: x.split(".")[0])
        # df["updated"] = df["updated"].apply(lambda x: x.split(":")[0] + ":" + x.split(":")[1])
        # print(df)
        df["updated"] = pd.to_datetime(df["updated"])
        plt.style.use("dark_background")

        if time == 0:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1H")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Hour")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Hour")
            plt.savefig(
                "generations/plotPDF.pdf", facecolor="black", bbox_inches="tight", dpi=150
            )
        elif time == 1:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1D")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Day")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Day")
            plt.savefig(
                "generations/plotPDF.pdf", facecolor="black", bbox_inches="tight", dpi=150
            )
        elif time == 2:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1W")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Week")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Week")
            plt.savefig(
                "generations/plotPDF.pdf", facecolor="black", bbox_inches="tight", dpi=150
            )
        elif time == 3:
            hourly_count = df.groupby(pd.Grouper(key="updated", freq="1M")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Month")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Month")
            plt.savefig(
                "generations/plotPDF.pdf", facecolor="black", bbox_inches="tight", dpi=150
            )

        root.textbox.insert(
            "0.0", "PDF generated at " + root.current_path + "/generations\n"
        )

    def load_start_date(root):
        """loads the start date

        Args:
            root

        Returns:
            string
        """
        settings_dict = main.load_settings()
        date_2 = settings_dict["DATE_2"]
        return date_2

    def load_end_date(root):
        """loads the end date

        Args:
            root

        Returns:
            string
        """
        settings_dict = main.load_settings()
        date_1 = settings_dict["DATE_1"]

        return date_1

    def load_graph(root):
        """loads the image of the graph

        Args:
            root
        """
        root.plot_image = customtkinter.CTkImage(
            Image.open(root.current_path + "/generations/plot.jpg"), size=(650, 400)
        )
        root.graph_label.configure(image=root.plot_image, anchor=CENTER)

    def load_start_time(root):
        """loads the start time

        Args:
            root

        Returns:
            string
        """
        settings_dict = main.load_settings()
        time_2 = settings_dict["SET_TIME_2"]
        return time_2

    def load_end_time(root):
        """loads the end time

        Args:
            root

        Returns:
            string
        """
        settings_dict = main.load_settings()
        time_1 = settings_dict["SET_TIME_1"]
        return time_1

    # Doesnt work yet, shouldn't be implemented now
