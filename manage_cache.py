#!/usr/bin/env python

import requests
import json
import dbm
import os
import sys
import re
import os 
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
from ruv_downloader import manage_kvs, pprint
kvs = manage_kvs()



def print_help():
    print()
    print("usage is: ")
    print(sys.argv[0] + " <list|get|delete> [key] ")
    print()
    print(sys.argv[0] + " list                  # lists all keys in cache")
    print(sys.argv[0] + " get {name-of-key}     # prints out the information of that key")
    print(sys.argv[0] + " delete {name-of-key}  # delete a key")
    print()




if len(sys.argv) == 1:
    print_help()
    exit()


arg_1 = sys.argv[1].lower()

if arg_1 == "list":
    kvs.list_keys(True)
elif arg_1 == "get":
    if len(sys.argv) != 3:
        print_help()
        exit()

    key = sys.argv[2]

    if kvs.exists(key):
        key_data, is_json = kvs.decode_key(key)
        if is_json:
            pprint(key_data,False)
        else:
            print(key_data)

    else:
        print("Key " + key + " does not exist")

elif arg_1 == "delete":
    if len(sys.argv) != 3:
        print_help()
        exit()


    key = sys.argv[2]

    kvs.delete_key(key)

else:
    print_help()
    exit()


