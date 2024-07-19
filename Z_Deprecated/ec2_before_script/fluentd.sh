#!/bin/bash

# Installing apache and toolsets
sudo yum update -y
sudo amazon-linux-extras install php8.0 mariadb10.5
sudo yum install -y httpd
sudo yum start httpd
sudo systemctl enable httpd

# # Setting up ec2-user ability to modifty apache files
# sudo usermod -a -G apache ec2-user
# sudo chown -R ec2-user:apache /var/www
# sudo chmod 2775 /var/www
# find /var/www -type d -exec sudo chmod 2775 {} \;
# find /var/www -type f -exec sudo chmod 0664 {} \;

# Installing fluentD for outputting logs to Amazon S3
curl -L https://toolbelt.treasuredata.com/sh/install-amazon2-td-agent4.sh | sh
sudo systemctl start td-agent.service
sudo systemctl enable td-agent

# Not needed if using td-agent
# curl -L https://calyptia-fluentd.s3.us-east-2.amazonaws.com/calyptia-fluentd-1-amazon-2.sh | sh
# sudo systemctl start calyptia-fluentd.service
# sudo systemctl enable calyptia-fluentd

# Changing the directory permissions so td-agent can tail the logs.
chmod 0645 /var/log/httpd