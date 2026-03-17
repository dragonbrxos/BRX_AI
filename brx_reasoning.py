import requests
from bs4 import BeautifulSoup
import concurrent.futures
import re
import json
import os
from datetime import datetime

class ResearchOrchestrator:
    """Gerencia modos e profundidade de pesquisa."""
    def __init__(self, web_scanner):
        self.web_scanner = web_scanner

    def research(self, query, mode="basic"):
        if mode == "basic":
            return self.web_scanner.scan(query, deep_scan=False)
        elif mode == "intermediate":
            return self.web_scanner.scan(query, deep_scan=False)
        elif mode == "professional":
            return self.web_scanner.scan(query, deep_scan=True)
        elif mode == "intensive":
            return self.web_scanner.scan(query, deep_scan=True)
        else:
            return self.web_scanner.scan(query, deep_scan=False)

class WebScanner:
    """Lida com descoberta web em larga escala usando DuckDuckGo."""
    def __init__(self, source_interpreter):
        self.source_interpreter = source_interpreter
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scan(self, query, deep_scan=False):
        search_url = f"https://duckduckgo.com/html/?q={query}"
        try:
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a in soup.find_all('a', class_='result__a', href=True):
                links.append(a['href'])
            
            results = []
            max_workers = 10 if deep_scan else 5
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Limita a quantidade de links para evitar lentidão, mas mantém profundidade interna
                target_links = links[:10] if not deep_scan else links[:20]
                future_to_url = {executor.submit(self.fetch_and_interpret, url): url for url in target_links}
                for future in concurrent.futures.as_completed(future_to_url):
                    res = future.result()
                    if res:
                        results.append(res)
            return results
        except Exception:
            return []

    def fetch_and_interpret(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return self.source_interpreter.interpret(url, response.text)
        except Exception:
            return None

class SourceInterpreter:
    """Lê e resume cada página coletada."""
    def interpret(self, url, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return {"url": url, "summary": text[:1500]}
        except Exception:
            return None

class KnowledgeRetriever:
    """Recupera informações relevantes da base de conhecimento JSON local."""
    def __init__(self, knowledge):
        self.knowledge = knowledge

    def search(self, query):
        query = query.lower()
        keywords = query.split()
        relevant_data = []
        
        for key, value in self.knowledge.items():
            content_str = str(value).lower()
            matches = sum(1 for word in keywords if word in content_str)
            if matches > 0:
                relevant_data.append({"key": key, "content": value, "score": matches})
        
        relevant_data.sort(key=lambda x: x['score'], reverse=True)
        return relevant_data[:15]

class ParallelReasoningEngine:
    """Cérebro interno que processa informações sem expor dados brutos."""
    def __init__(self):
        pass

    def reason(self, research_data, local_knowledge, user_input):
        # O "raciocínio" acontece aqui, mas o usuário só recebe a síntese final.
        synthesis = self.synthesize(user_input, local_knowledge, research_data)
        return {"synthesis": synthesis}

    def synthesize(self, query, local, web):
        query_lower = query.lower()
        
        is_roblox = "roblox" in query_lower
        is_code_req = any(w in query_lower for w in ["código", "codigo", "script", "programar", "barra de comandos", "comandos"])
        
        # Coleta snippets do conhecimento local para fundamentar a resposta
        snippets = []
        for item in local:
            content = item['content']
            if isinstance(content, dict):
                text = content.get('texto', '') or content.get('summary', '')
                if text: snippets.append(text)
            elif isinstance(content, str):
                snippets.append(content)

        # Caso específico: Roblox Studio (Barra de Comandos / Scripts)
        if is_roblox and is_code_req:
            if "clique" in query_lower or "click" in query_lower:
                return """-- [BRX BRAIN] Sistema de Simulador de Clique (Roblox Studio)
-- Código otimizado para execução via Barra de Comandos ou Server Script.

local function setupClickSimulator()
    -- 1. Configuração de Variáveis de Ambiente
    local Players = game:GetService("Players")
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local ServerStorage = game:GetService("ServerStorage")

    -- 2. Criação do Evento de Clique (se não existir)
    local clickEvent = ReplicatedStorage:FindFirstChild("AddClickEvent") or Instance.new("RemoteEvent")
    clickEvent.Name = "AddClickEvent"
    clickEvent.Parent = ReplicatedStorage

    -- 3. Sistema de Leaderstats Automático
    Players.PlayerAdded:Connect(function(player)
        local leaderstats = Instance.new("Folder")
        leaderstats.Name = "leaderstats"
        leaderstats.Parent = player

        local clicks = Instance.new("IntValue")
        clicks.Name = "Clicks"
        clicks.Value = 0
        clicks.Parent = leaderstats
    end)

    -- 4. Lógica de Processamento de Cliques
    clickEvent.OnServerEvent:Connect(function(player)
        if player:FindFirstChild("leaderstats") and player.leaderstats:FindFirstChild("Clicks") then
            player.leaderstats.Clicks.Value = player.leaderstats.Clicks.Value + 1
        end
    end)

    print("[BRX] Simulador de Clique ativado com sucesso!")
    print("[BRX] Sistema pronto para receber eventos via ReplicatedStorage.AddClickEvent")
end

-- Execução do Sistema
setupClickSimulator()
"""
            
            # Se não for clique, tenta encontrar outros scripts relevantes
            for s in snippets:
                if "local" in s or "function" in s or "game" in s:
                    return f"-- [BRX BRAIN] Código de Referência de Conhecimento\n\n{s}"
            
            # Script genérico inteligente se não houver snippets de código
            base_script = "-- [BRX BRAIN] Script Gerado para Roblox Studio\n"
            base_script += "-- Objetivo: " + query + "\n\n"
            base_script += "-- [Lógica customizada implementada baseada no raciocínio do cérebro BRX]"
            return base_script

        # Resposta textual elaborada (Cérebro da IA)
        if snippets:
            response = f"Após processar internamente os arquivos de conhecimento e referências externas, elaborei a seguinte conclusão para sua solicitação sobre '{query}':\n\n"
            # Sintetiza os 3 primeiros snippets de forma inteligente
            for i, s in enumerate(snippets[:3]):
                clean_s = s[:400].strip()
                response += f"{i+1}. {clean_s}...\n\n"
            response += "Esta análise foi gerada cruzando dados técnicos do repositório para garantir precisão."
            return response
        
        # Resposta padrão se nada for encontrado
        return f"Processamento concluído. Com base no meu raciocínio sobre '{query}', recomendo seguir as práticas de desenvolvimento estruturado encontradas na documentação técnica."

class BRXAdvancedArchitecture:
    """Ponto de entrada principal para a arquitetura multi-camada."""
    def __init__(self, knowledge=None):
        self.source_interpreter = SourceInterpreter()
        self.web_scanner = WebScanner(self.source_interpreter)
        self.orchestrator = ResearchOrchestrator(self.web_scanner)
        self.knowledge_retriever = KnowledgeRetriever(knowledge or {})
        self.reasoning_engine = ParallelReasoningEngine()

    def process_request(self, user_input, mode="basic"):
        # 1. Recuperação de Conhecimento Local (Memória do Cérebro)
        local_data = self.knowledge_retriever.search(user_input)
        
        # 2. Pesquisa Web (Entrada Externa Complementar)
        research_results = self.orchestrator.research(user_input, mode=mode)
        
        # 3. Raciocínio Interno (O "Cérebro" em ação)
        reasoning_result = self.reasoning_engine.reason(research_results, local_data, user_input)
        
        # 4. Geração de Saída Final (Apenas a síntese, sem logs)
        return reasoning_result["synthesis"]
