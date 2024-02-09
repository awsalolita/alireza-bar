#!/bin/bash -xe
yum update -y
amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
yum install -y httpd mariadb-server        
systemctl start mariadb
systemctl enable mariadb
# usermod -a -G apache cloud_user
# chown -R cloud_user:apache /var/www
cd /var/www/html
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp -r wordpress/* /var/www/html/
rm -rf wordpress
rm -rf latest.tar.gz
chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0664 {} \;
cp wp-config-sample.php wp-config.php
sed -i "s/database_name_here/wordpress"/g wp-config.php
sed -i "s/username_here/wpuser/g" wp-config.php
sed -i "s/password_here/Password1/g" wp-config.php
sed -i "s/localhost/db.mydomain.local/g" wp-config.php
echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php
systemctl start httpd
systemctl enable httpd
