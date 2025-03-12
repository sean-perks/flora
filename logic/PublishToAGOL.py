import os
from datetime import datetime
from zipfile import ZipFile

class PublishToAGOL:
    @staticmethod
    def ESRI_login():
        from arcgis.gis import GIS
        gis_user = None
        # connect to arcGIS (must have been logged into arcPro recently)
        try:
            gis = GIS("pro")
            gis_user = gis.users.me
            if gis_user is not None:
                print(f'Welcome, {gis_user}')
        except Exception as e1:
            print(e1)
            try:
                home = ('https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=APPID&response_type=token&redirect_uri=<redirect_uri>')
                gis = GIS(home)
                gis_user = gis.users.me
                if gis_user is not None:
                    print(f'Welcome, {gis_user}')
            except Exception as e2:
                print("Login Failed", e2)
        if gis_user is None or gis_user == "None":
            return None
        else:
            return gis



    @staticmethod
    def publish(shp_folder, location, gis):
        now = datetime.now()
        str_time = now.strftime("%d_%m_%Y__%H_%M%S")
        print(shp_folder)
        project = location.get_project().replace(" ", "_").replace("\\", "_").replace("/", "_")

        print("Saving shapefiles to a zip folder")
        if os.path.exists(shp_folder):
            zip_fold = shp_folder + ".zip"

            if not os.path.exists(zip_fold):
                z = ZipFile(zip_fold, "w")
            else:
                z = zip_fold
            for file in os.listdir(shp_folder):
                if not file.endswith('.zip'):
                    file = os.path.join(shp_folder, file)
                    # Then start adding files:
                    z.write(file)
                    # close zip
            z.close()
            ### publish to AGOL ###
            # agol params
            params = {'title': f'{project}_{str_time}', 'tags': 'known populations', 'type': 'Shapefile'}

            # data to be published
            data = zip_fold
            # define feature to be published
            shpfile = gis.content.add(params, data)
            print("Publishing shapefiles")
            # publish shapefiles as one feature service
            published_service = shpfile.publish()
            print(f'Feature published to agol')

        print('finished')


if __name__ == "__main__":
    gis_user = PublishToAGOL.ESRI_login()
