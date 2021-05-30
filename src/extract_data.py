import requests, zipfile, io
import os
import json

from arcgis.features import FeatureLayer
import geopandas as gpd


def download_zip(zip_file_url, directory):
    request = requests.get(zip_file_url, stream=True)
    if request.ok:
        print(f'downloading {zip_file_url}...')
        z = zipfile.ZipFile(io.BytesIO(request.content))
        print('extracting zip file contents...')
        z.extractall(directory)


def extract_geopandas_dataframe_from_ESRI_API(url, crs=None):
    """

    Notes
    ------
    Implementation based on [1]_. More details for the arcgis API can be found
    in [2]_

    .. [1] https://hub.arcgis.com/pages/a0db1c6905934fb5a522137f0fec6c7b
    .. [2] https://developers.arcgis.com/python/api-reference/
    """

    feature_layer = FeatureLayer(url)
    feature_set = feature_layer.query()
    spatial_df = feature_set.sdf
    # geopandas expects a 'geometry' column
    spatial_df = spatial_df.rename(columns={'SHAPE': 'geometry'})
    sdf = gpd.GeoDataFrame(spatial_df)
    if crs:
        sdf = sdf.set_crs(crs)
    return sdf


def check_and_extract_data(name, file_path, url, crs):
    if os.path.exists(file_path):
        print(f'{file_path} already exists.')
    else:
        print(f'Downloading {name}...')
        sdf = extract_geopandas_dataframe_from_ESRI_API(url, crs)
        sdf.to_feather(file_path)


if __name__ == '__main__':
    cwd = os.getcwd()
    assert 'data' in os.listdir(cwd), 'extract_data.py needs to be called from the top directory so it has access to the `data` directory'

    # Ecozones
    # Layer: Total land and water area (ha) by ecozone (ID: 42)
    name = 'ecozones_area'
    file_path = f'data/raw/{name}.feather'
    url = 'https://www5.agr.gc.ca/atlas/rest/services/mapservices/aafc_national_ecological_framework_of_canada/MapServer/42'
    crs = 'EPSG:3857'

    check_and_extract_data(name, file_path, url, crs)

    # Layer: Total land and water area (ha) by ecoprovince (ID: 29)
    name = 'ecoprovinces_area'
    file_path = f'data/raw/{name}.feather'
    url = 'https://www5.agr.gc.ca/atlas/rest/services/mapservices/aafc_national_ecological_framework_of_canada/MapServer/29'
    crs = 'EPSG:3857'

    check_and_extract_data(name, file_path, url, crs)

    # Layer: Terrestrial ecozones of Canada (ID: 40)
    name = 'ecozones_name'
    file_path = f'data/raw/{name}.feather'
    url = 'https://www5.agr.gc.ca/atlas/rest/services/mapservices/aafc_national_ecological_framework_of_canada/MapServer/40'
    crs = 'EPSG:3857'

    check_and_extract_data(name, file_path, url, crs)

    # Layer: Total land and water area (ha) by ecoregion (ID: 16)
    name = 'ecoregions_area'
    file_path = f'data/raw/{name}.feather'
    url = 'https://www5.agr.gc.ca/atlas/rest/services/mapservices/aafc_national_ecological_framework_of_canada/MapServer/16'
    crs = 'EPSG:3857'

    check_and_extract_data(name, file_path, url, crs)

    # Wildfire statistics:  National Burned Area Composite
    file_path = 'data/raw/nbac/nbac_1986_to_2019_20200921.shp'
    zip_file_url = 'https://cwfis.cfs.nrcan.gc.ca/downloads/nbac/nbac_1986_to_2019_20200921.zip'
    save_directory = 'data/raw/nbac'

    if os.path.exists(file_path):
        print(f'{file_path} already exists.')
    else:
        download_zip(zip_file_url, save_directory)

    # provincial boundaries
    file_path = 'data/raw/prov_boundaries/lpr_000b16a_e.shp'
    zip_file_url = 'https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lpr_000b16a_e.zip'
    save_directory = 'data/raw/prov_boundaries'
    if os.path.exists(file_path):
        print(f'{file_path} already exists.')
    else:
        download_zip(zip_file_url, save_directory)

    # ecozone names
    file_path = 'data/raw/ecozones_name.json'
    if os.path.exists(file_path):
        print(f'{file_path} already exists.')
    else:
        ecozones = {
            1: 'Arctic Cordillera',
            2: 'Northern Arctic',
            3: 'Southern Arctic',
            4: 'Taiga Plains',
            5: 'Taiga Shield',
            6: 'Boreal Shield',
            7: 'Atlantic Maritime',
            8: 'Mixedwood Plains',
            9: 'Boreal Plains',
            10: 'Prairies',
            11: 'Taiga Cordillera',
            12: 'Boreal Cordillera',
            13: 'Pacific Maritime',
            14: 'Montane Cordillera',
            15: 'Hudson Plains'
        }
        with open(file_path, 'w') as fp:
            json.dump(ecozones, fp)
