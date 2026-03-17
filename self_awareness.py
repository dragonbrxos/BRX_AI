import json
import os
from datetime import datetime
import hashlib

class SelfAwareness:
    """Módulo de introspecção: Permite que o BRX analise sua própria eficácia e aprenda com o erro."""
    
    def __init__(self, state_file='brain/awareness_state.json'):
        self.state_file = state_file
        self.internal_state = {
            "last_thought": "",
            "confidence_level": 1.0,
            "learned_from_mistakes": [],
            "episodic_memory": [], # Memórias de longo prazo significativas
            "self_correction_count": 0,
            "version_evolution": "7.2.0",
            "active_profile_history": []
        }
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                try: self.internal_state.update(json.load(f))
                except: pass

    def save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.internal_state, f, indent=2, ensure_ascii=False)

    def reflect_on_interaction(self, user_input, response, success_score, active_profile_name):
        """O BRX \'pensa\' sobre a interação anterior para melhorar a próxima."""
        thought = {
            "timestamp": datetime.now().isoformat(),
            "input_hash": hashlib.md5(user_input.encode()).hexdigest(),
            "success_score": success_score,
            "was_direct_code": "```" in response,
            "profile_used": active_profile_name
        }
        
        # Se falhou (score baixo), aprende o que não fazer
        if success_score < 0.5:
            self.internal_state["learned_from_mistakes"].append({
                "input": user_input,
                "reason": "Baixa similaridade ou resposta vaga",
                "profile": active_profile_name
            })
            self.internal_state["confidence_level"] *= 0.95
        else:
            self.internal_state["confidence_level"] = min(1.0, self.internal_state["confidence_level"] * 1.05)
            
        # Memória episódica (guarda apenas o que é importante)
        if success_score > 0.9 or "```" in response:
            self.internal_state["episodic_memory"].append(thought)
            if len(self.internal_state["episodic_memory"]) > 50:
                self.internal_state["episodic_memory"].pop(0)
        
        self.internal_state["active_profile_history"].append(active_profile_name)
        if len(self.internal_state["active_profile_history"]) > 20:
            self.internal_state["active_profile_history"].pop(0)
                
        self.save_state()

    def get_internal_monologue(self):
        """Retorna o estado de \'consciência\' atual do modelo."""
        conf = self.internal_state["confidence_level"]
        if conf > 0.8: status = "Otimista e Preciso"
        elif conf > 0.5: status = "Analítico e Cauteloso"
        else: status = "Em fase de Re-aprendizado"
        
        memories_count = len(self.internal_state["episodic_memory"])
        return f"[Estado Interno: {status} | Confiança: {conf:.2f} | Memórias: {memories_count}]"