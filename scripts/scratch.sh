apt-get update
#apt-get upgrade
apt-get -y install openssh-server
sudo iptables -A INPUT -p tcp -s 192.168.168.250 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT