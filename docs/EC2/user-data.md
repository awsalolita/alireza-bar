# Debug
* user-data , after modules:final there is the log for user-data
```bash
cat /var/log/cloud-init-output.log | grep -iA 20  modules:final
/var/lib/cloud/instances/[instance-id]/user-data.txt
```


# ACCESS VM
## (1) describe keypair to get public key
```bash
aws ec2 describe-key-pairs --key-names Local --include-public-key
```
### Cloud-init add sshkey
```yaml
#cloud-config
cloud_final_modules:
- [users-groups,always]
users:
  - name: arpjoker
    groups: [ wheel ]
    sudo:     
      - "ALL=(ALL) NOPASSWD:ALL"
    shell: /bin/bash
    ssh-authorized-keys: 
    - "ssh-rsa AB3nzExample"
```

# (2) Userdata
## First time
*ONLY For amazon linux
```bash
#!/bin/bash
echo "ec2-user:arpjoker" | chpasswd 
sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config
sudo service sshd restart 
```
## EveryTime
* Be Carefull to delete it
```yaml
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"
#!/bin/bash
echo "ec2-user:arpjoker" | chpasswd 
sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config
sudo service sshd restart 
```


## (3) setup user for ssh
* ubuntu and amazon linux 
```bash
#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Username to enable SSH password authentication
username="arpjoker"

# Check if the user already exists
if id "$username" &>/dev/null; then
    echo "User $username already exists."
else
    echo "User $username does not exist. Creating..."
    # Create the user
    useradd -m -s /bin/bash "$username"
fi

# Set password for the user
echo "Setting password for $username"
echo "$username:arpjoker" | chpasswd

# Enable SSH password authentication only for the specified user
echo -e "\n" /etc/ssh/sshd_config
echo -e "\n" /etc/ssh/sshd_config
echo "Match User $username" >> /etc/ssh/sshd_config
echo -e  "    PasswordAuthentication yes\n" >> /etc/ssh/sshd_config

# Grant full root access to the user without password
echo "$username ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/$username"

# Restart SSH service
systemctl restart sshd

echo "SSH password authentication enabled only for user $username."
echo "User $username has been granted full root access without requiring a password."

```


# Make Service or run the binary
* [systemd](../../ec2_before_script/service.sh)
* user-data
```bash
cd /app
chmod +x ./binary
./binary &
```

# MetaData
```bash
#!/bin/bash
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"
INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id)
```
* get iam credentials from `http://169.254.169.254/latest/meta-data/iam/....`


# recover wordpress
```bash
sed "20i  define( 'WP_HOME', 'http://myWPAppALB-1365555772.us-west-2.elb.amazonaws.com' );\ndefine( 'WP_SITEURL', 'http://myWPAppALB-1365555772.us-west-2.elb.amazonaws.com' );" wp-config-sample.php
```
# nginx
* return text in nginx 
```c++
location /health/startup {
    add_header Content-Type text/plain;
    return 200 'healthy';
}

location / {
    default_type text/html;
    return 200 "<!DOCTYPE html><h2>gangnam style!</h2>\n";
}
```

```c++
server {
      listen 80;
  location / {
    return 200 $remote_addr ; 
    add_header Content-Type text/html;
  }
}
```