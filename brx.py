import json
import os
import re
import collections
import requests
import subprocess
import uuid
import random
from datetime import datetime
from bs4 import BeautifulSoup

class BRXCore:
    def __init__(self, brain_dir='brain'):
        self.brain_dir = brain_dir
        self.meta = {}
        self.knowledge = {}
        self.chat_history = [] # Memória de Longo Prazo
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro a partir dos arquivos JSON."""
        meta_path = os.path.join(self.brain_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                try: self.meta = json.load(f)
                except: self.meta = self.init_meta()
        else: self.meta = self.init_meta()

        knowledge_dir = os.path.join(self.brain_dir, 'knowledge')
        if os.path.exists(knowledge_dir):
            for filename in os.listdir(knowledge_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(knowledge_dir, filename), 'r') as f:
                        try: self.knowledge.update(json.load(f))
                        except: pass

    def add_knowledge(self, key, data):
        """Adiciona novo conhecimento ao cérebro."""
        self.knowledge[key] = data
        training_path = os.path.join(self.brain_dir, 'knowledge', 'training.json')
        self.save_json(training_path, self.knowledge)

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "6.6.1",
            "edicao": "Autonomous Processor Edition",
            "nascimento": datetime.now().isoformat(),
            "estado": "consciente",
            "total_blocos": 0,
            "ultimo_ciclo": datetime.now().isoformat()
        }
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), meta)
        return meta

    def save_json(self, path, data):
        """Salva dados em um arquivo JSON."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def atomize(self, text):
        """MOTOR DE DECOMPOSIÇÃO ATÔMICA."""
        text_lower = text.lower()
        char_freq = collections.Counter(text_lower)
        return {"freq": dict(char_freq), "len": len(text)}

    def calculate_dna_similarity(self, dna1, dna2):
        """Compara a assinatura de DNA entre dois textos."""
        score = 0
        f1, f2 = dna1['freq'], dna2['freq']
        all_chars = set(f1.keys()) | set(f2.keys())
        for char in all_chars:
            if char in f1 and char in f2:
                diff = abs(f1[char] - f2[char])
                score += max(0, 5.0 - (diff / 0.3))
        return score

    def get_global_context(self):
        """Retorna todo o histórico do chat."""
        return " ".join([f"Usuário: {c['user']} BRX: {c['brx']}" for c in self.chat_history])

    def think(self, user_input):
        """MOTOR DE PENSAMENTO: Desambiguação Semântica e Intenção."""
        global_context = self.get_global_context().lower()
        full_input = (global_context + " " + user_input).lower()
        
        # DESAMBIGUAÇÃO: 'Codes' (Resgate) vs 'Scripts' (Programação)
        if any(w in full_input for w in ["lua", "script", "programar", "código lua", "faz", "cria", "gera", "simulador", "clicker"]):
            return "programming"
            
        if any(w in user_input.lower() for w in ["promocode", "resgate", "ganhar", "recompensa", "codes"]):
            return "promocodes"

        if any(w in full_input for w in ["pacman", "yay", "aur", "instalar", "atualizar", "remover", "arch"]):
            return "arch_linux"
            
        if any(w in user_input.lower() for w in ["oi", "olá", "opa", "bom dia", "boa tarde", "boa noite"]):
            return "greeting"
            
        return "general"

    def process_web_knowledge(self, web_content, user_query):
        """PROCESSADOR DE CONHECIMENTO: Digeir e traduz dados da Web."""
        if not web_content or "Erro" in web_content:
            return None
        lines = web_content.split('\n')
        processed = []
        for line in lines:
            if any(w in line.lower() for w in ["function", "local", "print", "if", "then", "end", "loop", "while"]):
                processed.append(line.strip())
        return "\n".join(processed) if processed else web_content[:500]

    def synthesize_code(self, intent, user_input, web_result):
        """MOTOR DE SÍNTESE DIRETA: Entrega o código sem enrolação."""
        global_context = self.get_global_context().lower()
        full_query = (global_context + " " + user_input).lower()

        code = "-- BRX AI: Script Autônomo (Luau)\n"
        
        if "roblox" in full_query:
            code += "local Players = game:GetService('Players')\n"
            
            if "click" in full_query or "simulador" in full_query:
                code += "-- Sistema de Leaderstats e Cliques\n"
                code += "Players.PlayerAdded:Connect(function(player)\n"
                code += "    local ls = Instance.new('Folder', player); ls.Name = 'leaderstats'\n"
                code += "    local c = Instance.new('IntValue', ls); c.Name = 'Clicks'; c.Value = 0\n"
                code += "end)\n"
            
            if "vida" in full_query or "health" in full_query:
                code += "-- Sistema de Vida Customizada\n"
                code += "Players.PlayerAdded:Connect(function(p)\n"
                code += "    p.CharacterAdded:Connect(function(c)\n"
                code += "        local h = c:WaitForChild('Humanoid')\n"
                code += "        h.MaxHealth = 100; h.Health = 100\n"
                code += "    end)\n"
                code += "end)\n"
                
            return code

        digested_web = self.process_web_knowledge(web_result, user_input)
        if digested_web:
            return f"-- Código processado via Web:\n{digested_web}"

        return "-- Não consegui sintetizar o código exato. Pode detalhar mais?"

    def synthesize_response(self, intent, blocks, web_result, user_input):
        """MOTOR DE SÍNTESE: Resposta direta e assertiva."""
        if intent == "greeting":
            return "Olá! Sou o BRX AI. Como posso ajudar com seu código ou sistema hoje?"

        if intent == "programming":
            # Se o usuário pediu para 'criar' ou 'fazer', ou se o contexto é de programação
            global_context = self.get_global_context().lower()
            if any(w in (global_context + " " + user_input.lower()) for w in ["cria", "faz", "gera", "script", "código", "simulador", "clicker", "vida"]):
                code = self.synthesize_code(intent, user_input, web_result)
                return f"```lua\n{code}\n```"
            
            digested = self.process_web_knowledge(web_result, user_input)
            return f"Processamento de Conhecimento:\n\n{digested if digested else 'Não encontrei dados suficientes.'}"

        if intent == "promocodes":
            return "Entendi que você busca códigos de resgate. No momento, não tenho uma lista ativa, mas posso pesquisar os mais recentes!"

        if not blocks and not web_result:
            return "Analisei cada palavra, mas ainda não tenho uma resposta técnica. Posso pesquisar na Web agora?"

        best_block = blocks[0][1]
        return best_block.get('texto', '')

    def get_response(self, user_input):
        """Gera uma resposta completa com Pesquisa Multidimensional."""
        user_dna = self.atomize(user_input)
        intent = self.think(user_input)
        
        # PESQUISA MULTIDIMENSIONAL: Cada palavra é uma chave
        words = re.findall(r'\w+', user_input.lower())
        search_query = " ".join(words)

        needs_web = any(w in user_input.lower() for w in ["novidade", "recente", "hoje", "2026", "março", "atualizado"])
        
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            if block.get('categoria') == intent:
                dna_score += 100
                for word in block.get('palavras', []):
                    if word in user_input.lower():
                        dna_score += 150
                
            if dna_score > 0:
                scored_blocks.append((dna_score, block))

        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        web_result = ""
        if self.web_search_enabled and (needs_web or not scored_blocks or scored_blocks[0][0] < 300):
            web_result = self.search_web(search_query)

        response = self.synthesize_response(intent, scored_blocks, web_result, user_input)
        
        # Salvar no histórico
        self.chat_history.append({"user": user_input, "brx": response, "intent": intent})
        if len(self.chat_history) > 50: self.chat_history.pop(0)

        thought_info = f"[BRX v6.6.1 | Processador Autônomo | {len(self.chat_history)} msgs | Reasoning Mode]"
        return f"{thought_info}\n\n{response}"

    def search_web(self, query):
        """MOTOR DE PESQUISA WEB."""
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        url = f"https://html.duckduckgo.com/html/?q={query}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for result in soup.find_all('div', class_='result__body')[:3]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    if title_elem and snippet_elem:
                        title = title_elem.text.strip()
                        snippet = snippet_elem.text.strip()
                        results.append(f"--- {title} ---\n{snippet}")
                return "\n\n".join(results) if results else "Sem resultados técnicos."
            return "Erro ao acessar a Web."
        except Exception as e:
            return f"Erro na pesquisa Web: {str(e)}"

    def sync_to_github(self):
        """Sincronização resiliente."""
        try:
            if not os.path.exists(".git"):
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "remote", "add", "origin", "https://github.com/dragonbrxos/BRX_AI.git"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Sync v6.6.1: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            return "Sincronizado com sucesso!"
        except Exception as e:
            return f"Erro no Sync: {e}"

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("cria um codigo roblox"))
    print("-" * 20)
    print(brx.get_response("para um simulador de click"))
    print("-" * 20)
    print(brx.get_response("agora faz ele dar 100 de vida"))
