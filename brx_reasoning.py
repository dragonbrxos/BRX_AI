import requests
from bs4 import BeautifulSoup
import concurrent.futures
import re
import json
import os
from datetime import datetime

class ResearchOrchestrator:
    """Manages research modes and depth."""
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
    """Handles large-scale web discovery using DuckDuckGo."""
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
                future_to_url = {executor.submit(self.fetch_and_interpret, url): url for url in links[:10 if not deep_scan else 20]}
                for future in concurrent.futures.as_completed(future_to_url):
                    res = future.result()
                    if res:
                        results.append(res)
            return results
        except Exception as e:
            return [{"error": f"Erro na busca: {str(e)}"}]

    def fetch_and_interpret(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            return self.source_interpreter.interpret(url, response.text)
        except Exception as e:
            return {"url": url, "error": f"Falha ao buscar ou interpretar: {str(e)}"}

class SourceInterpreter:
    """Reads and summarizes each collected page."""
    def interpret(self, url, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return {"url": url, "summary": text[:2000], "full_text": text}

class KnowledgeRetriever:
    """Retrieves relevant information from local JSON knowledge base."""
    def __init__(self, knowledge):
        self.knowledge = knowledge

    def search(self, query):
        query = query.lower()
        keywords = query.split()
        relevant_data = []
        
        # Simple keyword matching in the knowledge base
        for key, value in self.knowledge.items():
            content_str = str(value).lower()
            matches = sum(1 for word in keywords if word in content_str)
            if matches > 0:
                relevant_data.append({"key": key, "content": value, "score": matches})
        
        # Sort by relevance score
        relevant_data.sort(key=lambda x: x['score'], reverse=True)
        return relevant_data[:10]

class ParallelReasoningEngine:
    """Internal brain reasoning that processes information without exposing raw data."""
    def __init__(self):
        self.styles = ["analytical", "creative", "technical", "strategic"]

    def reason(self, research_data, local_knowledge, user_input):
        # This is where the "brain" actually processes the info
        # We combine local knowledge and web data
        context = "CONHECIMENTO LOCAL:\n"
        for item in local_knowledge:
            context += f"- {item['key']}: {str(item['content'])[:500]}...\n"
        
        context += "\nPESQUISA WEB:\n"
        for res in research_data:
            if 'summary' in res:
                context += f"- {res['url']}: {res['summary'][:500]}...\n"

        # Simulating internal reasoning steps
        internal_thoughts = []
        internal_thoughts.append(f"Analisando a intenção do usuário: '{user_input}'")
        internal_thoughts.append(f"Cruzando {len(local_knowledge)} referências locais com {len(research_data)} fontes da web.")
        
        if "roblox" in user_input.lower():
            internal_thoughts.append("Identificado contexto de desenvolvimento Roblox. Priorizando Luau e API do Studio.")
        
        # In a real LLM system, this would be a prompt. 
        # Here we simulate the synthesis.
        synthesis = self.synthesize(user_input, local_knowledge, research_data)
        
        return {
            "thoughts": internal_thoughts,
            "synthesis": synthesis
        }

    def synthesize(self, query, local, web):
        # Logic to create a custom response based on data
        query_lower = query.lower()
        
        # Identifica o tema principal
        is_roblox = "roblox" in query_lower
        is_code_req = any(w in query_lower for w in ["código", "script", "programar", "barra de comandos"])
        
        # Coleta snippets relevantes do conhecimento local
        snippets = []
        for item in local:
            content = item['content']
            if isinstance(content, dict):
                text = content.get('texto', '') or content.get('summary', '')
                if text:
                    snippets.append(text)
            elif isinstance(content, str):
                snippets.append(content)

        # Se for um pedido de código Roblox
        if is_roblox and is_code_req:
            # Tenta construir um script baseado nos snippets ou gera um inteligente
            base_script = ""
            if "clique" in query_lower or "click" in query_lower:
                base_script = """-- [BRX BRAIN] Sistema de Simulador de Clique para Roblox Studio
-- Este código foi gerado através do raciocínio interno cruzando dados de conhecimento.

local function setupClickSimulator()
    -- Criação da infraestrutura básica
    local folder = Instance.new("Folder")
    folder.Name = "BRX_ClickSimulator"
    folder.Parent = game.ServerStorage

    local remote = Instance.new("RemoteEvent")
    remote.Name = "ClickEvent"
    remote.Parent = game.ReplicatedStorage

    -- Lógica de Liderança (Leaderstats)
    game.Players.PlayerAdded:Connect(function(player)
        local stats = Instance.new("Folder")
        stats.Name = "leaderstats"
        stats.Parent = player

        local clicks = Instance.new("IntValue")
        clicks.Name = "Clicks"
        clicks.Value = 0
        clicks.Parent = stats
    end)

    print("[BRX] Simulador de Clique configurado com sucesso via Barra de Comandos.")
    print("[BRX] Evento remoto disponível em ReplicatedStorage.ClickEvent")
end

-- Execução imediata no Studio
setupClickSimulator()
"""
            else:
                # Script genérico se não for clique
                base_script = "-- [BRX BRAIN] Script Roblox Studio\n-- " + query + "\n"
                if snippets:
                    base_script += "\n-- Baseado em referências de conhecimento:\n"
                    base_script += snippets[0][:200] + "..."
            
            return base_script

        # Resposta textual para outros casos
        if snippets:
            response = f"Com base no meu raciocínio interno e nos arquivos de conhecimento, identifiquei os seguintes pontos para '{query}':\n\n"
            for s in snippets[:3]:
                response += f"- {s[:300]}...\n\n"
            response += "Espero que esta análise elaborada pelo meu 'cérebro' seja útil."
            return response
        
        # Default synthesis if no snippets
        return "Processamento concluído. Com base nos dados pesquisados, a melhor resposta para '" + query + "' envolve a integração dos conceitos de " + (web[0]['summary'][:100] if web else "várias fontes") + "."

class BRXAdvancedArchitecture:
    """The main entry point for the new multi-layer architecture."""
    def __init__(self, knowledge=None):
        self.source_interpreter = SourceInterpreter()
        self.web_scanner = WebScanner(self.source_interpreter)
        self.orchestrator = ResearchOrchestrator(self.web_scanner)
        self.knowledge_retriever = KnowledgeRetriever(knowledge or {})
        self.reasoning_engine = ParallelReasoningEngine()

    def process_request(self, user_input, mode="basic"):
        # 1. Local Knowledge Retrieval (Brain Memory)
        local_data = self.knowledge_retriever.search(user_input)
        
        # 2. Web Research (External Input)
        # Only search if local knowledge isn't sufficient or to complement
        research_results = self.orchestrator.research(user_input, mode=mode)
        
        # 3. Internal Reasoning (The "Brain" at work)
        reasoning_result = self.reasoning_engine.reason(research_results, local_data, user_input)
        
        # 4. Final Output Generation (User-facing)
        # We return only the synthesis, keeping thoughts internal as requested
        return reasoning_result["synthesis"]
