from ui.Location import Location
from ui.LocationList import LocationList
class Database:

    @staticmethod
    def read_data():
        hebo = Location("Mount Hebo", "Mount hebo on the coast range and surrounding area.",
                        45.255747, -123.676318, 45.136035, -123.856713)
        hcrhst = Location("HCRHST", "historic columbia river highway state trail",
                         45.814922, -121.041708, 45.460196, -122.119985)
        region6 = Location("Region 6", "All of oregon and washington",
                           49.17717, -116.0311, 41.82407, -124.8842)
        umatilla = Location("Umatilla", "Umatilla National Forest rectangle",
                           46.36909, -117.0060, 44.39115, -120.6138)
        siuslaw = Location("Siuslaw", "Siuslaw National Forest rectangle",
                           46.136469, -122.698017, 42.026048, -124.541937)
        yellowstone = Location("yellowstone", "Approximate yellowstone np boundary", 45.1266229,
                               -109.8245215, 44.1158603, -111.1665014)




        rst = LocationList("Restoration Services Team", [hebo, hcrhst, yellowstone])
        regional = LocationList("Regional/State", [region6])
        forests = LocationList("Forests", [umatilla, siuslaw])
        all_locations_obj = LocationList(LocationList.ALL_LOCATIONS, [hebo, hcrhst, region6, siuslaw, umatilla])

        all_locations_list = [hebo, hcrhst, region6, umatilla, siuslaw]
        all_location_categories = [rst, regional, forests, all_locations_obj]

        return all_locations_list, all_location_categories, all_locations_obj

