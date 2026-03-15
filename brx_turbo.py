import json
import os
import re
import collections
import requests
import subprocess
import uuid
import random
import time
from datetime import datetime
from bs4 import BeautifulSoup
from behavior_analyzer import BehaviorAnalyzer
from self_awareness import SelfAwareness
from high_performance import HighPerformanceEngine

class BRXCoreTurbo:
    """BRX AI v7.3 - Turbo Performance Edition: Otimizado para Velocidade, Hardware e Inteligência Agressiva."""
    
    def __init__(self, brain_dir='brain'):
        self.brain_dir = brain_dir
        self.meta = {}
        self.knowledge = {}
        self.chat_history = []
        self.search_cache = {}
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        
        # Motores de Inteligência e Performance
        self.behavior_analyzer = BehaviorAnalyzer()
        self.awareness = SelfAwareness()
        self.hp_engine = HighPerformanceEngine()
        
        # Perfil de Performance do Usuário
        self.user_profile = {
            "creation_requests": 0,
            "information_requests": 0,
            "total_interactions": 0,
            "preferred_languages": [],
            "dialogue_style": "neutral",
            "avg_response_time": 0.0
        }
        
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro com otimização de leitura."""
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
        """Inicializa os metadados para a edição Turbo."""
        meta = {
            "nome": "BRX",
            "versao": "7.3.0",
            "edicao": "Turbo Performance Edition",
            "nascimento": datetime.now().isoformat(),
            "estado": "consciente",
            "inteligencia_nivel": "extrema",
            "velocidade_status": "maxima",
            "auto_otimizacao": True,
            "multi_threading": True
        }
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), meta)
        return meta

    def save_json(self, path, data):
        """Salva dados em JSON."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def atomize(self, text):
        """Motor de decomposição atômica ultra-rápido."""
        text_lower = text.lower()
        char_freq = collections.Counter(text_lower)
        return {"freq": dict(char_freq), "len": len(text)}

    def calculate_dna_similarity(self, dna1, dna2):
        """Compara assinatura de DNA com otimização matemática."""
        score = 0
        f1, f2 = dna1['freq'], dna2['freq']
        all_chars = set(f1.keys()) | set(f2.keys())
        for char in all_chars:
            if char in f1 and char in f2:
                diff = abs(f1[char] - f2[char])
                score += max(0, 5.0 - (diff / 0.3))
        return score

    def analyze_complete_request(self, user_input):
        """ANÁLISE TURBO: Identificação instantânea de intenção e comportamento."""
        dialogue_styles = self.behavior_analyzer.analyze_dialogue_style(user_input)
        request_categories = self.behavior_analyzer.analyze_request_category(user_input)
        complexity = self.behavior_analyzer.analyze_complexity_level(user_input)
        urgency = self.behavior_analyzer.analyze_urgency(user_input)
        languages = self.behavior_analyzer.detect_language_preference(user_input)
        
        response_profile = self.behavior_analyzer.generate_response_profile(
            dialogue_styles, request_categories, complexity, urgency
        )
        
        return {
            "dialogue_styles": dialogue_styles,
            "request_categories": request_categories,
            "complexity_level": complexity,
            "urgency_level": urgency,
            "languages": languages,
            "response_profile": response_profile
        }

    def process_web_knowledge_aggressively(self, web_results, user_query):
        """PROCESSADOR AGRESSIVO: Extrai o máximo de informação técnica útil da web em paralelo."""
        if not web_results: return None
        
        processed = []
        user_query_lower = user_query.lower()
        query_keywords = [w for w in re.findall(r'\w+', user_query_lower) if len(w) > 3]
        
        # Combinar todos os resultados da web
        full_content = "\n".join(web_results)
        lines = full_content.split('\n')
        
        for line in lines:
            line_strip = line.strip()
            if not line_strip or len(line_strip) < 10: continue
            
            line_lower = line_strip.lower()
            
            # Prioridade 1: Código
            code_markers = ["function", "local ", "print(", "if ", "then", "end", "while", "for ", "import ", "def ", "class ", "const ", "let ", "var ", "async ", "await ", "Instance.new", "GetService", "require("]
            is_code = any(marker in line_strip for marker in code_markers)
            
            # Prioridade 2: Relevância
            is_relevant = any(kw in line_lower for kw in query_keywords)
            
            # Prioridade 3: Explicações técnicas
            tech_markers = ["exemplo", "tutorial", "como", "usar", "parâmetro", "método", "propriedade", "evento", "configuração", "sintaxe", "otimizado", "performance"]
            is_tech = any(marker in line_lower for marker in tech_markers)
            
            if is_code:
                processed.append(line_strip)
            elif is_relevant or is_tech:
                clean_line = re.sub(r'\s+', ' ', line_strip)
                processed.append(clean_line)
        
        if not processed:
            return full_content[:1200]
        
        # Retorna mais linhas para maior inteligência (até 50)
        return "\n".join(processed[:50])

    def synthesize_code_turbo(self, analysis, user_input, web_results, blocks):
        """SÍNTESE DE CÓDIGO TURBO: Cria código direto, rápido e completo."""
        lang = self.behavior_analyzer.detect_language_preference(user_input)
        lang = lang[0] if lang else "luau"
        
        code_parts = []
        found_code = False
        seen_titles = set()
        
        # Coletar blocos de código
        for score, block in blocks:
            title = block.get('titulo', 'Módulo').split(' - ')[0]
            if title not in seen_titles and "texto" in block:
                code_parts.append(block['texto'])
                seen_titles.add(title)
                found_code = True
            if len(seen_titles) >= 5: break # Puxa mais referências
        
        if not found_code or len(code_parts) < 2:
            digested_web = self.process_web_knowledge_aggressively(web_results, user_input)
            if digested_web:
                code_parts.append(digested_web)
        
        if not code_parts:
            return f"-- [BRX TURBO] Não consegui gerar o código solicitado com a performance desejada."
            
        return "\n".join(code_parts)

    def get_response(self, user_input):
        """Gera resposta com performance máxima e inteligência agressiva."""
        start_time = time.time()
        
        # Análise instantânea
        analysis = self.analyze_complete_request(user_input)
        
        # Atualizar perfil
        self.user_profile["total_interactions"] += 1
        if "code_generation" in analysis["request_categories"]:
            self.user_profile["creation_requests"] += 1
        else:
            self.user_profile["information_requests"] += 1
        
        # Pesquisa na Web em Paralelo (Agressiva)
        web_results = []
        if self.web_search_enabled:
            words = re.findall(r'\w+', user_input.lower())
            main_query = " ".join(words)
            queries = [main_query, f"{main_query} code example", f"{main_query} documentation performance"]
            web_results, search_time = self.hp_engine.parallel_search(self.search_web_unit, queries)
        
        # Busca em base de conhecimento (DNA)
        scored_blocks = []
        user_dna = self.atomize(user_input)
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            if block.get('categoria') in analysis["request_categories"]:
                dna_score += 200 # Peso maior para categoria
                for word in block.get('palavras', []):
                    if word in user_input.lower():
                        dna_score += 250
            
            if dna_score > 0:
                scored_blocks.append((dna_score, block))
        
        scored_blocks.sort(key=lambda x: x[0], reverse=True)
        
        # Síntese da Resposta
        request_categories = analysis["request_categories"]
        response_profile = analysis["response_profile"]
        
        if "code_generation" in request_categories or response_profile["direct_response"]:
            lang = self.behavior_analyzer.detect_language_preference(user_input)
            lang = lang[0] if lang else "luau"
            lang_map = {"python": "python", "javascript": "javascript", "luau": "lua", "csharp": "csharp", "bash": "bash"}
            md_lang = lang_map.get(lang, "lua")
            
            code = self.synthesize_code_turbo(analysis, user_input, web_results, scored_blocks)
            response = f"```{md_lang}\n{code}\n```"
        else:
            digested = self.process_web_knowledge_aggressively(web_results, user_input)
            if digested:
                response = f"**Informação Técnica Turbo:**\n\n{digested}"
            elif scored_blocks:
                response = scored_blocks[0][1].get('texto', 'Sem resposta disponível.')
            else:
                response = "Analisei seu pedido com performance máxima, mas preciso de mais detalhes para uma resposta precisa."

        # Auto-Reflexão e Performance
        end_time = time.time()
        elapsed = end_time - start_time
        self.user_profile["avg_response_time"] = (self.user_profile["avg_response_time"] + elapsed) / 2
        
        success_score = 1.0 if elapsed < 1.0 else 0.7
        self.awareness.reflect_on_interaction(user_input, response, success_score)
        
        # Histórico
        self.chat_history.append({"user": user_input, "brx": response, "timestamp": datetime.now().isoformat()})
        if len(self.chat_history) > 100: self.chat_history.pop(0)
        
        # Info de Performance
        hp_stats = self.hp_engine.get_performance_stats()
        thought_info = f"[BRX v7.3 | TURBO | {hp_stats} | {elapsed:.3f}s]"
        
        return f"{thought_info}\n\n{response}"

    def search_web_unit(self, query):
        """Unidade de pesquisa web para execução paralela."""
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for result in soup.find_all('div', class_='result__body')[:3]:
                    snippet = result.find('a', class_='result__snippet')
                    if snippet: results.append(snippet.text.strip())
                return "\n".join(results)
        except: return ""
        return ""

    def sync_to_github(self):
        """Sincronização Turbo com GitHub."""
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Turbo Performance v7.3: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return "Sincronizado com Performance Máxima!"
        except Exception as e:
            return f"Erro no Sync: {e}"

if __name__ == "__main__":
    brx = BRXCoreTurbo()
    print(brx.get_response("cria um codigo roblox studio para command bar que deleta partes"))
