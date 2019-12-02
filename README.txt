The autoPyrate suite
====================

See config.py for configurations to change the software to your needs

1. autotorrent.py
   - Takes a magnet link as input and starts a torrent dowload on the configured server
   - Downloads to configured server directory
   - Displays percentage of dowload and gives option whether to seed or not

2. autotransfer.py
   - Lists files in configured directory and numbers them for later reference
   - Takes a number as input and transfers the respective file to the configured local directory
   - Uses the scp command localy

3. autodelete.py
   - Lists files in configured directory and numbers them for later refence
   - Takes number as input and deletes the respective file from the configured directory

These programs will be combined to create autoPyrate_suite.py 
