import boto3
import random

sns_client = boto3.client('sns', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')


def lambda_handler(event, context):
    token = generate_random_token(6)

    # Tópico do SNS para envio da mensagem
    topic_arn = ''

    sns_client.publish(
        TopicArn=topic_arn,
        Message=f"Seu token aleatório: {token}"
    )

    queue_url = ""  # Url da fila sqs
    sqs_client.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageBody=token
    )

    return {
        'statusCode': 200,
        'body': 'Token enviado com sucesso!'
    }


def generate_random_token(length):
    token = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return token
