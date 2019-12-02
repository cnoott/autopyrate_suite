The autoPyrate suite
Created by Liam Amadio  
====================

See config.py for configurations to change the software to your needs

autoPyrate_suite is a combination of 3 programs that work seperatly to torrent on a server to then transfer to a client via SCP, or delete those files to free up space. I created it because my university blocks peer-to-peer traffic on their network (I wonder why) and I wanted a way I could download torrents. This script works by remotley accesing a server via ssh and running the neccesary programs. This program is by no means meant for piracy. Peer-to-peer networks have their advantages and it sucks that univesities have to block them. 

Dependencies:
- python3
- paramiko python module
- a server with transmission-daemon and transmission-cli installed

My server-side setup:
raspberry pi 3
    -running raspian
    -port forwarded ssh
    -transmission-daemon and transmission-cli for torrent client (also comes with a web interface)


Individual_programs:
1. autotorrent.py
   - Takes a magnet link as input and starts a torrent dowload using transmission-daemon/transmission-cli on the configured server
   - Downloads to configured server directory
   - Displays percentage of dowload and gives option whether to seed or not

2. autotransfer.py
   - Lists files in configured directory and numbers them for later reference
   - Takes a number as input and transfers the respective file to the configured local directory
   - Uses the scp command localy

3. autodelete.py
   - Lists files in configured directory and numbers them for later refence
   - Takes number as input and deletes the respective file from the configured directory

