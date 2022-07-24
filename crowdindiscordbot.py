from __future__ import unicode_literals
import time
import urllib.request

from nextcord.ext import commands
from nextcord import *
import nextcord

import crowdin_api.exceptions
from crowdin_api import CrowdinClient


# Gets the bot token from a seperate file called BotToken.py that looks like this:
# token = "insert_your_token_here"
from BotToken import token
from BotToken import crowdintoken


# invite Link for dc bot:
# https://discord.com/api/oauth2/authorize?client_id=949725454477168661&permissions=140123630656&scope=applications.commands%20bot

testingserverId = [587658490764591123,801080634670972940,302152934249070593,955576967346921654]






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









client = commands.Bot(command_prefix="!", help_command=None, activity=nextcord.Game(name="/help"))

@client.event
async def on_ready():
    print("Bot online.")



@client.command() # context is automatically passed in rewrite
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
            url="https://cdn.discordapp.com/attachments/588044295810973705/955152835782246400/DiscordBotCommandBanners_fileupload.png")

        await ctx.send(embed=embed3)

        time.sleep(5)
        await ctx.channel.purge(limit=2)

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
                url="https://cdn.discordapp.com/attachments/588044295810973705/955152835782246400/DiscordBotCommandBanners_fileupload.png")
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
                    url="https://cdn.discordapp.com/attachments/588044295810973705/955152835782246400/DiscordBotCommandBanners_fileupload.png")
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
                    url="https://cdn.discordapp.com/attachments/588044295810973705/955152835782246400/DiscordBotCommandBanners_fileupload.png")
                await ctx.send(embed=embed3)
                time.sleep(3)
                await ctx.channel.purge(limit=3)


        # Second Check: Checks if the Json Syntax is correct.
        elif s.__contains__("Incorrect json in request body. Syntax error"):
            #print("Error: Incorrect json in request body. Syntax error.")
            embed1 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                                   description="**ADDING A FILE**")
            embed1.add_field(
                name="`⚠️`** › Error**",
                value="`⚠️` › Incorrect json in request body. Syntax error!", inline=False)
            embed1.set_image(
                url="https://cdn.discordapp.com/attachments/588044295810973705/955173313062268958/DiscordBotCommandBanners_fileupload_error.png")
            await ctx.send(embed=embed1)






@client.slash_command(name="language_progress", description="Shows the Translation Progress.", guild_ids=testingserverId)
async def progress(interaction: Interaction):
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
        if lang_id == "ar":
            lang_id = ":flag_ae: Arabic:"
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




        embed.add_field(name=lang_id, value=str(trans_prog) + "%", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955150814698160178/DiscordBotCommandBanners_langprog.png")

    await interaction.response.send_message(embed=embed)







@client.slash_command(name="add_language", description="Requests to add a Language to the Crowdin Project.", guild_ids=testingserverId)
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
    embed.add_field(name="requested the Language: " + language_name + ".", value="Discord-Server: " + guild_onserver, inline=False)

    await user.send(embed=embed)




    embed1 = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                          description="**LANGUAGE REQUEST**")
    embed1.add_field(name="`🔣` › Request to add the following language has been sent:\n`🔽`\n **" + language_name + "**\n`🔼`", value="`⚠️` › A project manager has to add the language manually. This can take up to 1 day. Please be patient. ❤️", inline=False)
    embed1.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955148545248334014/DiscordBotCommandBanners_langrequest.png")

    await interaction.response.send_message(embed=embed1)




