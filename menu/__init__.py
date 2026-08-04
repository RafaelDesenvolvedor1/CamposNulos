import sys
import pathlib
import questionary
import bucket.main as bk_main

# Arquivos de persistência de cache
CACHE_FILE = pathlib.Path(__file__).parent / ".path_cache"
HISTORY_FILE = pathlib.Path(__file__).parent / ".path_history"


def menu_select(options, title):
    style = questionary.Style([
        ('pointer', 'fg:cyan bold'),
        ('highlighted', 'fg:cyan bold'),
    ])

    escolha = questionary.select(
        title,
        choices=options,
        pointer='> ',
        use_indicator=False,
        style=style
    ).ask()

    if escolha is None:
        return None

    return options.index(escolha)


def ler_historico():
    if not HISTORY_FILE.exists():
        return []
    linhas = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in linhas if l.strip() and pathlib.Path(l.strip()).exists()]


def salvar_no_historico(caminho):
    caminhos = ler_historico()

    if caminho in caminhos:
        caminhos.remove(caminho)

    caminhos.insert(0, caminho)
    caminhos = caminhos[:5]

    HISTORY_FILE.write_text("\n".join(caminhos), encoding="utf-8")


def escolherDir(forçar_selecao=False):
    if not forçar_selecao and CACHE_FILE.exists():
        caminho_saved = CACHE_FILE.read_text(encoding="utf-8").strip()
        path_salvo = pathlib.Path(caminho_saved)
        if path_salvo.exists():
            print(f" Diretório carregado do cache: {path_salvo}")
            return str(path_salvo)

    historico = ler_historico()
    if historico:
        print("\n--- Atalhos de Diretórios Recentes ---")
        opcoes_historico = [f"⭐ {p}" for p in historico]
        opcoes_historico.append("[Navegar manualmente por outro diretório]")
        opcoes_historico.append(" [Sair]")

        escolha_hist_idx = menu_select(opcoes_historico, "Escolha um diretório recente ou navegue:")

        if escolha_hist_idx is None:
            sys.exit(0)

        opcao_hist = opcoes_historico[escolha_hist_idx]

        if "⭐" in opcao_hist:
            caminho_escolhido = opcao_hist.replace("⭐ ", "").strip()
            CACHE_FILE.write_text(caminho_escolhido, encoding="utf-8")
            salvar_no_historico(caminho_escolhido)
            print(f"\n⚡ Carregado via atalho: {caminho_escolhido}\n")
            return caminho_escolhido

        elif "Sair" in opcao_hist:
            sys.exit(0)

    diretorio_atual = pathlib.Path.cwd()

    while True:
        subpastas = [item.name for item in diretorio_atual.iterdir() if item.is_dir()]
        opcoes = ["[Confirmar e usar este diretório] "]

        if diretorio_atual.parent != diretorio_atual:
            opcoes.append("[.. (Voltar para pasta anterior)] ")

        opcoes.extend(subpastas)
        opcoes.append("[Sair do Script] ")

        escolha_idx = menu_select(
            opcoes,
            f"Diretório atual: {diretorio_atual}\nSelecione uma pasta para entrar ou confirme:"
        )

        if escolha_idx is None:
            sys.exit(0)

        opcao_selecionada = opcoes[escolha_idx]

        if opcao_selecionada == "[Confirmar e usar este diretório] ":
            caminho_final = str(diretorio_atual)
            print(f"\n Diretório de trabalho selecionado: {caminho_final}\n")

            CACHE_FILE.write_text(caminho_final, encoding="utf-8")
            salvar_no_historico(caminho_final)
            return caminho_final

        elif opcao_selecionada == "[.. (Voltar para pasta anterior)] ":
            diretorio_atual = diretorio_atual.parent

        elif opcao_selecionada == "[Sair do Script] ":
            sys.exit(0)

        else:
            diretorio_atual = diretorio_atual / opcao_selecionada


def escolherAcao():
    opcoes_acao = [
        "Criar Pastas",
        "Corrigir Campos nulos",
        "Titulo não bancarizado",
        "Trocar Diretório de Trabalho",
        "voltar"
    ]

    while True:
        idx_projeto = menu_select(opcoes_acao, "Selecione a ação: ")

        if idx_projeto is None:
            return None

        match idx_projeto:
            case 0 | 1 | 2 | 3:
                return opcoes_acao[idx_projeto]
            case _:
                return


def menu_dinamico(filesList, titulo="Selecione a opção:"):
    opcoes_str = [str(item) for item in filesList]
    return menu_select(opcoes_str, titulo)


# MODIFICAÇÃO: Aceita o parâmetro transaction_uid injetado do main.py
def escolherCliente(destino, transaction_uid):
    cliente = menu_dinamico(
        filesList=['Voxcred', 'Crediffato'],
        titulo='Escolha o projeto:'
    )

    match cliente:
        case 0:
            bk_main.bx_vox(
                transactionuid=transaction_uid,
                destino=destino
            )
        case 1:
            bk_main.bx_cred(
                transactionuid=transaction_uid,
                destino=destino
            )
        case _:
            return None


# MODIFICAÇÃO: Aceita o parâmetro transaction_uid injetado do main.py
def enviarParaCliente(orig, transaction_uid):
    cliente = menu_dinamico(
        filesList=['Voxcred', 'Crediffato'],
        titulo='Escolha o projeto:'
    )

    match cliente:
        case 0:
            bk_main.enviar_bx_vox(
                transactionuid=transaction_uid,
                origem=orig
            )
        case 1:
            bk_main.enviar_bx_cred(
                transactionuid=transaction_uid,
                origem=orig
            )
        case _:
            return None