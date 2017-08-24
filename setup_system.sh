#http://bit.ly/ics355_scratchraw
#fix apt-get issue https://askubuntu.com/questions/132059/how-to-make-a-package-manager-wait-if-another-instance-of-apt-is-running
DATE=`date +%d-%m-%y` 
echo 'sudo curl -L http://bit.ly/ics355_scratchraw | sudo bash' > ~/run_scratch.sh && chmod +x ~/run_scratch.sh
apt-get update
#apt-get upgrade
apt-get -y install openssh-server
#sudo iptables -A INPUT -p tcp -s 192.168.168.250 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
#sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
apt-get -y install iptables-persistent
sudo cp /etc/iptables/rules.v4 /etc/iptables/rules.v4.bak_$DATE
sudo iptables -A INPUT -p tcp -s 192.168.168.250 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables/rules.v4
#cp ~/authorized_keys ~/authorized_keys_Backup
mkdir ~/.ssh
cat id_rsa.pub >> ~/.ssh/authorized_keys
sudo chown administrator:administrator ~/.ssh 
sudo chown administrator:administrator ~/.ssh/authorized_keys 
sudo chmod 600 ~/.ssh/authorized_keys 
sudo chmod 700 ~/.ssh
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config_orig-2017-08-16
sudo cp sshd_config /etc/ssh/sshd_config
sudo /etc/init.d/ssh restart
#THISHOST=$(hostname -f)
THISHOST=$(hostname)
echo "127.0.1.1 $THISHOST" | sudo tee --append /etc/hosts
exit
