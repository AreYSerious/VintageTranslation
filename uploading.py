import crowdin_api.exceptions
from crowdin_api import CrowdinClient
import os

crowdintoken = "6b453cab0052429b4498f637fff52c8bcfc5a873a387139adf5ae82dbbf7ad970176f23dcaba7e05"
project_id = 497567
directory_uploads = 'mod_langfiles'

class FirstCrowdinClient(CrowdinClient):
    TOKEN = crowdintoken
    TIMEOUT = 60  # Optional, sets http request timeout.
    RETRY_DELAY = 0.1  # Optional, sets the delay between failed requests
    MAX_RETRIES = 5  # Optional, sets the number of retries
    HEADERS = {"Some-Header": ""}  # Optional, sets additional http request headers
    PAGE_SIZE = 500  # Optional, sets default page size


crowdin_client = FirstCrowdinClient()


def list_storages():
    """
    Get and print a list of storages from Crowdin.
    """
    try:
        storages = crowdin_client.storages.list_storages()
        #print(storages)
    except Exception as e:
        print(f"Error fetching storages: {e}")


def list_directories(project_id):
    """
    Get and print a list of directories for a given project in Crowdin.

    Args:
    project_id (str): The project ID for which directories are listed.
    """
    try:
        directories = crowdin_client.source_files.list_directories(projectId=project_id)
        #print(directories)
    except Exception as e:
        print(f"Error fetching directories for project {project_id}: {e}")


def add_file(file_name):
    """
    Uploads a file to storage and then adds it to the Crowdin project.

    Args:
    file_name (str): The name of the file to be uploaded.
    """
    try:
        with open(file_name, 'rb') as file:
            storage = crowdin_client.storages.add_storage(file)
        my_file = crowdin_client.source_files.add_file(project_id, storage['data']['id'], file_name)
    except Exception as e:
        print(f"Error adding file {file_name}: {e}")



def update_file(file_name):
    """
    Checks existing files in the Crowdin project and updates the specified file if it exists.

    Args:
    file_name (str): The name of the file to be updated.
    """
    try:
        files_list = crowdin_client.source_files.list_files(project_id)
        file_names = [file["data"]["name"] for file in files_list["data"]]
        file_ids = [file["data"]["id"] for file in files_list["data"]]

        if file_name in file_names:
            file_index = file_names.index(file_name)
            file_id = file_ids[file_index]

            with open(file_name, 'rb') as file:
                storage = crowdin_client.storages.add_storage(file)

            crowdin_client.source_files.update_file(
                project_id, file_id, storage['data']['id'],
                updateOption="keep_translations_and_approvals"
            )
        else:
            print(f"File {file_name} not found in project.")
    except Exception as e:
        print(f"Error updating file {file_name}: {e}")


def uploading_or_updating(filename):
    """
    Tries to upload a file, and if it already exists, updates it.

    Args:
    filename (str): The name of the file to be uploaded or updated.
    """
    try:
        add_file(filename)
        #print("Added a file.")
    except crowdin_api.exceptions.ValidationError as err:
        error_message = str(err)
        print(error_message)

        # Check if the file name already exists
        if "Invalid name given. Name must be unique" in error_message or "already exists in this folder" in error_message:
            print("File already exists, updating the file.")
            update_file(filename)
        elif "Incorrect json in request body. Syntax error" in error_message:
            print("Incorrect JSON format in the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def renaming_filename(filename):
    """
    Renames a file by removing specific special characters.

    Args:
    filename (str): The original file name.

    Returns:
    str: The renamed file name or an empty string if an error occurred.
    """
    try:
        chars_to_remove = "#%&{}\\<>?/$!'\":@`|="
        renamed_version = filename.translate({ord(c): None for c in chars_to_remove})
        os.rename(filename, renamed_version)
        return renamed_version
    except Exception as e:
        return ""





# iterate over files in that directory
dirc_list = [f for f in os.listdir(directory_uploads) if os.path.isfile(os.path.join(directory_uploads, f))]

os.chdir(directory_uploads)
print(dirc_list)

for filename in dirc_list:
    try:
        # Use the renaming_filename function here
        renamed_version = renaming_filename(filename)
        if renamed_version:
            uploading_or_updating(renamed_version)
            print(f"Uploaded or updated: {renamed_version}")
        else:
            print(f"Failed to rename: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nUploading completed.")