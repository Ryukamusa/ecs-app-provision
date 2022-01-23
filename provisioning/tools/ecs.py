import json
from tools.client_builder import session


__client = session.client('ecs')


def create_ecs_cluster(name):
    __client.create_cluster(clusterName=name)


def create_task_definition(name, image='992209052841.dkr.ecr.eu-west-1.amazonaws.com/veo-sample-app:1.0', ports={'host': 80, 'container': 80}):
    iam = session.resource('iam')
    role = iam.Role('ecsTaskExecutionRole')

    task_response = __client.register_task_definition(family=name, executionRoleArn=role.arn,
                                                      networkMode='awsvpc', requiresCompatibilities=['FARGATE'], cpu='256', memory='512',
                                                      runtimePlatform={'operatingSystemFamily': 'LINUX'}, containerDefinitions=[
                                                          {'name': name, 'image': image,
                                                           'portMappings': [{
                                                               'hostPort': ports.get('host'),
                                                               'protocol': 'tcp',
                                                               'containerPort': ports.get('container')}],
                                                              'essential': True}])
    return task_response.get('taskDefinition')


## Should not create fargate with public IP but since my default vpc has public ip it was the way to make it work
def create_service_from_task(name, cluster_name, task_info, target_group_info, ecs_sg_id):
    __client.create_service(cluster=cluster_name, serviceName=name, taskDefinition=task_info.get('taskDefinitionArn'),
                            loadBalancers=[{'containerName': task_info.get('family'), 'containerPort': target_group_info.get('Port'),
                                            'targetGroupArn': target_group_info.get('TargetGroupArn')}],
                            desiredCount=2, launchType='FARGATE', platformVersion='LATEST',
                            networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'securityGroups': [
                                ecs_sg_id], 'subnets': ['subnet-01df444f1cae62f36', 'subnet-06e902ec9fb5815d6']}},
                            healthCheckGracePeriodSeconds=0, schedulingStrategy='REPLICA', enableECSManagedTags=True, enableExecuteCommand=False,
                            deploymentConfiguration={'maximumPercent': 200, 'minimumHealthyPercent': 100,
                                'deploymentCircuitBreaker': {'enable': False, 'rollback': False}})
