# LabAutomation
Tools that will be used to help automate a lab in an education environment.

There are 3 components:
* ScriptRunner - a SSH automation script
* Scripts - A user driven script for quick changes.
* WoL - Wake on Lan scripts for the lab

Each station needs an SSH server to be installed and associated configuration scripts set up. Also iptables must allow incoming connections to the SSH server. The setup_system.sh script attempts to do all of this. I recommend coping it to a USB drive and running on each system.

# ScriptRunner
This is a SSH automation script that will automatically login to each IP within a range and execute a script. It can be execute using the following command:
 
 sudo python lab_automation.py
 
Once executed it will leverage the credentials in the password.conf file or PKI certs in your .ssh directory to authenticate. It will then copy over the contents of the "auto_script.sh" and execute it.

# Scripts
This is a very simply scratch space used to rapidly deploy tools. It is meant to be execute by the user using the following command:
 
 sudo curl -L http://bit.ly/ics355_scratchraw | sudo bash
 
 # WoL
 Wake on Lan scripts that send the magic packet to turn on each machine. Just run the shell script and it will do it all.
 
 Requires wakeonlan
 
  sudo apt-get install wakeonlan

