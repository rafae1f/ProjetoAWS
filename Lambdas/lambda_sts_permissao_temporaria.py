import boto3


def lambda_handler(event, context):
    sts_client = boto3.client('sts')

    # Defina os detalhes da função que o usuário assumirá temporariamente
    role_arn = ''
    role_session_name = ''

    # Defina a duração da sessão para 10 minutos (600 segundos)
    session_duration = 900

    # Solicite credenciais temporárias usando a função assume_role do STS
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
        DurationSeconds=session_duration
    )

    # Obtenha as credenciais temporárias
    temporary_credentials = assumed_role['Credentials']
    temporary_ID = str(temporary_credentials['AccessKeyId'])
    temporary_KEY = str(temporary_credentials['SecretAccessKey'])
    temporary_SESSION = str(temporary_credentials['SessionToken'])

    # Use temporary_credentials para acessar os recursos desejados com as permissões temporárias

    return {
        'statusCode': 200,
        'body': [temporary_ID, temporary_KEY, temporary_SESSION]
    }
