# LabAutomation
Tools that will be used to help automate a lab in an education environment.

There are 2 components:
* ScriptRunner - a SSH automation script
* Scripts - A user driven script for quick changes.

# ScriptRunner
This is a SSH automation script that will automatically login to each IP within a range and execute a script. It can be execute using the following command:
 sudo python lab_automation.py
 
Once executed it will leverage the credentials in the password.conf file or PKI certs in your .ssh directory to authenticate. It will then copy over the contents of the "auto_script.sh" and execute it.

# Scripts
This is a very simply scratch space used to rapidly deploy tools. It is meant to be execute by the user using the following command:
 sudo curl -L http://bit.ly/ics355_scratchraw | sudo bash

