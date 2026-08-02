"""
1 - Definir o diretório
2 - definir coluna a ser analisada
3 - definir critério para remoção de linha
4 - retornar o novo arquivo na pasta mod
"""

import pathlib
from unittest import case

import pandas as pd
import sys
from simple_term_menu import TerminalMenu
import menu
from bucket.main import bx_vox


def renderizarMenu():
    print("""
    1. Criar Pastas
    2. Corrigir Campos nulos
    (Pressione qualquer tecla para sair)  
    """)


# Criar diretórios
def retornarDataAtual():
    import datetime
    getDate = datetime.datetime.now()
    return getDate.strftime("%d-%m-%Y")


def criarDiretorio(caminho):
    diretorio = pathlib.Path(caminho)
    dataHoje = retornarDataAtual()
    pastaIntermediaria = menu.menu_dinamico(['Data de hoje', 'Escolher nome', 'Sair'])

    match pastaIntermediaria:
        case 0:
            pastaIntermediaria = dataHoje
        case 1:
            pastaIntermediaria = input('Informe o nome do arquivo: ')
        case _:
            return

    dirOrig = diretorio / pastaIntermediaria / 'orig'
    dirMod = diretorio / pastaIntermediaria / 'mod'

    dirOrig.mkdir(parents=True, exist_ok=True)
    dirMod.mkdir(parents=True, exist_ok=True)
    print(f"\nPastas criadas com sucesso em: {pastaIntermediaria}")


# NOVO MÉTODO: Permite o usuário navegar e escolher qual pasta quer processar
def escolherSubdiretorio(caminho_base):
    diretorio = pathlib.Path(caminho_base)

    # 1. Filtramos apenas os diretórios dentro do caminho base
    subdiretorios_path = [item for item in diretorio.iterdir() if item.is_dir()]

    if not subdiretorios_path:
        print("\n⚠️ Nenhuma pasta encontrada no diretório base! Crie uma primeiro.")
        return None

    # 2. Ordenamos os objetos Path pela data de modificação (st_mtime)
    # reverse=True garante que as pastas criadas/modificadas MAIS RECENTEMENTE fiquem no topo da lista (índice 0)
    subdiretorios_path.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # 3. Extraímos apenas os nomes para exibir no menu dinâmico
    subdiretorios_nomes = [item.name for item in subdiretorios_path]

    print("\n--- Selecione a pasta do lote que deseja processar ---")
    opcao = menu.menu_dinamico(subdiretorios_nomes)

    if opcao is None:
        return None

    # 4. Retornamos o caminho completo baseado no objeto Path ordenado correspondente
    return subdiretorios_path[opcao]


# 3 - Procurar o arquivo.csv dentro da pasta 'orig'.
def listarArquivos(caminho):
    pasta = pathlib.Path(caminho)
    # Lista arquivos .csv (inclusive os já marcados como [FEITO] para caso queira reprocessar)
    arquivos = [item.name for item in pasta.glob('*.csv') if item.is_file()]
    return arquivos

# ALTERADO: Adicionada opção de voltar ao menu principal
def escolherArquivo(lista_arquivos):
    # Criamos uma nova lista com a opção de voltar no topo
    opcoes = ["[Voltar para o Menu Principal]"] + lista_arquivos

    # Passamos o título desejado diretamente para o menu dinâmico
    titulo_menu = "--- Arquivos encontrados na pasta Original (orig) ---"
    opcao = menu.menu_dinamico(opcoes, titulo_menu)

    # Se o usuário apertar 'Esc' ou escolher a primeira opção (índice 0), retornamos None
    if opcao is None or opcao == 0:
        return None

    # Como adicionamos um item no topo, o índice do arquivo real é 'opcao - 1'
    return lista_arquivos[opcao - 1]

# 4 - Vai analisar a coluna que eu determinar em uma constante e separar quais linhas dessa coluna estão vazias.
def analisarCSV(arquivo, coluna, valores_remover=None):
    # Usamos sep=None com o motor 'python' para auto-detectar o separador nos dois fluxos de forma idêntica
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')

    if valores_remover is not None:
        # 1. Convertemos os valores a remover para strings limpas
        valores_remover_str = [str(val).strip() for val in valores_remover]

        # 2. Convertemos a coluna alvo para strings limpas (ex: remove .0 de floats se houver)
        coluna_str = df[coluna].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        # 3. Pegamos os índices exatos de onde esses valores aparecem
        filtrados = df[coluna_str.isin(valores_remover_str)]
        indices = filtrados.index.tolist()
    else:
        # Fluxo original de campos nulos
        vazias = df[df[coluna].isna() | (df[coluna].astype(str).str.strip() == "")]
        indices = vazias.index.tolist()

    return df, indices

# 4.1 - Lê o arquivo de erro e extrai os N_DOCs (4ª coluna / índice 3)
def analisarNdocs(caminho_erro):
    if not caminho_erro.exists():
        print(f"⚠️ Atenção: Arquivo de erro '{caminho_erro.name}' não encontrado nesta pasta!")
        return []

    df = pd.read_csv(caminho_erro, sep=';', header=None, engine='python', encoding='utf-8-sig')
    valores_quarta_coluna = df[3].dropna().unique().tolist()

    documentos_limpos = []
    for val in valores_quarta_coluna:
        try:
            documentos_limpos.append(int(float(val)))
        except ValueError:
            documentos_limpos.append(str(val).strip())

    return list(set(documentos_limpos))

