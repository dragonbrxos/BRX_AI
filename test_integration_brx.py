from brx import BRXCore
import os
import json
from datetime import datetime

def run_integration_test():
    print("="*60)
    print("   TESTE DE INTEGRAÇÃO - PESQUISA WEB & SYNC GITHUB   ")
    print("="*60)

    brx = BRXCore()
    brx.web_search_enabled = True
    brx.auto_train_enabled = True
    
    # 1. Teste de Pesquisa Web (Pergunta sobre algo muito recente ou específico)
    query = "Quais as novidades do Arch Linux em Março de 2026?"
    print(f"\n[TESTE 1] Pesquisa Web: '{query}'")
    response = brx.get_response(query)
    print(f"\n[RESPOSTA DO BRX]:\n{response}")
    
    if "Pesquisa Web" in response:
        print("\n[STATUS] OK - Pesquisa Web funcionando.")
    else:
        print("\n[STATUS] FALHA - Pesquisa Web não foi acionada.")

    # 2. Simular Auto-Treinamento (Salvar novo conhecimento localmente)
    print("\n[TESTE 2] Simulando Auto-Treinamento...")
    new_knowledge = {
        "test_sync_id": {
            "id": "test_sync_id",
            "texto": f"Conhecimento de teste gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "categoria": "general",
            "palavras": ["teste", "sync", "github"]
        }
    }
    training_path = os.path.join(brx.brain_dir, 'knowledge', 'training.json')
    brx.save_json(training_path, new_knowledge)
    print(f"[STATUS] OK - Novo conhecimento salvo em {training_path}")

    # 3. Teste de Sincronização (Sync)
    print("\n[TESTE 3] Executando Sincronização com GitHub...")
    sync_result = brx.sync_to_github()
    print(f"[RESULTADO SYNC]: {sync_result}")

if __name__ == "__main__":
    run_integration_test()
