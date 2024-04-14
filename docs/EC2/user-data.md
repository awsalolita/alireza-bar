* user-data , after modules:final there is the log for user-data
```
at /var/log/cloud-init-output.log | grep -iA 20  modules:final
```

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

```
#!/bin/bash
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
service sshd restart
useradd arpjoker
echo 'arpjoker:arpjoker' | chpasswd
usermod -aG wheel arpjoker
echo 'arpjoker ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/arpjoker
chmod 0440 /etc/sudoers.d/arpjoker`
```