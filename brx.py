import json
import os
import re
from datetime import datetime
import collections

class BRXCore:
    def __init__(self, brain_dir='brain'):
        self.brain_dir = brain_dir
        self.meta = {}
        self.index = {}
        self.knowledge = {}
        self.reasoning = {}
        self.visited = []
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro a partir dos arquivos JSON."""
        # Carregar meta.json
        meta_path = os.path.join(self.brain_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                try:
                    self.meta = json.load(f)
                except json.JSONDecodeError:
                    self.meta = self.init_meta()
        else:
            self.meta = self.init_meta()

        # Carregar index/words.json
        index_path = os.path.join(self.brain_dir, 'index', 'words.json')
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                try:
                    self.index = json.load(f)
                except json.JSONDecodeError:
                    self.index = {}

        # Carregar knowledge/*.json
        knowledge_dir = os.path.join(self.brain_dir, 'knowledge')
        if os.path.exists(knowledge_dir):
            for filename in os.listdir(knowledge_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(knowledge_dir, filename), 'r') as f:
                        try:
                            self.knowledge.update(json.load(f))
                        except json.JSONDecodeError:
                            pass

        # Carregar reasoning/*.json
        reasoning_dir = os.path.join(self.brain_dir, 'reasoning')
        if os.path.exists(reasoning_dir):
            for filename in os.listdir(reasoning_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(reasoning_dir, filename), 'r') as f:
                        try:
                            self.reasoning[filename[:-5]] = json.load(f)
                        except json.JSONDecodeError:
                            pass

        # Carregar visited.json
        visited_path = os.path.join(self.brain_dir, 'visited.json')
        if os.path.exists(visited_path):
            with open(visited_path, 'r') as f:
                try:
                    self.visited = json.load(f)
                except json.JSONDecodeError:
                    self.visited = []

    def init_meta(self):
        """Inicializa os metadados do cérebro."""
        meta = {
            "nome": "BRX",
            "versao": "2.0",
            "nascimento": datetime.now().isoformat(),
            "ciclos": 0,
            "estado": "ativo",
            "total_blocos": 0,
            "total_fatos": 0,
            "total_paginas": 0,
            "ultimo_ciclo": datetime.now().isoformat()
        }
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), meta)
        return meta

    def save_json(self, path, data):
        """Salva dados em um arquivo JSON."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def analyze_chars(self, text):
        """Analisa a frequência e presença de cada caractere/letra."""
        return collections.Counter(text.lower())

    def preprocess_input(self, text):
        """Limpa e extrai palavras-chave e análise de caracteres."""
        text_clean = text.lower()
        words = re.findall(r'\w+', text_clean)
        char_analysis = self.analyze_chars(text_clean)
        return words, char_analysis

    def get_response(self, user_input):
        """Gera uma resposta baseada na análise de palavras e caracteres."""
        words, char_analysis = self.preprocess_input(user_input)
        
        if not words and not char_analysis:
            return "Olá! Eu sou o BRX. Estou pronto para analisar cada letra do que você disser."

        # Motor de Inferência Granular
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            score = 0
            block_text = block.get('texto', '').lower()
            block_words = set(block.get('palavras', []))
            
            # 1. Pontuação por palavras (Macro)
            for word in words:
                if word in block_words:
                    score += 10  # Palavras exatas valem mais
                elif word in block_text:
                    score += 5   # Palavra contida no texto
            
            # 2. Pontuação por caracteres (Micro - A inteligência real do BRX)
            block_char_analysis = self.analyze_chars(block_text)
            for char, count in char_analysis.items():
                if char in block_char_analysis:
                    # Se o caractere existe no bloco, ganha pontos
                    # Quanto mais próxima a frequência, maior a relevância
                    diff = abs(count - block_char_analysis[char])
                    score += max(0, 1 - (diff / 10)) 

            if score > 0:
                scored_blocks.append((score, block))

        # Ordenar por relevância
        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        if scored_blocks:
            best_block = scored_blocks[0][1]
            
            # Simular "pensamento" baseado na análise
            thought_process = f"[BRX Pensando: Analisei {len(user_input)} caracteres e identifiquei padrões em '{best_block.get('titulo')}']"
            
            response = f"{thought_process}\n\n{best_block.get('texto')}"
            
            # Registrar visita
            self.visited.append({
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "chars": dict(char_analysis),
                "block_id": best_block.get('id')
            })
            self.save_json(os.path.join(self.brain_dir, 'visited.json'), self.visited)
            
            return response
        else:
            return "Interessante... Analisei cada letra da sua mensagem, mas ainda não tenho um padrão correspondente no meu cérebro JSON. Posso aprender isso?"

    def add_knowledge(self, block_id, text, category, keywords, title="", topic="", source=""):
        """Adiciona conhecimento e atualiza índices."""
        new_block = {
            "id": block_id,
            "texto": text,
            "categoria": category,
            "fonte": source,
            "titulo": title,
            "topico": topic,
            "palavras": [k.lower() for k in keywords],
            "char_map": dict(self.analyze_chars(text))
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

        # Atualizar índice de palavras
        for word in keywords:
            word = word.lower()
            if word not in self.index: self.index[word] = []
            if block_id not in self.index[word]: self.index[word].append(block_id)
        
        self.save_json(os.path.join(self.brain_dir, 'index', 'words.json'), self.index)
        
        # Atualizar meta
        self.meta['total_blocos'] = len(self.knowledge)
        self.meta['ultimo_ciclo'] = datetime.now().isoformat()
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), self.meta)

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("Teste de caracteres"))
