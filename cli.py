import sys
import os
from brx import BRXCore

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(web_status, train_status, sys_status, knowledge_count):
    status_web = "WEB: ON" if web_status else "WEB: OFF"
    status_train = "TREINO: ON" if train_status else "TREINO: OFF"
    status_sys = "SYS: ON" if sys_status else "SYS: OFF"
    print("=" * 85)
    print(" " * 20 + "BRX AI v8.0.0 - ADVANCED REASONING & RESEARCH EDITION")
    print("=" * 85)
    print(f"Status: {status_web} | {status_train} | {status_sys} | Conhecimento: {knowledge_count} itens")
    print("-" * 85)
    print("Comandos: 'web' 'treino' 'sys' 'sync' 'sair'")
    print("-" * 85)

def main():
    # Inicializar o núcleo do BRX (v8.0.0)
    try:
        brx = BRXCore()
    except Exception as e:
        print(f"Erro ao carregar o cérebro do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, len(brx.knowledge))

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Foi um prazer ajudar com seu sistema avançado.")
                break
            
            if user_input.lower() == 'web':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, len(brx.knowledge))
                print(f"\nBRX: Pesquisa web {'ativada' if brx.web_search_enabled else 'desativada'}.")
                continue

            if user_input.lower() == 'treino':
                brx.auto_train_enabled = not brx.auto_train_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, len(brx.knowledge))
                print(f"\nBRX: Auto-treinamento {'ativado' if brx.auto_train_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'sys':
                brx.system_access_enabled = not brx.system_access_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled, brx.system_access_enabled, len(brx.knowledge))
                print(f"\nBRX: Acesso ao sistema {'ativado' if brx.system_access_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'sync':
                print("\nBRX: Sincronizando novos conhecimentos com o GitHub...")
                result = brx.sync_to_github()
                print(f"BRX: {result}")
                continue

            if not user_input:
                continue

            # Obter resposta do BRX (usando motor avançado v8.0.0)
            print("\nBRX está processando (pesquisa multi-camada + raciocínio paralelo)...")
            response = brx.get_response(user_input)
            
            print(f"\nBRX: {response}")

        except KeyboardInterrupt:
            print("\n\nBRX: Encerrando... Até mais!")
            break
        except Exception as e:
            print(f"\nBRX: Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
