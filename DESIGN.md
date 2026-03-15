# Arquitetura do BRX AI

Este documento descreve a arquitetura proposta para o modelo de IA BRX, um sistema leve e modular projetado para rodar nativamente no Arch Linux. O foco principal é a utilização de arquivos JSON para o armazenamento do "cérebro" da IA, garantindo leveza e facilidade de manutenção.

## 1. Visão Geral

O BRX AI será composto por três componentes principais:

*   **BRX Core (`brx.py`):** O coração da aplicação, responsável por carregar o cérebro, processar as entradas do usuário e gerar respostas.
*   **Cérebro (`brain/`):** Uma coleção de arquivos JSON que armazenam o conhecimento, o raciocínio e os índices da IA.
*   **Interface de Chat (`cli.py`):** Uma interface de linha de comando (CLI) para interação com o usuário.

## 2. BRX Core (`brx.py`)

Este será o script principal em Python que orquestra as operações do BRX. Suas responsabilidades incluirão:

*   **Carregamento do Cérebro:** Inicializar e carregar os dados dos arquivos JSON do diretório `brain/`.
*   **Processamento de Entrada:** Analisar as consultas do usuário, extrair palavras-chave e identificar a intenção.
*   **Motor de Inferência:** Utilizar os dados do cérebro para buscar informações relevantes, realizar raciocínio básico e formular uma resposta.
*   **Geração de Resposta:** Construir uma resposta em linguagem natural a partir das informações recuperadas e inferidas.

## 3. Cérebro (`brain/`)

O cérebro do BRX será uma estrutura de diretórios contendo arquivos JSON, projetada para ser modular e facilmente extensível. A estrutura será a seguinte:

```
brain/
├── meta.json
├── index/
│   └── words.json
├── knowledge/
│   ├── general.json
│   ├── code.json
│   ├── science.json
│   └── tech.json
├── reasoning/
│   ├── facts.json
│   ├── connections.json
│   └── questions.json
└── visited.json
```

### 3.1. `meta.json`

Este arquivo armazenará metadados sobre o estado atual do cérebro, como:

*   `nome`: Nome do modelo (e.g., "CEREBRO")
*   `versao`: Versão da estrutura do cérebro.
*   `nascimento`: Data e hora de criação do cérebro.
*   `ciclos`: Número de ciclos de treinamento/atualização.
*   `estado`: Estado atual (e.g., "consciente", "treinando").
*   `total_blocos`: Número total de blocos de conhecimento.
*   `total_fatos`: Número total de fatos armazenados.
*   `total_paginas`: Número total de "páginas" ou documentos de conhecimento.
*   `ultimo_ciclo`: Data e hora do último ciclo de atualização.

### 3.2. `index/words.json`

Um índice invertido que mapeia palavras-chave para os IDs dos blocos de conhecimento onde elas aparecem. Isso permitirá uma recuperação rápida de informações relevantes com base nas palavras da consulta do usuário.

### 3.3. `knowledge/*.json`

Estes arquivos conterão o corpo principal do conhecimento da IA, categorizado por tópicos. Cada entrada será um objeto JSON com os seguintes campos:

*   `id`: Um identificador único para o bloco de conhecimento.
*   `texto`: O conteúdo textual do conhecimento.
*   `categoria`: A categoria do conhecimento (e.g., "general", "code").
*   `fonte`: URL ou referência da fonte original.
*   `titulo`: Título do bloco de conhecimento.
*   `topico`: Tópico principal do conhecimento.
*   `palavras`: Lista de palavras-chave associadas a este bloco.

### 3.4. `reasoning/facts.json`

Armazenará fatos atômicos ou informações derivadas que podem ser usadas para raciocínio. Cada fato pode ter um ID, uma declaração e uma referência ao bloco de conhecimento de onde foi extraído.

### 3.5. `reasoning/connections.json`

Definirá as relações e conexões entre diferentes blocos de conhecimento ou fatos. Isso pode incluir tipos de conexão como "mesma_pagina", "relacionado_a", "causa_efeito", etc., com um peso associado para indicar a força da conexão.

### 3.6. `reasoning/questions.json`

Armazenará perguntas comuns e suas respostas diretas ou referências a blocos de conhecimento que contêm a resposta. Isso pode ajudar a IA a responder a perguntas frequentes de forma mais eficiente.

### 3.7. `visited.json`

Um arquivo para registrar blocos de conhecimento que foram "visitados" ou utilizados em interações anteriores, para evitar repetições ou para fins de aprendizado/otimização.

## 4. Interface de Chat (`cli.py`)

Este script fornecerá uma interface de linha de comando simples para o usuário interagir com o BRX. Ele será responsável por:

*   Exibir um prompt para o usuário.
*   Capturar a entrada do usuário.
*   Enviar a entrada para o BRX Core.
*   Exibir a resposta do BRX Core ao usuário.
*   Manter um histórico da conversa.

## 5. Fluxo de Interação (Exemplo)

1.  O usuário digita uma pergunta no `cli.py`.
2.  `cli.py` envia a pergunta para `brx.py`.
3.  `brx.py` processa a entrada:
    *   Extrai palavras-chave.
    *   Consulta `index/words.json` para encontrar blocos de conhecimento relevantes.
    *   Recupera os blocos de `knowledge/*.json`.
    *   Utiliza `reasoning/facts.json` e `reasoning/connections.json` para inferir uma resposta.
    *   Verifica `reasoning/questions.json` para respostas diretas.
4.  `brx.py` gera uma resposta em linguagem natural.
5.  `brx.py` envia a resposta de volta para `cli.py`.
6.  `cli.py` exibe a resposta ao usuário.

## 6. Considerações para Leveza e Desempenho

*   **JSON:** A escolha do JSON para o cérebro visa a leveza e a facilidade de leitura/escrita, evitando a necessidade de bancos de dados complexos.
*   **Indexação:** O `index/words.json` será crucial para a velocidade de recuperação, minimizando a necessidade de varrer todos os arquivos de conhecimento.
*   **Modularidade:** A divisão do conhecimento em arquivos JSON separados permite carregar apenas o necessário e facilita a expansão.
*   **Python Nativo:** A implementação em Python puro garantirá compatibilidade e desempenho em ambientes Linux.

Este design servirá como base para a implementação do BRX AI.
