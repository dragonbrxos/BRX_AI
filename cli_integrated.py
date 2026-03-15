import sys
import os
from brx_integrated import BRXCoreIntegrated

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(brx):
    status_web = "WEB: ON" if brx.web_search_enabled else "WEB: OFF"
    status_train = "TREINO: ON" if brx.auto_train_enabled else "TREINO: OFF"
    status_sys = "SYS: ON" if brx.system_access_enabled else "SYS: OFF"
    
    profile = brx.get_user_profile()
    
    print("=" * 85)
    print(" " * 20 + "BRX AI v7.1 - INTEGRATED ENHANCED EDITION")
    print("=" * 85)
    print(f"Status: {status_web} | {status_train} | {status_sys}")
    print(f"Comportamento: Criações={profile['creation_requests']} | Informações={profile['information_requests']} | Total={profile['total_interactions']}")
    print(f"Estilo de Diálogo: {profile['dialogue_style']} | Linguagens: {', '.join(profile['preferred_languages']) if profile['preferred_languages'] else 'N/A'}")
    print(f"Comandos: 'web' 'treino' 'sys' 'sync' 'perfil' 'comportamento' 'sair'")
    print("-" * 85)

def print_user_profile(brx):
    profile = brx.get_user_profile()
    print("\n" + "=" * 85)
    print("PERFIL DO USUÁRIO")
    print("=" * 85)
    print(f"Total de Interações: {profile['total_interactions']}")
    print(f"Pedidos de Criação: {profile['creation_requests']}")
    print(f"Pedidos de Informação: {profile['information_requests']}")
    print(f"Estilo de Diálogo Predominante: {profile['dialogue_style']}")
    print(f"Linguagens Preferidas: {', '.join(profile['preferred_languages']) if profile['preferred_languages'] else 'Nenhuma detectada'}")
    print("=" * 85 + "\n")

def print_behavior_summary(brx):
    summary = brx.get_behavior_summary()
    print("\n" + "=" * 85)
    print("RESUMO DE COMPORTAMENTO")
    print("=" * 85)
    
    if isinstance(summary, str):
        print(summary)
    else:
        print(f"Total de Interações Registradas: {summary.get('total_interactions', 0)}")
        print(f"Tipo de Pedido Mais Comum: {summary.get('most_common_request_type', 'N/A')}")
        print(f"Estilo de Diálogo Mais Comum: {summary.get('most_common_dialogue_style', 'N/A')}")
        
        if summary.get('request_distribution'):
            print("\nDistribuição de Tipos de Pedidos:")
            for req_type, count in summary['request_distribution'].items():
                print(f"  - {req_type}: {count}")
        
        if summary.get('behaviour_distribution'):
            print("\nDistribuição de Estilos de Comportamento:")
            for style, count in summary['behaviour_distribution'].items():
                print(f"  - {style}: {count}")
    
    print("=" * 85 + "\n")

def main():
    try:
        brx = BRXCoreIntegrated()
    except Exception as e:
        print(f"Erro ao carregar o cérebro do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header(brx)

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Foi um prazer ajudar.")
                break
            
            if user_input.lower() == 'web':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx)
                print(f"\nBRX: Pesquisa web {'ativada' if brx.web_search_enabled else 'desativada'}.")
                continue

            if user_input.lower() == 'treino':
                brx.auto_train_enabled = not brx.auto_train_enabled
                clear_screen()
                print_header(brx)
                print(f"\nBRX: Auto-treinamento {'ativado' if brx.auto_train_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'sys':
                brx.system_access_enabled = not brx.system_access_enabled
                clear_screen()
                print_header(brx)
                print(f"\nBRX: Acesso ao sistema {'ativado' if brx.system_access_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'perfil':
                print_user_profile(brx)
                continue

            if user_input.lower() == 'comportamento':
                print_behavior_summary(brx)
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
