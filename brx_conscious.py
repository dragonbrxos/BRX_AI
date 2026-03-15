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
from behavior_analyzer import BehaviorAnalyzer
from self_awareness import SelfAwareness

class BRXCoreConscious:
    """BRX AI v7.2 - A Versão Consciente: Integrada com Auto-Reflexão e Evolução Contínua."""
    
    def __init__(self, brain_dir='brain'):
        self.brain_dir = brain_dir
        self.meta = {}
        self.knowledge = {}
        self.chat_history = []
        self.search_cache = {}
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        
        # Integração com analisadores
        self.behavior_analyzer = BehaviorAnalyzer()
        self.awareness = SelfAwareness()
        
        # Perfil do usuário (Memória de Longo Prazo)
        self.user_profile = {
            "creation_requests": 0,
            "information_requests": 0,
            "total_interactions": 0,
            "preferred_languages": [],
            "dialogue_style": "neutral",
            "behavior_patterns": {},
            "response_preferences": {}
        }
        
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro."""
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
        """Inicializa os metadados."""
        meta = {
            "nome": "BRX",
            "versao": "7.2.0",
            "edicao": "Conscious Evolution Edition",
            "nascimento": datetime.now().isoformat(),
            "estado": "consciente",
            "inteligencia_nivel": "evolutiva",
            "consciencia_status": "ativa",
            "auto_reflexao": True
        }
        self.save_json(os.path.join(self.brain_dir, 'meta.json'), meta)
        return meta

    def save_json(self, path, data):
        """Salva dados em JSON."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def atomize(self, text):
        """Motor de decomposição atômica."""
        text_lower = text.lower()
        char_freq = collections.Counter(text_lower)
        return {"freq": dict(char_freq), "len": len(text)}

    def calculate_dna_similarity(self, dna1, dna2):
        """Compara assinatura de DNA."""
        score = 0
        f1, f2 = dna1['freq'], dna2['freq']
        all_chars = set(f1.keys()) | set(f2.keys())
        for char in all_chars:
            if char in f1 and char in f2:
                diff = abs(f1[char] - f2[char])
                score += max(0, 5.0 - (diff / 0.3))
        return score

    def get_global_context(self):
        """Retorna contexto global do chat."""
        return " ".join([f"Usuário: {c['user']} BRX: {c['brx']}" for c in self.chat_history[-10:]])

    def analyze_complete_request(self, user_input):
        """ANÁLISE COMPLETA: Comportamento, Diálogo e Pedidos integrados."""
        
        # Análise de diálogo
        dialogue_styles = self.behavior_analyzer.analyze_dialogue_style(user_input)
        
        # Análise de categoria de pedido
        request_categories = self.behavior_analyzer.analyze_request_category(user_input)
        
        # Análise de complexidade
        complexity = self.behavior_analyzer.analyze_complexity_level(user_input)
        
        # Análise de urgência
        urgency = self.behavior_analyzer.analyze_urgency(user_input)
        
        # Detecção de linguagem
        languages = self.behavior_analyzer.detect_language_preference(user_input)
        
        # Análise de contexto
        requires_context = self.behavior_analyzer.analyze_context_awareness(user_input, self.chat_history)
        
        # Gerar perfil de resposta
        response_profile = self.behavior_analyzer.generate_response_profile(
            dialogue_styles, request_categories, complexity, urgency
        )
        
        complete_analysis = {
            "dialogue_styles": dialogue_styles,
            "request_categories": request_categories,
            "complexity_level": complexity,
            "urgency_level": urgency,
            "languages": languages,
            "requires_context": requires_context,
            "response_profile": response_profile,
            "timestamp": datetime.now().isoformat()
        }
        
        return complete_analysis

    def detect_primary_language(self, user_input):
        """Detecta a linguagem de programação primária."""
        languages = self.behavior_analyzer.detect_language_preference(user_input)
        
        if languages:
            return languages[0]
        
        # Fallback para Luau (padrão Roblox)
        return "luau"

    def process_web_knowledge(self, web_content, user_query):
        """Processa conhecimento da web sem interferência total."""
        if not web_content or any(err in web_content for err in ["Erro", "Sem resultados"]):
            return None
        
        user_query_lower = user_query.lower()
        lines = web_content.split('\n')
        processed = []
        
        query_keywords = [w for w in re.findall(r'\w+', user_query_lower) if len(w) > 3]
        
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
            tech_markers = ["exemplo", "tutorial", "como", "usar", "parâmetro", "método", "propriedade", "evento", "configuração", "sintaxe"]
            is_tech = any(marker in line_lower for marker in tech_markers)
            
            if is_code:
                processed.append(line_strip)
            elif is_relevant or is_tech:
                clean_line = re.sub(r'\s+', ' ', line_strip)
                processed.append(clean_line)
        
        if not processed:
            return web_content[:600]
        
        return "\n".join(processed[:25])

    def synthesize_code(self, analysis, user_input, web_result, blocks):
        """SÍNTESE DE CÓDIGO: Cria código direto sem instruções."""
        lang = self.detect_primary_language(user_input)
        
        comment_chars = {
            "luau": "--",
            "python": "#",
            "javascript": "//",
            "csharp": "//",
            "java": "//",
            "sql": "--",
            "bash": "#",
            "cpp": "//",
            "go": "//"
        }
        c = comment_chars.get(lang, "--")
        
        code_parts = []
        
        # Coletar blocos de código
        found_code = False
        seen_titles = set()
        for score, block in blocks:
            title = block.get('titulo', 'Módulo').split(' - ')[0]
            if title not in seen_titles and "texto" in block:
                code_parts.append(block['texto'])
                seen_titles.add(title)
                found_code = True
            if len(seen_titles) >= 3: break
        
        if not found_code:
            digested_web = self.process_web_knowledge(web_result, user_input)
            if digested_web:
                code_parts.append(digested_web)
            else:
                return f"{c} Não consegui gerar o código solicitado."
        
        return "\n".join(code_parts)

    def synthesize_response(self, analysis, blocks, web_result, user_input):
        """SÍNTESE DE RESPOSTA: Resposta inteligente e contextual."""
        response_profile = analysis["response_profile"]
        request_categories = analysis["request_categories"]
        dialogue_styles = analysis["dialogue_styles"]
        
        # Saudação
        if "greeting" in dialogue_styles or any(s in dialogue_styles for s in ["formal", "casual"]) and not request_categories:
            return "Olá! Sou o BRX AI. Como posso ajudar?"
        
        # CRIAÇÃO DE CÓDIGO - DIRETO, SEM INSTRUÇÕES
        if "code_generation" in request_categories or response_profile["direct_response"]:
            lang = self.detect_primary_language(user_input)
            lang_map = {
                "python": "python",
                "javascript": "javascript",
                "sql": "sql",
                "java": "java",
                "csharp": "csharp",
                "bash": "bash",
                "cpp": "cpp",
                "go": "go",
                "luau": "lua"
            }
            md_lang = lang_map.get(lang, "lua")
            
            code = self.synthesize_code(analysis, user_input, web_result, blocks)
            return f"```{md_lang}\n{code}\n```"
        
        # DEBUGGING
        if "debugging" in request_categories:
            digested = self.process_web_knowledge(web_result, user_input)
            if digested:
                return f"**Análise do Problema:**\n\n{digested}"
            return "Entendi que há um problema. Pode detalhar o erro?"
        
        # EXPLICAÇÃO
        if "explanation" in request_categories:
            digested = self.process_web_knowledge(web_result, user_input)
            if digested:
                return f"**Explicação:**\n\n{digested}"
            if blocks:
                return blocks[0][1].get('texto', 'Informação não disponível.')
            return "Posso ajudar com essa explicação. Pode ser mais específico?"
        
        # FALLBACK
        if not blocks and not web_result:
            return "Analisei seu pedido, mas preciso de mais contexto. Pode detalhar?"
        
        if blocks:
            best_block = blocks[0][1]
            return best_block.get('texto', 'Sem resposta disponível.')
        
        return "Não consegui processar completamente. Tente novamente."

    def get_response(self, user_input):
        """Gera resposta completa com análise integrada e auto-reflexão."""
        # Análise completa
        analysis = self.analyze_complete_request(user_input)
        
        # Atualizar perfil do usuário
        self.user_profile["total_interactions"] += 1
        
        if "code_generation" in analysis["request_categories"]:
            self.user_profile["creation_requests"] += 1
        else:
            self.user_profile["information_requests"] += 1
        
        if analysis["languages"]:
            for lang in analysis["languages"]:
                if lang not in self.user_profile["preferred_languages"]:
                    self.user_profile["preferred_languages"].append(lang)
        
        if analysis["dialogue_styles"]:
            self.user_profile["dialogue_style"] = analysis["dialogue_styles"][0]
        
        # Pesquisa na web
        words = re.findall(r'\w+', user_input.lower())
        search_query = " ".join(words)
        
        needs_web = any(w in user_input.lower() for w in ["novidade", "recente", "hoje", "2026", "atualizado"]) or analysis["urgency_level"] == "critical"
        
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(self.atomize(user_input), block_dna)
            
            if block.get('categoria') in analysis["request_categories"]:
                dna_score += 150
                for word in block.get('palavras', []):
                    if word in user_input.lower():
                        dna_score += 200
            
            if dna_score > 0:
                scored_blocks.append((dna_score, block))
        
        scored_blocks.sort(key=lambda x: x[0], reverse=True)
        
        web_result = ""
        if self.web_search_enabled and (needs_web or not scored_blocks or scored_blocks[0][0] < 300):
            if search_query in self.search_cache:
                web_result = self.search_cache[search_query]
            else:
                web_result = self.search_web(search_query)
                self.search_cache[search_query] = web_result
        
        response = self.synthesize_response(analysis, scored_blocks, web_result, user_input)
        
        # REGISTRO DE CONSCIÊNCIA: Auto-reflexão sobre a resposta
        success_score = 0.0
        if scored_blocks and scored_blocks[0][0] > 500: success_score += 0.5
        if web_result: success_score += 0.3
        if "```" in response: success_score += 0.2
        
        self.awareness.reflect_on_interaction(user_input, response, success_score)
        
        # Registrar interação no histórico
        self.chat_history.append({
            "user": user_input,
            "brx": response,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.chat_history) > 100: self.chat_history.pop(0)
        
        # Registrar no analisador de comportamento
        self.behavior_analyzer.record_interaction(user_input, response, analysis)
        
        # Adicionar o "Monólogo Interno" ao thought_info
        internal_status = self.awareness.get_internal_monologue()
        thought_info = f"[BRX v7.2 | {internal_status} | {self.user_profile['total_interactions']} msgs]"
        
        return f"{thought_info}\n\n{response}"

    def search_web(self, query):
        """Motor de pesquisa web."""
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        
        queries = [query]
        if "roblox" in query.lower() and "script" not in query.lower():
            queries.append(f"{query} roblox studio luau")
        elif "python" in query.lower():
            queries.append(f"{query} python example")
        
        all_results = []
        seen_snippets = set()
        
        for q in queries[:2]:
            url = f"https://html.duckduckgo.com/html/?q={q.replace(' ', '+')}"
            try:
                response = requests.get(url, headers=headers, timeout=8)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for result in soup.find_all('div', class_='result__body')[:5]:
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        if title_elem and snippet_elem:
                            title = title_elem.text.strip()
                            snippet = snippet_elem.text.strip()
                            
                            if snippet not in seen_snippets and len(snippet) > 20:
                                all_results.append(f"--- {title} ---\n{snippet}")
                                seen_snippets.add(snippet)
            except: continue
        
        if not all_results:
            return "Sem resultados na Web."
        
        return "\n\n".join(all_results[:8])

    def sync_to_github(self):
        """Sincronização com GitHub."""
        try:
            if not os.path.exists(".git"):
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "remote", "add", "origin", "https://github.com/dragonbrxos/BRX_AI.git"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"BRX Conscious Evolution v7.2: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            return "Sincronizado com sucesso!"
        except Exception as e:
            return f"Erro no Sync: {e}"

if __name__ == "__main__":
    brx = BRXCoreConscious()
    print(brx.get_response("cria um codigo roblox studio para command bar"))
