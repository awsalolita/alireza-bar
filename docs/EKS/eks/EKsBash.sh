# install kubectl
curl -LO https://dl.k8s.io/release/v1.29.7/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
# install helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
# install eksctl
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin


# alias
#  aws eks update-kubeconfig --region region-code --name my-cluster
# kubectl rollout restart -n kube-system deployment coredns

echo "alias kd='kubectl describe'" >> ~/.bashrc
echo "alias kg='kubectl get'" >> ~/.bashrc
echo "alias kgp='kubectl get pods'" >> ~/.bashrc
echo "alias kdp='kubectl describe pods'" >> ~/.bashrc
echo "alias k=kubectl" >> ~/.bashrc
echo "alias kap='kubectl apply -f'" >> ~/.bashrc
echo "alias kcd='kubectl  config  set-context --current --namespace'" >> ~/.bashrc 
echo "source <(kubectl completion bash)" >> ~/.bashrc
echo "source <(helm completion bash)" >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
echo "complete -C '/usr/local/bin/aws_completer' aws" >> ~/.bashrc
echo "source /etc/bash_completion" >> ~/.bashrc
echo "source <(eksctl completion bash)" >> ~/.bashrc
echo "export KUBE_EDITOR='vim'" >> ~/.bashrc




# install aws cli

read -p "Do you want to install AWS CLI? (y/n): " install_aws
if [[ "$install_aws" == "y" || "$install_aws" == "Y" ]]; then
    # Download and install AWS CLI
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    echo "AWS CLI installed successfully."
else
    echo "AWS CLI installation skipped."
fi

read -p "Do you want to install go ? (y/n): " install_go
if [[ "$install_go" == "y" || "$install_go" == "Y" ]]; then
    # Download and install AWS CLI
    wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
    rm go1.22.5.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
else
    echo "go installation skipped."
fi


#curl -sS https://webinstall.dev/k9s | bash

wget https://github.com/derailed/k9s/releases/download/v0.32.5/k9s_linux_amd64.rpm

yum install k9s_linux_amd64.rpm -y
sudo rm -r aws*
sudo rm -r kubectl
sudo rm -r get_helm.sh
sudo rm -r Downloads

