# Automação de Campos Nulos em CSV �

Script em Python para automação de tratamento de dados contábeis/financeiros, totalmente containerizado para rodar em qualquer ambiente sem necessidade de instalação local de dependências.

## ✨ Funcionalidades

- **Ambiente Isolado:** Roda via Docker (Python 3.13 + Pandas), garantindo que nada precise ser instalado na sua máquina real.
- **Criação Automática:** Estrutura de pastas por data (`original` / `modificado`).
- **Interatividade:** Listagem e escolha de arquivos CSV via terminal.
- **Limpeza Inteligente:** Remoção de linhas com campos nulos em colunas configuráveis.
- **Relatório Financeiro:** Geração de somatória acumulativa em arquivo `.txt`.

## ⚙️ Pré-requisitos

- **Docker** instalado e em execução.
- Permissões de execução de scripts no sistema operacional.

---

## � Como Usar (Linux / macOS)

1. **Build da Imagem** (apenas na primeira execução):

```bash
sudo docker build -t campos-nulos-app .
```

2. **Permissão de Execução:**

```bash
chmod +x start.sh
```

3. **Execução:**

```bash
./start.sh
```

---

## � Como Usar (Windows - PowerShell)
No Windows, para garantir que o Docker tenha acesso aos seus arquivos e que o mapeamento de volumes funcione corretamente, utilize o procedimento manual abaixo via PowerShell:

### 1. Build da Imagem
*(Apenas na primeira execução ou após alterar o código)*

```powershell
docker build -t campos-nulos-app .
```

### 2. Rodar o Container

Substitua o caminho entre aspas pelo diretório onde você deseja processar os arquivos.  
Certifique-se de usar aspas duplas e barras normais (`/`).

```powershell
docker run -it --rm -v "S:/Bauk/baixas/vox:/app/dados" -e CAMINHO_TRABALHO="/app/dados/" campos-nulos-app
```

### 3. Verificação de Volume

Ao abrir o menu, escolha a **Opção [1] - Preparar Pastas**.  
Se o mapeamento estiver correto, a pasta com a data de hoje aparecerá instantaneamente no seu drive `S:`.

---

### ⚠️ Importante para usuários de Windows

Se você estiver usando um drive diferente do `C:`, verifique se ele está habilitado no Docker Desktop em:

`Settings > Resources > File Sharing`

## � Estrutura de Pastas e Funcionamento

Ao executar qualquer um dos scripts acima, você informará o caminho da sua pasta de trabalho. O Docker fará o mapeamento automático (Volume) e organizará os dados da seguinte forma:

```plaintext
Sua-Pasta-de-Trabalho/
└── DD-MM-YYYY/
    ├── original/    # Coloque seus arquivos CSV aqui
    └── modificado/  # Resultados e relatórios aparecerão aqui
```

**Nota:** Graças ao uso do Docker, o comportamento do script é idêntico em qualquer sistema. O container isola as diferenças de sistema operacional, garantindo que a lógica de pastas e o processamento de dados funcionem sempre da mesma forma.