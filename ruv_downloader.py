#!/usr/bin/env python

import requests
import json
import dbm
import time
from yt_dlp import YoutubeDL
import os
import sys
import re
import os 
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
import urllib.request





image_file_formats = ["ase","art","bmp","blp","cd5","cit","cpt","cr2","cut","dds","dib","djvu","egt","exif","gif","gpl","grf","icns","ico","iff","jng","jpeg","jpg","jfif","jp2","jps","lbm","max","miff","mng","msp","nef","nitf","ota","pbm","pc1","pc2","pc3","pcf","pcx","pdn","pgm","PI1","PI2","PI3","pict","pct","pnm","pns","ppm","psb","psd","pdd","psp","px","pxm","pxr","qfx","raw","rle","sct","sgi","rgb","int","bw","tga","tiff","tif","vtf","xbm","xcf","xpm","3dv","amf","ai","awg","cgm","cdr","cmx","dxf","e2d","egt","eps","fs","gbr","odg","svg","stl","vrml","x3d","sxd","v2d","vnd","wmf","emf","art","xar","png","webp","jxr","hdp","wdp","cur","ecw","iff","lbm","liff","nrrd","pam","pcx","pgf","sgi","rgb","rgba","bw","int","inta","sid","ras","sun","tga","heic","heif"]



class manage_kvs:
    def __init__(self,dbm_file=".kvs"):
        self.dbm_handle = dbm.open(dbm_file, 'c')

    def write(self,field,data):

        data["timestamp"] = time.time()

        try:
            self.dbm_handle[field] = json.dumps(data)
            return True,"ok"
        except Exeption as e:
            return False,e


    def read(self,field):

        try:
            data = json.loads(self.dbm_handle[field].decode())
            return data
        except:
            return False

    def exists(self,field):
        if field in self.dbm_handle:
            return True
        else:
            return False

    def valid(self,field,maxage=3600):

        if not self.exists(field):
            return False

        data = self.read(field)
        if "timestamp" not in data:
            return False

        now = time.time()
        delta = now - data["timestamp"] 

        if delta > 3600:
            return False
        else:
            return True

    def list_keys(self,do_print=False):


        data = { }
        data["keys"] = { }
        keys = self.dbm_handle.keys()
        pads = [ 30, 50 ]
        total_pad = sum(pads)
        header = "key Name".ljust(pads[0]) + "Key Info".ljust(pads[1]) + "\n" + "".ljust(total_pad,"-")

        if do_print:
            print(header)


        for key in keys:
            key_name = key.decode()
            key_data = self.dbm_handle[key].decode()


            try:
                key_data_json = json.loads(key_data)
                show_name = key_data_json["data"]["Program"]["title"]
                key_info = show_name
                data["keys"]["key_name"] = key_data_json
            except:
                key_info = "no show name found"
                data["keys"][key_name] = key_data

            line = key_name.ljust(pads[0]) + key_info.ljust(pads[1])

            if do_print:
                print(line)
        

        return data

    def decode_key(self,key):
        key_data_raw = self.dbm_handle[key].decode()

        try:
            key_data = json.loads(key_data_raw)
            is_json = True
        except:
            key_data = key_data_raw
            is_json = False

        return key_data, is_json

    def delete_key(self,key):

        if not self.exists(key):
            print("Key " + key + " does not exist")
        else:
            del self.dbm_handle[key]
            print("Key " + key + " deleted" )
            



def pprint(msg,ens_ascii=True):
    try:
        print(json.dumps(msg,indent=2,ensure_ascii=ens_ascii))
    except:
        print(msg)




def get_show_data(show_id):


    show_id = str(show_id)

    gql_search_url = "https://spilari.nyr.ruv.is/gql/?operationName=getEpisode&variables=%7B%22programID%22%3A" + show_id + "%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22f3f957a3a577be001eccf93a76cf2ae1b6d10c95e67305c56e4273279115bb93%22%7D%7D"

    
    kvs_key = "_graphql_cache-" + show_id

    if not kvs.valid(kvs_key):
        response = requests.request("GET", gql_search_url)
        data = response.json()
        kvs.write(kvs_key,data)
    else:
        data = kvs.read(kvs_key)

    return data


def list_episodes(show_id):


    gql_data = get_show_data(show_id)


    data = gql_data["data"]["Program"]


    show_data = {
            "name"  :   data["title"],
            "slug"  :   data["slug"]
            }


    episodes = data["episodes"]


def yt_dlp_monitor(d):

    filename  = d.get('info_dict').get('_filename')

def download_episode(url,filepath,show_config,episode):

    ydl_opts = {
            "prefer_ffmpeg": True,
            }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        file_ending = info["ext"]
        ydl_opts["outtmpl"] = filepath + "." + file_ending

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(url)
        except Exception as e:
            print(e)
            print("ERROR with: " + url)

