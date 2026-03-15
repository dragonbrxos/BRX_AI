from brx import BRXCore
import uuid

def seed():
    brx = BRXCore()
    
    # Adicionar conhecimento sobre o próprio BRX
    brx.add_knowledge(
        block_id=str(uuid.uuid4()),
        text="O BRX é um modelo de IA extremamente leve, projetado para rodar nativamente no Arch Linux. Ele utiliza arquivos JSON para armazenar seu conhecimento, o que o torna eficiente e fácil de manter em notebooks e sistemas com recursos limitados.",
        category="general",
        keywords=["brx", "ia", "modelo", "leve", "arch", "linux", "json", "notebook"],
        title="O que é o BRX?",
        topic="introdução ao brx",
        source="documentação oficial"
    )

    # Adicionar conhecimento sobre Arch Linux
    brx.add_knowledge(
        block_id=str(uuid.uuid4()),
        text="Arch Linux é uma distribuição Linux leve e flexível que segue o princípio KISS (Keep It Simple, Stupid). É conhecida por seu sistema de gerenciamento de pacotes pacman e pelo Arch User Repository (AUR).",
        category="tech",
        keywords=["arch", "linux", "kiss", "pacman", "aur", "distribuição"],
        title="Sobre o Arch Linux",
        topic="sistemas operacionais",
        source="arch wiki"
    )

    # Adicionar conhecimento sobre Python
    brx.add_knowledge(
        block_id=str(uuid.uuid4()),
        text="Python é uma linguagem de programação de alto nível, interpretada e de propósito geral. É amplamente utilizada em ciência de dados, inteligência artificial e automação devido à sua sintaxe clara e vasta biblioteca padrão.",
        category="code",
        keywords=["python", "programação", "linguagem", "ia", "automação"],
        title="Linguagem Python",
        topic="programação",
        source="python.org"
    )

    print("Cérebro inicial do BRX populado com sucesso!")

if __name__ == "__main__":
    seed()
