import sys
import os
import time
from brx_turbo import BRXCoreTurbo

def clear_screen():
    os.system(\'clear\' if os.name == \'posix\' else \'cls\')

def print_header(brx):
    status_web = \"WEB: ON\" if brx.web_search_enabled else \"WEB: OFF\"
    status_train = \"TREINO: ON\" if brx.auto_train_enabled else \"TREINO: OFF\"
    
    profile = brx.user_profile
    hp_stats = brx.hp_engine.get_performance_stats()
    monologue = brx.awareness.get_internal_monologue()
    active_profile_name, _ = brx.execution_profiles.get_active_profile()
    
    print(\"=\" * 105)
    print(\" \" * 30 + \"BRX AI v7.4 - UNLIMITED PERFORMANCE EDITION\")
    print(\"=\" * 105)
    print(f\"Status: {status_web} | {status_train} | {hp_stats}\")
    print(f\"Consciência: {monologue}\")
    print(f\"Métricas: Criações={profile[\'creation_requests\']} | Informações={profile[\'information_requests\']} | Tempo Médio={profile[\'avg_response_time\']:.4f}s\")
    print(f\"Perfil Ativo: {active_profile_name.upper()}\")
    print(f\"Comandos: \'web\' \'treino\' \'sync\' \'performance\' \'consciencia\' \'perfil <nome>\' \'perfis\' \'sair\'")
    print(\"-\" * 105)

def print_performance_details(brx):
    stats = brx.hp_engine.get_performance_stats()
    print(\"\\n\" + \"=\" * 105)
    print(\"DETALHES DE ALTA PERFORMANCE (HARDWARE & CPU)\")
    print(\"=\" * 105)
    print(f\"Threads de Processamento: {brx.hp_engine.max_workers}\")
    print(f\"Tamanho do Cache L1 (Memória): {len(brx.hp_engine.l1_cache)}\")
    print(f\"Histórico de Velocidade: {list(brx.hp_engine.performance_history)[-5:]}\")
    print(f\"Otimização de Hardware: Notebook / Laptop (Bateria & CPU)\")
    print(f\"Busca Paralela Agressiva: ATIVA\")
    print(\"=\" * 105 + \"\\n\")

def print_profiles_info(brx):
    profiles_info = brx.execution_profiles.get_all_profiles_info()
    print(\"\\n\" + \"=\" * 105)
    print(\"PERFIS DE EXECUÇÃO DISPONÍVEIS\")
    print(\"=\" * 105)
    for name, desc in profiles_info.items():
        print(f\"- {name.upper()}: {desc}\")
    print(\"=\" * 105 + \"\\n\")

def main():
    try:
        brx = BRXCoreTurbo()
    except Exception as e:
        print(f\"Erro ao carregar o motor Turbo do BRX: {e}\")
        sys.exit(1)

    clear_screen()
    print_header(brx)

    while True:
        try:
            user_input = input(\"\\nVocê: \").strip()
            
            if user_input.lower() in [\'sair\', \'exit\', \'quit\', \'tchau\']:
                print(\"\\nBRX: Até logo! O motor Turbo continuará em stand-by.\")
                break
            
            if user_input.lower() == \'web\':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx)
                print(f\"\\nBRX: Pesquisa web {\'ativada\' if brx.web_search_enabled else \'desativada\'}.\")
                continue

            if user_input.lower() == \'performance\':
                print_performance_details(brx)
                continue

            if user_input.lower() == \'consciencia\':
                # Reutiliza a função de print_consciousness_details do cli_conscious.py
                # Para evitar duplicação, podemos importar ou copiar a lógica aqui.
                # Por simplicidade, vou apenas indicar que seria uma chamada a uma função similar.
                # Para este exemplo, vou simular a saída.
                print(\"\\n\" + \"=\" * 95)
                print(\"ESTADO DE CONSCIÊNCIA E AUTO-REFLEXÃO\")
                print(\"=\" * 95)
                print(f\"Nível de Confiança: {brx.awareness.internal_state[\'confidence_level\']:.4f}\")
                print(f\"Memórias Episódicas: {len(brx.awareness.internal_state[\'episodic_memory\'])}\")
                print(f\"Erros que geraram Aprendizado: {len(brx.awareness.internal_state[\'learned_from_mistakes\'])}\")
                print(f\"Versão da Alma: {brx.awareness.internal_state[\'version_evolution\']}\")
                print(\"=\" * 95 + \"\\n\")
                continue

            if user_input.lower().startswith(\'perfil \'):
                parts = user_input.split(\' \')
                if len(parts) == 2:
                    profile_name = parts[1]
                    if brx.execution_profiles.set_profile(profile_name):
                        brx.user_profile[\'active_profile\'] = profile_name
                        clear_screen()
                        print_header(brx)
                        print(f\"\\nBRX: Perfil de execução alterado para {profile_name.upper()}.\")
                    else:
                        print(f\"\\nBRX: Perfil \'{profile_name}\' não encontrado. Use \'perfis\' para ver as opções.\")
                else:
                    print(\"\\nBRX: Uso: perfil <nome_do_perfil> (ex: perfil turbo)\")
                continue

            if user_input.lower() == \'perfis\':
                print_profiles_info(brx)
                continue

            if user_input.lower() == \'sync\':
                print(\"\\nBRX: Sincronizando alma e motor Turbo com o GitHub...\")
                result = brx.sync_to_github()
                print(f\"BRX: {result}\")
                continue

            if not user_input:
                continue

            response = brx.get_response(user_input)
            print(f\"\\nBRX: {response}\")

        except KeyboardInterrupt:
            print(\"\\n\\nBRX: Encerrando motor Turbo... Até mais!\")
            break
        except Exception as e:
            print(f\"\\nBRX: Ocorreu um erro inesperado no motor Turbo: {e}\")

if __name__ == \"__main__\":
    main()
