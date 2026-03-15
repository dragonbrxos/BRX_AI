# BRX AI - Modelo de IA Leve para Arch Linux (v2.1)

O **BRX AI** é um modelo de inteligência artificial projetado para ser extremamente leve e eficiente, focado em rodar nativamente no **Arch Linux**. Ao contrário dos modelos tradicionais que utilizam arquivos de parâmetros gigantescos, o BRX utiliza uma estrutura modular baseada em **arquivos JSON** e processamento em **Python**.

## Novidades na Versão 2.1: Pesquisa Web Nativa

Agora o BRX AI possui a capacidade de **pesquisar na web em tempo real** utilizando o motor DuckDuckGo, sem a necessidade de chaves de API pagas. Isso permite que a IA acesse informações atualizadas sempre que seu cérebro local não possuir a resposta.

## Diferenciais do BRX

*   **Análise Granular:** O BRX não analisa apenas palavras, mas cada **letra e caractere** individualmente, permitindo uma compreensão profunda e precisa do texto.
*   **Pesquisa Web Ilimitada:** Função de busca integrada que pode ser ativada/desativada a qualquer momento.
*   **Extremamente Leve:** Projetado para notebooks e sistemas com recursos limitados, ocupando apenas alguns megabytes.
*   **Cérebro JSON:** Todo o conhecimento e raciocínio são armazenados em arquivos JSON legíveis e fáceis de manter.
*   **Nativo para Arch Linux:** Desenvolvido com foco na simplicidade e eficiência do ecossistema Arch.

## Estrutura do Cérebro

O "cérebro" do BRX é dividido em módulos:
- `brain/knowledge/`: Conhecimento categorizado (geral, código, ciência, tecnologia).
- `brain/index/`: Índices de palavras para busca rápida.
- `brain/reasoning/`: Fatos, conexões e lógica de pensamento.
- `brain/meta.json`: Metadados e estado atual da IA.

## Instalação no Arch Linux

### Método 1: Via Repositório (Recomendado)

1.  Clone o repositório:
    ```bash
    git clone https://github.com/dragonbrxos/BRX_AI.git
    cd BRX_AI
    ```

2.  Execute o script de instalação:
    ```bash
    chmod +x install.sh
    sudo ./install.sh
    ```

3.  Inicie o chat:
    ```bash
    brx
    ```

### Método 2: Via PKGBUILD (Padrão Arch)

1.  Clone o repositório e entre na pasta.
2.  Gere o pacote e instale:
    ```bash
    makepkg -si
    ```

## Como Usar

Após a instalação, basta digitar `brx` no seu terminal para iniciar uma conversa interativa com a IA. 

*   **Comando `web`:** Dentro do chat, digite `web` para ativar ou desativar a pesquisa na internet em tempo real.
*   **Comando `sair`:** Encerra a sessão do BRX.

O BRX analisará cada caractere da sua entrada para fornecer a resposta mais precisa baseada em seu cérebro JSON ou na web.

---
Desenvolvido por **dragonbrxos** com o auxílio do **Manus AI**.
