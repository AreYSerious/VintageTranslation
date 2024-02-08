### Revisited and first tests worked

import shutil
import time
import crowdin_api.exceptions
from crowdin_api import CrowdinClient
import json
import time
import os
import wget
import zipfile
import glob
import shutil


# Crowdin Project Id
project_id = 497567
crowdintoken = "6b453cab0052429b4498f637fff52c8bcfc5a873a387139adf5ae82dbbf7ad970176f23dcaba7e05"

class FirstCrowdinClient(CrowdinClient):
    TOKEN = crowdintoken
    TIMEOUT = 60  # Optional, sets http request timeout.
    RETRY_DELAY = 0.1  # Optional, sets the delay between failed requests
    MAX_RETRIES = 5  # Optional, sets the number of retries
    HEADERS = {"Some-Header": ""}  # Optional, sets additional http request headers
    PAGE_SIZE = 500  # Optional, sets default page size



crowdin_client = FirstCrowdinClient()


def storages__list():
    try:
        store = crowdin_client.storages.list_storages()
        #print(store)
    except crowdin_api.exceptions.CrowdinException as e:
        print(f"Error listing storages: {e}")

def directories__list():
    try:
        directs = crowdin_client.source_files.list_directories(projectId=project_id)
        #print(directs)
    except crowdin_api.exceptions.CrowdinException as e:
        print(f"Error listing directories: {e}")

def adding_a_file(file_name):
    try:
        with open(file_name, 'rb') as file:
            storage = crowdin_client.storages.add_storage(file)
            crowdin_client.source_files.add_file(project_id, storage['data']['id'], file_name)
    except crowdin_api.exceptions.CrowdinException as e:
        print(f"Error adding file: {e}")


def updating_a_file(file_name):
    try:
        files_list = crowdin_client.source_files.list_files(project_id)
        file_data = next((f for f in files_list["data"] if f["data"]["name"] == file_name), None)

        if file_data:
            file_id = file_data["data"]["id"]
            with open(file_name, 'rb') as file:
                storage = crowdin_client.storages.add_storage(file)
                crowdin_client.source_files.update_file(project_id, file_id, storage['data']['id'], updateOption="keep_translations_and_approvals")
    except crowdin_api.exceptions.CrowdinException as e:
        print(f"Error updating file: {e}")



def building_file(filename, downloaded_zip):
    # Extract language IDs from project progress
    project_progress = crowdin_client.translation_status.get_project_progress(project_id)
    language_id_list = [data["data"]["languageId"] for data in project_progress["data"]]

    # Extract file names and file IDs
    files = crowdin_client.source_files.list_files(project_id)
    file_names, file_ids = zip(*[(file["data"]["name"], file["data"]["id"]) for file in files["data"]])

    try:
        index_file_names = file_names.index(filename)
    except ValueError:
        print("Issue with the Filename. Couldn't find it in the list of files. Maybe inputed the wrong name.")
        return

    actual_file_id = file_ids[index_file_names]

    # Extract files from zip
    with zipfile.ZipFile(downloaded_zip, 'r') as zip_ref:
        zip_ref.extractall("unzipped")

    # Create or clear export directory
    export_dir = "export"
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.mkdir(export_dir)

    # Copy specific files to export directory
    for lang_id in language_id_list:
        specific_filepath = glob.glob(f"unzipped/{lang_id}/{filename}")
        if specific_filepath:
            shutil.copyfile(specific_filepath[0], f"{export_dir}/{lang_id}.json")

    # Rename files in export directory for consistency
    for filepath in glob.iglob(f'{export_dir}/*'):
        new_name = filepath.lower()
        os.rename(filepath, new_name)

    # Remove empty JSON files
    for filepath in glob.iglob(f'{export_dir}/*'):
        delete_file = False
        with open(filepath, encoding="utf-8-sig") as file:
            if not json.load(file):
                delete_file = True
        if delete_file:
            os.remove(filepath)

    # Create a zip archive of the export directory
    shutil.make_archive(filename[:-5], 'zip', export_dir)

    # Clean up
    #time.sleep(1)
    shutil.rmtree(export_dir)
    shutil.rmtree("unzipped")
    print("Finished Building and Downloading.")

def cleanup_folder(folder):
    """ Remove all files and subdirectories in the specified folder. """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')





# Folder name
folder_name = "translated_exports"

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created.")
else:
    print(f"Folder '{folder_name}' already exists.")


# Ensure folder exists
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
else:
    # Clean up the folder before starting the script
    cleanup_folder(folder_name)


os.chdir(folder_name)

# Building the crowdin project
build = crowdin_client.translations.build_project_translation(projectId=project_id, request_data={"skipUntranslatedStrings": True, "exportApprovedOnly": False})

# Getting the Id of the latest build for downloading
builds_list = crowdin_client.translations.list_project_builds(projectId=project_id)
latest_build = builds_list['data'][0]['data']['id']

# Downloading project translations
download = None
for _ in range(40):  # 40 attempts
    try:
        download = crowdin_client.translations.download_project_translations(projectId=project_id, buildId=latest_build)
        if "data" in download and "url" in download["data"]:
            break
    except:
        pass
    time.sleep(2)

if not download:
    print("Failed to download project translations.")
    exit()

download_url = download["data"]["url"]
downloaded_zip = wget.download(download_url)

# Listing file names
files = crowdin_client.source_files.list_files(project_id)
file_names_list = [file["data"]["name"] for file in files["data"]]
print(file_names_list)
print(len(file_names_list))

# Processing each file
for filename in file_names_list:
    building_file(filename, downloaded_zip)

# Cleaning up folders and files
folders_to_clean = ["export", "unzipped"]
files_to_clean = [downloaded_zip, "export/pt-br.json"]

for folder in folders_to_clean:
    if os.path.exists(folder):
        shutil.rmtree(folder)

for file in files_to_clean:
    if os.path.exists(file):
        os.remove(file)