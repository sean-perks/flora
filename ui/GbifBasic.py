from datetime import datetime
from pygbif import occurrences
# from GetElevation import GetElevation
import geopandas
import pandas as pd
import os

def get_df_from_gbif(sp_list, location, shape_dir, shapefile_csv_both = 's'):
    now = datetime.now()
    str_time = now.strftime("%d_%m_%Y__%H_%M%S")
    shp_fold = None

    geopandas.options.io_engine = "pyogrio"
    my_crs = "EPSG:4326"
    my_epsg = '4326'

    df_list = []

    print("\nretrieving data from gbif, records come in chunks of 300")
    project = location.get_project().replace(" ", "_").replace("\\", "_").replace("/", "_")
    sw_lat = location.get_sw_lat()
    sw_lon = location.get_sw_lon()
    ne_lat = location.get_ne_lat()
    ne_lon = location.get_ne_lon()

    for spec in sp_list:
        list_of_dicts = []
        c = 300
        while c == 300:
            out = occurrences.search(scientificName=spec, decimalLatitude=f'{sw_lat}, {ne_lat}',
                                     decimalLongitude=f'{sw_lon}, {ne_lon}',
                                     hasCoordinate=True, offset=len(list_of_dicts)).get('results')

            if len(out) == 300:
                print(f"{len(list_of_dicts) + 300} records received, more on the way..")

            # new list of dicts with only desired values
            for dic in out:
                sp_dict = {'species': dic.get('species'), 'latitude': dic.get('decimalLatitude'),
                           'longitude': dic.get('decimalLongitude'), 'date': dic.get('dateIdentified'),
                           'elev_m': dic.get('elevation'), 'references': dic.get('references'),
                           'inst_code': dic.get('institutionCode')}
                list_of_dicts.append(sp_dict)
            c = len(out)
        # list of dictionaries to a df

        occur = pd.DataFrame.from_records(list_of_dicts)
        print(f"\n{len(list_of_dicts)} {spec} records total.")
        #try:
         #   GetElevation.add_elevation_to_df(occur, "latitude", "longitude")
        #except Exception as e:
         #   print(e)
          #  print("failed to extract elevation data from PRISM DEM.")
        # Make sure the # of occurrences is not 0
        if len(occur) > 0:

            if shapefile_csv_both in ['s', 'b']:
                if shapefile_csv_both == 'b':
                    df_list.append(occur)

                occur = geopandas.GeoDataFrame(occur,
                                               geometry=geopandas.points_from_xy(occur["longitude"], occur["latitude"]),
                                               crs=my_crs)
                occur.to_crs(crs=my_crs, epsg=my_epsg, inplace=True)


                #### SAVE OUTPUT ####
                # Create folder dir as project plus time
                foldy = project + "_" + str_time

                # join output folder with timestamp folder
                shp_fold = os.path.join(shape_dir, foldy)

                # create timestamp output folder
                if not os.path.exists(shp_fold):
                    os.mkdir(shp_fold)
                    print("Output directory created")
                # make shapelife name
                new_path = os.path.join(shp_fold, f'{spec}_{project}.shp')

                # write shapefile

                if not os.path.exists(new_path):
                    occur.to_file(new_path, driver='ESRI Shapefile')
                    print(f"{spec} shapefile saved..")

            else:
                df_list.append(occur)

        else:
            print(f"no results for {spec}")
    # End for loop

    if shapefile_csv_both in ['b', 'c']:
        if len(df_list) > 0:
            df = pd.concat(df_list, axis=0)
                # Create folder dir as project plus time
            file = project + "_" + str_time + ".csv"
            # join output folder with timestamp folder
            csv_file = os.path.join(shape_dir, file)
            df.to_csv(csv_file, index = False)
            print(f"\ncsv saved to {csv_file}")
            return shp_fold
        else:
            return None
    else:
        return shp_fold

