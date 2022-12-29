## General

The source files on the [Crowdin project](https://crowdin.com/project/vintage-story-mods) are getting updated daily.
That means the `en.json` files from the latest released or updated mods are getting pulled from the official [Moddb](https://mods.vintagestory.at/).
So the next time you update or release your mod they will get uploaded automatically.

The translated files can be grabbed by mod authors from this [Dropbox Page](https://www.dropbox.com/scl/fo/q7u3idxz3edsytki8n6m4/h?dl=0&rlkey=mc3xn22a49qwrjp5cmx1he0ay). (The up-to-date translations are being updated daily as well. No LIVE updates)

### Restrictions









## Guide for Modders

WIP








## DiscordBot Guide

Shows how a modder can upload his mods sourcefile (en).

### 1. Inviting the Bot

Inviting the Bot to your server or joining a discord server that has the bot already.

Invite link: [Invite bot](https://discord.com/api/oauth2/authorize?client_id=949725454477168661&permissions=140123630656&scope=applications.commands%20bot)

Link to a discord server that has the command: [VSWorks](https://discord.gg/7z5mxQN3sm)

### 2. Uploading sourcefiles

Get your mods english language file.


https://user-images.githubusercontent.com/100879715/208253780-65f459a1-cb23-40ef-b54e-24433dae87c7.mp4



Rename your en.json file to contain your modid and modauthor name.

From `en.json` to `Modname-Author.json`

Example

`Backpackpackstandard-Mr1k3.json`


https://user-images.githubusercontent.com/100879715/208253772-b644414f-59e1-422a-905b-0259e8deb063.mp4



Now its time to use the first command on the bot.

Open discord and use a textchannel of your choice. (most servers have dedicated channels for bot commands)

The command you want to use for uploading a file is called `!addfile`

Enter `!addfile` and click on the `+` to the left.

Now select your renamed language file `Modname-Author.json` and send your message.



https://user-images.githubusercontent.com/100879715/208253743-06bf4b1d-8893-4817-946a-70565c94d610.mp4



Nice now your sourcefile is on the project and can be translated by anyone.





## Commands

### /help

Shows a list of all possible commands.

![help](https://i.imgur.com/fKKbxeB.png)

### /addfile

Explains the usage of the !addfile command and how to upload a file to the project.

Adding a file:
 
![addfiletut](https://i.imgur.com/BGWvOF7.png)


Updating a file:
 
![updatingfiletut](https://i.imgur.com/odrHsUw.png)

### !addfile

Uploads a file to the project for translation, can update a file aswell.

![Addfile](https://i.imgur.com/JP3CnT3.png)

### /updatefile

Explains the usage of the !addfile command and how to update a file to the project.

![updatefiletut](https://i.imgur.com/emUzByv.png)

### /language_progress

Shows the translation progress of each language.

![languageprogress](https://i.imgur.com/yKuf1Vc.png)

### /add_language

Sends a request to add a language to the project.

![addlanguage](https://i.imgur.com/Yro7d4q.png)

### /listfiles

Lists all filenames on the project.

![listfiles](https://i.imgur.com/PBWWbMm.png)
