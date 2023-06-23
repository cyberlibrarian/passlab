#!/bin/bash
### 
### This is intended to be used the user-data section of an AWS
### Launch Template. The script will install all the components
### needed to create a GPU-powered password cracking instance
###
### https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html
###

# install kernel module build packages
#sudo yum remove falcon-sensor -y
sudo yum update -y
sudo amazon-linux-extras install epel -y
sudo yum groupinstall "Development Tools"
sudo yum install -y p7zip git gcc kernel-devel-$(uname -r)

# Install the GRID drivers from AWS
#aws s3 cp --recursive s3://ec2-linux-nvidia-drivers/latest/ .
#chmod +x NVIDIA-Linux-x86_64*.run
#sudo /bin/sh ./NVIDIA-Linux-x86_64*.run
# copy paste your aws creds first
#https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html

# Install the public NVIDIA Tesla T4 drivers
# Get the public NVIDIA drivers for Telsa T4 on CUDA 12
VERSION="525.105.17"
mkdir ~/src
cd ~/src/

#wget https://us.download.nvidia.com/tesla/${VERSION}/NVIDIA-Linux-x86_64-${VERSION}.run
#chmod +x NVIDIA-Linux-x86_64-${VERSION}.run
# TODO: Make this happen silently with no UI
#sudo ./NVIDIA-Linux-x86_64-${VERSION}.run

wget https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_530.30.02_linux.run
sudo sh cuda_12.1.1_530.30.02_linux.run --tmpdir=/home/ec2-user/ --silent --installpath=/home/ec2-user/local
# TODO: Add this to the global bash scripts so we don't need to set it manual
export PATH=/home/ec2-user/local/bin:$PATH
export LD_LIBRARY_PATH=/home/ec2-user/local/lib64:$LD_LIBRARY_PATH

# For NVIDIA driver version >= 14.x on G4dn instances, disable GSP
sudo touch /etc/modprobe.d/nvidia.conf
echo "options nvidia NVreg_EnableGpuFirmware=0" | sudo tee --append /etc/modprobe.d/nvidia.conf

# Set GPU clock speed to maxiumum on G4dn instances
# TODO: Set this permanently
sudo nvidia-smi -ac 5001,1590

# Reboot
sudo reboot

####################################################################

# For VNC Desktop of Port Forward
# from https://repost.aws/knowledge-center/ec2-linux-2-install-gui
# sudo amazon-linux-extras install epel -y
# sudo amazon-linux-extras install mate-desktop1.x -y
# sudo bash -c 'echo PREFERRED=/usr/bin/mate-session > /etc/sysconfig/desktop'
# sudo yum install tigervnc-server -y
# sudo mkdir /etc/tigervnc
# sudo bash -c 'echo localhost > /etc/tigervnc/vncserver-config-mandatory'
# sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@.service
# sudo sed -i 's/<USER>/ec2-user/' /etc/systemd/system/vncserver@.service
# sudo systemctl daemon-reload
# sudo systemctl enable vncserver@:1
# sudo systemctl start vncserver@:1
# echo SecurityTypes=None >> ~/.vnc/config
# sudo systemctl daemon-reload
# sudo yum install chromium

# Grow the /home directory to the full size that we added to the EBS store
#sudo lsblk
#sudo pvs
#sudo pvresize /dev/nvme1n1
#sudo lvextend -l +100%FREE /dev/datavg/lvhome
#sudo xfs_growfs /dev/datavg/lvhome
