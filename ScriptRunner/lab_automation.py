# Based: https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html
# Threading Reference: https://stackoverflow.com/questions/3485428/creating-multiple-ssh-connections-at-a-time-using-paramiko
import paramiko
import time
import ConfigParser
import uuid
import os.path
import traceback
import base64
import threading
import sys, os, string
import logging
import socket

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class patched_SSHClient(paramiko.SSHClient):
    def _auth(self, username, password, *args):
        if not password:
            try:
                self._transport.auth_none(username)
                return
            except paramiko.BadAuthenticationType:
                pass
        paramiko.SSHClient._auth(self, username, password, *args)

#USER_CONFIG="administrator"
USER_CONFIG="administrator"
SCRIPT_TO_RUN="auto_script.sh"
TEMP_DIR="/tmp"
#In some cases it is better to send an entire script to a temp file, execute the script, and move onto the next box. This will do exactly that. Otherwise it runs the commands one at a time.
USE_TEMP_FILE=True

#Allowed user types
ROOT=1
USER=2
USERTYPES={"root":ROOT,"user":USER}


# Example target IP setup. Each octet can be a range. Use a list to indicate the upper and lower bound inclusively
# Example
# IP_RANGE_A=192
# IP_RANGE_B=168
# IP_RANGE_C=168
# IP_RANGE_D=[1,30]
IP_RANGE_A=192
IP_RANGE_B=168
IP_RANGE_C=168
IP_RANGE_D=[1,30] #Dells
#IP_RANGE_D=[31,60] #PIs
#IP_RANGE_D=10 #Direct

#Threading output semaphore
outlock = threading.Lock()

#Expand out a list similiar to the range function put make it IP friendly
# lRange = Either a list of 2 elements corrisponding the lower and upper bound of a IP space or a single integer.
def get_range(lRange):
    if type(lRange)==int and lRange >0 and lRange <256:
        return [str(lRange)]
    elif type(lRange)==list and len(lRange)==2 and lRange[0] > 0 and lRange[0] < lRange[1] and lRange[1] < 256:
        #Note that Range is not inclusive so add 1
        return [str(x) for x in range(lRange[0],lRange[1]+1)]
    else:
        print "Error: IP setup incorrect"
        exit()

#Generate a list of IPs based on the ranges.
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
    usertype=config.get(login_section, "type")
    if usertype not in USERTYPES.keys():
        print "User type incorrect in config file. Must be one of ", USERTYPES.keys()
        exit()
    return [username,password,usertype]

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def Exec_per_ip():
    lThreads =[]
    
    with open(SCRIPT_TO_RUN,"r") as fScript:
        sScript=fScript.readlines()
    
    sTmpFileName=str(uuid.uuid1())+".sh"
    for ip in get_ip_list():
        myThread = threading.Thread(target=do_ssh_runcmd, args=(ip,sScript,sTmpFileName,)) #do_ssh_runcmd(ip,sScript,outlock)
        myThread.start()
        lThreads.append(myThread)
    
    with outlock:    
        print "^"*75
        print "All threads started... waiting to finish"
        print "^"*75
    for t in lThreads:
        t.join()
        
            
def do_ssh_runcmd(ip,sScript,sTmpFileName,retries=5):

    runlog=[]
    runlog.append("########### IP:" + ip)
    username,password,usertype = get_creds(USER_CONFIG)

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient() #patched_SSHClient() #paramiko.

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    try:

        # initiate SSH connection
        runlog.append("Starting SSH connection with " + ip)
        retry_count = 0
        while retry_count < retries:
            try:
                isSuccessful=remote_conn_pre.connect(ip, username=username, look_for_keys=True, allow_agent=False, timeout=5)
                #remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=True, allow_agent=False, timeout=1)
                #remote_conn_pre.connect(ip, username=username, )#key_filename="/Users/vp/.ssh/id_rsa.pub"
                #self._chan = self.ssh_connection.invoke_shell(width=9999999,
                #                                              height=9999999)
                
                if isSuccessful is not None:
                    break
            except (paramiko.SSHException,socket.error), msg:
                retry_count = retry_count + 1
                runlog.append("Connect attempt {0} failed: {1}".format(
                    retry_count,
                    msg))
            except paramiko.BadHostKeyException, e:
                raise BadHostKeyError(e.hostname, e.key, e.expected_key)
            except paramiko.AuthenticationException, e:
                raise AuthenticationError()

        if retry_count >= retries:
            runlog.append("Too many connection attempts for " + ip)
            return
            
        runlog.append("SSH connection established to " + ip)

        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        runlog.append("Interactive SSH session established")

        # Strip the initial router prompt
        output = remote_conn.recv(1000)

        # See what we have
        runlog.append(output)

        # Turn off paging
        #disable_paging(remote_conn)

        remote_conn.send("\n")
        if USE_TEMP_FILE:
            bInMultiLineComment=False
            for sLine in sScript:
                if sLine.startswith("'''"): 
                    bInMultiLineComment= not bInMultiLineComment
                if not sLine.startswith("#") and not sLine.startswith("'''") and not len(sLine.strip())<=1 and bInMultiLineComment==False:
                    # Now let's try to send a command
                    runlog.append("Sending: " + "echo '" + sLine.strip() + "' >> " + os.path.join(TEMP_DIR,sTmpFileName))
                    remote_conn.send("echo '" + sLine.strip() + "' >> " + os.path.join(TEMP_DIR,sTmpFileName) + "\n")

                    # Wait for the command to complete
                    time.sleep(.3)
                
                    output = remote_conn.recv(5000)
                    runlog.append(output)
        
            sShCommand="nohup sh " + os.path.join(TEMP_DIR,sTmpFileName) + " && rm " + os.path.join(TEMP_DIR,sTmpFileName) + " && exit\n"
        else:
            #send the date command as the first command so that you know when it was started.
            sRunCmd="date"
            for sLine in sScript:
                if not sLine.startswith("#") and not len(sLine.strip())<=1:
                    sRunCmd=sRunCmd + " && " + sLine.strip()
            #Due the variety of escapes and things in scripts you need to base64 it before sending it over
            b64ShCmd=base64.standard_b64encode(sRunCmd)
            sShCommand="nohup echo '" + b64ShCmd + "' | base64 -d | sh && exit\n"
        if USERTYPES[usertype]==ROOT:
            runlog.append("!!!!Executing as ROOT!!!!")
            sShCommand="set +o history && echo '" + password + "' | sudo --stdin " + sShCommand
        runlog.append( "\n\n Running Command:" + sShCommand +"\n\n")
        remote_conn.send(sShCommand)
        #remote_conn.send("sh " + os.path.join(TEMP_DIR,sTmpFileName) + "\n")
        #stdin, stdout, stderr = ssh.exec_command(cmd)
        #stdin.write('xy\n')
        #stdin.flush()
        # Wait for the command to complete
        time.sleep(1)
        #remote_conn.send(password + "\n")
        # Wait for the command to complete
        #time.sleep(3)
        output = remote_conn.recv(5000)
        runlog.append("Client Returned:"+ output)
    except Exception as e: 
        runlog.append( "EXCEPTION for IP: "+ ip)
        runlog.append(e)
        #runlog.append(traceback.print_exc())
        runlog.append(traceback.format_exc())
        #print "!!!! Error connecting to " + ip
        #continue
    finally:
        with outlock:
            print "#" * 75
            for line in runlog:
                print line

if __name__ == '__main__':
    Exec_per_ip()
