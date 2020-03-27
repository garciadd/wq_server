#!/usr/bin/python3

#APIs
import argparse
import json
import os

#sat module
from sat_modules import config
from sat_modules import utils
from sat_modules import sentinel
from sat_modules import landsat

#satsr module
from deepaas.model.v2.wrapper import UploadedFile
from satsr.api import predict_data, predict_url

#atcor module
from at_modules import atcor

parser = argparse.ArgumentParser(description='Gets data from satellite')

parser.add_argument("-sat_args", action="store",
                    required=True, type=str)

parser.add_argument('-path',
                   help='output path',
                   required=True)

args = parser.parse_args()
sat_args = json.loads(args.sat_args)
output_path = args.path

local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_path = os.path.join(local_path, 'data')
if not (os.path.isdir(local_path)):
    os.mkdir(local_path)

#Check the format date and if end_date > start_date
sd, ed = utils.valid_date(sat_args['start_date'], sat_args['end_date'])

if sat_args['sat_type'] == "Sentinel2":

    print ("Downloading Sentinel data ...")

    #ESA credentials
    s2_credentials = config.sentinel_pass

    s2_args = {'inidate': sd,
               'enddate': ed,
               'region': sat_args['region'],
               'coordinates': sat_args['coordinates'],
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': sat_args['cloud'],
               'username': s2_credentials['username'],
               'password': s2_credentials['password'],
               'output_path': local_path}

    #download sentinel files
    s = sentinel.download_sentinel(**s2_args)
    s2_tiles = s.download()

    ## Satsr module to super-resolve the satellite bands
    for tile in s2_tiles:

        print ("Preprocessing data ...")
        print ("super resolution ...")

        tile = tile.split('.')[0]

        s2_file = os.path.join(s2_args['output_path'], '{}.zip'.format(tile))
        tif_file = os.path.join(s2_args['output_path'], '{}.tif'.format(tile))

        content_type = 'application/zip'

        coord = '[{},{},{},{}]'.format(sat_args['coordinates']['W'], sat_args['coordinates']['S'], sat_args['coordinates']['E'], sat_args['coordinates']['N'])

        file = UploadedFile(name='data', filename=s2_file, content_type=content_type)
        s2r_args = {'files': [file], 'output_path':json.dumps(tif_file), 'roi_x_y_test': "null" , 'roi_lon_lat_test': coord, 'max_res_test': "null"}
        predict_data(s2r_args)

        print ("atmospheric corrections ...")

        ## atcor_sat module to apply atmospheric correction
        at = atcor.atcor(s2_args['output_path'], tile, output_path)
        at.load_bands()

elif sat_args['sat_type'] == "Landsat8":

    print ("Downloading Landsat data ...")

    #NASA credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate': sd,
               'enddate': ed,
               'region': sat_args['region'],
               'coordinates': sat_args['coordinates'],
               'producttype': 'LANDSAT_8_C1',
               'cloud': sat_args['cloud'],
               'username': l8_credentials['username'],
               'password': l8_credentials['password'],
               'output_path': local_path}

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l8_tiles = l.download()

    for tile in l8_tiles:

        print ("Preprocessing data ...")
        print ("super resolution ...")

        tile = tile.split('.')[0]

        l8_file = os.path.join(l8_args['output_path'], '{}.zip'.format(tile))
        tif_file = os.path.join(l8_args['output_path'], '{}.tif'.format(tile))

        content_type = 'application/zip'

        coord = '[{},{},{},{}]'.format(sat_args['coordinates']['W'], sat_args['coordinates']['S'], sat_args['coordinates']['E'], sat_args['coordinates']['N'])

        file = UploadedFile(name='data', filename=l8_file, content_type=content_type)
        l8sr_args = {'satellite': '"landsat8"', 'output_path':json.dumps(tif_file), 'files': [file], 'roi_x_y_test': "null" , 'roi_lon_lat_test': coord, 'max_res_test': "null"}
        predict_data(l8sr_args)

        print ("atmospheric corrections ...")

        ## atcor_sat module to apply atmospheric correction
        at = atcor.atcor(l8_args['output_path'], tile, output_path)
        at.load_bands()

elif sat_args['sat_type'] == 'All':

    print ("Downloading Sentinel data ...")

    #credentials
    s2_credentials = config.sentinel_pass

    s2_args = {'inidate': sd,
               'enddate': ed,
               'region': sat_args['region'],
               'coordinates': sat_args['coordinates'],
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': sat_args['cloud'],
               'username': s2_credentials['username'],
               'password': s2_credentials['password'],
               'output_path': local_path}

    #download sentinel files
    s = sentinel.download_sentinel(**s2_args)
    s2_tiles = s.download()

    for tile in s2_tiles:

        print ("Preprocessing data ...")
        print ("super resolution ...")

        tile = tile.split('.')[0]

        s2_file = os.path.join(s2_args['output_path'], '{}.zip'.format(tile))
        tif_file = os.path.join(s2_args['output_path'], '{}.tif'.format(tile))

        content_type = 'application/zip'

        coord = '[{},{},{},{}]'.format(sat_args['coordinates']['W'], sat_args['coordinates']['S'], sat_args['coordinates']['E'], sat_args['coordinates']['N'])

        file = UploadedFile(name='data', filename=s2_file, content_type=content_type)
        s2r_args = {'files': [file], 'output_path':json.dumps(tif_file), 'roi_x_y_test': "null" , 'roi_lon_lat_test': coord, 'max_res_test': "null"}
        predict_data(s2r_args)

        print ("atmospheric corrections ...")

        ## atcor_sat module to apply atmospheric correction
        at = atcor.atcor(s2_args['output_path'], tile, output_path)
        at.load_bands()

    print ("Downloading Landsat data ...")

    #credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate': sd,
               'enddate': ed,
               'region': sat_args['region'],
               'coordinates': sat_args['coordinates'],
               'producttype': 'LANDSAT_8_C1',
               'cloud': sat_args['cloud'],
               'username': l8_credentials['username'],
               'password': l8_credentials['password'],
               'output_path': local_path}

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l8_tiles = l.download()

    for tile in l8_tiles:

        print ("Preprocessing data ...")
        print ("super resolution ...")

        tile = tile.split('.')[0]

        l8_file = os.path.join(l8_args['output_path'], '{}.zip'.format(tile))
        tif_file = os.path.join(l8_args['output_path'], '{}.tif'.format(tile))

        content_type = 'application/zip'

        coord = '[{},{},{},{}]'.format(sat_args['coordinates']['W'], sat_args['coordinates']['S'], sat_args['coordinates']['E'], sat_args['coordinates']['N'])

        file = UploadedFile(name='data', filename=l8_file, content_type=content_type)
        l8sr_args = {'satellite': '"landsat8"', 'output_path':json.dumps(tif_file), 'files': [file], 'roi_x_y_test': "null" , 'roi_lon_lat_test': coord, 'max_res_test': "null"}
        predict_data(l8sr_args)

        print ("atmospheric corrections ...")

        ## atcor_sat module to apply atmospheric correction
        at = atcor.atcor(l8_args['output_path'], tile, output_path)
        at.load_bands()
