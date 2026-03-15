from brx import BRXCore
import json

def run_coder_tests():
    print("="*60)
    print("   TESTE DE GERAÇÃO DE CÓDIGO E PESQUISA - BRX AI v6.1   ")
    print("="*60)

    brx = BRXCore()
    # Ativar pesquisa web para o teste
    brx.web_search_enabled = True
    
    test_queries = [
        "Crie um script de Roblox para dar 100 de vida ao jogador quando ele tocar em um bloco.",
        "Como criar uma classe em Java que imprime 'Olá Mundo'?",
        "Como fazer um sistema de pulo no Unity usando C#?"
    ]

    for query in test_queries:
        print(f"\n[TESTE] Pergunta: '{query}'")
        print("[BRX PENSANDO...]")
        
        # O motor v6.1 deve detectar a intenção de programação e buscar na web se necessário
        response = brx.get_response(query)
        
        print(f"\n[RESPOSTA DO BRX]:\n{response}")
        print("-" * 60)

if __name__ == "__main__":
    run_coder_tests()
