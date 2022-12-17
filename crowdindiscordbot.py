from __future__ import unicode_literals

import json
import time
import urllib.request
import os
import wget
import zipfile
import glob
import shutil

from nextcord.ext import commands
from nextcord import *
import nextcord

import crowdin_api.exceptions
from crowdin_api import CrowdinClient

# Gets the bot token from a seperate file called BotToken.py that looks like this:
# token = "insert_your_token_here"
# crowdintoken = "insert_your_crowdintoken_here"
from BotToken import token
from BotToken import crowdintoken


# invite Link for dc bot:
# https://nextcord.com/api/oauth2/authorize?client_id=949725454477168661&permissions=140123630656&scope=applications.commands%20bot


testingserverid = [910242831103320064]

class FirstCrowdinClient(CrowdinClient):
    TOKEN = crowdintoken
    TIMEOUT = 60  # Optional, sets http request timeout.
    RETRY_DELAY = 0.1  # Optional, sets the delay between failed requests
    MAX_RETRIES = 5  # Optional, sets the number of retries
    HEADERS = {"Some-Header": ""}  # Optional, sets additional http request headers
    PAGE_SIZE = 25  # Optional, sets default page size

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

    for x in range(number_of_files_in_project):
        filName = list__files["data"][x]["data"]["name"]
        filId = list__files["data"][x]["data"]["id"]
        # print(str(filName) + " has the Id: " + str(filId))
        filName_list.append(filName)
        filId_list.append(filId)

    index_filName = filName_list.index(file_name)
    filename_id = filId_list[index_filName]

    storage = crowdin_client.storages.add_storage(open(file_name, 'rb'))

    crowdin_client.source_files.update_file(project_id, filename_id, storage['data']['id'], updateOption="keep_translations_and_approvals")



# nextcord Bot Setup

client = commands.Bot(command_prefix="!", help_command=None, activity=nextcord.Game(name="/help"), intents=nextcord.Intents.default())


# Response if ready

@client.event
async def on_ready():
    print("Bot online.")




@client.command() # !addfile command
async def addfile(ctx):
    attachment = ctx.message.attachments[0]
    # gets first attachment that user
    # sent along with command
    # print(attachment.url)
    url = attachment.url

    list1 = str(url).split("/")
    lenlist1 = len(list1)
    callenlist1 = lenlist1 - 1

    file_name = list1[callenlist1]

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    g = urllib.request.urlopen(req)

    with open(file_name, 'b+w') as f:
        f.write(g.read())

    try:
        # Trys to add a file
        adding_a_file(file_name)
        embed3 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                description="**ADDING A FILE**")
        embed3.add_field(
            name="`⏏️` › File upload",
            value="`✅` › Successfully", inline=False)
        embed3.set_image(
            url="https://i.imgur.com/mZLV5Ld.png")

        await ctx.send(embed=embed3)

        time.sleep(1)
        #await ctx.channel.purge(limit=2)

    except crowdin_api.exceptions.ValidationError as err:
        s = str(err)
        print(s)
        # Checks the error message to specify the Error


        # First Check: Checks if the Name of the file is already given.
        if s.__contains__("Invalid name given. Name must be unique"):
            #print("Error: Invalid name given. Name must be unique.")

            # If the file is already existing the user gets asked if he wants to really add a file or update an existing file

            yas = '✅'
            nay = '❌'

            valid_reactions = ['✅', '❌']

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in valid_reactions

            embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                    description="**ADDING A FILE**")
            embed.add_field(name="`📁` › The file you tried to add is already existing or another file has the same name.\n`⚠️`\n`🆕` › If you want to add a new file please change the filename to something unique.\n`⚠️`", value="`🆙` › Otherwise if you want to update your existing file react to this message with ✅.", inline=False)
            embed.set_image(
                url="https://i.imgur.com/29QVHgW.png")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')



            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == yas:
                updating_a_file(file_name)
                embed2 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                        description="**ADDING A FILE**")
                embed2.add_field(
                    name="`⏏️` › File updated",
                    value="`✅` › Successfully", inline=False)
                embed2.set_image(
                    url="https://i.imgur.com/mZLV5Ld.png")
                await ctx.send(embed=embed2)

                time.sleep(10)
                await ctx.channel.purge(limit=3)
            if str(reaction.emoji) == nay:
                embed3 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                        description="**ADDING A FILE**")
                embed3.add_field(
                    name="`❌`",
                    value="**Aborting...**", inline=False)
                embed3.set_image(
                    url="https://i.imgur.com/MGzs1Sh.png")
                await ctx.send(embed=embed3)
                time.sleep(1)
                #await ctx.channel.purge(limit=3)


        # Second Check: Checks if the Json Syntax is correct.
        elif s.__contains__("Incorrect json in request body. Syntax error"):
            #print("Error: Incorrect json in request body. Syntax error.")
            embed1 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                   description="**ADDING A FILE**")
            embed1.add_field(
                name="`⚠️`** › Error**",
                value="`⚠️` › Incorrect json in request body. Syntax error!", inline=False)
            embed1.set_image(
                url="https://i.imgur.com/MGzs1Sh.png")
            await ctx.send(embed=embed1)





