import sys
import pathlib
from simple_term_menu import TerminalMenu

# Arquivos de persistência de cache
CACHE_FILE = pathlib.Path(__file__).parent / ".path_cache"
HISTORY_FILE = pathlib.Path(__file__).parent / ".path_history"


def menu(options, title):
    return TerminalMenu(
        options,
        title=title,
        menu_cursor='> ',
        menu_cursor_style=("fg_cyan", "bold"),
        cycle_cursor=True,
        clear_screen=True,        # <-- Força a limpeza da tela antes de renderizar para evitar fantasmas
        clear_menu_on_exit=True   # <-- Remove o menu da tela ao sair, mantendo o terminal limpo
    )


def ler_historico():
    """Lê os diretórios salvos no histórico."""
    if not HISTORY_FILE.exists():
        return []
    linhas = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
    # Retorna apenas caminhos que ainda existem fisicamente na máquina
    return [l.strip() for l in linhas if l.strip() and pathlib.Path(l.strip()).exists()]


def salvar_no_historico(caminho):
    """Adiciona um caminho ao histórico, mantendo apenas os 5 mais recentes e sem duplicar."""
    caminhos = ler_historico()

    # Se o caminho já existe, removemos para reinseri-lo no topo (mais recente)
    if caminho in caminhos:
        caminhos.remove(caminho)

    caminhos.insert(0, caminho)

    # Limita aos 5 diretórios mais recentes
    caminhos = caminhos[:5]

    HISTORY_FILE.write_text("\n".join(caminhos), encoding="utf-8")


def escolherDir(forçar_selecao=False):
    # 1. Se já existir cache e não estivermos forçando, carrega o último direto
    if not forçar_selecao and CACHE_FILE.exists():
        caminho_salvo = CACHE_FILE.read_text(encoding="utf-8").strip()
        path_salvo = pathlib.Path(caminho_salvo)
        if path_salvo.exists():
            print(f" Diretório carregado do cache: {path_salvo}")
            return str(path_salvo)

    # 2. Se o usuário pediu para trocar, vamos dar a opção de pegar do Histórico Rápido
    historico = ler_historico()
    if historico:
        print("\n--- Atalhos de Diretórios Recentes ---")
        opcoes_historico = [f"⭐ {p}" for p in historico]
        opcoes_historico.append("[Navegar manualmente por outro diretório]")
        opcoes_historico.append(" [Sair]")

        menu_hist = menu(opcoes_historico, "Escolha um diretório recente ou navegue:")
        escolha_hist_idx = menu_hist.show()

        if escolha_hist_idx is None:
            sys.exit(0)

        opcao_hist = opcoes_historico[escolha_hist_idx]

        if "⭐" in opcao_hist:
            # Recupera o caminho limpo (tirando o emoji "⭐ ")
            caminho_escolhido = opcao_hist.replace("⭐ ", "").strip()
            # Atualiza o cache principal e o topo do histórico
            CACHE_FILE.write_text(caminho_escolhido, encoding="utf-8")
            salvar_no_historico(caminho_escolhido)
            print(f"\n⚡ Carregado via atalho: {caminho_escolhido}\n")
            return caminho_escolhido

        elif "Sair" in opcao_hist:
            sys.exit(0)

    # 3. Navegador Manual Tradicional (caso não escolha um recente)
    diretorio_atual = pathlib.Path.cwd()

    while True:
        subpastas = [item.name for item in diretorio_atual.iterdir() if item.is_dir()]
        opcoes = ["[Confirmar e usar este diretório] "]

        if diretorio_atual.parent != diretorio_atual:
            opcoes.append("[.. (Voltar para pasta anterior)] ")

        opcoes.extend(subpastas)
        opcoes.append("[Sair do Script] ")

        menu_diretorio = menu(opcoes,
                              f"Diretório atual: {diretorio_atual}\nSelecione uma pasta para entrar ou confirme:")
        escolha_idx = menu_diretorio.show()

        if escolha_idx is None:
            sys.exit(0)

        opcao_selecionada = opcoes[escolha_idx]

        if opcao_selecionada == "[Confirmar e usar este diretório] ":
            caminho_final = str(diretorio_atual)
            print(f"\n Diretório de trabalho selecionado: {caminho_final}\n")

            # Grava no cache e no histórico de recentes
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
        "Trocar Diretório de Trabalho",  # Limpar/alterar o cache
        "voltar"
    ]

    menu_acao = menu(opcoes_acao, "Selecione a ação: ")

    while True:
        idx_projeto = menu_acao.show()

        match idx_projeto:
            case 0 | 1 | 2 | 3:
                return opcoes_acao[idx_projeto]
            case _:
                return


def menu_dinamico(filesList, titulo="Selecione a opção:"):
    opcoes_str = [str(item) for item in filesList]
    # Passa o título customizado para a instância do TerminalMenu
    menu_fileList = menu(opcoes_str, titulo)
    return menu_fileList.show()