# 5 - Vai pegar a lista do passo anterior, excluir as linhas do arquivo.csv.
def excluirLinhas(df_original, linhasExcluir):
    df_novo = df_original.drop(index=linhasExcluir)
    return df_novo

# 6 - Após apagar as linhas, vai salvar o arquivo modificado na pasta 'mod'.
def modificarSalvar(arquivoEntrada, arquivoSaida, coluna):
    if coluna == 'VALOR_OPR':
        df_origem, indices = analisarCSV(arquivoEntrada, coluna)
        df_final = excluirLinhas(df_origem, indices)
        df_final.to_csv(arquivoSaida, index=False, sep=';', encoding='utf-8-sig')
        return df_final

    elif coluna == 'N_DOC':
        caminho_erro = pathlib.Path(arquivoEntrada).parent / "error-report-0"

        # 1. Separamos os títulos do error-report-0
        documentos_para_remover = analisarNdocs(caminho_erro)
        print(f"Documentos identificados para remoção: {documentos_para_remover}")

        # 2. Como seu arquivo original tem cabeçalho (VALOR_OPR, N_DOC, etc.),
        # a 4ª coluna real tem o nome correspondente (no caso, 'N_DOC')
        # Buscamos os índices dessas linhas usando nossa nova versão da analisarCSV
        df_origem, indices = analisarCSV(arquivoEntrada, coluna, valores_remover=documentos_para_remover)

        # 3. Excluímos as linhas usando o mesmo método físico de drop por índice
        df_final = excluirLinhas(df_origem, indices)

        # 4. Salvamos mantendo o cabeçalho original
        df_final.to_csv(arquivoSaida, index=False, sep=';', encoding='utf-8-sig')
        return df_final

# 7 - Vai somar todos os valores da coluna 'Valor operacional'
def somarColuna(df):
    if 'VALOR_OPR' in df.columns:
        total = pd.to_numeric(df['VALOR_OPR'], errors='coerce').sum()
    else:
        total = pd.to_numeric(df[5], errors='coerce').sum()
    return total

def criarArquivoTXT(diretorio, nome_arquivo, soma_valor):
    diretorioFinal = pathlib.Path(diretorio) / "Historico_Somas.txt"
    with open(diretorioFinal, mode='a', encoding='utf-8') as f:
        f.write(f"Arquivo: {nome_arquivo} | Soma: R$ {soma_valor:.2f} \n")

# NOME DO MÉTODO ATUALIZADO: fluxo genérico para processar qualquer limpeza de arquivo
def processarArquivo(caminho_base, coluna):
    # 1. Escolher interativamente qual lote/pasta processar
    pasta_selecionada = escolherSubdiretorio(caminho_base)
    if not pasta_selecionada:
        return

    pasta_original = pasta_selecionada / "orig"
    pasta_modificado = pasta_selecionada / "mod"


    # 2.1 Buscar o arquivo da baixa no bucket
    match menu.menu_dinamico(['Sim', 'Não'], 'Quer buscar o arquivo no bucket?'):
        case 0:
            menu.escolherCliente(destino=pasta_original)



    # 2.2 Listar arquivos disponíveis na pasta "orig" correspondente
    arquivos = listarArquivos(pasta_original)

    if not arquivos:
        print(f"❌ Nenhum arquivo CSV encontrado em: {pasta_original}")
        return

    # 3. INTERAÇÃO COM USUÁRIO: Escolher qual arquivo processar
    nome_selecionado = escolherArquivo(arquivos)

    # Se o usuário escolheu "Voltar" (retorna None), cancelamos a operação graciosamente
    if nome_selecionado is None:
        print("\n↩️ Operação cancelada. Retornando ao menu principal...")
        return

    path_entrada = pasta_original / nome_selecionado
    path_saida = pasta_modificado / nome_selecionado

    print(f"\nProcessando: {nome_selecionado}...")

    # 4. Executar a limpeza e salvar CSV
    df_limpo = modificarSalvar(path_entrada, path_saida, coluna)

    # 5. Gerar a soma e o relatório TXT
    total = somarColuna(df_limpo)
    criarArquivoTXT(pasta_modificado, nome_selecionado, total)

    # 6. MARCAR COMO FEITO: Renomeia o arquivo original para indicar conclusão
    if not nome_selecionado.startswith("[FEITO] - "):
        novo_nome = f"[FEITO] - {nome_selecionado}"
        path_entrada.rename(pasta_original / novo_nome)
        print(f"� Arquivo original marcado como processado: '{novo_nome}'")

    print(f"\n✅ Sucesso! Arquivo gerado e salvo na pasta 'mod'.")


def main():
    # Inicializa definindo o diretório de trabalho usando cache
    CAMINHO_LOGICO = menu.escolherDir()

    while True:
        escolha = menu.escolherAcao()

        match escolha:
            case 'Criar Pastas':
                criarDiretorio(CAMINHO_LOGICO)
            case 'Corrigir Campos nulos':
                processarArquivo(CAMINHO_LOGICO, 'VALOR_OPR')
            case 'Titulo não bancarizado':
                processarArquivo(CAMINHO_LOGICO, 'N_DOC')
            case 'Trocar Diretório de Trabalho':
                # Força a re-seleção do diretório de trabalho e atualiza a variável global do loop
                CAMINHO_LOGICO = menu.escolherDir(forçar_selecao=True)
            case _:
                print("Saindo...")
                break


main()