# Debug
* user-data , after modules:final there is the log for user-data
```
cat /var/log/cloud-init-output.log | grep -iA 20  modules:final
```
# nginx
* return text in nginx 
```
location /health/startup {
    add_header Content-Type text/plain;
    return 200 'healthy';
}

location / {
    default_type text/html;
    return 200 "<!DOCTYPE html><h2>gangnam style!</h2>\n";
}
```

```
server {
      listen 80;
  location / {
    return 200 $remote_addr ; 
    add_header Content-Type text/html;
  }
}
```




# setup user for ssh
* ubuntu and amazon linux 
```
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
echo "Match User $username" >> /etc/ssh/sshd_config
echo "    PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Grant full root access to the user without password
echo "$username ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/$username"

# Restart SSH service
systemctl restart sshd

echo "SSH password authentication enabled only for user $username."
echo "User $username has been granted full root access without requiring a password."

```

# Make Service
[systemd](../../ec2_before_script/service.sh)

#