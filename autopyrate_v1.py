#Created by Liam Amadio
#November 17, 2019
#This program specifically designed to automatically transfer a torrented file from my server to this machine.

import os
import config

ip_addr ='173.224.111.159:' #inlcude colon for formatting purposes
source_dir = '/opt/plexmedia/movies/'
dest_dir = '~/Downloads'
login = 'pi@'

print("\n\nWelcome to autoPyrate\n====================")


file_name = input('Enter exact filename here (rename and or paste from transmission client)')

cmd = 'scp -r {0}{1}{2}{3} {4}'.format(login,ip_addr,source_dir,file_name,dest_dir)
os.system(cmd)
