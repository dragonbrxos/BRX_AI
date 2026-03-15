import re
from datetime import datetime
from collections import defaultdict

class BehaviorAnalyzer:
    """Analisador avançado de comportamento, diálogo e padrões de pedidos do usuário."""
    
    def __init__(self):
        self.dialogue_history = []
        self.behavior_patterns = defaultdict(int)
        self.request_patterns = defaultdict(int)
        self.user_preferences = {
            "response_style": "direct",
            "verbosity": "concise",
            "code_comments": True,
            "explanation_level": "medium"
        }
    
    def analyze_dialogue_style(self, text):
        """Analisa o estilo de diálogo do usuário."""
        text_lower = text.lower()
        
        style_indicators = {
            "formal": r"(gostaria|poderia|solicito|requeiro|prezado|senhor|senhora)",
            "casual": r"(tipo|sabe|entende|né|cê|tá|tô|pra|pro|blz|vlw|tmj|opa)",
            "technical": r"(implementar|algoritmo|estrutura|otimizar|refatorar|debug|stack|heap|cache)",
            "urgent": r"(rápido|urgente|agora|já|imediatamente|logo|asap)",
            "curious": r"(por que|como|o que|qual|quando|onde|explique|entenda|mostre)",
            "demanding": r"(preciso|tenho que|deve|obrigatório|exijo|necessário)",
            "polite": r"(por favor|obrigado|desculpa|se puder|se possível|agradeço)"
        }
        
        detected_styles = []
        for style, pattern in style_indicators.items():
            if re.search(pattern, text_lower):
                detected_styles.append(style)
        
        return detected_styles if detected_styles else ["neutral"]
    
    def analyze_request_category(self, text):
        """Categoriza o tipo de pedido do usuário."""
        text_lower = text.lower()
        
        categories = {
            "code_generation": {
                "keywords": ["cria", "faz", "gera", "escreve", "implementa", "desenvolve", "script", "código", "programa"],
                "patterns": [
                    r"(cria|faz|gera)\s+(um\s+)?(script|código|programa|função)",
                    r"(script|código)\s+(para|que|em|com)",
                    r"(escreve|implementa|desenvolve)\s+(um\s+)?(sistema|app|aplicativo)"
                ]
            },
            "debugging": {
                "keywords": ["erro", "bug", "não funciona", "quebrou", "problema", "falha", "debug"],
                "patterns": [
                    r"(erro|bug|problema|falha)\s+(em|no|na|com)",
                    r"(não\s+)?(funciona|roda|executa)",
                    r"(como\s+)?(corrigir|consertar|arrumar|debugar)"
                ]
            },
            "explanation": {
                "keywords": ["explica", "como", "o que", "qual", "por que", "entenda", "mostre"],
                "patterns": [
                    r"^(como|o que|qual|por que|explique|entenda)",
                    r"(me\s+)?(explica|explique|mostre|mostra)",
                    r"(como\s+)?(funciona|usa|implementa)"
                ]
            },
            "optimization": {
                "keywords": ["otimiza", "melhora", "performance", "rápido", "eficiente", "refatora"],
                "patterns": [
                    r"(otimiza|melhora|refatora)\s+(o|a|este|esse)",
                    r"(performance|velocidade|eficiência)",
                    r"(como\s+)?(melhorar|otimizar|acelerar)"
                ]
            },
            "integration": {
                "keywords": ["integra", "conecta", "usa", "com", "junto", "combine"],
                "patterns": [
                    r"(integra|conecta|usa)\s+(com|junto|a)",
                    r"(como\s+)?(integrar|conectar|combinar)",
                    r"(com\s+)?(api|banco|sistema|serviço)"
                ]
            },
            "learning": {
                "keywords": ["aprenda", "tutorial", "passo a passo", "guia", "exemplo"],
                "patterns": [
                    r"(tutorial|guia|passo\s+a\s+passo|exemplo)",
                    r"(como\s+)?(aprender|começar|iniciar)",
                    r"(me\s+)?(ensina|ensine|mostre|mostra)"
                ]
            }
        }
        
        detected_categories = []
        
        for category, details in categories.items():
            # Verificar keywords
            for keyword in details["keywords"]:
                if keyword in text_lower:
                    detected_categories.append(category)
                    break
            
            # Verificar patterns
            if category not in detected_categories:
                for pattern in details["patterns"]:
                    if re.search(pattern, text_lower):
                        detected_categories.append(category)
                        break
        
        return detected_categories if detected_categories else ["general"]
    
    def analyze_complexity_level(self, text):
        """Analisa o nível de complexidade implícito no pedido."""
        text_lower = text.lower()
        
        complexity_indicators = {
            "beginner": r"(básico|simples|fácil|iniciante|começo|novo|primeiro)",
            "intermediate": r"(intermediário|médio|normal|comum|padrão)",
            "advanced": r"(avançado|complexo|difícil|expert|profissional|otimizado)",
            "expert": r"(expert|master|ninja|guru|hardcore|extreme|edge\s+case)"
        }
        
        for level, pattern in complexity_indicators.items():
            if re.search(pattern, text_lower):
                return level
        
        return "intermediate"
    
    def analyze_urgency(self, text):
        """Analisa o nível de urgência do pedido."""
        text_lower = text.lower()
        
        urgency_levels = {
            "critical": r"(urgente|crítico|emergência|agora|já|imediatamente|asap)",
            "high": r"(rápido|logo|em breve|logo|prioridade)",
            "normal": r"(quando\s+puder|sem pressa|normal|comum)",
            "low": r"(sem pressa|quando tiver tempo|futuramente|eventualmente)"
        }
        
        for level, pattern in urgency_levels.items():
            if re.search(pattern, text_lower):
                return level
        
        return "normal"
    
    def detect_language_preference(self, text):
        """Detecta a linguagem de programação preferida."""
        text_lower = text.lower()
        
        languages = {
            "python": ["python", "py", "django", "flask", "pandas"],
            "javascript": ["javascript", "js", "react", "node", "express", "typescript", "ts"],
            "luau": ["lua", "luau", "roblox", "studio"],
            "csharp": ["c#", "csharp", "unity", ".net"],
            "java": ["java", "spring", "maven"],
            "sql": ["sql", "database", "banco de dados", "postgresql", "mysql"],
            "bash": ["bash", "shell", "sh", "linux", "arch", "terminal"],
            "cpp": ["c++", "cpp", "c plus plus"],
            "go": ["golang", "go"],
            "rust": ["rust", "cargo"],
            "php": ["php", "laravel", "wordpress"],
            "ruby": ["ruby", "rails", "gem"]
        }
        
        detected = []
        for lang, keywords in languages.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected.append(lang)
                    break
        
        return detected if detected else []
    
    def analyze_context_awareness(self, current_text, history):
        """Analisa se o pedido requer contexto do histórico."""
        text_lower = current_text.lower()
        
        context_indicators = {
            "continuation": r"^(também|e|mas|porém|contudo|todavia|além disso)",
            "reference": r"(isso|aquilo|anterior|anterior|acima|abaixo|último)",
            "modification": r"(muda|altera|modifica|ajusta|corrige|melhora)\s+(o|a|isso|aquilo)",
            "expansion": r"(adiciona|inclui|expande|estende|aumenta)\s+(mais|também|outro)"
        }
        
        requires_context = False
        for indicator_type, pattern in context_indicators.items():
            if re.search(pattern, text_lower):
                requires_context = True
                break
        
        return requires_context
    
    def generate_response_profile(self, dialogue_styles, request_categories, complexity, urgency):
        """Gera um perfil de resposta baseado na análise."""
        profile = {
            "dialogue_styles": dialogue_styles,
            "request_categories": request_categories,
            "complexity_level": complexity,
            "urgency_level": urgency,
            "response_format": self._determine_response_format(request_categories),
            "detail_level": self._determine_detail_level(complexity),
            "code_style": self._determine_code_style(dialogue_styles),
            "include_explanation": "explanation" in request_categories or "learning" in request_categories,
            "include_examples": "learning" in request_categories or complexity in ["beginner", "intermediate"],
            "direct_response": "code_generation" in request_categories or urgency in ["critical", "high"]
        }
        return profile
    
    def _determine_response_format(self, categories):
        """Determina o formato de resposta ideal."""
        if "code_generation" in categories:
            return "code_block"
        elif "explanation" in categories:
            return "detailed_explanation"
        elif "learning" in categories:
            return "tutorial"
        elif "debugging" in categories:
            return "step_by_step"
        else:
            return "standard"
    
    def _determine_detail_level(self, complexity):
        """Determina o nível de detalhe da resposta."""
        levels = {
            "beginner": "high",
            "intermediate": "medium",
            "advanced": "low",
            "expert": "minimal"
        }
        return levels.get(complexity, "medium")
    
    def _determine_code_style(self, dialogue_styles):
        """Determina o estilo de código (comentários, formatação, etc)."""
        if "casual" in dialogue_styles:
            return "concise"
        elif "technical" in dialogue_styles:
            return "optimized"
        elif "formal" in dialogue_styles:
            return "documented"
        else:
            return "standard"
    
    def record_interaction(self, user_input, brx_response, analysis_result):
        """Registra uma interação para aprendizado futuro."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "brx_response": brx_response,
            "analysis": analysis_result
        }
        self.dialogue_history.append(interaction)
        
        # Atualizar padrões
        for category in analysis_result.get("request_categories", []):
            self.request_patterns[category] += 1
        
        for style in analysis_result.get("dialogue_styles", []):
            self.behavior_patterns[style] += 1
    
    def get_user_profile_summary(self):
        """Retorna um resumo do perfil do usuário baseado no histórico."""
        if not self.dialogue_history:
            return "Nenhuma interação registrada ainda."
        
        total_interactions = len(self.dialogue_history)
        
        # Padrões mais frequentes
        most_common_request = max(self.request_patterns, key=self.request_patterns.get) if self.request_patterns else "N/A"
        most_common_style = max(self.behavior_patterns, key=self.behavior_patterns.get) if self.behavior_patterns else "N/A"
        
        summary = {
            "total_interactions": total_interactions,
            "most_common_request_type": most_common_request,
            "most_common_dialogue_style": most_common_style,
            "request_distribution": dict(self.request_patterns),
            "behaviour_distribution": dict(self.behavior_patterns)
        }
        
        return summary

# Exemplo de uso
if __name__ == "__main__":
    analyzer = BehaviorAnalyzer()
    
    test_inputs = [
        "cria um script roblox para deletar partes",
        "como funciona o sistema de loops em python?",
        "urgente: conserta esse bug no meu código",
        "tutorial: como começar com javascript?"
    ]
    
    for test in test_inputs:
        print(f"\nAnalisando: {test}")
        print(f"Estilo de Diálogo: {analyzer.analyze_dialogue_style(test)}")
        print(f"Categoria de Pedido: {analyzer.analyze_request_category(test)}")
        print(f"Nível de Complexidade: {analyzer.analyze_complexity_level(test)}")
        print(f"Urgência: {analyzer.analyze_urgency(test)}")
        print(f"Linguagens Detectadas: {analyzer.detect_language_preference(test)}")
