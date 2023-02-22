import crowdin_api.exceptions
from crowdin_api import CrowdinClient
import os

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



def uploading_or_updating(filename):

    try:
        adding_a_file(filename)
        print("Added a file.")

    except crowdin_api.exceptions.ValidationError as err:
        s = str(err)
        print(s)
        # Checks the error message to specify the Error

        # First Check: Checks if the Name of the file is already given.
        if s.__contains__("Invalid name given. Name must be unique") or s.__contains__("already exists in this folder"):
            # print("Error: Invalid name given. Name must be unique.")
            # If the file is already existing the user gets asked if he wants to really add a file or update an existing file
            updating_a_file(filename)
        # Second Check: Checks if the Json Syntax is correct.
        elif s.__contains__("Incorrect json in request body. Syntax error"):
            print("Incorrect Json.")


def renaming_filename(filename):
    try:
        renamedversion = str(filename).replace("#","").replace("%","").replace("&","").replace("{","").replace("}","").replace("\\","").replace("<","").replace(">","").replace("*","").replace("?","").replace("/","").replace(" ","").replace("$","").replace("!","").replace("'","").replace('"',"").replace(":","").replace("@","").replace("`","").replace("|","").replace("=","").replace(" ","")
        os.rename(filename,renamedversion)
    except:
        ""



# assign directory
directory_uploads = 'mod_langfiles'

# iterate over files in
# that directory
dirc_list = []
for filename in os.listdir(directory_uploads):
    f = os.path.join(directory_uploads, filename)
    # checking if it is a file
    if os.path.isfile(f):
        dirc_list.append(filename)

os.chdir("mod_langfiles")
print(dirc_list)

for x in range(len(dirc_list)):

    try:
        renamedversion = str(dirc_list[x]).replace("#","").replace("%","").replace("&","").replace("{","").replace("}","").replace("\\","").replace("<","").replace(">","").replace("*","").replace("?","").replace("/","").replace(" ","").replace("$","").replace("!","").replace("'","").replace('"',"").replace(":","").replace("@","").replace("`","").replace("|","").replace("=","").replace(" ","")
        os.rename(dirc_list[x],renamedversion)
        filename = renamedversion
        uploading_or_updating(dirc_list[x])
    except:
        ""

    print("Uploaded or updated: " + str(dirc_list[x]))

print(" ")
print(" ")
print("Done with test.py")
print(" ")
print(" ")



