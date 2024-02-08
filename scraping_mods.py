### Notes:
### Revisited: Added Json5 compatibility


import json
import json5
import time
import datetime
import requests
import os
import wget
import zipfile
import shutil
import traceback

# Configuration
BASE_URL = "http://mods.vintagestory.at/api"
DOWNLOAD_BASE_URL = "https://mods.vintagestory.at/download?fileid="
ORDER_BY_LAST_RELEASED = "/mods?orderby=lastreleased"
MODE = "endless"  # Options: "2 days", "endless", or other specific modes
AMOUNT_OF_MODS = 200  # Options: "endless" or a specific number
CONVERT_JSON5_TO_JSON = True  # Set to False to disable conversion



# Utility Functions

def clear_folder(folder_path):
    """Empties all contents of a specified folder.

    Args:
    folder_path (str): The path of the folder to be cleared.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def delete_folder(folder_name):
    try:
        shutil.rmtree(folder_name)
    except FileNotFoundError:
        pass


def make_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder {folder_name}: {e}")


def write_list_to_json(data_list, filename):
    try:
        with open(filename, "w") as file:
            json.dump(data_list, file)
    except IOError as e:
        print(f"Error writing to {filename}: {e}")


def read_json_to_list(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json5.load(file)
        except json5.JSONDecodeError as e:
            print(f"JSON5 decode error in {filename}: {e}")
            return []
    except IOError as e:
        print(f"Error reading from {filename}: {e}")
        return []


# Fetch Mod Information
def fetch_mod_information():
    response = requests.get(BASE_URL + ORDER_BY_LAST_RELEASED)
    if response.status_code != 200:
        print("Failed to fetch mod information")
        return []

    data = response.json()
    if AMOUNT_OF_MODS == "endless":
        return data["mods"]
    else:
        return data["mods"][:int(AMOUNT_OF_MODS)]


# Filter Mods Based on Mode
def filter_mods(mods):
    if MODE != "2 days":
        return [mod["modid"] for mod in mods]

    mod_ids = []
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    for mod in mods:
        try:
            last_released = datetime.datetime.strptime(mod["lastreleased"].split(" ")[0], '%Y-%m-%d').date()
            if last_released in [today, yesterday]:
                mod_ids.append(mod["modid"])
        except (KeyError, ValueError):
            print("Error parsing last release date for a mod.")

    return mod_ids


# Fetch and Download Mods
def fetch_and_download_mods(mod_ids):
    file_ids = []
    for mod_id in mod_ids:
        try:
            response = requests.get(f"{BASE_URL}/mod/{mod_id}")
            if response.status_code == 200:
                file_id = response.json()["mod"]["releases"][0]["fileid"]
                file_ids.append(file_id)

                download_and_extract_mod(file_id)
            else:
                print(f"Failed to fetch file ID for mod {mod_id}")
        except KeyError:
            print(f"Error processing mod {mod_id}")

    return file_ids


# Download and Extract Mod
def download_and_extract_mod(file_id):
    delete_folder("temp_extract")
    make_folder("temp_extract")
    make_folder("mod_downloads")

    mod_download_url = f"{DOWNLOAD_BASE_URL}{file_id}"
    download_path = f"mod_downloads/id{file_id}.zip"

    try:
        wget.download(mod_download_url, out=download_path)
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall("temp_extract")
        process_downloaded_mod(file_id)
    except Exception as e:
        print(f"Error downloading or extracting mod {file_id}: {e}")


# Process Downloaded Mod
def process_downloaded_mod(file_id):
    try:
        mod_info = read_json_to_list("temp_extract/modinfo.json")
        mod_author = extract_mod_author(mod_info)
        mod_name = mod_info.get("name", mod_info.get("Name", "Unknown"))
        mod_id = mod_info.get("modid", mod_info.get("ModID", "Unknown"))

        lang_files_exist = copy_language_files(mod_id)
        rename_and_move_language_file(mod_id, mod_author, lang_files_exist)
    except Exception as e:
        print(f"Error processing mod {file_id}: {e}")
        traceback.print_exc()
    finally:
        delete_folder("temp_extract")


# Extract Mod Author
def extract_mod_author(mod_info):
    author = mod_info.get("authors", mod_info.get("Authors", mod_info.get("author", mod_info.get("Author", []))))
    if isinstance(author, list) and author:
        return author[0]
    return author


# Copy Language Files
def copy_language_files(mod_id):
    lang_folder_path = f"temp_extract/assets/{mod_id.lower()}/lang"
    if os.path.exists(lang_folder_path) and os.listdir(lang_folder_path):
        make_folder(f"translatedlangfiles/{mod_id.lower()}")
        shutil.copytree(lang_folder_path, f"translatedlangfiles/{mod_id.lower()}", dirs_exist_ok=True)
        return True
    else:
        print(f"No language files found for mod {mod_id}")
        return False




def rename_and_move_language_file(mod_id, mod_author, lang_files_exist):
    if not lang_files_exist:
        return

    try:
        src = f"temp_extract/assets/{mod_id.lower()}/lang/en.json"
        dst = f"mod_langfiles/{mod_id.lower()}-{mod_author.lower()}.json"
        make_folder("mod_langfiles")

        if os.path.exists(src):
            shutil.move(src, dst)
        else:
            print(f"No English language file found for mod {mod_id}")
    except FileNotFoundError:
        print(f"No English language file found for mod {mod_id}")

def convert_json5_to_json(json5_filepath, json_filepath):
    try:
        with open(json5_filepath, 'r', encoding='utf-8') as file:
            data = json5.load(file)

        with open(json_filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error converting file {json5_filepath}: {e}")

def convert_all_json5_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json5_filepath = os.path.join(folder_path, filename)
            json_filepath = os.path.join(folder_path, filename)
            convert_json5_to_json(json5_filepath, json_filepath)

# Main Execution
def main():
    clear_folder("mod_downloads")
    mods = fetch_mod_information()
    mod_ids = filter_mods(mods)
    file_ids = fetch_and_download_mods(mod_ids)
    write_list_to_json(file_ids, "fileid_list.json")

    if CONVERT_JSON5_TO_JSON:
        convert_all_json5_in_folder("mod_langfiles")

    print("\nDone with script execution")


if __name__ == "__main__":
    main()