@client.slash_command(name="addfile", description="Explanation on how to Upload a File for Translation.", guild_ids=testingserverId)
async def addfile(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**TUTORIAL ADDING A FILE**")
    embed.add_field(name="`▶️` Enter:", value="› ` !addfile `\n \n`▶️` Press the **+** button to the left to attach a file to the message.\n \n`▶️` Send the message.\n \n`⚠️` The name of the **Filename** should something like: \n› ` Modname-Author.supportedformat `\n \n`❓` Supported formats:\nhttps://support.crowdin.com/supported-formats/\n \n`🎞️` **Check out the tutorial video below this message.**", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955526438835073086/DiscordBotCommandBanners_tutorial.png")
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=nextcord.File("AddingAFileTutorial.webm"))




@client.slash_command(name="updatefile", description="Explanation on how to update a file for translation.", guild_ids=testingserverId)
async def updatefile(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**TUTORIAL UPDATING A FILE**")
    embed.add_field(name="`▶️` Enter:", value="› ` !addfile `\n \n`▶️` Press the **+** button to the left to attach a file to the message.\n \n`▶️` Send the message.\n \n`▶️` Read the response from the bot and react to the message with ✅ to continue.\n \n`⚠️` The **Filename** has to be the **same name** as the file you want to update!\n`⚠️` You can get a list of all filenames in the project with:\n› ` /listfiles `\n \n`⚠️` The name of the **Filename** should something like: \n› ` Modname-Author.supportedformat `\n \n`❓` Supported formats:\nhttps://support.crowdin.com/supported-formats/\n \n`🎞️` **Check out the tutorial video below this message.**", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955526438835073086/DiscordBotCommandBanners_tutorial.png")
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=nextcord.File("UpdatingAFileTutorial.webm"))





@client.slash_command(name="help", description="Shows all commands for the VintageTranslation Bot.", guild_ids=testingserverId)
async def help(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                           description="**HELP/COMMANDS**")
    embed.add_field(name="› ` /addfile `", value="`▶️` Explains the usage of the !addfile command and how to upload a file to the project.", inline=False)
    embed.add_field(name="› ` !addfile `", value="`▶️` Uploads a file to the project for translation, can update a file aswell.", inline=False)
    embed.add_field(name="› ` /updatefile `", value="`▶️` Explains the usage of the !addfile command and how to update a file to the project.", inline=False)
    embed.add_field(name="› ` /language_progress `", value="`▶️` Shows the translation progress of each language.", inline=False)
    embed.add_field(name="› ` /add_language `", value="`▶️` Sends a request to add a language to the project.", inline=False)
    embed.add_field(name="› ` /listfiles `", value="`▶️` Lists all filenames on the project.", inline=False)
    embed.add_field(name="› ` /project `", value="`▶️` Shares a link to the Crowdin project.", inline=False)
    embed.add_field(name="› ` /wip `", value="`▶️` Shares a link to the Development progress board.", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/953741054677499954/DiscordBotCommandBanners111.png")

    await interaction.response.send_message(embed=embed)



@client.slash_command(name="listfiles", description="List of all filenames.", guild_ids=testingserverId)
async def listfile(
    interaction: Interaction,
):

    files = crowdin_client.source_files.list_files(project_id)
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods", description="**LIST OF FILENAMES**")
    list0123 = []
    for x in range(len(files["data"])):
        list0123.append("`📁` › " + files["data"][x]["data"]["name"])

    names = "\n".join(list0123)
    embed.add_field(name="**Filenames:**", value=names, inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955144349568626748/DiscordBotCommandBanners_filenames.png")
    await interaction.response.send_message(embed=embed)


@client.slash_command(name="project", description="Shares a link to the Crowdin project.", guild_ids=testingserverId)
async def project(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**PROJECT**")
    embed.add_field(name="`🔗` Use the following link to access the Crowdin project:", value="`▶️` https://crowdin.com/project/vintage-story-mods", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955566317405085756/DiscordBotCommandBanners_project.png")
    await interaction.response.send_message(embed=embed)



@client.slash_command(name="wip", description="Overview of the Bot development.", guild_ids=testingserverId)
async def wip(
    interaction: Interaction,
):
    embed = nextcord.Embed(title="Crowdin Project", url="https://crowdin.com/project/vintage-story-mods",
                            description="**WORK IN PROGRESS**")
    embed.add_field(name="`🔗` Use the following link to access the development progress board:", value="`▶️` https://trello.com/b/ZGKWSCZO/vintagetranslationdiscordbot", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/588044295810973705/955572836737634384/DiscordBotCommandBanners_wip.png")
    await interaction.response.send_message(embed=embed)



client.run(token)
