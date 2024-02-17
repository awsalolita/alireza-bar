wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
echo Y | sh install.sh

curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash


echo "alias k=kubectl" >> ~/.zshrc
echo "alias kcd='kubectl  config  set-context  --current --namespace'" >> ~/.zshrc 
echo "source <(kubectl completion zsh)" >> ~/.zshrc
echo "source <(helm completion zsh)" >> ~/.zshrc
echo "complete -C '/usr/local/bin/aws_completer' aws" >> ~/.zshrc
echo "source <(docker completion zsh)" >> ~/.zshrc


# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin

# eksctl completion
echo "source <(eksctl completion zsh)" >> ~/.zshrc

zsh
