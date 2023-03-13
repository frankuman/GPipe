"""
GPipe GUI.py
"""
import json
import os
import threading
from tkinter import (CENTER, END,  # This is recommended, pylance shouldn't
                     IntVar)

import customtkinter
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

import gpipe_main  # We're going to use circular dependancy until we fix spaghetti

#give warning here, see https://docs.python.org/3/library/tkinter.html




WELCOME_TEXT = r""" __          __  _                            _           _____ _____ _
 \ \        / / | |                          | |         / ____|  __ (_)
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |  __| |__) | _ __   ___
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | | |_ |  ___/ | '_ \ / _ \
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |__| | |   | | |_) |  __/
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____|_|   |_| .__/ \___|
                                                                       | |
                                                                       |_|"""
INTRO_TEXT = """
GPipe is a Gerrit Analysis Pipeline
GPipe was made by Oliver Bölin during a university course at Blekinge Tekniska University (BTH)
Usage:
(Warning!) Searching all users for about a month timeframe takes around 5 minutes, so try to filter your search!
Since this was made within 3 months it is prone to crashing if abused (◕‿-)

Time settings - Here you can set the time for your search, default is current time-1 day
Graph settings - Here you can choose the X-axis and if you want to popout pyplot
Generate graph - If you have made a run you can now generate a graph on that data, you can also change the x-axis in graph settings
Generate PDF - If you have made a run you can now generate a PDF on that data, you can also change the x-axis in graph settings
Generate Eexcel - If you have made a run you can now generate an Eexcel on that data
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

    def __init__(self):
        """Simple and easy menu that loads the function needed to set different things.

        Args:
            self
        """

        super().__init__()

        self.geometry(f"{self.width}x{self.height}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.attributes("-alpha", 1)
        # Optional, but the UI is made for this size
        self.resizable(False, False)
        self.data_frame = ""
        self.plot_image = ""
        self.title("gpipe")
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        # Load a font :)
        customtkinter.FontManager.load_font("assets/font/Poppins-SemiBold.ttf")
        self.iconbitmap("assets/images/favicon.ico")

        self.right_top_frame()
        # Search button - WIP, doesnt do anything right now
        self.entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Enter ID/Project name/Branch",
            height=50,
            corner_radius=24,
            fg_color="white",
            text_color="black",
        )
        self.entry.grid(
            row=3, column=4, columnspan=1, padx=(10, 10), pady=(20, 20), sticky="nsew"
        )

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text="/  Crawl",
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
            hover_color="#181818",
            command=self.run_crawl_event,
        )
        self.main_button_1.grid(
            row=3, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        # Settings tab

        self.radiobutton_frame_3 = customtkinter.CTkTabview(
            self, width=150, fg_color="#171717", height=40, border_width=0
        )
        self.radiobutton_frame_3.grid(
            row=1, column=4, padx=(10, 10), pady=(10, 0), sticky="nsew"
        )
        self.radiobutton_frame_3.add("Time settings")
        self.radiobutton_frame_3.add("Graph settings")
        self.radiobutton_frame_3.tab("Time settings").grid_columnconfigure(
            0, weight=0
        )  # configure button of individual tabs
        self.radiobutton_frame_3._segmented_button.grid(padx=20)
        for (
            self.button
        ) in (
            self.radiobutton_frame_3._segmented_button._buttons_dict.values()
        ):  # configure button of individual tabs
            self.button.configure(
                width=150,
                height=50,
                font=customtkinter.CTkFont(
                    size=15, weight="bold", family="Poppins SemiBold"
                ),
                corner_radius=12,
            )

        self.date_text_1 = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Time settings"),
            text="Time settings",
            font=customtkinter.CTkFont(
                size=24, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        self.date_text_1.grid(
            row=1, column=3, columnspan=1, padx=10, pady=(5, 1), sticky="nsew"
        )

        self.settings_text_1 = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Time settings"),
            text="From",
            font=customtkinter.CTkFont(
                size=18, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        self.settings_text_1.grid(
            row=2, column=3, columnspan=1, padx=10, pady=(10, 1), sticky="nsew"
        )

        self.date_entry_1 = customtkinter.CTkEntry(
            master=self.radiobutton_frame_3.tab("Time settings"),
            width=110,
            height=40,
            border_width=0,
            placeholder_text=self.load_start_date(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        self.date_entry_1.grid(row=3, column=3, padx=10, pady=(5, 1), sticky="nsew")

        self.settings_text_2 = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Time settings"),
            text="To",
            font=customtkinter.CTkFont(
                size=18, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        self.settings_text_2.grid(
            row=4, column=3, columnspan=1, padx=(10, 5), pady=1, sticky="nsew"
        )

        self.date_entry_2 = customtkinter.CTkEntry(
            master=self.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            placeholder_text=self.load_end_date(),
            border_width=0,
            border_color="#3E454A",
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        self.date_entry_2.grid(row=5, column=3, padx=10, pady=1, sticky="nsew")

        self.time_entry_1 = customtkinter.CTkEntry(
            master=self.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            border_width=0,
            placeholder_text=self.load_start_time(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        self.time_entry_1.grid(row=3, column=4, padx=10, pady=(5, 1), sticky="nsew")

        self.time_entry_2 = customtkinter.CTkEntry(
            master=self.radiobutton_frame_3.tab("Time settings"),
            width=90,
            height=40,
            border_width=0,
            placeholder_text=self.load_end_time(),
            font=customtkinter.CTkFont(weight="bold", family="Poppins SemiBold"),
        )
        self.time_entry_2.grid(row=5, column=4, padx=10, pady=(5, 1), sticky="nsew")

        # Graph settings
        # Popout
        self.tab_2_text = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            text="Graph settings",
            font=customtkinter.CTkFont(
                size=24, weight="bold", family="Poppins SemiBold"
            ),
            anchor="w",
        )
        self.tab_2_text.grid(
            row=1, column=1, columnspan=2, padx=5, pady=(5, 1), sticky="nsew"
        )
        self.popout = IntVar(value=0)
        self.label_radio_group_2 = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            text="Popout PyPlot?",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.label_radio_group_2.grid(
            row=2, column=1, columnspan=1, padx=(5, 1), pady=10, sticky="n"
        )
        self.radio_button_4 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.popout,
            value=0,
            text="No",
        )
        self.radio_button_4.grid(row=3, column=1, pady=5, padx=(5, 1), sticky="n")
        self.radio_button_5 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.popout,
            value=1,
            text="Yes",
        )
        self.radio_button_5.grid(row=4, column=1, pady=5, padx=(5, 1), sticky="n")

        self.sortby_label = customtkinter.CTkLabel(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            text="X-axis",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.sortby_label.grid(
            row=2, column=2, columnspan=1, padx=(10, 1), pady=10, sticky="n"
        )
        self.time = IntVar(value=0)
        self.hour_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.time,
            value=0,
            text="Hour",
        )
        self.hour_radio_button.grid(row=3, column=2, pady=5, padx=(35, 1), sticky="n")

        self.day_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.time,
            value=1,
            text="Day",
        )
        self.day_radio_button.grid(row=4, column=2, pady=5, padx=(35, 1), sticky="n")

        self.week_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.time,
            value=2,
            text="Week",
        )
        self.week_radio_button.grid(row=5, column=2, pady=5, padx=(35, 1), sticky="n")
        self.month_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame_3.tab("Graph settings"),
            variable=self.time,
            value=3,
            text="Month",
        )
        self.month_radio_button.grid(row=6, column=2, pady=5, padx=(35, 1), sticky="n")
        # check
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(
            row=1, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )

        self.checkbox_slider_group_2 = customtkinter.CTkLabel(
            master=self.checkbox_slider_frame,
            text="is:",
            anchor="n",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.checkbox_slider_group_2.grid(row=0, column=0, padx=5, pady=5, sticky="")
        self.open_v = IntVar(value=0)
        self.watched_v = IntVar(value=0)
        self.unassigned_v = IntVar(value=0)
        self.reviewed_v = IntVar(value=0)
        self.closed_v = IntVar(value=0)
        self.merged_v = IntVar(value=0)
        self.pending_v = IntVar(value=0)
        self.abandoned_v = IntVar(value=0)
        self.checkbox_1 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="open", variable=self.open_v
        )
        self.checkbox_1.grid(row=1, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_2 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="watched", variable=self.watched_v
        )
        self.checkbox_2.grid(row=2, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_3 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame,
            text="unassigned",
            variable=self.unassigned_v,
        )
        self.checkbox_3.grid(row=3, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_4 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="reviewed", variable=self.reviewed_v
        )
        self.checkbox_4.grid(row=4, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_5 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="closed", variable=self.closed_v
        )
        self.checkbox_5.grid(row=5, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_6 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="merged", variable=self.merged_v
        )
        self.checkbox_6.grid(row=6, column=0, pady=(5, 5), padx=20, sticky="n")

        self.checkbox_7 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="pending", variable=self.pending_v
        )
        self.checkbox_7.grid(row=7, column=0, pady=(5, 5), padx=20, sticky="n")
        self.checkbox_8 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame,
            text="abandonded",
            variable=self.abandoned_v,
        )
        self.checkbox_8.grid(row=8, column=0, pady=(5, 5), padx=20, sticky="n")
        # create textbox
        self.textbox = customtkinter.CTkTextbox(
            self,
            width=1100,
            corner_radius=8,
            border_width=2,
        )

        self.textbox.grid(
            row=0, column=1, columnspan=4, padx=(10, 10), pady=(20, 0), sticky="nsew"
        )
        self.textbox.configure(
            font=("Consolas", 13)
        )  # Only works with consolas

        self.textbox.delete("0.0", END)
        self.textbox.insert("0.0", WELCOME_TEXT + "\n" + INTRO_TEXT + "\n")
        # create graphbox

        self.graph_frame = customtkinter.CTkFrame(
            self, width=700, corner_radius=8, fg_color="#121212", border_width=0
        )
        self.graph_frame.grid(
            row=1,
            column=2,
            columnspan=1,
            rowspan=3,
            padx=(10, 5),
            pady=(20, 0),
            sticky="nsew",
        )
        self.graph_label = customtkinter.CTkLabel(
            self.graph_frame, text="", width=700, height=400
        )
        self.graph_label.grid(sticky="n", pady=(0, 40), padx=(10, 0))
        self.graph_button_frame = customtkinter.CTkFrame(
            self, width=100, corner_radius=8, fg_color="#181818", border_width=0
        )
        self.graph_button_frame.grid(
            row=1, column=1, rowspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        self.generation = customtkinter.CTkLabel(
            self.graph_button_frame,
            text="Generate",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
            anchor="center",
        )
        self.generation.grid(row=0, column=0, padx=(25, 0), pady=(5, 1), sticky="n")
        self.graph_button = customtkinter.CTkButton(
            self.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=int(self.graph_button_frame._current_width),
            text="Graph",
            hover_color="#121212",
            command=self.run_graph_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.graph_button.grid(row=2, column=0, padx=(30, 0), pady=10, sticky="n")
        self.pdf_button = customtkinter.CTkButton(
            self.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=int(self.graph_button_frame._current_width),
            text="PDF",
            hover_color="#121212",
            command=self.run_pdf_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.pdf_button.grid(row=3, column=0, padx=(30, 0), pady=10, sticky="n")
        self.excel_button = customtkinter.CTkButton(
            self.graph_button_frame,
            fg_color="transparent",
            border_width=2,
            height=55,
            width=int(self.graph_button_frame._current_width),
            text="Eexcel",
            hover_color="#121212",
            command=self.run_excel_event,
            font=customtkinter.CTkFont(
                size=15, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.excel_button.grid(row=4, column=0, padx=(30, 0), pady=10, sticky="n")
        # Sidebar,
        # https://github.com/TomSchimansky/CustomTkinter
        self.logo_image = customtkinter.CTkImage(
            Image.open("assets/images/gpipe.png"), size=(140, 50)
        )

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0, fg_color="#000000"
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_image_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            image=self.logo_image,
            text="",
            height=0,
            fg_color="#000000",
        )
        self.logo_image_label.grid(row=0, column=0, sticky="n", padx=10, pady=(10, 0))

        self.run_button = customtkinter.CTkButton(
            self.sidebar_frame,
            height=50,
            text="/      Run",
            anchor="w",
            command=self.run_gpipe_event,
            font=customtkinter.CTkFont(
                size=20, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.run_button.grid(row=1, column=0, padx=0, pady=10)

        self.quit_button = customtkinter.CTkButton(
            self.sidebar_frame,
            height=50,
            anchor="w",
            text="/      Quit",
            command=self.quit_gpipe_event,
            font=customtkinter.CTkFont(
                size=20, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.quit_button.grid(row=5, column=0, padx=0, pady=(20, 20))

    def right_top_frame(self):
        """right top frame

        Args:
            self
        """
        self.radiobutton_frame = customtkinter.CTkFrame(self)

        self.radiobutton_frame.grid(
            row=0, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.radio_var = IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.radiobutton_frame,
            text="Platform:",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.label_radio_group.grid(
            row=0, column=4, columnspan=1, padx=10, pady=(5, 5), sticky="nsew"
        )
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=0,
            text="Chromium",
        )
        self.radio_button_1.grid(row=1, column=4, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=1,
            text="OpenDEV",
        )
        self.radio_button_2.grid(row=2, column=4, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=2,
            text="Android",
        )
        self.radio_button_3.grid(row=3, column=4, pady=10, padx=20, sticky="n")
        # More radio buttons, doesnt do anything rn, could be used for later purpose

        self.radio_var_2 = IntVar(value=0)

        self.label_radio_group_2 = customtkinter.CTkLabel(
            master=self.radiobutton_frame,
            text="Chungite:",
            font=customtkinter.CTkFont(
                size=16, weight="bold", family="Poppins SemiBold"
            ),
        )
        self.label_radio_group_2.grid(
            row=4, column=4, columnspan=1, padx=10, pady=10, sticky=""
        )
        self.radio_button_4 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var_2,
            value=0,
            text="Yes",
        )
        self.radio_button_4.grid(row=5, column=4, pady=10, padx=20, sticky="n")
        self.radio_button_5 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var_2,
            value=1,
            text="Tomorrow",
        )
        self.radio_button_5.grid(row=6, column=4, pady=10, padx=20, sticky="n")
        self.radio_button_6 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var_2,
            value=2,
            text="Ooga",
        )
        self.radio_button_6.grid(row=7, column=4, pady=10, padx=20, sticky="n")

    def run_gpipe_event(self, crawl=None):
        """Threading is used within this event
        to create faster running time and no crashing for the GUI

        Args:
            self
            crawl: Defaults to None.
        """

        platform = self.radio_var.get()

        gpipe_main.set_platform(platform) #We set the platform

        gpipe_main.set_time( #We set the time
            self.date_entry_1.get(),
            self.date_entry_2.get(),
            self.time_entry_1.get(),
            self.time_entry_2.get(),
        )
        #Depending on crawl, we start a thread
        if crawl is None:
            thread = threading.Thread(target=self.thread_start)
        else:
            thread = threading.Thread(target=self.thread_start(crawl=crawl))
        thread.setDaemon(
            True
        )  # We create a Daemon so when we quit all other threads this one also
        # quits. Meaning quit_gpipe_event still works
        thread.start()

        self.textbox.configure(
            font=("Consolas", 15),
        )
        #While the thread is alive we update the textbox
        if thread.is_alive() is True:

            self.textbox.delete("0.0", END)
            self.textbox.insert(
                "0.0", "GPipe is loading... \nYou should probably grab a coffee\n"
            )

    def thread_start(self, crawl=None):
        """starts the thread

        Args:
            self
            crawl Defaults to None.
        """
        if crawl is None:
            self.data_frame = gpipe_main.run_gpipe(self)
        else:
            self.data_frame = gpipe_main.run_gpipe(self, crawl)
        #When the thread is finished, it will print the results
        self.textbox.configure(
            font=("Consolas", 13)
        )  # Only works with consolas
        print(self.data_frame)
        settings = gpipe_main.update_current_settings()
        # Credit to help at shorturl.at/kELN2

        self.textbox.delete("0.0", END)
        self.textbox.insert("0.0", settings + "\n" + self.data_frame + "\n\n")

    def quit_gpipe_event(self):
        """quits gpipe as a event

        Args:
            self
        """
        self.destroy()
        self.quit()

    def run_graph_event(self):
        """starts gpipe as a event

        Args:
            self
        """
        try:
            self.graph_data(self.time.get(), self.popout.get())
        except KeyError as graph_error:
            self.textbox.insert("0.0",
                                 "********    ERROR: Couldn't generate graph, "
                                 "did the run work? See error below    ******** \n"
                                   + str(graph_error) + "\n\n")
        self.load_graph()

    def run_crawl_event(self):
        """runs the search engine

        Args:
            self
        """
        self.run_gpipe_event(crawl=self.entry.get())

    def graph_data(self, time=0, popout=0):
        """Reads a JSON file and converts it to a Pandas dataframe.
        It then groups the data based on a specified time interval and generates
        a bar chart using Matplotlib:

        Args:
            self _
            time (int, optional): Defaults to 0.
            popout (int, optional): Defaults to 0.
        """
        #I know i should just have 1 function to call that does this
        #But this works
        with open("src/JSON/out.json", "r", encoding="utf-8") as out_file:
            data = json.load(out_file)
        data_frame = pd.DataFrame(data)
        data_frame = data_frame[["updated"]]
        data_frame["updated"] = data_frame["updated"].apply(lambda x: x.split(".")[0])
        data_frame["updated"] = pd.to_datetime(data_frame["updated"])
        plt.style.use("dark_background")

        if time == 0:
            hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1H")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Hour")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Hour")
            plt.savefig(
                "generations/plot.jpg",
                bbox_inches="tight",
                facecolor="#121212",
                dpi=150,
            )
        elif time == 1:
            hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1D")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Day")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Day")
            plt.savefig(
                "generations/plot.jpg",
                facecolor="#121212",
                bbox_inches="tight",
                dpi=150,
            )
        elif time == 2:
            hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1W")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Week")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Week")
            plt.savefig(
                "generations/plot.jpg",
                facecolor="#121212",
                bbox_inches="tight",
                dpi=150,
            )
        elif time == 3:
            hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1M")).size()
            hourly_count.plot(kind="bar", figsize=(10, 6))
            plt.xlabel("Month")
            plt.ylabel("Number of Changes")
            plt.title("Number of Changes per Month")
            plt.savefig(
                "generations/plot.jpg",
                facecolor="#121212",
                bbox_inches="tight",
                dpi=150,
            )
        if popout == 1:
            plt.ion()
            plt.show()
        self.textbox.insert("0.0", "PNG generated at /generations folder\n")

    def run_excel_event(self):
        """generates a excel of the dataframe

        Args:
            self
        """
        try:
            with open("src/JSON/out.json", "r", encoding="utf-8") as out_file:
                data = json.load(out_file)
            data_frame = pd.DataFrame(data)

            # We just make the data_frame pretty

            data_frame = data_frame[["owner", "project", "branch",
                                    "updated", "insertions", "deletions"]]
            data_frame["owner"] = data_frame["owner"].apply(
                lambda x: x["_account_id"]
            )  # Removes unnecesary lines that makes the data_frame way too long
            data_frame["updated"] = data_frame["updated"].apply(lambda x: x.split(".")[0])
            data_frame["project"] = data_frame["project"].str.replace("chromium", "...")
            data_frame["branch"] = data_frame["branch"].apply(
                lambda x: "/".join(x.split("/")[-2:]) if len(x) > 10 else x
            )
            data_frame["branch"] = data_frame["branch"].apply(
                lambda x: "..." + x if len(x) > 10 else x
            )
            data_frame["project"] = data_frame["project"].apply(
                lambda x: "..." + x if len(x) > 10 else x
                )
            data_frame.to_excel(excel_writer="generations/excelGPipe.xlsx", sheet_name="excelGPipe")
            self.textbox.insert("0.0", "Excel generated at /generations folder\n")
        except KeyError as excel_error:
            self.textbox.insert("0.0",
                                 "********    ERROR: Couldn't generate EXCEL,"
                                   " did the run work? See error below    ******** \n"
                                   + str(excel_error) + "\n\n")
    def run_pdf_event(self):
        """generates a PDF of the graph

        Args:
            self
        """
        try:
            time = self.time.get()
            with open("src/JSON/out.json", "r", encoding="utf-8") as out_file:
                data = json.load(out_file)
            data_frame = pd.DataFrame(data)
            data_frame = data_frame[["updated"]]
            data_frame["updated"] = data_frame["updated"].apply(
                lambda x: x.split(".")[0])

            data_frame["updated"] = pd.to_datetime(data_frame["updated"])
            plt.style.use("dark_background")

            if time == 0:
                hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1H")).size()
                hourly_count.plot(kind="bar", figsize=(10, 6))
                plt.xlabel("Hour")
                plt.ylabel("Number of Changes")
                plt.title("Number of Changes per Hour")
                plt.savefig(
                    "generations/plotPDF.pdf",
                    facecolor="black",
                    bbox_inches="tight",
                    dpi=150,
                )
            elif time == 1:
                hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1D")).size()
                hourly_count.plot(kind="bar", figsize=(10, 6))
                plt.xlabel("Day")
                plt.ylabel("Number of Changes")
                plt.title("Number of Changes per Day")
                plt.savefig(
                    "generations/plotPDF.pdf",
                    facecolor="black",
                    bbox_inches="tight",
                    dpi=150,
                )
            elif time == 2:
                hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1W")).size()
                hourly_count.plot(kind="bar", figsize=(10, 6))
                plt.xlabel("Week")
                plt.ylabel("Number of Changes")
                plt.title("Number of Changes per Week")
                plt.savefig(
                    "generations/plotPDF.pdf",
                    facecolor="black",
                    bbox_inches="tight",
                    dpi=150,
                )
            elif time == 3:
                hourly_count = data_frame.groupby(pd.Grouper(key="updated", freq="1M")).size()
                hourly_count.plot(kind="bar", figsize=(10, 6))
                plt.xlabel("Month")
                plt.ylabel("Number of Changes")
                plt.title("Number of Changes per Month")
                plt.savefig(
                    "generations/plotPDF.pdf",
                    facecolor="black",
                    bbox_inches="tight",
                    dpi=150,
                )

            self.textbox.insert("0.0", "PDF generated at /generations folder\n")
        except KeyError as pdf_error:
            self.textbox.insert("0.0",
                                 "********    ERROR: Couldn't generate PDF, "
                                   "did the run work? See error below    ******** \n"
                                   + str(pdf_error) + "\n\n")
#These functions are needed for the inputs in GUI,
#  for them to find the default date and display them
    def load_start_date(self):
        """loads the start date

        Args:
            self

        Returns:
            string
        """
        settings_dict = gpipe_main.load_settings()
        date_2 = settings_dict["DATE_2"]
        return date_2

    def load_end_date(self):
        """loads the end date

        Args:
            self

        Returns:
            string
        """
        settings_dict = gpipe_main.load_settings()
        date_1 = settings_dict["DATE_1"]

        return date_1

    def load_graph(self):
        """loads the image of the graph

        Args:
            self
        """
        self.plot_image = customtkinter.CTkImage(
            Image.open("generations/plot.jpg"), size=(650, 400)
        )
        self.graph_label.configure(image=self.plot_image, anchor=CENTER)

    def load_start_time(self):
        """loads the start time

        Args:
            self

        Returns:
            string
        """
        settings_dict = gpipe_main.load_settings()
        time_2 = settings_dict["SET_TIME_2"]
        return time_2

    def load_end_time(self):
        """loads the end time

        Args:
            self

        Returns:
            string
        """
        settings_dict = gpipe_main.load_settings()
        time_1 = settings_dict["SET_TIME_1"]
        return time_1

    # Doesnt work yet, shouldn't be implemented now
