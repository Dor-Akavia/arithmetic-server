#!/bin/bash
# =============================================================================
# user_data.sh.tpl — Bootstrap script for the Jenkins EC2 instance.
# is the only template variable — Terraform substitutes it at plan time.
# =============================================================================
set -e   # Exit immediately if any command fails

echo "==> Updating package index"
apt-get update -y

echo "==> Installing Java 17, Git, and gnupg2"
# git    — required by Jenkins to clone repositories
# gnupg2 — required to import the Jenkins signing key
apt-get install -y fontconfig openjdk-17-jre git gnupg2

echo "==> Adding Jenkins signing key"
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7198F4B714ABFC68

# Export the key in binary format into the trusted keyrings directory
gpg --export 7198F4B714ABFC68 > /usr/share/keyrings/jenkins-keyring.gpg

echo "==> Adding Jenkins apt repository"
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/" \
  | tee /etc/apt/sources.list.d/jenkins.list > /dev/null

echo "==> Installing Jenkins"
apt-get update -y
apt-get install -y jenkins

echo "==> Installing Docker"
# get.docker.com is the official convenience script — installs the latest stable Docker Engine
curl -fsSL https://get.docker.com | sh

echo "==> Adding jenkins user to the docker group"
# Without this, Jenkins can't run docker commands (permission denied on /var/run/docker.sock)
usermod -aG docker jenkins

echo "==> Enabling and starting Jenkins service"
# systemctl enable makes Jenkins start at every boot automatically
systemctl enable jenkins
systemctl start jenkins

echo "==> Jenkins installation complete"
echo "Access Jenkins at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
