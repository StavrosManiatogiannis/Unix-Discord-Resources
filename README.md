# Unix-Discord-Resources
## INTRODUCTION
UNIX Discord Resources(or UDR for short) is a discord bot which gives a Server's Managers the ability to utilize the familiar UNIX commands for managing files and directories into managing Categories and Channels , allowing faster and more efficient server administration.


## DEPENDENCIES
* Python
* Discord.py
* python-dotenv
* Discord bot token
#### You will need to install or get these before being able to use this bot.
## DOCUMENTATION
A list of the available commands
* ### whoami
Sends back a message with the user's username.

* ### pwd
Sends back a message with the working channel. 

* ### ls
Sends back a message with the subchannels of the working channel.
It has 2 options:
* -a   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; shows hidden channels (the ones whose name begins with ".")
* -l   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; changes the format of the message the bot sends into a list
* -al or -la   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if you want to use both

* ### cd
Changes the current working channel to the path specified. It accepts both absolute and relative paths.

* ### mk
Makes a non-category channel with the specified name in the working channel.Doesn't make category channels nor can it be used if the current channel is non-category. By default makes text channel. It has 2 options:
* -t    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; makes text channel (default)
* -v    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; makes voice channel

* ### rm
Removes a non-category channel with the specified name. By deafult it doesn't remove non-empty channels. It has 1 option:
* -f    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; removes non-empty channel

* ### mkdir
Makes a category channel with the specified name.Can only be used when working channel is "/".

* ### rmdir
Removes a category channel with the speicified name. By default it doesn't remove categories who have channels (even if those channels are empty). It has 2 options:
* -r &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for a non-empty category removes all empty channels inside it and if there are no channels left removes the category too
* -f &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; removes a category and all its channels regardless of whether they are empty

* ### mv
Moves a channel with a specified path to another specified path, works with both absolute and relative paths.

## SETTING UP
* Download the Python programming language
* Use the following command in the terminal in order to install the python packages ```python -m pip install discord.py python-dotenv```
* Go to Discord Developer Portal, create a new Application and copy it's token
* Go to the ".env" file and paste your token after the "=" sign with no space in between
* Inivte the bot to your server, execute the main.py function and the bot is online.
* Have fun!
