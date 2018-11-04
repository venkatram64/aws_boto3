step 1: sudo apt-get install python-pip
step 2: sudo pip install awscli
step 3(a): pip install boto3
step 3(b): pip install pyboto3

step 4: create aws free account
capture the following information from you account
 
    step 1: IAM (Welcome to Identity and Access Management)
    step 2: User Creation
      user name: deployment
      
      access type: programatic access
      
    step 3: click "Copy Permissions from existing user"
    step 4: click "Attach existing policies directly"
    step 5: check "Administrator Access"
    step 6: click "Next Review"
    step 7: click "Create user"
    deployment  xxxxxxxxxxxxx    xxxxxxxxxxxxxxx 

step 5:
aws configure

AWS Access Key ID [None]: XXXXXXXX
AWS Secret Access Key [None]: XXXXXXXX
Default region name [None]: us-east-1
Default output format [None]: json



below information is for installing docker on ubuntu

step 1: sudo apt-get update
step 2: sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
 
 
step 3: sudo gedit /etc/apt/sources.list.d/docker.list
copy this
deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable
step 4:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
step 5: sudo apt-get update
sudo apt install docker-ce
step 6: sudo docker run hello-world

below information for installing pycharm on ubuntu

sudo snap install --classic pycharm-community
