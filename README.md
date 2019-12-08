The autoPyrate suite
Created by Liam Amadio  
====================

See config.py for configurations to change the software to your needs

autoPyrate is a script that allows the user to search, download, transfer, or delete torrents on a remote server. Each of these atributes can be modified to the users needs via the config.py file that comes packaged. This program is not explicitly for piracy nor do I condone it.
### Installation Instructions
* Clone the repo
    git clone https://github.com/cnoott/autopyrate_suite.git
* Edit config.py to your server-side needs
*Install the requirements
    pip3 install -r requirements.txt
*Run the program
    python3 autopyrate_suite.py

Dependencies:
- python3
- a server with transmission-daemon and transmission-cli installed
    MODULES:
        - paramiko
        - beautifulsoup4
        - requests

My server-side setup:
raspberry pi 3
    - running raspian
    - port forwarded ssh
    - transmission-daemon and transmission-cli for torrent client (also comes with a web interface)
    - plex


Individual_funfunctions
1. autosearch()
    - Allows a user to search for a torrent.
    - Uses beautifulsoup4 + requests to parse the html page from the url variable provided in the config.py file.
    - Returns a list of avaliable torrents from search result.
    - Reutrns the magnet link from what the users chooses.

2. autotorrent()
   - Takes a magnet link as input and starts a torrent dowload using transmission-daemon/transmission-cli on the configured server
   - Downloads to configured server directory
   - Displays percentage of dowload and gives option whether to seed or not

3. autotransfer()
   - Lists files in configured directory and numbers them for later reference
   - Takes a number as input and transfers the respective file to the configured local directory
   - Uses the scp command localy

4. autodelete()
   - Lists files in configured directory and numbers them for later refence
   - Takes number as input and deletes the respective file from the configured directory

