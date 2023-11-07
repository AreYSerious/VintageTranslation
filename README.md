## Links

- [Crowdin](https://crowdin.com/project/vintage-story-mods) for translating.
- [Dropbox](https://www.dropbox.com/scl/fo/q7u3idxz3edsytki8n6m4/h?dl=0&rlkey=mc3xn22a49qwrjp5cmx1he0ay) for grabbing the translated files.

## Table of content

- [General](#general)
- [Uploading translations](#uploading-translations)
- [Downloading translations](#downloading-translations)
- [Restrictions](#restrictions)
- [Possible Moddb integration](#possible-moddb-integration)
- [Useful scripts](#useful-scripts)


## General

The source files on the [Crowdin project](https://crowdin.com/project/vintage-story-mods) are getting updated daily.
That means the `en.json` files from the latest released or updated mods are getting pulled from the official [Moddb](https://mods.vintagestory.at/).
So the next time you update or release your mod they will get uploaded automatically.

The translated files can be grabbed by mod authors from this [Dropbox page](https://www.dropbox.com/scl/fo/q7u3idxz3edsytki8n6m4/h?dl=0&rlkey=mc3xn22a49qwrjp5cmx1he0ay). (The up-to-date translations are being updated daily as well. No LIVE updates)

### Uploading translations

If your mod has already translated files you need to manually add them to the crowdin project.

The following Tutorial shows how that can be done:


https://user-images.githubusercontent.com/100879715/220736483-340a2165-9c1f-4a77-825c-8ce34a12b02b.mp4


### Downloading translations

If you want to update your mod and want to use the uptodate translations head over to this [Dropbox](https://www.dropbox.com/scl/fo/q7u3idxz3edsytki8n6m4/h?dl=0&rlkey=mc3xn22a49qwrjp5cmx1he0ay).
You can download the translated files for each mod.

### Restrictions

- manual one time uploading of already translated files via [Crowdin](https://crowdin.com/project/vintage-story-mods) for modauthors.
- only `en.json` files from the modid folder are being uploaded. Example: `\assets\modid\lang\en.json` **NOT** `\assets\game\lang\en.json`
- the `en.json` file has to be correct [Json](https://www.json.org/json-en.html) syntax. **NOT** [Json5](https://json5.org/) which the game supports but not Crowdin.
- Daily updates no LIVE updates.

### Possible Moddb integration
![image](https://github.com/AreYSerious/VintageTranslation/assets/100879715/130a33c4-ee7c-44e2-b0b5-f021474be71a)

To reproduce this use the following image:

![image](https://github.com/AreYSerious/VintageTranslation/assets/100879715/b744a853-6a4a-496a-9298-f90d6f510415)

You can also use my reference here and use the same witdh and height:

```https://i.imgur.com/8vVoFzG.png```

![image](https://github.com/AreYSerious/VintageTranslation/assets/100879715/fa3a8384-be23-41df-b11d-7bc894cd3746)

The Link structure looks like this:

```https://crowdin.com/translate/vintage-story-mods/329```

So you will need to find your id for your mod. Which you can easily see in the url if you go into the editor for a random language for your mods file. And adjust that accordingly.

If you set up the link like above, your possible translators will get right into the editor and be able to select their lang and start translating <3

![image](https://github.com/AreYSerious/VintageTranslation/assets/100879715/9a092a13-cb1d-435e-9da7-6097cac60031)



### Useful scripts

by [@Gerste](https://github.com/G3rste)

I just did a small powershell skript to autodownload translations from crowdin directly into you project.
It automatically reads out all necessary data for downloading from your modinfo file (You might need to adjust the paths depending on where the script lies)
Feel free to steal if anybody is interested:
```powershell
$modinfo=Get-Content -Path resources\modinfo.json | ConvertFrom-Json
$modid=$modinfo.modid;
$authors=$modinfo.authors -Join '';
$downloadpath="resources/assets/$modid/lang/";
$downloadfile= $downloadpath + 'translations.zip';
Invoke-Webrequest -Uri "https://dl.dropboxusercontent.com/scl/fo/q7u3idxz3edsytki8n6m4/h/$modid-$authors.zip?dl=1&rlkey=mc3xn22a49qwrjp5cmx1he0ay" -OutFile $downloadfile;
Expand-Archive -Force -Path $downloadfile -DestinationPath $downloadpath;
Remove-Item -Path $downloadfile; 
```
