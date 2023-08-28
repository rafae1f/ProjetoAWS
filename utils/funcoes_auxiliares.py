import os
import boto3
import requests
from botocore.exceptions import ClientError


def valida_email(email):
    url = "" #url do api gateway
    header = {
        "authorizationToken": email
    }
    response = requests.get(url, headers=header)
    return response


def valida_token(token):
    url = "" #url do api gateway
    header = {
        "authorizationToken": token
    }
    response = requests.get(url, headers=header)
    return response


def select_bucket_s3(response):
    response_data = response.json()
    data_id = response_data['body'][0]
    data_key = response_data['body'][1]
    session_token = response_data['body'][2]
    s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=data_id,
                             aws_secret_access_key=data_key, aws_session_token=session_token)
    print("Listando Buckets...")
    try:
        response_s3 = s3_client.list_buckets()
        if 'Buckets' in response_s3:
            buckets = response_s3['Buckets']
            bucket_names = [bucket['Name'] for bucket in buckets]
            print("Escolha um bucket:")
            for idx, name in enumerate(bucket_names, start=1):
                print(f"{idx}: {name}")
            selected_index = int(input("Digite o número do bucket desejado: ")) - 1
            if 0 <= selected_index < len(bucket_names):
                selected_bucket = bucket_names[selected_index]
                print(f"Você escolheu o bucket: {selected_bucket}")
                return selected_bucket
            else:
                print("Número inválido.")
        else:
            print("Nenhum bucket encontrado.")
    except Exception as e:
        print(f'Ocorreu um erro ao listar os buckets: {e}')


def insert_dados_s3(response, local_path, bucket_name):
    response_data = response.json()
    data_id = response_data['body'][0]
    data_key = response_data['body'][1]
    session_token = response_data['body'][2]
    s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=data_id,
                             aws_secret_access_key=data_key, aws_session_token=session_token)
    try:
        if os.path.exists(local_path):
            if os.path.isfile(local_path):
                # Upload de arquivo único
                file_name = os.path.basename(local_path)
                try:
                    s3_client.upload_file(local_path, bucket_name, file_name,
                                          ExtraArgs={'ServerSideEncryption': 'AES256'})
                    print(f'Arquivo "{file_name}" migrado para o bucket "{bucket_name}".')
                except ClientError as upload_error:
                    print(f'Ocorreu um erro ao fazer upload do arquivo "{file_name}": {upload_error}')
            elif os.path.isdir(local_path):
                # Upload de diretório inteiro
                for root, dirs, files in os.walk(local_path):
                    for file_name in files:
                        local_file_path = os.path.join(root, file_name)
                        s3_object_key = os.path.relpath(local_file_path, local_path)
                        try:
                            s3_client.upload_file(local_file_path, bucket_name, s3_object_key,
                                                  ExtraArgs={'ServerSideEncryption': 'AES256'})
                            print(
                                f'Arquivo "{file_name}" migrado para o bucket "{bucket_name}" como "{s3_object_key}".')
                        except ClientError as upload_error:
                            print(f'Ocorreu um erro ao fazer upload do arquivo "{file_name}": {upload_error}')
                print('Migração de dados concluída.')
            else:
                print('Caminho não é um arquivo nem um diretório válido.')
        else:
            print('Caminho não existe.')
    except Exception as e:
        print(f'Ocorreu um erro geral durante a migração dos dados: {e}')
