from tools.client_builder import session


def create_table(name, attribute_name, attribute_type = 'S', key_type = 'HASH', billing_mode = 'PAY_PER_REQUEST', read_capacity_units = 10, write_capacity_units = 10):
    client = session.client('dynamodb')
    existent_table_names = client.list_tables().get('TableNames')
    if name not in existent_table_names:
        if billing_mode == 'PAY_PER_REQUEST':
            client.create_table(TableName = name, AttributeDefinitions = [{'AttributeName': attribute_name, 'AttributeType': attribute_type}],
                KeySchema = [{'AttributeName': attribute_name, 'KeyType': key_type}], BillingMode = billing_mode)
        elif billing_mode == 'PROVISIONED':
            client.create_table(TableName = name, AttributeDefinitions = [{'AttributeName': attribute_name, 'AttributeType': attribute_type}],
                KeySchema = [{'AttributeName': attribute_name, 'KeyType': key_type}], 
                ProvisionedThroughput={'ReadCapacityUnits': read_capacity_units, 'WriteCapacityUnits': write_capacity_units})
        else:
            raise ValueError('Invalid billing_mode')