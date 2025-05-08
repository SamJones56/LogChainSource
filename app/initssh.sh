# https://medium.com/@habibsemouma/setting-up-metasploitable2-and-kali-in-docker-for-pentesting-6b71a089c4a2

# Set ssh password
echo 'root:password1' | chpasswd
# allow root login
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# make auth.log
mkdir -p /run/sshd
mkdir -p /var/log
touch /var/log/auth.log

# Add to config
echo "SyslogFacility AUTH" >> /etc/ssh/sshd_config
echo "LogLevel INFO" >> /etc/ssh/sshd_config

chown syslog:adm /var/log/auth.log
chmod 640 /var/log/auth.log

# start logging
rsyslogd

# start ssh
echo "SSH running"
exec /usr/sbin/sshd &
