#!/bin/bash
mkdir -p /app
cat <<EOF > /app/a.py
while(1):
        print(1)
EOF


cat <<EOF > /etc/systemd/system/myapp.service
[Unit]
Description=My Python Application
After=network.target

[Service]
User=ec2-user
ExecStart=python3 /app/a.py

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable myapp.service
systemctl start myapp.service