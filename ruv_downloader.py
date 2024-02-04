import requests
import json
import dbm
import time
from yt_dlp import YoutubeDL
import os
import sys
import re





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

        





def pprint(msg):
    try:
        print(json.dumps(msg,indent=2))
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
    #kvs.write("filename_tmp",json.dumps(filename))

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


    episodes = kvs.read("_graphql_cache-" + show_id)["data"]["Program"]["episodes"]
    

    filename_front = show_config["filename"].split("-")[0]
    filename_mid = show_config["filename"].split("-")[1].split("{")[0]


    show_name = kvs.read("_graphql_cache-" + show_id)["data"]["Program"]["title"]





    
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
                    print(e)

            

        ep_num = max(ep_nums)
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

    from config import *

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

    else:
        print_help()
        exit(1)



