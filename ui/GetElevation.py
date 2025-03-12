"""
from input_validation import *
import rasterio
import pandas as pd
from osgeo import gdal
import geopandas as gpd
from rasterio.transform import rowcol
import numpy as np
from rasterio.transform import from_origin
import os

class GetElevation:

    user = os.getlogin()
    # hardcode DEM path
    DEM_PATH = f"C:/Users/{user}/Box/DorenaGRC/Operations/Nursery/SeedCollection/other tools/PRISM_us_dem_800m_bil.bil"

    @classmethod
    def add_elevation_to_df(cls, df, lat_col, lon_col):

        # lat_col, lon_col, elevation_col = cls.get_csv_lat_lon_elevation_columns(df)

        # Open the DEM file using rasterio
        with rasterio.open(cls.DEM_PATH) as dem:
            # Extract the affine transform and the inverse of the transform
            transform = dem.transform
            inv_transform = ~transform

            # Create a list to hold the elevation data
            elevations = []

            # Loop through each point in the CSV
            for index, row in df.iterrows():
                lat, lon = row[lat_col], row[lon_col]

                # Get the (row, col) position in the DEM array
                row_col = inv_transform * (lon, lat)
                try:
                    col, row = int(row_col[0]), int(row_col[1])
                except ValueError as e:
                    print(e)
                    col, row = 999999, 999999

                # Ensure the indices are within bounds
                if 0 <= row < dem.height and 0 <= col < dem.width:
                    # Read the elevation value at the given row and column
                    elevation = dem.read(1)[row, col]

                    # convert to feet
                    elevation = int(elevation * 3.28084)
                    elevations.append(int(elevation))
                    # print(elevation)
                else:
                    # Handle out-of-bounds points
                    elevations.append("")

        # Add the elevation data to the DataFrame
        df["elev_ft"] = elevations
        print("finished")
        return df
"""