'''
###############
# Support Functions
# Examples taken from here: https://github.com/ghoulmann/Raspliance-Core/blob/master/compile_tklpatch.sh
install ()
{
	apt-get update
	DEBIAN_FRONTEND=noninteractive apt-get -y \
        -o DPkg::Options::=--force-confdef \
        -o DPkg::Options::=--force-confold \
        install $@
}

purge ()
{
	apt-get purge
	DEBIAN_FRONTEND=noninteractive apt-get -y \
        -o DPkg::Options::=--force-confdef \
        -o DPkg::Options::=--force-confold \
	purge $@
}
'''
###############
#Common Tasks
###############
#apt-get autoremove -y
cd ~
rm ~/nohup.out
rm -f /var/crash/*
sudo chown -R administrator:administrator ~/*
sudo shutdown -h now
exit
###############


###############
#Setup Stuff
###############
#echo "ssh-rsa [put key here]" >> ~/.ssh/authorized_keys
#sudo apt-get update
#sudo apt-get -y install python-pip
#pip install futures
#sudo apt-get -y install python-bs4
#sudo apt-get -y install python-scapy
#mkdir ~/ics355
#cp -r * ~/ics355
###############


###############
# Install DanBot
#sudo curl -L https://raw.githubusercontent.com/danman10000/IRC-Bot/master/setup.sh | bash
###############


##############
#Raspberry Pi Rollout
#sudo apt-get update
#sudo apt-get install dcfldd
##############


##############
#RDP
#sudo apt-get -y install rdesktop
##############


##############
#General Updates
#sudo apt-get update
#sudo apt-get upgrade -y
##############

################################################
################################################
#Demo Prep
################################################
################################################
##############
#DES Demo
#mkdir ~/ics355_demos
#cd ~/ics355_demos
#rm demo_crypt.py
#wget https://raw.githubusercontent.com/danman10000/ics355_demos/master/demo_crypt.py
#wget https://raw.githubusercontent.com/danman10000/ics355_demos/master/Entropy.sh
#sudo chown administrator:administrator *
#sudo apt-get update
#sudo apt-get install -y netpbm
#sudo apt-get install -y pv
#sudo apt-get install -y rng-tools
#sudo pip install pycrypto
#sudo pip install crcmod

##############
#Crypt Tools
# gnupg
##############
#sudo apt-get -y install gnupg
#sudo apt-get -y install pgpdump
#sudo apt-get -y install gpa
#sudo pip install python-gnupg
#sudo apt-get -y install seahorse-nautilus
#seahorse
#seahorse-tool 
#sudo apt-get install nautilus
#nautilus
##############
#steghide
##############
#sudo apt-get -y install steghide
#sudo apt-get -f -y install
#sudo apt-get -y install openjdk-8-jre -f
#wget https://github.com/syvaidya/openstego/releases/download/openstego-0.7.0/openstego_0.7.0-1_amd64.deb
#sudo dpkg -i ./openstego_0.7.0-1_amd64.deb 
#echo java -Xmx512m -jar /usr/share/openstego/lib/openstego.jar > ~/ics355_run_stego.sh
#chmod +x ~/ics355_run_stego.sh
##############
#Hashing
##############
#sudo apt-get -y install gtkhash

