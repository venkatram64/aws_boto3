from src.ec2.vpc import VPC
from src.client_locator import EC2Client
from src.ec2.ec2 import EC2


def main():
    # create a VPC

    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()
    print("VPC created: " + str(vpc_response))

    #Add name tag to VPC
    vpc_name = 'Boto3_VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    print('Added ' + vpc_name + ' to ' + vpc_id)

    #create an Internet Gateway
    ig_response = vpc.create_internet_gateway()

    ig_id = ig_response['InternetGateway']['InternetGatewayId']

    #attaching internet gateway to vpc
    vpc.attach_ig_to_vpc(vpc_id, ig_id)

    #Create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, "10.0.1.0/24")

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    print('Subnet created for VPC ' + vpc_id + " : " + str(public_subnet_response))

    # Add name tag to public subnet
    vpc.add_name_tag(public_subnet_id, "Boto3-Public-Subnet")

    #Create a public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)

    #Adding Internet Gateway to Public Route Table
    rt_id = public_route_table_response['RouteTable']['RouteTableId']

    vpc.create_ig_route_to_public_route_table(rt_id, ig_id)

    # Associate public subnet with route table
    vpc.associate_subnet_with_route_table(public_subnet_id, rt_id)

    #Allow auto-assign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)

    #Create a private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print("Created private subnet " + private_subnet_id + " for VPC " + vpc_id)

    #Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, "Boto3-Private-Subnet")


    #EC2 Instances
    ec2 = EC2(ec2_client)

    #Create a key pair
    key_pair_name = "Boto3-KeyPair"
    key_pair_response = ec2.create_key_pair(key_pair_name)

    print("Created key pair with name " + key_pair_name + " : " + str(key_pair_response))

    # Create a Security Group
    public_security_group_name = "Boto3-Public-SG"
    public_security_group_description = "Public Security Group for Public Subnet Internet Access"
    public_security_group_response = ec2.create_security_group(public_security_group_name, public_security_group_description, vpc_id)

    #Add public access to security group
    public_security_group_id = public_security_group_response['GroupId']

    # Add rule to public security group
    ec2.add_inbound_rule_to_sg(public_security_group_id)

    print("Added public access rule to security group " + public_security_group_name)

    user_data = """#!/bin/bash
                yum update -y
                yum install httpd24 -y
                service httpd start
                chkconfig httpd on
                echo "<html><body><h1>Hello from <b>Boto3</b> using Python!
                 </h1></body></html>" > /var/www/html/index.html"""


    ami_id = 'ami-xxxxxxx'

    #Launching public  EC2 Instance
    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, public_security_group_id, public_subnet_id, user_data)

    print("Launching public EC2 Instance using AMI ami-ddddddddd")

    #Adding another security group for private EC2 Instance
    private_security_group_name = "Boto3-Private-SG"
    private_security_group_description = "Private Security Group for private subnet"
    private_security_group_response = ec2.create_security_group(private_security_group_name, private_security_group_description,vpc_id)

    private_security_group_id = private_security_group_response['GroupId']

    #Add rule to private security group
    ec2.add_inbound_rule_to_sg(private_security_group_id)

    #Launching private EC2 Instance
    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, private_security_group_id, private_subnet_id, """""")

    print("Launching private EC2 Instance using AMI ami-dddddddddd")


def describe_instances():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.describe_ec2_instances()

    print(str(ec2_response))

def modify_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.modify_ec2_instances('i-xxxxxxxxxxxxx')


def stop_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.stop_instance('i-xxxxxxxxxxx')

    print(str(ec2_response))

def start_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.start_instance('i-xxxxxxxxxx')

    print(str(ec2_response))

def terminate_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.terminate_instance('i-xxxxxxxxxx')

    print(str(ec2_response))

if __name__ == '__main__':
    #main()
    #describe_instances()
    #modify_instance()
    #stop_instance()
    #start_instance()
    terminate_instance()