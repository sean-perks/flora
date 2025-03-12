class LocationList:
    __name = ""
    __locations = []
    __map = {}  # lives on class NOT object

    ALL_LOCATIONS = "All locations"

    def __init__(self, name, locations):
        self.__name = name
        self.__locations = locations
        self.__class__.__map[name.lower()] = self

    # prints the class nicely
    def __str__(self):
        return f"<{self.__name}>"

    def __contains__(self, item):
        return item in self.__locations

    # makes the class objects iterable
    # makes it so when you try to iterate over the class object, it iterates over the list property __accounts
    def __iter__(self):
        return self.__locations.__iter__()

    def get_name(self):
        return self.__name

    @classmethod
    def lookup(cls, name):
        try:
            item = cls.__map[name.lower()]
            return item
        except KeyError:
            return None

    def search(self, name):
        for title in self.__locations:
            if title.get_title().lower() == name.lower():
                return name

        return None

    def remove(self, location):
        self.__locations.remove(location)

    def add(self, location):
        self.__locations.append(location)

    # get data from database
    @staticmethod
    def read_data():
        from ui.Database import Database
        return Database.read_data()
