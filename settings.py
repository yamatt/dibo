DEBUG=True

# how long to wait for shutdown
TIMEOUT=5

# ways of data getting in to main process
INPUTS_DIR="inputs"
INPUTS=[]

# things that respond to inputs
PLUGINS_DIR="plugins"
PLUGINS=['connect', 'pingpong', 'nick_handler']

# irc server
SERVER="localhost"
PORT=6667
AUTOJOIN=['#channel1']

# bot details
NAME="dibo"
NAME_BACKUP_1="dibo1"
NAME_BACKUP_2="dibo2"
PASSWORD="!! CH4NG3 M3 !!" # must choose better one
