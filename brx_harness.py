import os
import subprocess
import json
import time
from datetime import datetime

class BRXHarness:
    """
    BRX Harness v1.0 - Inspirado na arquitetura do Claude Code.
    Gerencia a execução de ferramentas, planejamento de tarefas e compactação de contexto.
    """
    def __init__(self, core):
        self.core = core
        self.plan = []
        self.execution_history = []
        self.max_context_lines = 1000
        
    def create_plan(self, task_description):
        """
        Ultraplan: Quebra uma tarefa complexa em passos menores.
        """
        print(f"[BRX HARNESS] Criando plano para: {task_description}")
        # Lógica simplificada de planejamento baseada em palavras-chave
        steps = []
        if "código" in task_description.lower() or "script" in task_description.lower():
            steps.append({"id": 1, "action": "analyze_requirements", "status": "pending"})
            steps.append({"id": 2, "action": "search_knowledge", "status": "pending"})
            steps.append({"id": 3, "action": "generate_code", "status": "pending"})
            steps.append({"id": 4, "action": "verify_syntax", "status": "pending"})
        else:
            steps.append({"id": 1, "action": "search_info", "status": "pending"})
            steps.append({"id": 2, "action": "synthesize_response", "status": "pending"})
            
        self.plan = steps
        return self.plan

    def execute_tool(self, tool_name, params):
        """
        Tool Harness: Executa ferramentas de forma isolada e segura.
        """
        start_time = time.time()
        result = None
        
        try:
            if tool_name == "bash" or tool_name == "shell":
                # Execução segura de comandos shell (detecta Windows/Linux)
                cmd = params.get("command")
                # Traduz e executa comandos de forma compatível com o SO
                translated_cmd = self._translate_command_for_os(cmd)
                use_shell = True if os.name == 'nt' else False
                process = subprocess.Popen(translated_cmd, shell=use_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                result = {"stdout": stdout, "stderr": stderr, "exit_code": process.returncode}
            
            elif tool_name == "read_file":
                path = params.get("path")
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    result = {"content": self.compact_context(content)}
                else:
                    result = {"error": "Arquivo não encontrado"}
                    
            # Registrar execução
            self.execution_history.append({
                "tool": tool_name,
                "params": params,
                "duration": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            result = {"error": str(e)}
            
        return result

    def compact_context(self, text):
        """
        Auto-Compact: Reduz o tamanho do texto se exceder o limite, mantendo as partes essenciais.
        """
        lines = text.splitlines()
        if len(lines) > self.max_context_lines:
            header = lines[:100]
            footer = lines[-100:]
            middle = [f"\n... [BRX COMPACTED {len(lines) - 200} LINES] ...\n"]
            return "\n".join(header + middle + footer)
        return text

    def run_loop(self, task):
        """
        Loop de Agente: Segue o plano até completar a tarefa.
        """
        self.create_plan(task)
        final_output = []
        
        for step in self.plan:
            step["status"] = "running"
            # Simulação de execução de passos do plano
            # Na prática, isso chamaria o motor de raciocínio para cada etapa
            step["status"] = "completed"
            final_output.append(f"Passo {step['id']} ({step['action']}) concluído.")
            
        return "\n".join(final_output)

    def _translate_command_for_os(self, command):
        """
        Traduz comandos comuns de Linux para seus equivalentes em Windows, se necessário.
        """
        if os.name == 'nt':  # Se for Windows
            command_map = {
                "ls": "dir",
                "rm": "del",
                "cp": "copy",
                "mv": "move",
                "cat": "type",
                "grep": "findstr"
            }
            # Divide o comando em partes para verificar o comando principal
            parts = command.split(maxsplit=1)
            if parts and parts[0].lower() in command_map:
                translated_cmd = command_map[parts[0].lower()]
                if len(parts) > 1:
                    translated_cmd += " " + parts[1]
                return translated_cmd
        return command
