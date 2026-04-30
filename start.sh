#!/bin/bash

# --- CONFIGURAÇÃO ---
# Defina aqui o caminho que você MAIS usa no seu Debian
CAMINHO_PADRAO="/home/rafael/Compartilhado/Bauk/boraFazerMerda/baixas/vox/"
NOME_IMAGEM="campos-nulos-app"
# --------------------

clear
echo "===================================================="
echo "          PROCESSADOR DE CAMPOS NULOS               "
echo "===================================================="
echo ""

# Pergunta o caminho, sugerindo o padrão entre colchetes
echo "Qual pasta deseja processar?"
echo "Pressione ENTER para usar o padrão: $CAMINHO_PADRAO"
read -p "Caminho: " USER_PATH

# Se o usuário não digitou nada (vazio), usa o CAMINHO_PADRAO
USER_PATH=${USER_PATH:-$CAMINHO_PADRAO}

# Validação: Verifica se a pasta existe de fato
if [ ! -d "$USER_PATH" ]; then
    echo ""
    echo "❌ ERRO: O diretório '$USER_PATH' não existe."
    exit 1
fi

echo ""
echo "� Iniciando Container..."
echo "� Mapeando: $USER_PATH -> /app/dados"
echo "----------------------------------------------------"

# Execução do Docker
# -it: Interativo (para o menu)
# --rm: Remove o container ao fechar (limpeza)
# -v: Faz a ponte entre as pastas
# -e: Diz ao Python qual pasta usar lá dentro
sudo docker run -it --rm \
  -v "$USER_PATH:/app/dados" \
  -e CAMINHO_TRABALHO="/app/dados/" \
  $NOME_IMAGEM

echo ""
echo "✅ Execução finalizada."