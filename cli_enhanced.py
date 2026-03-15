import sys
import os
from brx_enhanced import BRXCore

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(web_status, train_status, sys_status, behavior_profile):
    status_web = "WEB: ON" if web_status else "WEB: OFF"
    status_train = "TREINO: ON" if train_status else "TREINO: OFF"
    status_sys = "SYS: ON" if sys_status else "SYS: OFF"
    
    creation_count = behavior_profile["creation_requests"]
    info_count = behavior_profile["information_requests"]
    dialogue = behavior_profile["dialogue_style"]
    
    print("=" * 80)
    print(" " * 20 + "BRX AI v7.0 - ENHANCED EDITION")
    print("=" * 80)
    print(f"Status: {status_web} | {status_train} | {status_sys}")
    print(f"Comportamento: Criações={creation_count} | Informações={info_count} | Diálogo={dialogue}")
    print(f"Comandos: 'web' 'treino' 'sys' 'sync' 'perfil' 'sair'")
    print("-" * 80)

def print_behavior_profile(profile):
    print("\n" + "=" * 80)
    print("PERFIL DE COMPORTAMENTO DO USUÁRIO")
    print("=" * 80)
    print(f"Pedidos de Criação: {profile['creation_requests']}")
    print(f"Pedidos de Informação: {profile['information_requests']}")
    print(f"Estilo de Diálogo: {profile['dialogue_style']}")
    print(f"Linguagens Preferidas: {', '.join(profile['preferred_languages']) if profile['preferred_languages'] else 'Nenhuma detectada'}")
    print(f"Padrões de Interação: {len(profile['interaction_patterns'])} padrões detectados")
    print("=" * 80 + "\n")

def main():
    try:
        brx = BRXCore()
    except Exception as e:
        print(f"Erro ao carregar o cérebro do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, brx.user_behavior_profile)

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Foi um prazer ajudar.")
                break
            
            if user_input.lower() == 'web':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, brx.user_behavior_profile)
                print(f"\nBRX: Pesquisa web {'ativada' if brx.web_search_enabled else 'desativada'}.")
                continue

            if user_input.lower() == 'treino':
                brx.auto_train_enabled = not brx.auto_train_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, brx.user_behavior_profile)
                print(f"\nBRX: Auto-treinamento {'ativado' if brx.auto_train_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'sys':
                brx.system_access_enabled = not brx.system_access_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, brx.user_behavior_profile)
                print(f"\nBRX: Acesso ao sistema {'ativado' if brx.system_access_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'perfil':
                print_behavior_profile(brx.user_behavior_profile)
                continue

            if user_input.lower() == 'sync':
                print("\nBRX: Sincronizando conhecimentos com o GitHub...")
                result = brx.sync_to_github()
                print(f"BRX: {result}")
                continue

            if not user_input:
                continue

            response = brx.get_response(user_input)
            print(f"\nBRX: {response}")

        except KeyboardInterrupt:
            print("\n\nBRX: Encerrando... Até mais!")
            break
        except Exception as e:
            print(f"\nBRX: Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
