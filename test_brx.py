from brx import BRXCore
import json

def run_tests():
    print("="*50)
    print("   TESTE DE ESTRESSE - BRX AI v6.0 (PROFESSIONAL)   ")
    print("="*50)

    brx = BRXCore()
    
    test_cases = [
        ("Olá, quem é você?", "general"),
        ("Como eu atualizo o sistema no Arch Linux?", "arch_linux"),
        ("Quanto é 15 + 25?", "math"),
        ("Como fazer um loop for em Python?", "programming"),
        ("O que é o systemctl status?", "systemd")
    ]

    for query, expected_intent in test_cases:
        print(f"\n[TESTE] Pergunta: '{query}'")
        intent = brx.think(query)
        response = brx.get_response(query)
        
        print(f"[RESULTADO] Intenção Detectada: {intent}")
        print(f"[RESPOSTA] {response}")
        
        if intent == expected_intent:
            print("[STATUS] OK - Intenção correta.")
        else:
            print(f"[STATUS] AVISO - Intenção esperada: {expected_intent}, mas obteve: {intent}")
        print("-" * 50)

    print("\n[TESTE] Verificando Memória de Contexto...")
    brx.get_response("Meu nome é Manus.")
    context_response = brx.get_response("Qual é o meu nome?")
    print(f"[RESPOSTA CONTEXTO] {context_response}")

    print("\n[TESTE] Verificando Conexão Internet...")
    print(f"[INTERNET] {brx.check_internet()}")

if __name__ == "__main__":
    run_tests()
