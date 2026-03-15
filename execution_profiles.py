import json

class ExecutionProfiles:
    """Gerencia diferentes perfis de execução para o BRX AI, otimizados para consumo, velocidade ou profundidade."""
    
    def __init__(self):
        self.profiles = {
            "lite": {
                "description": "Otimizado para baixo consumo de recursos e respostas rápidas, ideal para notebooks com bateria. Mantém inteligência total, mas com foco na concisão.",
                "web_search_aggressiveness": 1, # Número de queries paralelas
                "knowledge_search_depth": 3,    # Número de blocos de conhecimento a considerar
                "response_verbosity": "concise",
                "max_web_snippets": 3,          # Número de snippets da web a processar
                "max_code_references": 2,       # Número de referências de código a incluir
                "cpu_utilization": "low",
                "memory_footprint": "small"
            },
            "turbo": {
                "description": "Equilíbrio entre velocidade e profundidade. Utiliza multi-threading e cache para respostas rápidas e abrangentes.",
                "web_search_aggressiveness": 2,
                "knowledge_search_depth": 5,
                "response_verbosity": "standard",
                "max_web_snippets": 5,
                "max_code_references": 3,
                "cpu_utilization": "medium",
                "memory_footprint": "medium"
            },
            "ultra": {
                "description": "Máxima profundidade e inteligência agressiva. Utiliza todos os recursos disponíveis para as respostas mais completas e detalhadas, sem limites de tamanho.",
                "web_search_aggressiveness": 3,
                "knowledge_search_depth": 10,   # Maior profundidade de busca
                "response_verbosity": "detailed",
                "max_web_snippets": 8,          # Mais snippets da web
                "max_code_references": 5,       # Mais referências de código
                "cpu_utilization": "high",
                "memory_footprint": "large"
            }
        }
        self.active_profile_name = "turbo"
        self.active_profile = self.profiles[self.active_profile_name]

    def set_profile(self, profile_name):
        if profile_name.lower() in self.profiles:
            self.active_profile_name = profile_name.lower()
            self.active_profile = self.profiles[self.active_profile_name]
            return True
        return False

    def get_active_profile(self):
        return self.active_profile_name, self.active_profile

    def get_profile_setting(self, setting_name):
        return self.active_profile.get(setting_name)

    def get_all_profiles_info(self):
        info = {}
        for name, profile in self.profiles.items():
            info[name] = profile["description"]
        return info

# Exemplo de uso
if __name__ == "__main__":
    profiles = ExecutionProfiles()
    print(f"Perfil ativo inicial: {profiles.get_active_profile()[0]}")
    print(f"Agressividade web: {profiles.get_profile_setting("web_search_aggressiveness")}")
    
    profiles.set_profile("ultra")
    print(f"\nPerfil ativo após mudança: {profiles.get_active_profile()[0]}")
    print(f"Agressividade web: {profiles.get_profile_setting("web_search_aggressiveness")}")
    print(f"Profundidade de conhecimento: {profiles.get_profile_setting("knowledge_search_depth")}")