def download_show(show_config):    

    show_id = str(show_config["show_id"])


    list_episodes(show_id)


    graphql_data = kvs.read("_graphql_cache-" + show_id)

    #episodes = kvs.read("_graphql_cache-" + show_id)["data"]["Program"]["episodes"]
    episodes = graphql_data["data"]["Program"]["episodes"]
    

    filename_front = show_config["filename"].split("-")[0]
    filename_mid = show_config["filename"].split("-")[1].split("{")[0]


    #show_name = kvs.read("_graphql_cache-" + show_id)["data"]["Program"]["title"]
    show_name = graphql_data["data"]["Program"]["title"]



    existing_files = os.listdir(show_config["dl_folder"]) 

    if download_posters:

        show_poster_files = [ ]
        for iff in image_file_formats:
            spf = "show." + iff
            show_poster_files.append(spf)

        if not any(x in show_poster_files for x in existing_files):
            try:
                show_poster_url = graphql_data["data"]["Program"]["image"]
                file_type = httpx.head(show_poster_url).headers['Content-Type'].split("/")[1]
            
                file_name = "show." + file_type
                file_path = show_config["dl_folder"] + "/" + file_name

                urllib.request.urlretrieve(show_poster_url,file_path)

            

            except Exception as e:
                print("Unable to get poster for show: " + show_name)
                print(e)
        


    
    for episode in episodes:
        already_downloaded = False
        ep_title = episode["title"]

        existing_files = os.listdir(show_config["dl_folder"])
        files_to_analyze = [ ]

        if "identifier" in show_config:


            if show_config["identifier"] == "NAME":
                match_pattern = ep_title
            elif show_config["identifier"] == "ID":
                match_pattern = episode["id"]
            else:
                match_pattern = False

        for file in existing_files:
            if match_pattern:
                if match_pattern in file:
                    already_downloaded = True
            if filename_front in file:
                files_to_analyze.append(file)

        ep_nums = [ 1 ]
        if len(files_to_analyze) > 0:
            for file in files_to_analyze:

                try:
                    ep_num = file.split("-")[1].strip()
                except Exception as e:
                    print(e)

                if "e" in ep_num.lower():
                    ep_num = re.split("e", ep_num, flags=re.IGNORECASE)[1]

                try:
                    ep_num = int(ep_num)
                    ep_nums.append(ep_num)
                except Exception as e:
                    print("Unable to determine s{NUM}e{NUM} of file: " + file)

            

        ep_num = max(ep_nums)
        ep_num += 1
        filename = show_config["filename"]

        
        if "{NAME}" in filename:
            filename = filename.replace("{NAME}",ep_title)
        if "{NUM}" in filename:
            filename = filename.replace("{NUM}",str(ep_num))
        if "{ID}" in filename:
            filename = filename.replace("{ID}",episode["id"])

        full_file_path = show_config["dl_folder"] + "/" + filename


        show_url = show_config["show_url"]
        if not show_url.endswith("/"):
            show_url = show_url + "/"
        episode_url = show_url + episode["id"]



        if not already_downloaded:
            print("Downloading episode".ljust(30) + show_name.ljust(30) + ep_title.ljust(20) )
            download_episode(episode_url,full_file_path,show_config,episode)
        else:
            print("Episode already downloaded".ljust(30) + show_name.ljust(30) + ep_title.ljust(20) )


	
def print_help():

    print("\nWrong Usage.\nUsage is:")
    print(sys.argv[0] + " <download|.....>")
    print("\n..... currently there is only download ...\n")







if __name__ == "__main__":
    kvs = manage_kvs()

    config_file = script_dir + "/config.py"

    if not os.path.exists(config_file):
        print("")
        print("config.py not found")
        print("look at config.py.example to create a config.py file")
        print("")
        exit(1)

    try:
        from config import *
    except Exception as e:
        print("!!!UNABLE TO IMPORT CONFIG!!!")
        print("Error is:")
        print(e)
        exit()

    download_posters = False
    stop_on_fail = False


    if 'SETTINGS' in locals():
        if "download_posters" in SETTINGS:
            if SETTINGS["download_posters"]:
                try:
                    import httpx
                    download_posters = True
                except:
                    print("\n-------------------------")
                    print("Unable to import httpx, posters will not be downloaded")
                    print("Install httpx to fix this ( pip install httpx")
                    print("-------------------------\n")

        if "stop_on_fail" in SETTINGS:
            stop_on_fail = SETTINGS["stop_on_fail"]





    if len(sys.argv) != 2:
        print_help()
        exit(1)

    if "download" in sys.argv[1].lower():

        from config import *


        for show in shows:
            try:
                download_show(show)
            except Exception as e:
                print(e)
                print("Error with   " + show["show_id"])
                if stop_on_fail:
                    print("STOP ON FAIL ENABLED\nExiting")
                    exit(1)

    else:
        print_help()
        exit(1)



