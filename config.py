#This is the autoPyrate suite configuration file
#Here you can change destination ip, login information, etc

#destination IP address of server
ip_addr = '173.224.111.159'
#destination of torrented files from server
source_dir = '/opt/plexmedia/movies/'
#destination directory of downloded files (client)
dest_dir = '~/Downloads'
#default login for sever
login = 'pi'

#torrent website (thepiratebay is the only one that work at the moment, more to be added!)
url = 'https://thepiratebay.org/search/'
#transmission torrent client config
#default login
transmission_login = "transmission"
transmission_pass = True #set True if transmission password is the same as server login password

#seed time
seedtime = 600
