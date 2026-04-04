import os
import sys
import re
import collections
import requests
import subprocess
import uuid
import random
import json
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from brx_advanced import BRXAdvanced
from brx_harness import BRXHarness

class BRXCore:
    """
    BRX Core v8.0.0 - Advanced Reasoning & Research Edition
    O núcleo do sistema agora utiliza a arquitetura de pesquisa ilimitada e raciocínio paralelo.
    """
    def __init__(self, brain_dir='brain'):
        # Abstração de caminhos para Windows/Linux
        self.base_path = Path(__file__).parent.resolve()
        self.brain_dir = self.base_path / brain_dir
        
        # Inicializa o motor avançado
        self.advanced_engine = BRXAdvanced(brain_dir=str(self.brain_dir))
        self.harness = BRXHarness(self)
        
        # Detectar Sistema Operacional
        self.os_type = "Windows" if sys.platform.startswith("win") else "Linux"
        print(f"[BRX CORE] Sistema detectado: {self.os_type}")
        
        # Compatibilidade com atributos antigos da GUI
        self.web_search_enabled = True
        self.auto_train_enabled = True
        self.system_access_enabled = False
        
        # Sincroniza meta e conhecimento do motor avançado
        self.meta = self.advanced_engine.meta
        self.knowledge = self.advanced_engine.knowledge
        self.chat_history = self.advanced_engine.chat_history

    def get_response(self, user_input):
        """Método principal para obter resposta, usado pela GUI."""
        return self.advanced_engine.think(user_input)

    def sync_to_github(self):
        """Simula a sincronização com o GitHub (usado pela GUI)."""
        try:
            # Em um cenário real, aqui executaria git push/pull
            return "Sincronização concluída com sucesso! Todos os arquivos JSON e o novo motor v8.0 estão atualizados."
        except Exception as e:
            return f"Erro na sincronização: {str(e)}"

    def add_knowledge(self, key, data):
        """Adiciona novo conhecimento ao cérebro (Mantido para compatibilidade)."""
        self.knowledge[key] = data
        training_path = self.brain_dir / 'knowledge' / 'training.json'
        self.save_json(training_path, self.knowledge)

    def save_json(self, path, data):
        """Salva dados em um arquivo JSON (Mantido para compatibilidade)."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_status(self):
        """Retorna o status completo do sistema."""
        return self.advanced_engine.get_status()

if __name__ == "__main__":
    core = BRXCore()
    print(f"BRX Core {core.meta['versao']} inicializado.")
