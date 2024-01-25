# Remnant: From the Files
Move Remnant II files from Game Pass to Steam and vice versa.

This is a very rudimentary script to get the job done for now. Please take care when using this. I've tested it... alas don't have unit tests yet, but wanted to get this out into the wild.

Take manual backups if you want starting out in case something goes wrong.

This was made possible by this [post](https://www.reddit.com/r/remnantgame/comments/187rfdq/transferring_save_files_from_pcsteam_to_xbox) from [spectralhunt](https://www.reddit.com/user/spectralhunt/).

# Before Running
Make sure to install Python if not already. This was developed using Python 3.12.1.

Update `config.ini` with your Steam ID. This can be found by navigating to: [https://www.steamidfinder.com/](https://www.steamidfinder.com/) and doing a search using your profile name, or other piece of Steam information for you. Once you find the right results you'll want to get the `steamID3` number. We only want the last bits of the information though.

Example:
    You'll see [U:1:########] for your steamID3. Grab the last part after the right most colon without the end bracket and then update `config.ini`.

Also, make sure you have created a character in Game Pass first if moving to Steam. This is because of how files are stored for Remant 2 for Gam Pass. I would do the same for Steam just to make sure files and folders are there.

# To Run
Open up your terminal and run `python3 address_to_folder\main.py`. Follow the on screen prompts.

# What it's doing
When the script first runs it finds the files for Steam and Game Pass, and keeps those in memory. Then prompts you to decide if you want to move/copy your files to Steam or Game Pass. Once you've decided, there's no going back now, it'll take backups of your current files in both locations and them copy the files from the source you've chosen to the destination.

That's it. Once it's done you should be able to load up which ever version and play the game.

# Limitations
This only does one game save for now. Will be working on making it so it'll do more than just one in the future.

# config.ini
Below is an explanation of what type of data or values are accepted for entries in the config.

[GENERAL]
TakeBackups = true/false
TestImplementation = true/false

[STEAM]
SteamUserId = SteamID3

