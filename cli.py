import sys
import os
from brx import BRXCore

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    print("=" * 50)
    print(" " * 15 + "BRX AI - CHAT INTERATIVO")
    print("=" * 50)
    print("Bem-vindo ao BRX! Digite 'sair' para encerrar.")
    print("-" * 50)

def main():
    # Inicializar o núcleo do BRX
    try:
        brx = BRXCore()
    except Exception as e:
        print(f"Erro ao carregar o cérebro do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header()

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Foi um prazer conversar com você.")
                break
            
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
