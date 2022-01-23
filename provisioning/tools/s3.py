from tools.client_builder import session


def create_bucket(name, region = 'eu-west-1', acl = 'private'):
    s3_client = session.client('s3')
    existent_bucket_names = [bucket.get('Name') for bucket in s3_client.list_buckets().get('Buckets')]
    if name not in existent_bucket_names:
        s3_client.create_bucket(Bucket = name, ACL = acl, CreateBucketConfiguration = {'LocationConstraint': region})
        s3_client.put_public_access_block(Bucket=name, PublicAccessBlockConfiguration={'BlockPublicAcls': True, 'IgnorePublicAcls': True,
            'BlockPublicPolicy': True, 'RestrictPublicBuckets': True})
