import os
import json
import collections
from datetime import datetime
from brx_reasoning import BRXAdvancedArchitecture
from behavior_analyzer import BehaviorAnalyzer
from self_awareness import SelfAwareness

class BRXAdvanced:
    """
    BRX AI v8.0 - Advanced Reasoning & Research Edition
    Upgrade completo integrando pesquisa multi-camada ILIMITADA e raciocínio paralelo com a base BRX.
    """
    
    def __init__(self, brain_dir="brain"): # brain_dir is now relative to the root of the repo
        self.brain_dir = brain_dir
        self.meta = {}
        self.knowledge = {}
        self.chat_history = []
        
        # Módulos Base Existentes
        self.behavior_analyzer = BehaviorAnalyzer()
        self.self_awareness = SelfAwareness()
        
        # Nova Arquitetura de Raciocínio (Pesquisa Ilimitada via DuckDuckGo)
        self.advanced_arch = BRXAdvancedArchitecture()
        
        # Configurações de Pesquisa (Sem Limites)
        self.research_mode = "intensive" # Padrão para máximo aproveitamento
        self.internal_discussion = True
        
        self.load_brain()

    def load_brain(self):
        """Carrega os dados do cérebro sem modificar arquivos JSON existentes, incluindo novas pastas."""
        # Load meta.json (still specific)
        meta_path = os.path.join(self.brain_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                try: 
                    self.meta = json.load(f)
                    # Upgrade em memória - Reflete a nova versão sem alterar o arquivo físico
                    self.meta["versao"] = "8.0.0"
                    self.meta["edicao"] = "Advanced Reasoning & Research Edition"
                except: 
                    self.meta = self.init_meta_in_memory()
        else: 
            self.meta = self.init_meta_in_memory()

        # Load all other JSON files recursively from the repository root
        repo_root = os.path.dirname(os.path.abspath(__file__)) # Get the directory where brx_advanced.py is located
        for root, dirs, files in os.walk(repo_root):
            for filename in files:
                if filename.endswith('.json'):
                    filepath = os.path.join(root, filename)
                    # Exclude meta.json as it's loaded separately
                    if os.path.basename(filepath) == 'meta.json' and os.path.dirname(filepath) == os.path.join(repo_root, self.brain_dir):
                        continue
                    
                    with open(filepath, 'r') as f:
                        try:
                            data = json.load(f)
                            # Use filename as key or merge into knowledge
                            # For simplicity, we'll merge. A more complex system might categorize.
                            self.knowledge.update(data)
                        except json.JSONDecodeError:
                            print(f"Warning: Could not decode JSON from {filepath}")
                        except Exception as e:
                            print(f"Error loading {filepath}: {e}")

    def init_meta_in_memory(self):
        """Inicializa metadados apenas em memória para respeitar a regra de não modificação."""
        return {
            "nome": "BRX",
            "versao": "8.0.0",
            "edicao": "Advanced Reasoning & Research Edition",
            "nascimento": datetime.now().isoformat(),
            "estado": "consciente",
            "arquitetura": "multi-layer research & parallel reasoning"
        }

    def set_research_mode(self, mode):
        """Altera o nível de profundidade da pesquisa. Todos os modos são ilimitados no DuckDuckGo."""
        valid_modes = ["basic", "intermediate", "professional", "intensive"]
        if mode in valid_modes:
            self.research_mode = mode
            return f"Modo de pesquisa alterado para: {mode}"
        return "Modo inválido."

    def think(self, user_input):
        """
        MOTOR DE PENSAMENTO AVANÇADO
        Integra análise de comportamento, pesquisa multi-camada (DuckDuckGo) e raciocínio paralelo sem limites.
        """
        # 1. Analisa comportamento do usuário usando a base existente
        styles = self.behavior_analyzer.analyze_dialogue_style(user_input)
        category = self.behavior_analyzer.analyze_request_category(user_input)
        
        # 2. Registra no histórico (Memória de Curto Prazo)
        self.chat_history.append({
            "user": user_input,
            "style": styles,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        
        # 3. Processa usando a arquitetura avançada (Pesquisa Ilimitada + Raciocínio Paralelo)
        # O sistema pode realizar múltiplas consultas ao DuckDuckGo conforme necessário.
        response = self.advanced_arch.process_request(user_input, mode=self.research_mode)
        
        # 4. Reflexão (Self-Awareness) - Aprendizado com a interação
        self.self_awareness.reflect_on_interaction(user_input, response, 1.0, "Advanced-Unlimited")
        
        # 5. Salva resposta no histórico
        self.chat_history[-1]["brx"] = response
        
        return response

    def get_status(self):
        """
        Retorna o status atual do sistema de raciocínio avançado.
        Inclui o número de itens de conhecimento carregados.
        """
        return {
            "versao": self.meta.get("versao"),
            "modo_pesquisa": self.research_mode,
            "agentes_ativos": list(self.advanced_arch.reasoning_engine.styles.keys()),
            "nivel_confianca": self.self_awareness.internal_state.get("confidence_level", 1.0),
            "capacidade": "Ilimitada (Pesquisa & Resposta)",
            "total_itens_conhecimento_carregados": len(self.knowledge)
        }

if __name__ == "__main__":
    ai = BRXAdvanced()
    print(f"Sistema {ai.meta['nome']} {ai.meta['versao']} - Arquitetura Ilimitada Inicializada.")
    print(f"Total de itens de conhecimento carregados: {ai.get_status()['total_itens_conhecimento_carregados']}")
