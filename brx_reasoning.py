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

class PersonalityManager:
    """Gerencia a identidade e as regras de comunicação da BRX."""
    def __init__(self, personality_data):
        self.data = personality_data or {}
        self.identity = self.data.get("identity", {})
        self.rules = self.data.get("communication_rules", {})
        self.vocabulary = self.data.get("vocabulary_by_function", {})

    def get_greeting(self, style="casual"):
        greetings = self.vocabulary.get("greetings", {}).get(style, ["Olá."])
        import random
        return random.choice(greetings)

    def get_acknowledgment(self, type="confirmation"):
        acks = self.vocabulary.get("acknowledgments", {}).get(type, ["Recebido."])
        import random
        return random.choice(acks)

    def format_response(self, text):
        # Aplica regras de formatação (sem emojis, etc)
        # (Simulação de aplicação de regras)
        return text

class ParallelReasoningEngine:
    """Cérebro interno que processa informações e decide se precisa de mais dados."""
    def __init__(self, personality_manager):
        self.personality = personality_manager

    def reason(self, research_data, local_knowledge, user_input, chat_history):
        query_lower = user_input.lower()
        
        # 1. Análise de Intenção e Ambiguidade
        needs_clarification = self.check_ambiguity(query_lower, chat_history)
        if needs_clarification:
            return {"synthesis": needs_clarification, "status": "waiting_input"}

        # 2. Processamento de Conhecimento
        synthesis = self.synthesize(user_input, local_knowledge, research_data)
        return {"synthesis": synthesis, "status": "completed"}

    def check_ambiguity(self, query, history):
        # Se for um pedido de código genérico sem detalhes
        is_code_req = any(w in query for w in ["código", "codigo", "script", "programar"])
        is_roblox = "roblox" in query
        
        # Se for Roblox e código, mas muito curto
        if is_roblox and is_code_req:
            if len(query.split()) < 6:
                return "Especificar: o que o script deve fazer exatamente? Ou: usar um modelo padrão de simulador?"
            
            # Caso de "salvar e pegar" mencionado pelo usuário
            if any(w in query for w in ["salvar", "pegar", "save", "load"]):
                if not any(w in query for w in ["datastore", "líder", "stats", "moeda"]):
                    return "Especificar: salvar quais dados? (Ex: Coins, XP, Inventário). Detalhes?"

        return None

    def synthesize(self, query, local, web):
        query_lower = query.lower()
        is_roblox = "roblox" in query_lower
        is_code_req = any(w in query_lower for w in ["código", "codigo", "script", "programar", "barra de comandos", "comandos"])
        
        # Coleta snippets
        snippets = []
        for item in local:
            content = item['content']
            if isinstance(content, dict):
                text = content.get('texto', '') or content.get('summary', '')
                if text: snippets.append(text)
            elif isinstance(content, str):
                snippets.append(content)

        if is_roblox and is_code_req:
            # Lógica de simulador de clique (já refinada)
            if "clique" in query_lower or "click" in query_lower:
                return """-- [BRX BRAIN] Sistema de Simulador de Clique (Roblox Studio)
-- Processado via raciocínio interno.

local function setupClickSimulator()
    local Players = game:GetService("Players")
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    
    local clickEvent = ReplicatedStorage:FindFirstChild("AddClickEvent") or Instance.new("RemoteEvent")
    clickEvent.Name = "AddClickEvent"
    clickEvent.Parent = ReplicatedStorage

    Players.PlayerAdded:Connect(function(player)
        local stats = Instance.new("Folder", player)
        stats.Name = "leaderstats"
        local clicks = Instance.new("IntValue", stats)
        clicks.Name = "Clicks"
        clicks.Value = 0
    end)

    clickEvent.OnServerEvent:Connect(function(player)
        if player:FindFirstChild("leaderstats") then
            player.leaderstats.Clicks.Value += 1
        end
    end)

    print("BRX: Simulador de Clique pronto.")
end

setupClickSimulator()
"""
            # Se for salvar e carregar
            if any(w in query_lower for w in ["salvar", "carregar", "save", "load"]):
                 return """-- [BRX BRAIN] Sistema de Save/Load (DataStore Service)
-- Implementação robusta baseada em pcall.

local DataStoreService = game:GetService("DataStoreService")
local playerData = DataStoreService:GetDataStore("PlayerData_v1")

game.Players.PlayerAdded:Connect(function(player)
    local leaderstats = Instance.new("Folder", player)
    leaderstats.Name = "leaderstats"
    local coins = Instance.new("IntValue", leaderstats)
    coins.Name = "Coins"

    local success, data = pcall(function()
        return playerData:GetAsync(player.UserId)
    end)

    if success and data then
        coins.Value = data
    end
end)

game.Players.PlayerRemoving:Connect(function(player)
    pcall(function()
        playerData:SetAsync(player.UserId, player.leaderstats.Coins.Value)
    end)
end)

print("BRX: Sistema de salvamento ativo.")
"""

        # Resposta textual baseada em personalidade
        if snippets:
            response = f"Analisando '{query}' através do meu núcleo de conhecimento:\n\n"
            for i, s in enumerate(snippets[:2]):
                response += f"- {s[:300]}...\n\n"
            response += "Confirmar: esta informação atende sua necessidade? Ou: detalhar mais?"
            return response
        
        return f"Processamento concluído. Sem dados específicos para '{query}'. Fornecer mais detalhes?"

class BRXAdvancedArchitecture:
    """Ponto de entrada principal para a arquitetura multi-camada."""
    def __init__(self, knowledge=None):
        self.knowledge = knowledge or {}
        self.personality_manager = PersonalityManager(self.knowledge.get("Personalidade_BRX.json", {}))
        self.source_interpreter = SourceInterpreter()
        self.web_scanner = WebScanner(self.source_interpreter)
        self.orchestrator = ResearchOrchestrator(self.web_scanner)
        self.knowledge_retriever = KnowledgeRetriever(self.knowledge)
        self.reasoning_engine = ParallelReasoningEngine(self.personality_manager)

    def process_request(self, user_input, chat_history=None, mode="basic"):
        # 1. Recuperação de Conhecimento Local
        local_data = self.knowledge_retriever.search(user_input)
        
        # 2. Raciocínio Interno (Decide se responde ou pergunta)
        reasoning_result = self.reasoning_engine.reason([], local_data, user_input, chat_history or [])
        
        # 3. Se precisar de pesquisa web (apenas se não houver resposta local e não estiver esperando input)
        if reasoning_result.get("status") == "completed" and len(local_data) < 2:
             research_results = self.orchestrator.research(user_input, mode=mode)
             # Re-raciocina com dados da web se necessário
             # (Simplificado para este estágio)
        
        # 4. Retorno formatado pela personalidade
        return reasoning_result["synthesis"]
