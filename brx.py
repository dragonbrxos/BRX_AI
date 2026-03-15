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
        self.web_search_enabled = False
        self.auto_train_enabled = True
        self.system_access_enabled = False # Segurança: Acesso ao sistema desativado por padrão
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
            # Carregamento sob demanda para economizar RAM em notebooks
            for filename in os.listdir(knowledge_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(knowledge_dir, filename), 'r') as f:
                        try: self.knowledge.update(json.load(f))
                        except: pass

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "4.0",
            "edicao": "Arch Edition",
            "nascimento": datetime.now().isoformat(),
            "estado": "operacional",
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
                score += max(0, 2.5 - (diff / 1.5)) # Peso aumentado para precisão no Arch
        return score

    def think(self, user_input):
        """MOTOR DE PENSAMENTO: Analisa a intenção do usuário."""
        user_input = user_input.lower()
        intent = "general"
        
        if any(w in user_input for w in ["pacman", "yay", "aur", "instalar", "atualizar", "remover", "arch"]):
            intent = "arch_linux"
        elif any(w in user_input for w in ["systemctl", "serviço", "status", "start", "stop"]):
            intent = "systemd"
        elif any(c in user_input for c in "+-*/=" ) or "quanto" in user_input:
            intent = "math"
        elif any(w in user_input for w in ["como", "programar", "código", "python", "js", "rust"]):
            intent = "programming"
            
        return intent

    def execute_system_command(self, command):
        """Executa comandos do sistema (apenas se autorizado)."""
        if not self.system_access_enabled:
            return "Acesso ao sistema desativado. Use o comando 'sys' para ativar."
        
        try:
            # Segurança: Apenas comandos informativos por padrão
            safe_commands = ["pacman -Qs", "systemctl status", "uname -a", "uptime", "free -h"]
            if not any(command.startswith(safe) for safe in safe_commands):
                return f"Comando '{command}' não está na lista de segurança."
            
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=5)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Erro ao executar comando: {e}"

    def synthesize_response(self, intent, blocks, web_result):
        """MOTOR DE SÍNTESE: Monta a resposta final."""
        if not blocks and not web_result:
            return "Analisei cada letra, mas ainda não tenho uma resposta para o seu Arch. Posso pesquisar na Wiki?"

        if web_result:
            return f"Encontrei esta informação técnica: {web_result}"

        best_block = blocks[0][1]
        text = best_block.get('texto', '')
        
        if intent == "arch_linux":
            return f"Dica do Arch: {text}"
        elif intent == "systemd":
            return f"Gerenciamento de Sistema: {text}"
            
        return text

    def get_response(self, user_input):
        """Gera uma resposta completa: Atomizar -> Pensar -> Buscar -> Sintetizar."""
        user_dna = self.atomize(user_input)
        if user_dna['len'] == 0:
            return "BRX Arch Edition pronto. Como posso ajudar com seu sistema hoje?"

        intent = self.think(user_input)
        
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            if block.get('categoria') == intent:
                dna_score += 20 # Bônus alto para intenção do sistema
                
            if dna_score > 0:
                scored_blocks.append((dna_score, block))

        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        web_result = ""
        if self.web_search_enabled and (not scored_blocks or scored_blocks[0][0] < 30):
            # Pesquisa focada na Arch Wiki se a intenção for Arch
            query = f"site:wiki.archlinux.org {user_input}" if intent in ["arch_linux", "systemd"] else user_input
            web_result = self.search_web(query)

        response = self.synthesize_response(intent, scored_blocks, web_result)
        
        thought_info = f"[BRX Arch: Intenção '{intent}' | {user_dna['len']} chars | RAM Otimizada]"
        return f"{thought_info}\n\n{response}"

    def search_web(self, query):
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://html.duckduckgo.com/html/?q={query}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for result in soup.find_all('div', class_='result__body')[:2]:
                    title = result.find('a', class_='result__a').text
                    snippet = result.find('a', class_='result__snippet').text
                    results.append(f"{title}: {snippet}")
                return "\n".join(results) if results else "Sem resultados na Arch Wiki."
            return "Erro web."
        except: return "Erro na pesquisa."

    def sync_to_github(self):
        try:
            subprocess.run(["git", "add", "brain/"], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Arch Edition v4.0: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return "Sincronizado!"
        except: return "Erro sync."

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("Como atualizar o arch?"))