@client.slash_command(name="progress", description="Shows the Translation Progress.") # /progress
async def langprogress(interaction: Interaction):
    project_progress = crowdin_client.translation_status.get_project_progress(project_id)
    #print(len(project_progress["data"]))

    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods", description="**LANGUAGE PROGRESS**")
    for x in range(len(project_progress["data"])):
        lang_id = project_progress["data"][x]["data"]["languageId"]

        trans_prog = project_progress["data"][x]["data"]["translationProgress"]

        #
        #
        # Emoji Replacer
        if lang_id == "de":
            lang_id = ":flag_de: German:"
        if lang_id == "cs":
            lang_id = ":flag_cn: Chinese Simplified:"
        if lang_id == "eo":
            lang_id = ":flag_sa: Esperanto:"
        if lang_id == "ar":
            lang_id = ":flag_ae: Arabic:"
        if lang_id == "it":
            lang_id = ":flag_it: Italian:"
        if lang_id == "es-ES":
            lang_id = ":flag_es: Spanish:"
        if lang_id == "fr":
            lang_id = ":flag_fr: French:"
        if lang_id == "ja":
            lang_id = ":flag_jp: Japanese:"
        if lang_id == "pl":
            lang_id = ":flag_pl: Polish:"
        if lang_id == "pt-BR":
            lang_id = ":flag_br: Protuguese, Brazilian:"
        if lang_id == "ru":
            lang_id = ":flag_ru: Russian:"
        if lang_id == "sk":
            lang_id = ":flag_sk: Slovak:"
        if lang_id == "uk":
            lang_id = ":flag_ua: Ukrainian:"
        if lang_id == "nl":
            lang_id = ":flag_nl: Dutch:"
        if lang_id == "sv-SE":
            lang_id = ":flag_se: Swedish:"
        if lang_id == "zh-CN":
            lang_id = ":flag_cn: Chinese Simplified:"



        embed.add_field(name=lang_id, value=str(trans_prog) + "%", inline=False)
    embed.set_image(url="https://i.imgur.com/rDj32iY.png")

    await interaction.response.send_message(embed=embed)


@client.slash_command(name="reqlanguage", description="Requests to add a Language to the Crowdin Project.") # /reqlanguage
async def language(
    interaction: Interaction,
    language_name: str = SlashOption(description="Name of a language", required=True),
):
    msg_writter = interaction.user

    project_url = "https://crowdin.com/project/vintage-story-mods"
    myid = 352405873152229378
    user = await client.fetch_user(myid)
    guild_onserver = interaction.guild.name

    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods", description="User: " + str(msg_writter))
    embed.add_field(name="requested the Language: " + language_name + ".", value="nextcord-Server: " + guild_onserver, inline=False)

    await user.send(embed=embed)




    embed1 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                          description="**LANGUAGE REQUEST**")
    embed1.add_field(name="`🔣` › Request to add the following language has been sent:\n`🔽`\n **" + language_name + "**\n`🔼`", value="`⚠️` › A project manager has to add the language manually. This can take up to 1 day. Please be patient. ❤️", inline=False)
    embed1.set_image(url="https://i.imgur.com/f5pmpzU.png")

    await interaction.response.send_message(embed=embed1)


@client.slash_command(name="addfile", description="Explanation on how to Upload a File for Translation.") # /addfile
async def addfile(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**TUTORIAL ADDING A FILE**")
    embed.add_field(name="`▶️` Enter:", value="› `!addfile` (no space after the command) \n \n`▶️` Press the **+** button to the left to attach a file to the message.\n \n`▶️` Send the message.\n \n`⚠️` The name of the **Filename** should be called something like: \n› ` Modname-Author.supportedformat `\n \n`❓` Supported formats:\nhttps://support.crowdin.com/supported-formats/\n \n`🎞️` **Check out the tutorial video below this message.**", inline=False)
    embed.set_image(url="https://i.imgur.com/I4jNUO7.png")
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=nextcord.File("AddingAFileTutorial.webm"))


@client.slash_command(name="updatefile", description="Explanation on how to update a file for translation.") # /updatefile
async def updatefile(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**TUTORIAL UPDATING A FILE**")
    embed.add_field(name="`▶️` Enter:", value="› `!addfile` (no space after the command) \n \n`▶️` Press the **+** button to the left to attach a file to the message.\n \n`▶️` Send the message.\n \n`▶️` Read the response from the bot and react to the message with ✅ to continue.\n \n`⚠️` The **Filename** has to be the **same name** as the file you want to update!\n`⚠️` You can get a list of all filenames in the project with:\n› ` /filenames `\n \n`⚠️` The name of the **Filename** should something like: \n› ` Modname-Author.supportedformat `\n \n`❓` Supported formats:\nhttps://support.crowdin.com/supported-formats/\n \n`🎞️` **Check out the tutorial video below this message.**", inline=False)
    embed.set_image(url="https://i.imgur.com/SP4FfcN.png")
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=nextcord.File("UpdatingAFileTutorial.webm"))


