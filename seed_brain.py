from brx import BRXCore
import uuid

def seed():
    print("[+] Populando cérebro inicial do BRX AI...")
    brx = BRXCore()
    
    # Adicionar conhecimento sobre o próprio BRX
    brx.add_knowledge(
        key=str(uuid.uuid4()),
        data={
            "id": str(uuid.uuid4()),
            "texto": "O BRX é um modelo de IA extremamente leve, projetado para rodar nativamente no Arch Linux. Ele utiliza arquivos JSON para armazenar seu conhecimento, o que o torna eficiente e fácil de manter em notebooks e sistemas com recursos limitados.",
            "categoria": "general",
            "palavras": ["brx", "ia", "modelo", "leve", "arch", "linux", "json", "notebook"],
            "titulo": "O que é o BRX?",
            "topico": "introdução ao brx"
        }
    )

    # Adicionar conhecimento sobre Arch Linux
    brx.add_knowledge(
        key=str(uuid.uuid4()),
        data={
            "id": str(uuid.uuid4()),
            "texto": "Arch Linux é uma distribuição Linux leve e flexível que segue o princípio KISS (Keep It Simple, Stupid). É conhecida por seu sistema de gerenciamento de pacotes pacman e pelo Arch User Repository (AUR).",
            "categoria": "arch_linux",
            "palavras": ["arch", "linux", "kiss", "pacman", "aur", "distribuição"],
            "titulo": "Sobre o Arch Linux",
            "topico": "sistemas operacionais"
        }
    )

    # Adicionar conhecimento sobre Programação Lua
    brx.add_knowledge(
        key=str(uuid.uuid4()),
        data={
            "id": str(uuid.uuid4()),
            "texto": "Exemplo de código Lua:\n\nprint('Olá Mundo!')\n\n-- Variáveis e Funções\nlocal nome = 'BRX'\nfunction saudar(n)\n  print('Olá ' .. n)\nend\nsaudar(nome)",
            "categoria": "programming",
            "palavras": ["lua", "código", "script", "programar"],
            "titulo": "Linguagem Lua",
            "topico": "programação"
        }
    )

    print("[OK] Cérebro inicial populado com sucesso!")

if __name__ == "__main__":
    seed()
