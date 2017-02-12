# Based on https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html
import paramiko
import time
import ConfigParser
import uuid
import os.path

#USER_CONFIG="administrator"
USER_CONFIG="temp"
SCRIPT_TO_RUN="auto_script.sh"
TEMP_DIR="/tmp"
'''
IP_RANGE_A=192
IP_RANGE_B=168
IP_RANGE_C=168
IP_RANGE_D=[1,30]
'''

IP_RANGE_A=10
IP_RANGE_B=4
IP_RANGE_C=0
IP_RANGE_D=185

def get_range(lRange):
    if type(lRange)==int:
        return [str(lRange)]
    elif type(lRange)==list and len(lRange)==2:
        #Note that Range is not inclusive so add 1
        return [str(x) for x in range(lRange[0],lRange[1]+1)]
    else:
        return "Error: IP setup incorrect"
        exit()

def get_ip_list():
    lTarget_IPs=[] 
    dot = "."
    for sOctetA in get_range(IP_RANGE_A):
        for sOctetB in get_range(IP_RANGE_B):
            for sOctetC in get_range(IP_RANGE_C):
                for sOctetD in get_range(IP_RANGE_D):
                    lTarget_IPs.append(sOctetA+dot+sOctetB+dot+sOctetC+dot+sOctetD)
    return lTarget_IPs

def get_creds(login_section):
    config = ConfigParser.RawConfigParser()
    config.read('password.conf')
    username=config.get(login_section, "username")
    password=config.get(login_section, "password")
    return [username,password]

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def do_ssh_runcmd():
    with open(SCRIPT_TO_RUN,"r") as fScript:
        sScript=fScript.readlines()
    
    sTmpFileName=str(uuid.uuid1())+".sh"
    for ip in get_ip_list():
        username,password = get_creds(USER_CONFIG)

        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()

        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(
             paramiko.AutoAddPolicy())

        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip

        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established"

        # Strip the initial router prompt
        output = remote_conn.recv(1000)

        # See what we have
        print output

        # Turn off paging
        #disable_paging(remote_conn)

        remote_conn.send("\n")
        for sLine in sScript:
            # Now let's try to send a command
            remote_conn.send("echo " + sLine.strip() + " >> " + os.path.join(TEMP_DIR,sTmpFileName) + "\n")

            # Wait for the command to complete
            time.sleep(.5)
            
            output = remote_conn.recv(5000)
            print output
        remote_conn.send("nohup sh " + os.path.join(TEMP_DIR,sTmpFileName) + " && rm " + os.path.join(TEMP_DIR,sTmpFileName) + " && exit\n")
        #remote_conn.send("sh " + os.path.join(TEMP_DIR,sTmpFileName) + "\n")
        # Wait for the command to complete
        time.sleep(.5)
        output = remote_conn.recv(5000)
        print output

if __name__ == '__main__':
    do_ssh_runcmd()