class Location:
    __project = ""
    __description= ""
    __ne_lat = 0.0
    __ne_lon = 0.0
    __sw_lat = 0.0
    __sw_lon = 0.0
    __map = {}

    def __init__(self, project, description, ne_lat, ne_lon, sw_lat, sw_lon):
        self.__project = project
        self.__description = description
        self.__ne_lat = ne_lat
        self.__ne_lon = ne_lon
        self.__sw_lat = sw_lat
        self.__sw_lon = sw_lon
        Location.__map[project.lower()] = self

    def __str__(self):
        return f"{self.__project}, {self.__description}"

    @classmethod
    def lookup(cls, project):
        return cls.__map[project.lower()]

    def get_project(self):
        return self.__project

    def get_description(self):
        return self.__description

    def get_ne_lat(self):
        return self.__ne_lat

    def get_ne_lon(self):
        return self.__ne_lon

    def get_sw_lat(self):
        return self.__sw_lat

    def get_sw_lon(self):
        return self.__sw_lon
