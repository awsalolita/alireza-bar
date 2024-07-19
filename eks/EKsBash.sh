# install kubeadm
curl -LO https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl
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
sudo apt update 
sudo apt install unzip -y

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install


curl -sS https://webinstall.dev/k9s | bash