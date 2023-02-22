import json
import time
import traceback
import datetime
import requests
import os
import wget
import zipfile
import shutil
from distutils.dir_util import copy_tree

mode = "2 days" #2 days
setting_amount_of_mods = "endless"



def del_folder(foldername):
    try:
        shutil.rmtree(foldername)
    except:
        ""

def make_folder(foldername):
    try:
        os.mkdir(foldername)
    except:
        ""



def write_list(a_list, filename):
    print("Started writing list data into a json file")
    with open(filename, "w") as fp:
        json.dump(a_list, fp)
        print("Done writing JSON data into .json file")

# Read list to memory
def read_list(filename):
    # for reading also binary mode is important
    with open(filename, 'rb') as fp:
        n_list = json.load(fp)
        return n_list




base_url = "http://mods.vintagestory.at/api"
download_base_url = "https://mods.vintagestory.at/download?fileid="

url_additon = "/mods?orderby=lastreleased"


input = "NiclAss"
discordusername = "Niclas"


api_response = requests.get(base_url + url_additon)

api_response_json = api_response.json()

if setting_amount_of_mods == "endless":
    amount_of_mods = len(api_response_json["mods"])
else:
    amount_of_mods = setting_amount_of_mods

modid_list = []
for x in range(amount_of_mods):
    if mode == "2 days":

        try:
            lastreleased = api_response_json["mods"][x]["lastreleased"]

            date_format = '%Y-%m-%d'

            split_string1 = lastreleased.split(" ")
            split_string2 = split_string1[0].split("-")
            inputdate = split_string2[0] + "-" + split_string2[1] + "-" + split_string2[2]
            #print(inputdate)

            dateatm = time.localtime()
            formated_dateatm = str(dateatm.tm_year) + "-" + str(dateatm.tm_mon) + "-" + str(dateatm.tm_mday)
            #print(formated_dateatm)

            last_day = datetime.datetime.strptime(formated_dateatm, date_format) - datetime.timedelta(days=1)
            formated_last_day = str(last_day.strftime(date_format))
            #print(formated_last_day)

            if inputdate == formated_dateatm:
                print("From today.")
                modid_list.append(api_response_json["mods"][x]["modid"])
            if inputdate == formated_last_day:
                print("From yesterday.")
                modid_list.append(api_response_json["mods"][x]["modid"])

        except:

            print("Error while trying to get lastreleased date.")


    else:
        try:
            modid_list.append(api_response_json["mods"][x]["modid"])
        except:
            print("Error while trying to get lastreleased date.")
print(modid_list)






#
#
#



fileid_list = []
for y in range(len(modid_list)):
    try:
        fileid_response = requests.get(base_url + "/mod/" + str(modid_list[y]))
        fileid_response_json = fileid_response.json()
        fileid_list.append(fileid_response_json["mod"]["releases"][0]["fileid"])
    except:
        print("Error: No release found.")

print(fileid_list)
write_list(fileid_list, "fileid_list.json")



#
#
#

del_folder("mod_downloads")

localsaved_fileid_list = read_list("fileid_list.json")
len_localsaved_fileid_list = len(localsaved_fileid_list)

for z in range(len_localsaved_fileid_list):
    del_folder("temp_extract")
    make_folder("temp_extract")
    make_folder("mod_downloads")

    mod_download_url = download_base_url + str(localsaved_fileid_list[z])
    #print(mod_download_url)
    path = "mod_downloads"+os.sep+"id" + str(localsaved_fileid_list[z]) + ".zip"
    wget.download(mod_download_url, out=path)



    try:
        with zipfile.ZipFile("mod_downloads"+os.sep+"id" + str(localsaved_fileid_list[z]) + ".zip", 'r') as zip_ref:
            zip_ref.extractall("temp_extract")
    except:
        "File is not a zipfile!"


    try:
        temp_json = read_list("temp_extract"+os.sep+"modinfo.json")
    except:
        print("Error while trying to open modinfo.json")
    try:
        modauthor = ""
        modauthor = temp_json["authors"][0]
    except:
        try:

            modauthor = temp_json["Authors"]
            print(modauthor)
        except:
            try:

                modauthor = temp_json["author"]
                print(modauthor)
            except:
                try:

                    modauthor = temp_json["Author"]
                    print(modauthor)
                except:
                    print(modauthor)

    #print(type(modauthor))
    if type(modauthor) == list:
        modauthor = modauthor[0]


    try:
        modname = ""
        modname = temp_json["name"]
        print(modname)
    except:
        try:
            modname = ""
            modname = temp_json["Name"]
        except:
            print("No modname found.")

    try:
        modid = ""
        modid = temp_json["modid"]
        print(modid)
    except:
        try:
            modid = ""
            modid = temp_json["ModID"]
        except:
            print("No modid found.")


    try:
        os.mkdir("translatedlangfiles"+os.sep + str(modid).lower())

        copy_tree("temp_extract"+os.sep+"assets"+os.sep + str(modid).lower() + os.sep+"lang"+os.sep,"translatedlangfiles"+os.sep + str(modid).lower() + os.sep)
    except:
        print("Failed to create tranlatedlangfiles.")



    try:
        os.rename("temp_extract"+os.sep+"assets"+os.sep + str(modid).lower() + os.sep+"lang"+os.sep+"en.json", "temp_extract"+os.sep+"assets"+os.sep + str(modid).lower() + os.sep+"lang"+os.sep + str(modid).lower() + "-" + str(modauthor).lower() + ".json")




        shutil.copy("temp_extract"+os.sep+"assets"+os.sep + str(modid).lower() + os.sep+"lang"+os.sep+ str(modid).lower() + "-" + str(modauthor).lower() + ".json", "mod_langfiles"+ os.sep)
        del_folder("temp_extract")

    except Exception:
        traceback.print_exc()
        del_folder("temp_extract")



print(" ")
print(" ")
print("Done with call.py")
print(" ")
print(" ")



