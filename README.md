# Automação de Campos Nulos em CSV �

Script em Python para automação de tratamento de dados contábeis/financeiros.

## ✨ Funcionalidades
- Criação automática de estrutura de pastas por data (`original` / `modificado`).
- Listagem e escolha interativa de arquivos CSV.
- Limpeza de linhas com campos nulos em colunas específicas via **Pandas**.
- Geração de relatório de somatória acumulativa em TXT.

## ⚙️ Configuração Necessária

Antes de executar o script, você precisa configurar o diretório de trabalho no código-fonte:

1. Abra o arquivo `main.py`.
2. Localize a constante `CAMINHO_LOGICO` (logo no início do arquivo).
3. Altere o valor para o caminho da pasta onde você deseja que o script crie as pastas `original` e `modificado`.

## � Configuração por Cliente (Regra de Negócio)

Este script foi desenvolvido para suportar múltiplos diretórios de clientes. Para processar os dados de um cliente específico:

1. Localize a variável `CAMINHO_LOGICO` no arquivo `main.py`.
2. Insira o caminho da pasta raiz do cliente desejado.
3. O script criará automaticamente a estrutura `/DD-MM-YYYY/original` dentro deste diretório.

> **Nota:** Certifique-se de ter permissões de escrita no diretório informado.

Exemplo:
```python
# Se estiver no Windows:
CAMINHO_LOGICO = 'C:/Users/NomeUsuario/Documents/Processamento/'

# Se estiver no Linux:
CAMINHO_LOGICO = '/home/usuario/Documentos/testes/'

## � Como usar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute o `main.py`.
3. Escolha a opção [1] para preparar as pastas.
4. Coloque seus arquivos .csv na pasta `original` da data atual.
5. Escolha a opção [2] para processar.