import sys
from brx_advanced import BRXAdvanced

def main():
    print("="*50)
    print("BRX AI v8.0 - ADVANCED REASONING & RESEARCH EDITION")
    print("="*50)
    print("Comandos especiais:")
    print("  /mode [basic|intermediate|professional|intensive] - Altera profundidade da pesquisa")
    print("  /status - Mostra o status atual dos agentes de raciocínio")
    print("  /exit - Sair do sistema")
    print("="*50)
    
    ai = BRXAdvanced()
    
    while True:
        try:
            user_input = input("\nVocê: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == "/exit":
                print("Encerrando BRX Advanced...")
                break
                
            if user_input.startswith("/mode"):
                parts = user_input.split()
                if len(parts) > 1:
                    print(ai.set_research_mode(parts[1]))
                else:
                    print(f"Modo atual: {ai.research_mode}")
                continue
                
            if user_input.lower() == "/status":
                status = ai.get_status()
                print("\nStatus do Sistema:")
                for k, v in status.items():
                    print(f"  {k}: {v}")
                continue
            
            print("\nBRX está processando (pesquisa multi-camada + raciocínio paralelo)...")
            response = ai.think(user_input)
            print(f"\nBRX: {response}")
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
