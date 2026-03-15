import concurrent.futures
import time
import hashlib
import os
import json
from collections import deque

class HighPerformanceEngine:
    """Motor de Alta Performance: Otimiza CPU, Memória e Velocidade de Resposta."""
    
    def __init__(self, cache_size=1000):
        self.l1_cache = {} # Cache ultra-rápido em memória
        self.l2_cache_file = 'brain/l2_cache.json'
        self.max_workers = os.cpu_count() or 4
        self.performance_history = deque(maxlen=100)
        self.load_l2_cache()

    def load_l2_cache(self):
        if os.path.exists(self.l2_cache_file):
            try:
                with open(self.l2_cache_file, 'r') as f:
                    self.l1_cache.update(json.load(f))
            except: pass

    def save_l2_cache(self):
        os.makedirs(os.path.dirname(self.l2_cache_file), exist_ok=True)
        with open(self.l2_cache_file, 'w') as f:
            json.dump(self.l1_cache, f, indent=2, ensure_ascii=False)

    def fast_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def parallel_search(self, search_func, queries):
        """Executa buscas em paralelo para máxima velocidade."""
        start_time = time.time()
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_query = {executor.submit(search_func, q): q for q in queries}
            for future in concurrent.futures.as_completed(future_to_query):
                try:
                    data = future.result()
                    if data: results.append(data)
                except Exception as e:
                    print(f"Erro na busca paralela: {e}")
        
        elapsed = time.time() - start_time
        self.performance_history.append(elapsed)
        return results, elapsed

    def get_performance_stats(self):
        if not self.performance_history:
            return "Aguardando métricas..."
        avg_speed = sum(self.performance_history) / len(self.performance_history)
        return f"[Velocidade Média: {avg_speed:.4f}s | Threads: {self.max_workers} | Cache: {len(self.l1_cache)} itens]"

    def optimize_response_time(self, func, *args):
        """Monitora e otimiza o tempo de resposta de qualquer função."""
        start = time.time()
        result = func(*args)
        end = time.time()
        return result, end - start
