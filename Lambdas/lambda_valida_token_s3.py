import boto3


def lambda_handler(event, context):
    sqs = boto3.client('sqs', region_name='us-east-1')
    queue_url = ''  # Url da fila sqs
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    if "Messages" in response:
        token = response["Messages"][0]["Body"]

        if token == event['authorizationToken']:
            auth = 'Allow'
            receipt_handle = response["Messages"][0]["ReceiptHandle"]
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
    else:
        auth = 'Deny'

    authorizationpolicy = {"principalId": "authpolicy02", "policyDocument": {"Version": "2012-10-17", "Statement": [
        {"Action": "execute-api:Invoke", "Effect": auth,
         "Resource": [""]}]}}
    return authorizationpolicy
