DATE=`date +%d-%m-%y` 
echo 'sudo curl -L http://bit.ly/ics355_scratchraw | sudo bash' > ~/run_scratch.sh && chmod +x ~/run_scratch.sh
apt-get update
#apt-get upgrade
apt-get -y install openssh-server
sudo iptables -A INPUT -p tcp -s 192.168.168.250 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
apt-get -y install iptables-persistent
sudo cp /etc/iptables/rules.v4 /etc/iptables/rules.v4.bak_$DATE
sudo iptables -A INPUT -p tcp -s 192.168.168.250 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables/rules.v4