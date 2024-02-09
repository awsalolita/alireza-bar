#!/bin/bash

SG_NAME="mine2"
aws ec2 import-key-pair --key-name "my-key" --public-key-material fileb://~/.ssh/id_ed25519.pub &

vpc=$(aws ec2 describe-vpcs --query "Vpcs[0].VpcId" --output text )

sg=$(aws ec2 create-security-group --query "GroupId" --group-name $SG_NAME --description "My security group" --vpc-id $vpc --output text)

aws ec2 authorize-security-group-ingress --group-name $SG_NAME --protocol all --cidr 0.0.0.0/0 &

subnet=$(aws ec2 describe-subnets --query "Subnets[0].SubnetId" --output text)

aws ec2 run-instances --image-id ami-0c7217cdde317cfec --count 1 --instance-type t2.micro --key-name my-key --security-group-ids $sg --subnet-id $subnet
