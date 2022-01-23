from tools.s3 import create_bucket
from tools.dynamodb import create_table
from tools.security_group import create_security_group
from tools.ecs import create_ecs_cluster, create_task_definition, create_service_from_task
from tools.elb import create_target_group, create_elb

BUCKET_NAME = 'veo-s3'
TABLE_NAME = 'veo-table'
ELB_SG_NAME = 'veo-elb'
ECS_SG_NAME = 'veo-ecs-service'
ECS_CLUSTER_NAME = 'veo-cluster'
ECS_TASK_NAME = 'veo-app'
ECS_SERVICE_NAME = 'veo-service'


## Provision S3
# create_bucket(BUCKET_NAME)

## Provision DynamoDb Table
# create_table(TABLE_NAME, 'key', billing_mode= 'PROVISIONED')

## Provision Security Groups
elb_sg_name, elb_sg_id = create_security_group(ELB_SG_NAME)
_, ecs_sg_id = create_security_group(ECS_SG_NAME, source_name = elb_sg_name)

## Provision ELB of application type with listener on port 80
tg_info = create_target_group('veo-ecs-tg')
elb_info = create_elb('veo-ecs-alb', [elb_sg_id], target_group = tg_info)


## Provision ECS cluster with service listening on ELB
create_ecs_cluster(ECS_CLUSTER_NAME)
task_arn = create_task_definition(ECS_TASK_NAME)
create_service_from_task(ECS_SERVICE_NAME, ECS_CLUSTER_NAME, task_arn, tg_info, ecs_sg_id)
