from tools.client_builder import session

__elb_client = session.client('elbv2')


def create_target_group(name, port=80):
    tg_info = __elb_client.create_target_group(Name=name, Protocol='HTTP', Port=port, VpcId='vpc-054f995ed8e1250fe',
                                               HealthCheckProtocol='HTTP', HealthCheckPort='80', HealthCheckEnabled=True, HealthCheckPath='/', HealthCheckIntervalSeconds=60,
                                               HealthCheckTimeoutSeconds=10, HealthyThresholdCount=5, UnhealthyThresholdCount=5, Matcher={'HttpCode': '200'},
                                               TargetType='ip', IpAddressType='ipv4')
    return tg_info.get('TargetGroups')[0]


def create_elb(name, security_groups, target_group=None, subnets=['subnet-01df444f1cae62f36', 'subnet-06e902ec9fb5815d6']):
    response = __elb_client.create_load_balancer(Name=name, Subnets=subnets, SecurityGroups=security_groups,
                                                 Scheme='internet-facing', Type='application', IpAddressType='ipv4')
    lb_info = response.get('LoadBalancers')[0]
    if target_group != None:
        __elb_client.create_listener(LoadBalancerArn=lb_info.get('LoadBalancerArn'),
                                     Protocol=target_group.get('Protocol'), Port=target_group.get('Port'),
                                     DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group.get('TargetGroupArn'),
                                                      'ForwardConfig': {'TargetGroups': [{'TargetGroupArn':  target_group.get('TargetGroupArn'),
                                                                                          'Weight': 1}]}}])
    return lb_info
