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

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "3.5",
            "nascimento": datetime.now().isoformat(),
            "ciclos": 0,
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
                score += max(0, 2 - (diff / 2))
        return score

    def think(self, user_input):
        """
        MOTOR DE PENSAMENTO:
        Analisa a intenção do usuário antes de gerar a resposta.
        Decide se a resposta deve ser numérica, textual ou baseada em código.
        """
        user_input = user_input.lower()
        intent = "general"
        
        # Identificar intenção por padrões de caracteres e palavras
        if any(c in user_input for c in "+-*/=" ) or any(w in user_input for w in ["quanto", "calcula", "soma"]):
            intent = "math"
        elif any(w in user_input for w in ["como", "programar", "código", "python", "js", "rust"]):
            intent = "programming"
        elif len(user_input) < 5:
            intent = "greeting"
            
        return intent

    def synthesize_response(self, intent, blocks, web_result):
        """
        MOTOR DE SÍNTESE:
        Monta a resposta final de forma inteligente, não apenas copiando.
        """
        if not blocks and not web_result:
            return "Estou processando cada letra do que você disse, mas ainda não tenho uma resposta completa. Posso aprender isso?"

        # Se houver resultado da web, prioriza a informação nova
        if web_result:
            return f"Pensei sobre isso e encontrei na web: {web_result}"

        # Se houver blocos locais, sintetiza a melhor resposta
        best_block = blocks[0][1]
        text = best_block.get('texto', '')
        
        # Lógica de síntese baseada na intenção
        if intent == "math":
            return f"Analisando os números: {text}"
        elif intent == "programming":
            return f"Aqui está a lógica de programação que encontrei: {text}"
        elif intent == "greeting":
            return f"Olá! Sou o BRX. Como posso ajudar com meu cérebro atômico hoje?"
            
        return text

    def get_response(self, user_input):
        """Gera uma resposta completa: Atomizar -> Pensar -> Buscar -> Sintetizar."""
        # 1. Atomizar
        user_dna = self.atomize(user_input)
        if user_dna['len'] == 0:
            return "Olá! Eu sou o BRX. Digite algo para eu começar a pensar."

        # 2. Pensar (Intenção)
        intent = self.think(user_input)
        
        # 3. Buscar no Cérebro
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            # Bônus por intenção correta
            if block.get('categoria') == intent:
                dna_score += 10
                
            if dna_score > 0:
                scored_blocks.append((dna_score, block))

        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        # 4. Pesquisa Web (se necessário)
        web_result = ""
        if self.web_search_enabled and (not scored_blocks or scored_blocks[0][0] < 20):
            web_result = self.search_web(user_input)

        # 5. Sintetizar Resposta
        response = self.synthesize_response(intent, scored_blocks, web_result)
        
        # Registrar pensamento no histórico
        thought_info = f"[BRX Pensando: Intenção '{intent}' | Analisados {user_dna['len']} caracteres]"
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
                return "\n".join(results) if results else "Sem resultados."
            return "Erro web."
        except: return "Erro na pesquisa."

    def sync_to_github(self):
        try:
            subprocess.run(["git", "add", "brain/"], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Pensante v3.5: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return "Sincronizado!"
        except: return "Erro sync."

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("Olá"))
