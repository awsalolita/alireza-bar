aws configure 

bash ./startup.sh

ip=$(aws ec2 describe-instances --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

echo "bash <(curl -Ls https://raw.githubusercontent.com/vaxilu/x-ui/master/install.sh)"


echo  ssh ubuntu@$ip -t "sudo su"


