#This is the autoPyrate suite configuration file
#Here you can change destination ip, login information, etc

#destination IP address of server
ip_addr = ''
#destination of torrented files from server
source_dir = '/opt/plexmedia/movies/'
#destination directory of downloded files (client)
dest_dir = '~/Downloads'
#default login for sever
login = 'pi'

#torrent website (thepiratebay is the only one that works at the moment, more to be added) #this website is just to test
url = 'https://thepiratebay.org/search/'
#transmission torrent client config
#default login
transmission_login = "transmission"
transmission_pass = True #set True if transmission password is the same as server login password
transmission_password = '' #if previous option is set to False, enter transmission-client password here

#seed time
seedtime = 600
