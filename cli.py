import sys
import os
from brx import BRXCore

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(web_status, train_status):
    status_web = "WEB: ON" if web_status else "WEB: OFF"
    status_train = "TREINO: ON" if train_status else "TREINO: OFF"
    print("=" * 70)
    print(" " * 25 + "BRX AI v3.0 - COLABORATIVO")
    print("=" * 70)
    print(f"Status: {status_web} | {status_train} | 'web' 'treino' 'sync' 'sair'")
    print("-" * 70)

def main():
    # Inicializar o núcleo do BRX
    try:
        brx = BRXCore()
    except Exception as e:
        print(f"Erro ao carregar o cérebro do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header(brx.web_search_enabled, brx.auto_train_enabled)

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Foi um prazer conversar com você.")
                break
            
            if user_input.lower() == 'web':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled)
                print(f"\nBRX: Pesquisa web {'ativada' if brx.web_search_enabled else 'desativada'}.")
                continue

            if user_input.lower() == 'treino':
                brx.auto_train_enabled = not brx.auto_train_enabled
                clear_screen()
                print_header(brx.web_search_enabled, brx.auto_train_enabled)
                print(f"\nBRX: Auto-treinamento {'ativado' if brx.auto_train_enabled else 'desativado'}.")
                continue

            if user_input.lower() == 'sync':
                print("\nBRX: Sincronizando novos conhecimentos com o GitHub...")
                result = brx.sync_to_github()
                print(f"BRX: {result}")
                continue

            if not user_input:
                continue

            # Obter resposta do BRX
            response = brx.get_response(user_input)
            
            print(f"\nBRX: {response}")

        except KeyboardInterrupt:
            print("\n\nBRX: Encerrando... Até mais!")
            break
        except Exception as e:
            print(f"\nBRX: Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
