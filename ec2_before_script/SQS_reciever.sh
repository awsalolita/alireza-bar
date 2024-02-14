#!/bin/bash -xe
yum install python3 -y
python3 -m pip install boto3
if [[ 'true' == 'true' ]]; then
  echo 'zSf1t]aW' | passwd cloud_user --stdin
  USERNAME=cloud_user
else
  echo 'P@ssw0rd' | passwd ec2-user --stdin
  sed -i 's|[#]*PasswordAuthentication no|PasswordAuthentication yes|g' /etc/ssh/sshd_config
  systemctl restart sshd.service
  USERNAME=ec2-user
fi
su - $USERNAME -c 'aws configure set region us-east-1'
curl -o  /home/$USERNAME/receive_messages.py -L https://raw.githubusercontent.com/ACloudGuru-Resources/Course-Certified-Solutions-Architect-Associate/master/labs/scaling-ec2-using-sqs/receive_messages.py
chmod +x /home/$USERNAME/receive_messages.py
chown $USERNAME /home/$USERNAME/receive_messages.py
USERNAME=$USERNAME su $USERNAME -c "/home/${USERNAME}/receive_messages.py >> /home/${USERNAME}/receive_messages.log 2>&1 &"
