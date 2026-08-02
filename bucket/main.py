from bucket.aws_s3 import baixar_arquivos_s3
from bucket.aws_s3 import buscar_arquivos

def bx_vox(transactionuid, destino):
    bucket_name = 'backend-prd-bauk'
    caminho = buscar_arquivos(
        bucket_name=bucket_name,
        caminho=f'voxcred/bcard-prd/{transactionuid}/m1/downloadFile/',
    )
    baixar_arquivos_s3(
        bucket_name=bucket_name,
        s3_keys=caminho,
        pasta_destino=destino
    )

def bx_cred(transactionuid, destino):
    bucket_name = 'backend-prd-bauk'
    caminho_bx = buscar_arquivos(
        bucket_name=bucket_name,
        caminho=f'crediffato/prd/{transactionuid}/m1/downloadFile/',
    )

    baixar_arquivos_s3(
        bucket_name=bucket_name,
        s3_keys=caminho_bx,
        pasta_destino=destino
    )

    caminho_error_report= buscar_arquivos(
        bucket_name=bucket_name,
        caminho=f'crediffato/prd/{transactionuid}/m3/processWriteOffsFromM1Part/',
    )

    baixar_arquivos_s3(
        bucket_name=bucket_name,
        s3_keys=caminho_error_report,
        pasta_destino=destino
    )