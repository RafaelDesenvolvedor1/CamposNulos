import os
import boto3
import dotenv

dotenv.load_dotenv()

region = os.getenv('AWS_DEFAULT_REGION')
key = os.getenv('AWS_ACCESS_KEY_ID')
secret = os.getenv('AWS_SECRET_ACCESS_KEY')

# bucket_name = 'backend-prd-bauk'

s3_client = boto3.client('s3')


def buscar_arquivos(bucket_name, caminho):
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=caminho,
    )

    arquivos = []

    # Em vez de pastas (CommonPrefixes), pegamos os arquivos (Contents)
    if 'Contents' in response:
        for item in response['Contents']:
            # Ignora caso o S3 retorne a própria pasta como item
            if item['Key'] != caminho:
                arquivos.append(item['Key'])

    return arquivos

print(buscar_arquivos('backend-prd-bauk', 'voxcred/bcard-prd/4a7936cb-8840-4d81-b25f-c8c422caa762/m1/downloadFile/'))

def baixar_arquivos_s3(bucket_name, s3_keys, pasta_destino="downloads"):
    """
    bucket_name: string com o nome do bucket
    s3_keys: lista de strings (retorno da sua função de listagem)
    pasta_destino: pasta local onde os arquivos serão salvos
    """
    # Garante que a pasta de destino exista no seu computador
    os.makedirs(pasta_destino, exist_ok=True)

    if not s3_keys:
        print("Nenhum arquivo fornecido para download.")
        return False

    downloads_com_sucesso = 0

    try:
        print(f"Iniciando o download em massa de {len(s3_keys)} arquivo(s)...")

        for s3_key in s3_keys:
            # Extrai apenas o nome final do arquivo (ex: 'BX_126_...csv')
            nome_arquivo = s3_key.split('/')[-1]

            # Ignora caso venha uma string vazia (ex: diretório raiz)
            if not nome_arquivo:
                continue

            # Monta o caminho local final (ex: 'downloads/BX_126_...csv')
            caminho_completo_local = os.path.join(pasta_destino, nome_arquivo)

            print(f"Baixando: {nome_arquivo}...")

            # Chama a API da AWS para fazer a transferência de cada arquivo
            s3_client.download_file(
                Bucket=bucket_name,
                Key=s3_key,
                Filename=caminho_completo_local
            )

            print(f"✅ Salvo em: {caminho_completo_local}")
            downloads_com_sucesso += 1

        print(f"\nDownload concluído! {downloads_com_sucesso}/{len(s3_keys)} arquivos baixados em '{pasta_destino}'.")
        return True

    except Exception as e:
        print(f"Erro durante o download em massa: {e}")
        return False
# print(listar_vox())

