import json
import os
import re
import collections
import requests
import subprocess
import uuid
from datetime import datetime
from bs4 import BeautifulSoup

class BRXCore:
    def __init__(self, brain_dir='brain'):
        self.brain_dir = brain_dir
        self.meta = {}
        self.index = {}
        self.knowledge = {}
        self.reasoning = {}
        self.visited = []
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

        visited_path = os.path.join(self.brain_dir, 'visited.json')
        if os.path.exists(visited_path):
            with open(visited_path, 'r') as f:
                try: self.visited = json.load(f)
                except: self.visited = []

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "3.3",
            "nascimento": datetime.now().isoformat(),
            "ciclos": 0,
            "estado": "ativo",
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
        """
        MOTOR DE DECOMPOSIÇÃO ATÔMICA:
        Analisa cada letra, número e caractere individualmente.
        """
        # Mantemos o case original para análise de maiúsculas/minúsculas se necessário,
        # mas para a comparação de DNA padrão usamos lower().
        text_lower = text.lower()
        char_freq = collections.Counter(text_lower)
        char_sequence = [c for c in text_lower if c.isalnum()]
        return {
            "freq": dict(char_freq),
            "seq": char_sequence,
            "len": len(text)
        }

    def calculate_dna_similarity(self, dna1, dna2):
        """Compara a assinatura de DNA (letras e caracteres) entre dois textos."""
        score = 0
        f1, f2 = dna1['freq'], dna2['freq']
        
        all_chars = set(f1.keys()) | set(f2.keys())
        for char in all_chars:
            if char in f1 and char in f2:
                # Se o caractere existe em ambos, pontua baseado na proximidade da frequência
                diff = abs(f1[char] - f2[char])
                score += max(0, 2 - (diff / 2)) # Aumentado o peso da letra individual
        
        return score

    def get_response(self, user_input):
        """Gera uma resposta baseada na análise atômica profunda."""
        user_dna = self.atomize(user_input)
        
        if user_dna['len'] == 0:
            return "Olá! Eu sou o BRX. Estou pronto para analisar cada letra e número do que você disser."

        # 1. Busca no Cérebro JSON Local (Análise Atômica de Letras e Caracteres)
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna')
            if not block_dna:
                block_dna = self.atomize(block_text)
            
            # Comparação Atômica (DNA de Caracteres)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            # Bônus por palavras-chave
            words = re.findall(r'\w+', user_input.lower())
            for word in words:
                if word in block.get('palavras', []):
                    dna_score += 15

            if dna_score > 0:
                scored_blocks.append((dna_score, block))

        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        # 2. Pesquisa Web
        web_result = ""
        if self.web_search_enabled and (not scored_blocks or scored_blocks[0][0] < 20):
            web_result = self.search_web(user_input)

        # 3. Auto-Treinamento
        if self.auto_train_enabled and web_result and "Erro" not in web_result:
            new_id = str(uuid.uuid4())
            self.add_knowledge(
                block_id=new_id,
                text=web_result,
                category="learned",
                keywords=re.findall(r'\w+', user_input.lower())[:5],
                title=f"Aprendizado Atômico: {user_input[:20]}...",
                topic="auto-treinamento"
            )

        if scored_blocks or web_result:
            # Informação de análise atômica
            top_chars = sorted(user_dna['freq'].items(), key=lambda x: x[1], reverse=True)[:5]
            char_info = ", ".join([f"'{c}':{n}" for c, n in top_chars])
            thought_process = f"[BRX Atômico: {user_dna['len']} caracteres analisados | DNA: {char_info}]"
            
            if web_result:
                response = f"{thought_process}\n(Web):\n{web_result}"
            else:
                best_block = scored_blocks[0][1]
                response = f"{thought_process}\n(Cérebro Local - {best_block.get('titulo')}):\n{best_block.get('texto')}"
            
            return response
        else:
            return "Analisei cada letra e caractere da sua mensagem, mas ainda não encontrei um padrão correspondente no meu cérebro atômico. Posso aprender isso?"

    def add_knowledge(self, block_id, text, category, keywords, title="", topic="", source=""):
        dna = self.atomize(text)
        new_block = {
            "id": block_id,
            "texto": text,
            "categoria": category,
            "fonte": source,
            "titulo": title,
            "topico": topic,
            "palavras": [k.lower() for k in keywords],
            "dna": dna
        }
        
        cat_path = os.path.join(self.brain_dir, 'knowledge', f"{category}.json")
        cat_data = {}
        if os.path.exists(cat_path):
            with open(cat_path, 'r') as f:
                try: cat_data = json.load(f)
                except: pass
        
        cat_data[block_id] = new_block
        self.save_json(cat_path, cat_data)
        self.knowledge[block_id] = new_block
        
        self.meta['total_blocos'] = len(self.knowledge)
        self.meta['ultimo_ciclo'] = datetime.now().isoformat()
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), self.meta)

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
            subprocess.run(["git", "commit", "-m", f"BRX Atômico v3.3: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return "Sincronizado!"
        except: return "Erro sync."

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("ABC 123"))
