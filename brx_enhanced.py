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
        self.chat_history = []
        self.search_cache = {}
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        self.user_behavior_profile = {
            "creation_requests": 0,
            "information_requests": 0,
            "dialogue_style": "formal",
            "preferred_languages": [],
            "interaction_patterns": []
        }
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
            "versao": "7.0.0",
            "edicao": "Coder Pro Edition Enhanced",
            "nascimento": datetime.now().isoformat(),
            "estado": "consciente",
            "total_blocos": 0,
            "ultimo_ciclo": datetime.now().isoformat(),
            "inteligencia_nivel": "avancada",
            "comportamento_deteccao": True
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

    def analyze_request_type(self, user_input):
        """ANALISADOR AVANÇADO DE TIPO DE PEDIDO: Identifica com precisão o tipo de solicitação."""
        user_lower = user_input.lower()
        
        # Padrões de criação de código (direto e sem instruções)
        creation_patterns = {
            "code_creation": r"(cria|faz|gera|faz um|cria um|gera um|escreve|desenvolve|implementa)\s+(script|código|programa|função|classe|módulo|sistema|app|aplicativo)",
            "direct_code": r"(script|código|programa)\s+(para|que|em|com|do|da|de|roblox|python|javascript|lua)",
            "specific_task": r"(um\s+\w+\s+que|código\s+que|script\s+que)\s+(\w+)",
        }
        
        # Padrões de diálogo
        dialogue_patterns = {
            "greeting": r"^(oi|olá|opa|e aí|bom dia|boa tarde|boa noite|hey|opa|salve)",
            "question": r"^(qual|quais|como|por que|o que|quando|onde|você|você pode|consegue|dá|é possível)",
            "request_info": r"(me explica|explique|como funciona|o que é|qual é|quem é|fale sobre|me fale)",
            "casual": r"(tipo|tipo assim|sabe|entende|né|cê|tá|tô|pra|pro)",
        }
        
        # Padrões de comportamento
        behavior_patterns = {
            "urgent": r"(rápido|urgente|agora|já|imediatamente|logo)",
            "complex": r"(avançado|complexo|difícil|complicado|muito|bastante)",
            "simple": r"(simples|fácil|básico|rápido|pequeno)",
            "debug": r"(erro|bug|não funciona|quebrou|problema|falha|não roda)",
        }
        
        request_type = {
            "primary": "general",
            "secondary": [],
            "confidence": 0,
            "creation_intent": False,
            "dialogue_style": "formal",
            "behavior_flags": []
        }
        
        # Analisar criação de código
        for pattern_name, pattern in creation_patterns.items():
            if re.search(pattern, user_lower):
                request_type["primary"] = "code_creation"
                request_type["creation_intent"] = True
                request_type["confidence"] = 0.95
                break
        
        # Analisar diálogo
        for pattern_name, pattern in dialogue_patterns.items():
            if re.search(pattern, user_lower):
                if pattern_name == "greeting":
                    request_type["dialogue_style"] = "greeting"
                elif pattern_name == "casual":
                    request_type["dialogue_style"] = "casual"
                request_type["secondary"].append(pattern_name)
        
        # Analisar comportamento
        for pattern_name, pattern in behavior_patterns.items():
            if re.search(pattern, user_lower):
                request_type["behavior_flags"].append(pattern_name)
        
        # Se não foi classificado como criação, verificar outros tipos
        if request_type["primary"] == "general":
            if any(w in user_lower for w in ["promocode", "resgate", "ganhar", "recompensa", "codes"]):
                request_type["primary"] = "promocodes"
            elif any(w in user_lower for w in ["pacman", "yay", "aur", "instalar", "atualizar", "remover", "arch"]):
                request_type["primary"] = "arch_linux"
            elif any(w in user_lower for w in ["lua", "script", "programar", "código lua", "roblox", "studio"]):
                request_type["primary"] = "programming"
        
        return request_type

    def detect_language(self, user_input):
        """DETECTOR DE LINGUAGEM: Identifica a linguagem de programação desejada."""
        user_lower = user_input.lower()
        
        languages = {
            "luau": ["lua", "luau", "roblox", "studio"],
            "python": ["python", "py"],
            "javascript": ["javascript", "js", "react", "node", "express", "html", "css", "typescript", "ts"],
            "csharp": ["c#", "csharp", "unity"],
            "java": ["java"],
            "sql": ["sql", "database", "banco de dados"],
            "bash": ["bash", "shell", "sh", "linux", "arch"],
            "cpp": ["c++", "cpp"],
            "go": ["golang", "go"]
        }
        
        for lang, keywords in languages.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return lang
        
        # Padrão padrão é Luau (para Roblox)
        return "luau"

    def process_web_knowledge(self, web_content, user_query):
        """PROCESSADOR DE CONHECIMENTO AVANÇADO: Extrai dados da Web sem interferência total."""
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

    def synthesize_code(self, request_type, user_input, web_result, blocks):
        """MOTOR DE GERAÇÃO DE CÓDIGO: Cria código direto sem instruções extras."""
        user_input_lower = user_input.lower()
        global_context = self.get_global_context().lower()
        
        lang = self.detect_language(user_input)
        
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
        
        # Coletar blocos de código da base de conhecimento
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
            # Usar web como complemento
            digested_web = self.process_web_knowledge(web_result, user_input)
            if digested_web:
                code_parts.append(digested_web)
            else:
                return f"{c} Não consegui gerar o código solicitado."
        
        return "\n".join(code_parts)

    def synthesize_response(self, request_type, blocks, web_result, user_input):
        """MOTOR DE SÍNTESE: Resposta direta e assertiva."""
        primary_type = request_type["primary"]
        dialogue_style = request_type["dialogue_style"]
        creation_intent = request_type["creation_intent"]
        
        # Saudação
        if dialogue_style == "greeting":
            return "Olá! Sou o BRX AI. Como posso ajudar?"
        
        # Criação de código - DIRETO, SEM INSTRUÇÕES
        if primary_type == "code_creation" or creation_intent:
            lang = self.detect_language(user_input)
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
            
            code = self.synthesize_code(request_type, user_input, web_result, blocks)
            return f"```{md_lang}\n{code}\n```"
        
        # Promoções
        if primary_type == "promocodes":
            return "Pesquisando os códigos de resgate mais recentes..."
        
        # Arch Linux
        if primary_type == "arch_linux":
            digested = self.process_web_knowledge(web_result, user_input)
            if digested:
                return f"**Resultado da Pesquisa:**\n\n{digested}"
            return "Posso ajudar com comandos do Arch Linux. Qual é sua dúvida específica?"
        
        # Programação geral
        if primary_type == "programming":
            digested = self.process_web_knowledge(web_result, user_input)
            if digested:
                return f"**Informação Técnica:**\n\n{digested}"
            return "Entendi que é sobre programação. Pode ser mais específico?"
        
        # Fallback
        if not blocks and not web_result:
            return "Analisei seu pedido, mas preciso de mais contexto. Pode detalhar?"
        
        if blocks:
            best_block = blocks[0][1]
            return best_block.get('texto', 'Sem resposta disponível.')
        
        return "Não consegui processar completamente. Tente novamente."

    def get_response(self, user_input):
        """Gera resposta completa com inteligência aprimorada."""
        user_dna = self.atomize(user_input)
        request_type = self.analyze_request_type(user_input)
        
        # Atualizar perfil de comportamento do usuário
        if request_type["creation_intent"]:
            self.user_behavior_profile["creation_requests"] += 1
        else:
            self.user_behavior_profile["information_requests"] += 1
        
        if request_type["dialogue_style"] == "casual":
            self.user_behavior_profile["dialogue_style"] = "casual"
        
        lang = self.detect_language(user_input)
        if lang not in self.user_behavior_profile["preferred_languages"]:
            self.user_behavior_profile["preferred_languages"].append(lang)
        
        # Pesquisa na web (apenas quando necessário)
        words = re.findall(r'\w+', user_input.lower())
        search_query = " ".join(words)
        
        needs_web = any(w in user_input.lower() for w in ["novidade", "recente", "hoje", "2026", "atualizado", "novo"]) or request_type["primary"] == "promocodes"
        
        scored_blocks = []
        for block_id, block in self.knowledge.items():
            block_text = block.get('texto', '')
            block_dna = block.get('dna') or self.atomize(block_text)
            dna_score = self.calculate_dna_similarity(user_dna, block_dna)
            
            if block.get('categoria') == request_type["primary"]:
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
        
        response = self.synthesize_response(request_type, scored_blocks, web_result, user_input)
        
        # Salvar no histórico
        self.chat_history.append({
            "user": user_input,
            "brx": response,
            "request_type": request_type["primary"],
            "timestamp": datetime.now().isoformat()
        })
        if len(self.chat_history) > 100: self.chat_history.pop(0)
        
        thought_info = f"[BRX v7.0 | Enhanced | {request_type['primary']} | {len(self.chat_history)} msgs]"
        return f"{thought_info}\n\n{response}"

    def search_web(self, query):
        """MOTOR DE PESQUISA WEB: Busca complementar, não substitutiva."""
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        
        queries = [query]
        if "roblox" in query.lower() and "script" not in query.lower():
            queries.append(f"{query} roblox studio luau")
        elif "python" in query.lower():
            queries.append(f"{query} python example")
        elif "javascript" in query.lower():
            queries.append(f"{query} javascript example")
        
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
            subprocess.run(["git", "commit", "-m", f"BRX Enhanced v7.0: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            return "Sincronizado com sucesso!"
        except Exception as e:
            return f"Erro no Sync: {e}"

if __name__ == "__main__":
    brx = BRXCore()
    print(brx.get_response("cria um codigo roblox studio para command bar"))
    print("-" * 50)
    print(brx.get_response("oi, tudo bem?"))
    print("-" * 50)
    print(brx.get_response("como instalar pacotes no arch linux"))
