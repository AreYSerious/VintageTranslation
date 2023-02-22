import shutil
import time
import crowdin_api.exceptions
from crowdin_api import CrowdinClient
import os
import json
import time
import os
import wget
import zipfile
import glob
import shutil



crowdintoken = "6b453cab0052429b4498f637fff52c8bcfc5a873a387139adf5ae82dbbf7ad970176f23dcaba7e05"

class FirstCrowdinClient(CrowdinClient):
    TOKEN = crowdintoken
    TIMEOUT = 60  # Optional, sets http request timeout.
    RETRY_DELAY = 0.1  # Optional, sets the delay between failed requests
    MAX_RETRIES = 5  # Optional, sets the number of retries
    HEADERS = {"Some-Header": ""}  # Optional, sets additional http request headers
    PAGE_SIZE = 500  # Optional, sets default page size

crowdin_client = FirstCrowdinClient()

# Crowdin Project Id
project_id = 497567

def storages__list():
    # Get a list of Storages
    store = crowdin_client.storages.list_storages()
    print(store)

def directories__list():
    # Get a list of Directories
    directs = crowdin_client.source_files.list_directories(projectId=project_id)
    print(directs)

def adding_a_file(file_name):
    # Uploads the file to storage and after that adds it to the project
    storage = crowdin_client.storages.add_storage(open(file_name, 'rb'))
    my_file = crowdin_client.source_files.add_file(project_id, storage['data']['id'], file_name)

def updating_a_file(file_name):
    # checks existing files and tries to update the existing one
    filName_list = []
    filId_list = []

    list__files = crowdin_client.source_files.list_files(project_id)
    number_of_files_in_project = len(list__files["data"])
    #print(list__files)
    for x in range(number_of_files_in_project):
        filName = list__files["data"][x]["data"]["name"]
        filId = list__files["data"][x]["data"]["id"]
        #print(str(filName) + " has the Id: " + str(filId))
        filName_list.append(filName)
        filId_list.append(filId)

    index_filName = filName_list.index(file_name)
    filename_id = filId_list[index_filName]

    storage = crowdin_client.storages.add_storage(open(file_name, 'rb'))

    crowdin_client.source_files.update_file(project_id, filename_id, storage['data']['id'], updateOption="keep_translations_and_approvals")





def building_file(filename, download_zip):
    # Gets the project progress to extract all lang ids from it.
    project_progress = crowdin_client.translation_status.get_project_progress(project_id)
    language_id_list = []
    # Saves all lang ids in this project to language_id_list
    for x in range(len(project_progress["data"])):
        lang_id = project_progress["data"][x]["data"]["languageId"]
        language_id_list.append(lang_id)


    # Gets the files in the project to extract file_names and file_ids from it.
    files = crowdin_client.source_files.list_files(project_id)
    file_names = []
    file_ids = []
    for x in range(len(files["data"])):
        file_names.append(files["data"][x]["data"]["name"])
        file_ids.append(files["data"][x]["data"]["id"])
    #print(file_names)
    #print(file_ids)

    try:
        index_file_names = file_names.index(filename)
    except:
        print("Issue with the Filename. Couldn't find it in the list of files. Maybe inputed the wrong name.")


    actual_file_id = file_ids[index_file_names]
    #print(actual_file_id)





    with zipfile.ZipFile(downloaded_zip, 'r') as zip_ref:
        zip_ref.extractall("unzipped")


    try:
        os.mkdir("export")
    except:
        shutil.rmtree("export")
        os.mkdir("export")




    for x in range(len(project_progress["data"])):
        specific_filepath = glob.glob("unzipped/"+ language_id_list[x] +"/" + filename)
        #print("Specific Filepath: " + str(specific_filepath))
        if specific_filepath == []:
            pass # is Empty
        else:
            shutil.copyfile(specific_filepath[0], "export/" + language_id_list[x] + ".json")


    directoryx = "export"


    for filenamex in glob.iglob(f'{directoryx}/*'):
        # Windows
        if filenamex == "export\es-ES.json":
            os.rename(filenamex, "export\es-es.json")
        if filenamex == "export\pt-BR.json":
            os.rename(filenamex, "export\pt-br.json")
        if filenamex == "export\sv-SE.json":
            os.rename(filenamex, "export\sv-se.json")
        if filenamex == "export\zh-CN.json":
            os.rename(filenamex, "export\zh-cn.json")
        # Linux
        if filenamex == "export/es-ES.json":
            os.rename(filenamex, "export/es-es.json")
        if filenamex == "export/pt-BR.json":
            os.rename(filenamex, "export\pt-br.json")
        if filenamex == "export/sv-SE.json":
            os.rename(filenamex, "export/sv-se.json")
        if filenamex == "export/zh-CN.json":
            os.rename(filenamex, "export/zh-cn.json")


    for filenamex in glob.iglob(f'{directoryx}/*'):
        #print(filenamex)
        filex = open(filenamex, encoding="utf-8-sig")
        filex_content = json.load(filex)
        #print(filex_content)
        filex.close()
        if filex_content == {}:
            os.remove(filenamex)


    shutil.make_archive(filename[:-5], 'zip', "export")





    time.sleep(1)
    shutil.rmtree("export")
    shutil.rmtree("unzipped")

    #os.remove(filename[:-5] + ".zip")
    print("Finished Building and Downloading.")




os.chdir("translated_exports")

# Building the crowdin project
build = crowdin_client.translations.build_project_translation(projectId=project_id, request_data={"skipUntranslatedStrings": True, "skipUntranslatedFiles": False, "exportApprovedOnly": False})

# Getting the Id of the latest build for downloading
builds_list = crowdin_client.translations.list_project_builds(projectId=project_id)
latest_build = builds_list['data'][0]['data']['id']




#download = crowdin_client.translations.download_project_translations(projectId=project_id, buildId=latest_build)
#print(download)

counter1 = 40
val1 = False
while val1 == False:
    download = crowdin_client.translations.download_project_translations(projectId=project_id, buildId=latest_build)
    #print(download)
    counter1 = counter1 - 1
    if counter1 == 0:
        val1 = True
    try:
        download_url = download["data"]["url"]
        val1 = True
    except:
        time.sleep(2)





download_url = download["data"]["url"]
#print(download_url)

downloaded_zip = wget.download(download_url)
#print(downloaded_zip)


files = crowdin_client.source_files.list_files(project_id)
file_names_list = []
for x in range(len(files["data"])):
    file_names_list.append(files["data"][x]["data"]["name"])
print(file_names_list)
print(len(file_names_list))







for x in range(len(file_names_list)):
    building_file(file_names_list[x], downloaded_zip)



# Cleaning up folders
try:
    os.remove("export")
except:
    ""
try:
    os.remove("unzipped")
except:
    ""
try:
    os.remove(downloaded_zip)
except:
    ""
try:
    os.remove("export \\ pt-br.json")
except:
    ""
try:
    os.remove("export\\pt-br.json")
except:
    ""