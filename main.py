from utils.funcoes_auxiliares import valida_email, valida_token, select_bucket_s3, insert_dados_s3


def main():
    validador = True
    while validador:
        print("\n=============== MENU ===============")
        print("[1] Enviar Dados Para Bucket S3")
        print("[2] Sair")

        opcao = int(input("\nEscolha Uma Opção: "))

        if opcao == 1:
            print("Módulo S3 - Envio De Dados Para Bucket S3")
            email = input("Digite Seu Email: ")

            response = valida_email(email)

            if response.status_code == 200:
                print("Solicitando Token De Acesso Temporario, Verifique Seu E-mail.")
                token = input("Informe O Código Recebido Em Seu E-mail: ")

                response = valida_token(token)

                if response.status_code == 200:
                    print("Acesso Liberado!")
                    while True:
                        print("\n=============== MENU ===============")
                        print("[1] Transferir Dados Para o Bucket S3")
                        print("[2] Sair")

                        opcao = int(input("\nEscolha Uma Opção: "))

                        if opcao == 1:
                            bucket_s3_data = select_bucket_s3(response)
                            if bucket_s3_data:
                                local_path = input("Digite o caminho para o diretório local ou arquivo: ")
                                insert_dados_s3(response, local_path, bucket_s3_data)
                        elif opcao == 2:
                            print("Saindo... Obrigado por utilizar a aplicação!")
                            return True
                        else:
                            print("Opção Inválida. Tente Novamente.")
                else:
                    print(f"Acesso Negado. Token: {token} Informado É Inválido.")
            else:
                print(f"O Email: {email} Informado Não Possui Permissão De Acesso.")
        elif opcao == 2:
            print("Saindo... Obrigado por utilizar a aplicação!")
            validador = False
        else:
            print("Opção Inválida")


if __name__ == "__main__":
    main()
