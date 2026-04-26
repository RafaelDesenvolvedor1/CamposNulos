"""
1 - Definir um diretório para o script trabalhar (pode ser um caminho lógico)
2 - Criar uma pasta pegando a data atual do sistema, dentro dessa pasta criar mais duas pastas(Original e Modificado).
3 - Procurar o arquivo.csv dentro da pasta 'original'.
4 - Vai analisar a coluna que eu determinar em uma constante e separar quais linhas dessa coluna estão vazias (Retorna uma lista do que encontrar).
5 - Vai pegar a lista do passo anterior, excluir as linhas do arquivo.csv.
6 - Após apagar as linhas, vai salvar o arquivo modificado na pasta 'modificado'.
7 - vai somar todos os valores da coluna eu determinei no passo 4 e criar um arquivo.txt na pasta 'modificado'.
"""

import pathlib
import pandas as pd

def renderizarMenu():
    print("""
    1. Criar Pastas
    2. Corrigir Campos nulos
    (Pressione qualquer tecla para sair)  
    """)

# Definir um caminho lógico
CAMINHO_LOGICO = '/home/rafael/Compartilhado/python/testes/'

# Coluna para verificar
COLUNA_VERIFICAR = 'VALOR_OPR'

# Criar diretórios
def retornarDataAtual():
    import datetime
    getDate = datetime.datetime.now()
    return getDate.strftime("%d-%m-%Y")

def criarDiretorio(caminho, nomeDaPasta):
    diretorio = pathlib.Path(caminho)
    dataHoje = retornarDataAtual()
    caminhoDefinido = diretorio / dataHoje / nomeDaPasta

    if not caminhoDefinido.exists():
        caminhoDefinido.mkdir(parents=True)
        print("Pasta criada com sucesso!")
    else:
        print("Diretório já foi criado")

# 3 - Procurar o arquivo.csv dentro da pasta 'original'.
def lisarArquivos(caminho):
    pasta = pathlib.Path(caminho)
    arquivos = [item.name for item in pasta.glob('*.csv') if item.is_file()]
    return arquivos


def escolherArquivo(lista_arquivos):
    print("\n--- Arquivos encontrados na pasta Original ---")
    for i, arquivo in enumerate(lista_arquivos, start=1):
        print(f"[{i}] - {arquivo}")

    while True:
        try:
            opcao = int(input("\nDigite o número do arquivo que deseja processar: "))
            if 1 <= opcao <= len(lista_arquivos):
                return lista_arquivos[opcao - 1]
            else:
                print("Opção inválida! Escolha um número da lista.")
        except ValueError:
            print("Entrada inválida! Digite apenas o número.")

# 4 - Vai analisar a coluna que eu determinar em uma constante e separar quais linhas dessa coluna estão vazias (Retorna uma lista do que encontrar).
def analisarCSV(arquivo ,coluna):
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')
    vazias = df[df[coluna].isna() | (df[coluna].astype(str).str.strip() == "")]
    return df, vazias.index.tolist()
    # print(f"Linhas em branco: {indices}")

# 5 - Vai pegar a lista do passo anterior, excluir as linhas do arquivo.csv.
def excluirLinhas(df_original, linhasVazias):
    df_novo = df_original.drop(index=linhasVazias)
    return df_novo

# 6 - Após apagar as linhas, vai salvar o arquivo modificado na pasta 'modificado'.
def modificarSalvar(arquivoEntrada, arquivoSaida, coluna):
    df_origem, indices = analisarCSV(arquivoEntrada, coluna)
    df_final = excluirLinhas(df_origem, indices)
    df_final.to_csv(arquivoSaida, index=False, sep=';', encoding='utf-8-sig')
    return df_final

# 7 - vai somar todos os valores da coluna eu determinei no passo 4 e criar um arquivo.txt na pasta 'modificado'.
def somarColuna(df, coluna):
    total = pd.to_numeric(df[coluna], errors='coerce').sum()
    return total


def criarArquivoTXT(diretorio, nome_arquivo, soma_valor):
    diretorioFinal = pathlib.Path(diretorio) / "Historico_Somas.txt"
    with open(diretorioFinal, mode='a', encoding='utf-8') as f:
        f.write(f"Arquivo: {nome_arquivo} | Soma: R$ {soma_valor:.2f} \n")


def resolverCamposNulos(caminho_base, coluna):
    # 1. Preparar caminhos
    data_hoje = retornarDataAtual()
    pasta_original = pathlib.Path(caminho_base) / data_hoje / "original"
    pasta_modificado = pathlib.Path(caminho_base) / data_hoje / "modificado"

    # 2. Listar arquivos disponíveis
    arquivos = lisarArquivos(pasta_original)

    if not arquivos:
        print(f"Nenhum arquivo CSV encontrado em: {pasta_original}")
        return

    # 3. INTERAÇÃO COM USUÁRIO: Escolher qual arquivo processar
    nome_selecionado = escolherArquivo(arquivos)

    path_entrada = pasta_original / nome_selecionado
    path_saida = pasta_modificado / nome_selecionado

    print(f"\nProcessando: {nome_selecionado}...")

    # 4. Executar a limpeza e salvar CSV
    df_limpo = modificarSalvar(path_entrada, path_saida, coluna)

    # 5. Gerar a soma e o relatório TXT
    total = somarColuna(df_limpo, coluna)
    criarArquivoTXT(pasta_modificado, nome_selecionado, total)

    print(f"\n✅ Sucesso! Relatórios gerados na pasta 'modificado'.")

while True:
    renderizarMenu()
    escolha = input("Digite uma opção: ")

    match escolha:
        case '1':
            criarDiretorio(CAMINHO_LOGICO, "original")
            criarDiretorio(CAMINHO_LOGICO, "modificado")
        case '2':
            # Aqui ele já vai listar os arquivos e pedir o número
            resolverCamposNulos(CAMINHO_LOGICO, COLUNA_VERIFICAR)
        case _:
            print("Saindo...")
            break





