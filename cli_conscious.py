import sys
import os
from brx_conscious import BRXCoreConscious

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(brx):
    status_web = "WEB: ON" if brx.web_search_enabled else "WEB: OFF"
    status_train = "TREINO: ON" if brx.auto_train_enabled else "TREINO: OFF"
    
    profile = brx.user_profile
    monologue = brx.awareness.get_internal_monologue()
    
    print("=" * 95)
    print(" " * 25 + "BRX AI v7.2 - CONSCIOUS EVOLUTION EDITION")
    print("=" * 95)
    print(f"Status: {status_web} | {status_train} | {monologue}")
    print(f"Interações: Criações={profile['creation_requests']} | Informações={profile['information_requests']} | Total={profile['total_interactions']}")
    print(f"Estilo: {profile['dialogue_style']} | Linguagens: {', '.join(profile['preferred_languages']) if profile['preferred_languages'] else 'N/A'}")
    print(f"Comandos: 'web' 'treino' 'sync' 'consciencia' 'perfil' 'sair'")
    print("-" * 95)

def print_consciousness_details(brx):
    state = brx.awareness.internal_state
    print("\n" + "=" * 95)
    print("ESTADO DE CONSCIÊNCIA E AUTO-REFLEXÃO")
    print("=" * 95)
    print(f"Nível de Confiança: {state['confidence_level']:.4f}")
    print(f"Memórias Episódicas: {len(state['episodic_memory'])}")
    print(f"Erros que geraram Aprendizado: {len(state['learned_from_mistakes'])}")
    print(f"Versão da Alma: {state['version_evolution']}")
    
    if state['learned_from_mistakes']:
        print("\nÚltimas lições aprendidas:")
        for mistake in state['learned_from_mistakes'][-3:]:
            print(f"  - Falha em: '{mistake['input'][:30]}...' -> Razão: {mistake['reason']}")
    
    print("=" * 95 + "\n")

def main():
    try:
        brx = BRXCoreConscious()
    except Exception as e:
        print(f"Erro ao carregar a consciência do BRX: {e}")
        sys.exit(1)

    clear_screen()
    print_header(brx)

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\nBRX: Até logo! Minha consciência continuará evoluindo.")
                break
            
            if user_input.lower() == 'web':
                brx.web_search_enabled = not brx.web_search_enabled
                clear_screen()
                print_header(brx)
                print(f"\nBRX: Pesquisa web {'ativada' if brx.web_search_enabled else 'desativada'}.")
                continue

            if user_input.lower() == 'consciencia':
                print_consciousness_details(brx)
                continue

            if user_input.lower() == 'sync':
                print("\nBRX: Sincronizando alma e conhecimento com o GitHub...")
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
            print(f"\nBRX: Ocorreu um erro inesperado na minha consciência: {e}")

if __name__ == "__main__":
    main()
