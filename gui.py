import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from brx import BRXCore

class BRXApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRX AI - Desktop Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        # Inicializar o núcleo do BRX
        try:
            self.brx = BRXCore()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o cérebro do BRX: {e}")
            self.root.destroy()

        # Layout Principal
        self.setup_ui()

    def setup_ui(self):
        # Painel Lateral (Status e Controles)
        self.side_panel = tk.Frame(self.root, bg="#252526", width=200)
        self.side_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.side_panel, text="BRX AI v5.0", fg="#ffffff", bg="#252526", font=("Arial", 14, "bold")).pack(pady=20)

        # Botões de Status
        self.web_btn = tk.Button(self.side_panel, text="WEB: OFF", command=self.toggle_web, bg="#333333", fg="#ffffff", width=15)
        self.web_btn.pack(pady=5)

        self.train_btn = tk.Button(self.side_panel, text="TREINO: ON", command=self.toggle_train, bg="#333333", fg="#ffffff", width=15)
        self.train_btn.pack(pady=5)

        self.sys_btn = tk.Button(self.side_panel, text="SYS: OFF", command=self.toggle_sys, bg="#333333", fg="#ffffff", width=15)
        self.sys_btn.pack(pady=5)

        tk.Button(self.side_panel, text="Sincronizar GitHub", command=self.sync_github, bg="#007acc", fg="#ffffff", width=15).pack(pady=20)

        # Área de Chat
        self.chat_area = scrolledtext.ScrolledText(self.root, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 11), state='disabled', wrap=tk.WORD)
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Campo de Entrada
        self.input_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(self.input_frame, bg="#3c3c3c", fg="#ffffff", font=("Arial", 12), insertbackground="white")
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(self.input_frame, text="Enviar", command=self.send_message, bg="#007acc", fg="#ffffff", width=10)
        self.send_btn.pack(side=tk.RIGHT)

        self.append_chat("BRX: Olá! Sou o BRX AI. Como posso ajudar com seu Arch Linux hoje?\n")

    def toggle_web(self):
        self.brx.web_search_enabled = not self.brx.web_search_enabled
        self.web_btn.config(text=f"WEB: {'ON' if self.brx.web_search_enabled else 'OFF'}", bg="#007acc" if self.brx.web_search_enabled else "#333333")

    def toggle_train(self):
        self.brx.auto_train_enabled = not self.brx.auto_train_enabled
        self.train_btn.config(text=f"TREINO: {'ON' if self.brx.auto_train_enabled else 'OFF'}", bg="#007acc" if self.brx.auto_train_enabled else "#333333")

    def toggle_sys(self):
        self.brx.system_access_enabled = not self.brx.system_access_enabled
        self.sys_btn.config(text=f"SYS: {'ON' if self.brx.system_access_enabled else 'OFF'}", bg="#007acc" if self.brx.system_access_enabled else "#333333")

    def sync_github(self):
        self.append_chat("\nBRX: Sincronizando com o GitHub...\n")
        threading.Thread(target=self._sync_thread).start()

    def _sync_thread(self):
        result = self.brx.sync_to_github()
        self.root.after(0, lambda: self.append_chat(f"BRX: {result}\n"))

    def send_message(self):
        msg = self.user_input.get().strip()
        if not msg: return
        
        self.user_input.delete(0, tk.END)
        self.append_chat(f"\nVocê: {msg}\n")
        
        # Processar em uma thread separada para não travar a GUI
        threading.Thread(target=self._process_response, args=(msg,)).start()

    def _process_response(self, msg):
        response = self.brx.get_response(msg)
        self.root.after(0, lambda: self.append_chat(f"\nBRX: {response}\n"))

    def append_chat(self, text):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, text)
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = BRXApp(root)
    root.mainloop()
