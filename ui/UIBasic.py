import pandas as pd
import os
from tkinter import Tk
from tkinter import filedialog
from datetime import datetime
import geopandas as gpd
import osgeo


import ui.GbifBasic
from ui.input_validation import *
from ui.Species import Species
from ui.Location import Location
from ui.SpellCheck import SpellCheck
from ui.LocationList import LocationList
from logic.PublishToAGOL import PublishToAGOL

class Ui:
    __all_locations = None
    __all_location_groups = None
    __all_locations_obj = None
    __species_list = Species([], [], [], [], [])

    @staticmethod
    def print_welcome():
        print('''


                              <>--  Welcome to FLORA basic --<>
                (Flawlessly Leveraging Occurrence Retrieval into Awesomeness)


       This program pulls occurrence data from the Global Biodiversity Information Facility
                                   https://www.gbif.org/

                                             *''')

    CHOICES = ["1", "2", "3", "x"]

    @staticmethod
    def print_menu():
        print(
            """
            Options:
                1.  Download shapefiles/csv's
                2.  Spell check species list
                3.  Manage locations/projects
                x   Exit program 
            """
        )

    @staticmethod
    def print_location_menu():
        print(
            """
            Options:
                1.  Display all locations/projects
                2.  Select location by group (RST, Dorena, Regional/State, etc.)
                3.  Create new location group
                4.  Create new project/location
                5.  Delete group or location
                x   Exit location menu
            """
        )

    @staticmethod
    def print_shapefile_menu():
        print("""
          1. Produce CSV (contains lat/lon coordinate of occurrences)
          2. Produce Shapefiles (one for each species)
          3. Produce CSV and shapefiles
          4. Exit
          """)

    @classmethod
    def init(cls):
        from ui.Database import Database
        cls.__all_locations, cls.__all_location_groups, cls.__all_location_obj = Database.read_data()

    @classmethod
    def print_locations(cls):
        c = 1
        for location in cls.__all_locations:
            print(f"{c}. {location}")
            c+=1

    @classmethod
    def print_location_groups(cls):
        for group in cls.__all_location_groups:
            print(group)

    @classmethod
    def select_location(cls, prompt="Select location or add new: ", group='all', new=True):
        if group == 'all':
            cat = cls.__all_locations
        else:
            cat = group
        if new:
            choices = [f"{item.get_project()}" for item in cat] + ["New"] + ["Back"]
        else:
            choices = [f"{item.get_project()}" for item in cat] + ["Back"]
        print(f"\n{prompt}")
        c = 1
        choice_dict = {}
        for x in choices:
            if x == "New" and new:
                print(f"\n   {c}. Create New")
            else:
                print(f"   {c}. {x}")
            choice_dict[f"{c}"] = x
            c+=1

        location_name = select_item(prompt="\nEnter location name: ", error="location not found", choices=list(choice_dict.keys())).lower()
        if choice_dict.get(location_name) == "Back":
            return "back"
        if choice_dict.get(location_name) == "New":
            return "newnewnew"
        for location in cat:
            if choice_dict.get(location_name).lower() == location.get_project().lower():
                return location
        return None

    @classmethod
    def add_location(cls, group="all_groups"):
        if group == "all_groups":
            group = cls.__all_location_groups

        good = False
        exit_strings = ['x', 'exit', 'quit']
        print("\nEnter the coordinates in decimal degrees.")
        print('The "Area of Interest" is a rectangle of the NE lat/lon and SW lat/lon provided')
        print("*hint: google maps is an easy way to see the lat/long\n")
        while not good:
            print("Enter 'x', 'exit' or 'quit' to return to the main menu")
            name = input_string("Enter the name of the project/location: ")
            if name.lower() in exit_strings:
                return None
            description = input_string("Enter a description for this project/location: ")
            if description.lower() in exit_strings:
                return None
            sw_lat = input_float(prompt="Enter the south west latitude: ", error="Invalid!", ge=-90, gt=None, le=90,
                                 lt=None)
            sw_lon = input_float(prompt="Enter the south west longitude: ", error="Invalid!", ge=-180, gt=None, le=180,
                                 lt=None)
            ne_lat = input_float(prompt="Enter the north east latitude: ", error="Invalid!", ge=-90, gt=None, le=90,
                                 lt=None)
            while ne_lat <= sw_lat:
                print(f"Error, NE latitude must be greater than the value for SW latitude: {sw_lat}")
                ne_lat = input_float(prompt="Enter the north east latitude: ", error="Invalid!", ge=-90, gt=None, le=90,
                                     lt=None)
            ne_lon = input_float(prompt="Enter the north east longitude: ", error="Invalid!", ge=-180, gt=None, le=180,
                                 lt=None)
            while ne_lon < sw_lon:
                print(f"Error, NE longitude must be greater than the value for SW longitude: {sw_lon}")
                ne_lon = input_float(prompt="Enter the north east longitude: ", error="Invalid!", ge=-180, gt=None,
                                     le=180,
                                     lt=None)
            location = Location(name, description, ne_lat, ne_lon, sw_lat, sw_lon)

            print("\nDoes the following look correct?\n")
            print(f"Project/Location name: {name}")
            print(f"Description: {description}")
            print(f"North east latitude: {ne_lat}")
            print(f"North east longitude: {ne_lon}")
            print(f"South west latitude: {sw_lat}")
            print(f"South west longitude: {sw_lon}\n")
            good = y_n()
            if good:

                cls.__all_locations.append(location)
                group.add(location)

                return location

    @staticmethod
    def get_folder_output(prompt = "\nSelect folder via folder dialog, you may need to reduce windows to find the dialog box."):
        '''prompts user to enter folder'''
        print(prompt)
        folder = ''
        Tk().withdraw()
        folder = filedialog.askdirectory()

        if len(folder) < 1 or folder is None:
            return None

        return folder

    @staticmethod
    def get_file():
        '''prompts user to open a csv'''
        print("\nOpen your .csv, you may have to reduce windows to see the dialog box\n")
        Tk().withdraw()
        file = filedialog.askopenfile(filetypes=(("CSV Files", "*.csv"),))

        return file

    @classmethod
    def get_species_list(cls):
        sp_list = None
        if len(cls.__species_list.get_spell_checked_species()) != 0:
            yn = y_n("You have already spell checked this session, would you like to replace your previous spell check? (y/n): ")
            if yn:
                pass
            else:
                sp_list = cls.__species_list.get_spell_checked_species()
                return sp_list
        sp_choices = ["1", "2", "3"]
        print("""
        Select from the following:
              1. Enter species manually
              2. Upload species from .csv file with a species column
              3. Exit
              """)
        choice = select_item("Please select an option: ", "Invalid menu option!", choices=sp_choices)
        if choice == "1":
            sp_list = cls.enter_species_manually()
        elif choice == "2":
            sp_list = cls.get_species_from_csv()
        elif choice == "3":
            return None
        if sp_list is not None:
            cls.__species_list.set_species_list(sp_list)

        return sp_list

    @staticmethod
    def enter_species_manually():
        sp_list = []
        species = ""
        print("\nEnter species one at a time and press 'enter'")
        print("Enter 'x' or 'exit' to STOP\n")
        while species.lower() not in ['exit', 'x', 'quit', 'q']:
            species = input_string("Enter scientific name (Genus species): ")
            if not species.lower() in ['exit', 'x', 'quit', 'q']:
                if species not in sp_list:
                    sp_list.append(species.strip())
        if len(sp_list) == 0:
            sp_list = None

        return sp_list

    @classmethod
    def get_species_from_csv(cls):
        print("The .csv is required to have column names and a column with species names spelt correctly")
        has_headers = y_n("Does your .csv have column names (y/n): ")
        try:
            if has_headers:
                input_file = cls.get_file()
                df = pd.read_csv(input_file)
                columns = df.columns
                print("\nWhat is the name of the column containing the Genus/species?")
                for c in columns:
                    print("    " + c)
                sp_col = select_item("\nEnter column: ", error="Name not found", choices=columns)
                sp_list = list(df[sp_col])
                final_sp_list = []
                for s in sp_list:
                    s = s.strip()
                    if s not in final_sp_list:
                        final_sp_list.append(s)

                return final_sp_list
        except Exception as e:
            print(e)
            print("\nerror, make sure your csv has column names")
            return None
        return None

    @classmethod
    def manage_locations(cls):
        """
                    Options:
                        1.  Display all locations/projects
                        2.  Select location by group (RST, Dorena, Regional/State, etc.)
                        3.  Create new location group
                        4.  Create new project/location
                        5.  Delete group or location
                        x   Exit location menu
                    """
        loc_choices = ["1", "2", "3", "4", "5", "6", "x", "exit", "quit", "q"]
        while True:
            cls.print_location_menu()
            choice = select_item("Please select an option: ", "Invalid menu option!", choices=loc_choices)
            if choice in ['x', 'quit', 'q']:
                return
            elif choice == '1':
                cls.print_locations()
            elif choice == '2':
                loc, group = cls.select_location_by_group(allow_new=False)
                print(loc, group)
            elif choice == '3':
                print("Under construction")
            elif choice == '4':
                cat = cls.select_location_category(prompt="Select a project category to add location to: ")
                if cat is not None:
                    loc = cls.add_location(cat)
            elif choice == '5':
                print("Under construction")

    @classmethod
    def produce_csv(cls):
        sp_list = cls.get_species_list()
        if sp_list is None:
            return
        print(f"Species list: {sp_list}")
        location = "back"
        while location == "back":
            location = cls.select_or_add_location()
            if location is None:
                return

        shape_dir = cls.get_folder_output(
            "Select your output folder. You may need to reduce windows to see the dialog box.")
        if shape_dir is None:
            return
        final_list = []
        for s in sp_list:
            if s not in final_list:
                final_list.append(s)
        foldy = ui.GbifBasic.get_df_from_gbif(final_list, location, shape_dir, shapefile_csv_both='c')

    @classmethod
    def spell_check_names(cls):
        sp_list = cls.get_species_list()
        spell_checked = SpellCheck.spell_check_list(sp_list)
        if spell_checked is None:
            return
        yn = y_n("\nWould you like to use your results to download occurrence data? (y/n): ")
        if yn:
            cls.__species_list.set_spell_checked_species(spell_checked)

        yn = y_n("\nWould you like to export your results as a csv? (y/n): ")
        if yn:
            now = datetime.now()
            str_time = now.strftime("%d_%m_%Y__%H_%M%S")
            df_checked = pd.DataFrame()
            df_checked["old_name"] = sp_list
            df_checked["new_name"] = spell_checked
            out_fold = cls.get_folder_output(
                "Select your output folder. You may need to reduce windows to see the dialog box.")
            out_file = f"{str_time}_spell_checked_list.csv"
            out = os.path.join(out_fold, out_file)
            df_checked.to_csv(out, index = False)

    @staticmethod
    def publish_to_agol(foldy, location):
        print("\n")
        pub = y_n("Would you like to attempt to publish this to you content in ArcGIS Online? (y/n): ")
        if pub:
            cont = True
            while cont:
                # try to publish
                gis = PublishToAGOL.ESRI_login()
                if gis is None:
                    print("Attempt failed. Make sure you are connected to the VPN and \nhave logged into ArcGIS Pro within the last week.")
                    cont = y_n("Would you like to try again? (y/n): ")
                else:
                    try:
                        PublishToAGOL.publish(foldy, location, gis)
                        cont = False
                    except Exception as e:
                        print(e)
                        print("Publish failed")
                        cont = y_n("Would you like to try again? (y/n): ")


    @classmethod
    def produce_shapefile(cls):
        foldy = None
        sp_list = cls.get_species_list()
        if sp_list is None:
            return
        print(f"Species list: {sp_list}")
        location = "back"
        while location == "back":
            location = cls.select_or_add_location()
            if location is None:
                return
        if location is None:
            return
        shape_dir = cls.get_folder_output(
            "Select your output folder. You may need to reduce windows to see the dialog box.")
        if shape_dir is None:
            return
        final_list = []
        for s in sp_list:
            if s not in final_list:
                final_list.append(s)
        try:
            foldy = ui.GbifBasic.get_df_from_gbif(final_list, location, shape_dir, shapefile_csv_both='s')
        except Exception as e:
            print(e)
        cls.publish_to_agol(foldy, location)

    @classmethod
    def produce_shapefile_and_csv(cls):
        sp_list = cls.get_species_list()
        if sp_list is None:
            return
        print(f"Species list: {sp_list}")
        location = "back"
        while location == "back":
            location = cls.select_or_add_location()
            if location is None:
                return
        if location is None:
            return
        shape_dir = cls.get_folder_output(
            "Select your output folder. You may need to reduce windows to see the dialog box.")
        if shape_dir is None:
            return
        final_list = []
        for s in sp_list:
            if s not in final_list:
                final_list.append(s)
        foldy = ui.GbifBasic.get_df_from_gbif(final_list, location, shape_dir, shapefile_csv_both='b')
        cls.publish_to_agol(foldy, location)

    @classmethod
    def shapefile_menu(cls):
        cls.print_shapefile_menu()
        shp_choices = ["1", "2", "3", "4"]
        choice = select_item("Please select an option: ", "Invalid menu option!", choices=shp_choices)
        if choice == '4':
            return
        elif choice == '1':
            cls.produce_csv()
        elif choice == '2':
            cls.produce_shapefile()
        elif choice == '3':
            cls.produce_shapefile_and_csv()

    @classmethod
    def select_or_add_location(cls, allow_new=True, group="all_groups"):
        print()
        location, group = cls.select_location_by_group(allow_new=allow_new)
        if location == "newnewnew":
            location = cls.add_location(group=group)
        if location is None:
            return None
        if location == "back":
            return "back"
        return location

    @classmethod
    def select_location_category(cls, prompt="\nEnter a project category: "):
        names = [category.get_name() for category in cls.__all_location_groups] + ["Exit"]
        print("Pre-made locations are stored in the groups below.")
        print("Select a location group to see available locations or add a new location")
        prompt_string = "\nSelect location group: "
        choice_dict = {}
        c = 1
        for name in names:
            if name == "Exit":
                prompt_string += "\n"
            prompt_string += f"\n    {c}. {name}"
            choice_dict[f"{c}"] = name
            c+=1
        choices = list(choice_dict.keys())
        prompt_string += f"\n{prompt}"
        selected = select_item(prompt=prompt_string, error="Nope.", choices=choices)
        if selected == choices[-1]:
            return None
        print("Selected:", choice_dict.get(selected))
        selected_category = LocationList.lookup(choice_dict.get(selected))
        return selected_category

    @classmethod
    def select_location_by_group(cls, allow_new=True):
        cat = cls.select_location_category()
        if cat is None:
            return None, None
        loc = cls.select_location(group=cat, new=allow_new)
        return loc, cat

    @classmethod
    def run(cls):
        cls.print_welcome()
        while True:
            cls.print_menu()
            print()
            choice = select_item("Please select an option: ", "Invalid menu option!", choices=cls.CHOICES)
            if choice == 'x':
                break
            elif choice == '1':
                cls.shapefile_menu()
            elif choice == '2':
                cls.spell_check_names()
            elif choice == '3':
                cls.manage_locations()

        print("Goodbye!")

if __name__ == "__main__":
    print("CWD is: ")
    print(os.getcwd())
    Ui.init()
    Ui.run()
