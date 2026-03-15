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
        self.context = []
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro a partir dos arquivos JSON de forma otimizada."""
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
        """Adiciona novo conhecimento ao cérebro e salva no arquivo de treinamento."""
        self.knowledge[key] = data
        training_path = os.path.join(self.brain_dir, 'knowledge', 'training.json')
        self.save_json(training_path, self.knowledge)

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "6.3",
            "edicao": "Fix & Code Edition",
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
        """MOTOR DE DECOMPOSIÇÃO ATÔMICA: Analisa cada letra e caractere."""
        text_lower = text.lower()
        char_freq = collections.Counter(text_lower)
        return {
            "freq": dict(char_freq),
            "len": len(text)
        }

    def calculate_dna_similarity(self, dna1, dna2):
        """Compara a assinatura de DNA (letras e caracteres) entre dois textos."""
        score = 0
        f1, f2 = dna1['freq'], dna2['freq']
        all_chars = set(f1.keys()) | set(f2.keys())
        for char in all_chars:
            if char in f1 and char in f2:
                diff = abs(f1[char] - f2[char])
                score += max(0, 5.0 - (diff / 0.6)) # Peso aumentado para precisão máxima
        return score

    def think(self, user_input):
        """MOTOR DE PENSAMENTO: Analisa a intenção do usuário com maior precisão."""
        user_input = user_input.lower()
        
        # Saudações
        if any(w in user_input for w in ["oi", "olá", "opa", "bom dia", "boa tarde", "boa noite"]):
            return "greeting"
        
        # Arch Linux
        if any(w in user_input for w in ["pacman", "yay", "aur", "instalar", "atualizar", "remover", "arch"]):
            return "arch_linux"
        
        # Systemd
        if any(w in user_input for w in ["systemctl", "serviço", "status", "start", "stop"]):
            return "systemd"
        
        # Matemática
        if any(c in user_input for c in "+-*/=") or "quanto" in user_input:
            return "math"
        
        # Programação (Prioridade Alta)
        if any(w in user_input for w in ["como", "programar", "código", "python", "js", "rust", "java", "roblox", "luau", "c#", "unity", "script", "bladex", "combat", "lua"]):
            return "programming"
            
        return "general"

    def synthesize_response(self, intent, blocks, web_result, user_input):
        """MOTOR DE SÍNTESE: Monta a resposta final de forma assertiva."""
        if intent == "greeting":
            return "Olá! Sou o BRX AI, seu assistente nativo do Arch Linux. Como posso ajudar com seu sistema ou código hoje?"

        if not blocks and not web_result:
            return "Analisei cada letra da sua mensagem, mas ainda não tenho uma resposta técnica. Posso pesquisar na Web agora?"

        if web_result:
            # Se for programação, tentar formatar melhor o código
            if intent == "programming":
                return f"Encontrei esta lógica de programação via Pesquisa Web:\n\n{web_result}\n\nPosso ajudar a adaptar esse código para o seu projeto?"
            return f"Encontrei esta informação técnica via Pesquisa Web:\n\n{web_result}"

        best_block = blocks[0][1]
        text = best_block.get('texto', '')
        
        if intent == "arch_linux":
            return f"Dica do Arch: {text}"
        elif intent == "systemd":
            return f"Gerenciamento de Sistema: {text}"
        elif intent == "programming":
            return f"Lógica de Programação:\n\n{text}"
            
        return text

    def get_response(self, user_input):
        """Gera uma resposta completa: Atomizar -> Pensar -> Buscar -> Sintetizar."""
        user_dna = self.atomize(user_input)
        if user_dna['len'] == 0:
            return "BRX pronto. Como posso ajudar hoje?"

        intent = self.think(user_input)
        needs_web = any(w in user_input.lower() for w in ["novidade", "recente", "hoje", "2026", "março", "atualizado", "cria", "faz", "gera"])
        
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            if block.get('categoria') == intent:
                dna_score += 60
                for word in block.get('palavras', []):
                    if word in user_input.lower():
                        dna_score += 100
                
            if dna_score > 0:
                scored_blocks.append((dna_score, block))

        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        web_result = ""
        # Priorizar pesquisa web se for detectada necessidade de informação recente ou se o conhecimento local for fraco
        if self.web_search_enabled and (needs_web or not scored_blocks or scored_blocks[0][0] < 180):
            query = f"site:wiki.archlinux.org {user_input}" if intent in ["arch_linux", "systemd"] else user_input
            if intent == "programming":
                query = f"exemplo de código {user_input}"
            web_result = self.search_web(query)

        response = self.synthesize_response(intent, scored_blocks, web_result, user_input)
        
        thought_info = f"[BRX v6.3 | Intenção '{intent}' | {user_dna['len']} chars | Code Mode]"
        return f"{thought_info}\n\n{response}"

    def search_web(self, query):
        """MOTOR DE PESQUISA WEB: Busca e extrai conteúdo técnico."""
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
                
                return "\n\n".join(results) if results else "Sem resultados técnicos encontrados na Web."
            return "Erro ao acessar a Web (Status: " + str(response.status_code) + ")."
        except Exception as e:
            return f"Erro na pesquisa Web: {str(e)}"

    def check_internet(self):
        """Verifica se há conexão com a internet."""
        try:
            requests.get("https://github.com", timeout=5)
            return True
        except:
            return False

    def sync_to_github(self):
        """Sincronização resiliente com o GitHub."""
        if not self.check_internet():
            return "Erro: Sem conexão com a internet para sincronizar."
        
        try:
            # Garantir que é um repositório git
            if not os.path.exists(".git"):
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "remote", "add", "origin", "https://github.com/dragonbrxos/BRX_AI.git"], check=True)

            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Sync v6.3: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            return "Sincronizado com sucesso!"
        except subprocess.CalledProcessError as e:
            return f"Erro no Git: {e}"
        except Exception as e:
            return f"Erro inesperado no Sync: {e}"

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("cria um codigo lua"))