@client.slash_command(name="help", description="Shows all commands for the VintageTranslation Bot.") # /help
async def help(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                           description="**HELP/COMMANDS**")
    embed.add_field(name="› ` /addfile `", value="`▶️` Explains the usage of the !addfile command and how to upload a file to the project.", inline=False)
    embed.add_field(name="› ` !addfile `", value="`▶️` Uploads a file to the project for translation, can update a file aswell.", inline=False)
    embed.add_field(name="› ` /updatefile `", value="`▶️` Explains the usage of the !addfile command and how to update a file to the project.", inline=False)
    embed.add_field(name="› ` /build `", value="`▶️` Enter your filename to get a .zip with your mods translated files.", inline=False)
    embed.add_field(name="› ` /progress `", value="`▶️` Shows the translation progress of each language.", inline=False)
    embed.add_field(name="› ` /reqlanguage `", value="`▶️` Sends a request to add a language to the project.", inline=False)
    embed.add_field(name="› ` /filenames `", value="`▶️` Lists all filenames on the project.", inline=False)
    embed.add_field(name="› ` /project `", value="`▶️` Shares a link to the Crowdin project.", inline=False)
    embed.set_image(url="https://i.imgur.com/QjbOEQR.png")

    await interaction.response.send_message(embed=embed)


@client.slash_command(name="filenames", description="List of all filenames.") # /filenames
async def listfile(
    interaction: Interaction,
):

    files = crowdin_client.source_files.list_files(project_id)
    #print(files)
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods", description="**LIST OF FILENAMES**")
    list0123 = []
    for x in range(len(files["data"])):
        list0123.append("`📁` › " + files["data"][x]["data"]["name"])

    names = "\n".join(list0123)
    embed.add_field(name="**Filenames:**", value=names, inline=False)
    embed.set_image(url="https://i.imgur.com/oYjqgT7.png")
    await interaction.response.send_message(embed=embed)


@client.slash_command(name="project", description="Shares a link to the Crowdin project.") # /project
async def project(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**PROJECT**")
    embed.add_field(name="`🔗` Use the following link to access the Crowdin project:", value="`▶️` https://crowdin.com/project/vintage-story-mods", inline=False)
    embed.set_image(url="https://i.imgur.com/HENnP5W.png")
    await interaction.response.send_message(embed=embed)


@client.slash_command(name="build", description="Builds the Crowdin project.") # /build
async def build(
    interaction: Interaction,
    filename: str = SlashOption(description="Your Filename", required=True)
):

    #filename = filename +".json"

    project_progress = crowdin_client.translation_status.get_project_progress(project_id)
    language_id_list = []
    for x in range(len(project_progress["data"])):
        lang_id = project_progress["data"][x]["data"]["languageId"]
        language_id_list.append(lang_id)


    list_files = crowdin_client.source_files.list_files(projectId=project_id)
    #print(list_files)

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
        filenameissue_embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                               description="**Build**")
        filenameissue_embed.add_field(name="`⚠️` ! Incorrect filename !",
                        value="`▶️` Use /filenames to see all available filenames.", inline=False)
        filenameissue_embed.set_image(url="https://i.imgur.com/MGzs1Sh.png")
        await interaction.response.send_message(embed=filenameissue_embed)

    actual_file_id = file_ids[index_file_names]
    #print(actual_file_id)

    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                           description="**Build**")
    embed.add_field(name="`🔗` Building the uptodate Project and downloading your mod language files...",
                    value="`▶️` This takes up to 10 seconds pls be patient.", inline=False)
    embed.set_image(url="https://i.imgur.com/axpMy0D.png")
    await interaction.response.send_message(embed=embed)

    build = crowdin_client.translations.build_project_translation(projectId=project_id, request_data={"skipUntranslatedStrings": True, "skipUntranslatedFiles": False, "exportApprovedOnly": False})
    #time.sleep(10)

    builds_list = crowdin_client.translations.list_project_builds(projectId=project_id)
    #print(builds_list)
    latest_build = builds_list['data'][0]['data']['id']




    #download = crowdin_client.translations.download_project_translations(projectId=project_id, buildId=latest_build)
    #print(download)

    counter1 = 20
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

    with zipfile.ZipFile(downloaded_zip, 'r') as zip_ref:
        zip_ref.extractall("unzipped")


    try:
        os.mkdir("export")
    except:
        shutil.rmtree("export")
        os.mkdir("export")
        print("Error: Could not create export folder.")



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
        filex = open(filenamex, encoding="utf8")
        filex_content = json.load(filex)
        #print(filex_content)
        filex.close()
        if filex_content == {}:
            os.remove(filenamex)


    shutil.make_archive(filename[:-5], 'zip', "export")

    await interaction.followup.send(file=nextcord.File(filename[:-5] + ".zip"))




    time.sleep(1)
    shutil.rmtree("export")
    shutil.rmtree("unzipped")
    os.remove(downloaded_zip)
    os.remove(filename[:-5] + ".zip")
    print("Finished Building and Downloading.")

client.run(token)