from tools.client_builder import session


def create_security_group(name, source_ip = '0.0.0.0/0', source_name = None, protocol = 'tcp', from_port = 80, to_port = 80):
    ec2_client = session.client('ec2')
    ec2 = session.resource('ec2')
    security_group_available = ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [name]}],).get('SecurityGroups')
    if len(security_group_available) == 0:
        security_group_data = ec2_client.create_security_group(Description = name, GroupName = name, VpcId = 'vpc-054f995ed8e1250fe')
        security_group_id = security_group_data.get('GroupId')
    else:
        security_group_id = security_group_available[0].get('GroupId')
    

    security_group = ec2.SecurityGroup(security_group_id)
    allowed_ports = [permission.get('FromPort') for permission in security_group.ip_permissions]
    if from_port not in allowed_ports:
        if source_name != None:
            security_group.authorize_ingress(IpPermissions=[{'FromPort': from_port, 'IpProtocol': protocol, 'ToPort': to_port, 'UserIdGroupPairs': [{'GroupName': source_name}]}])
        else:
            security_group.authorize_ingress(CidrIp = source_ip, IpProtocol = protocol, FromPort = from_port, ToPort = to_port)

    return security_group.group_name, security_group_id
