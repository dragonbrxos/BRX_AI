#!/usr/bin/env python3
"""
LightBRX Complete Example
Demonstrates training, generation, and reasoning
"""

from pathlib import Path
from lightbrx.model import LightBRX

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Initialize Model
# ════════════════════════════════════════════════════════════════════════════

print("="*70)
print("  LightBRX — Complete Example")
print("="*70)

# Create model with minimal footprint (perfect for 4GB RAM)
model = LightBRX(
    vocab_size=4096,           # 4K vocabulary
    embedding_dim=16,          # 16D embeddings (ultra-light)
    max_seq_length=128,        # Max generation length
    model_dir=Path("./lightbrx_model")
)

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Training Data
# ════════════════════════════════════════════════════════════════════════════

training_corpus = [
    # AI & Machine Learning
    "Artificial intelligence is transforming technology and society.",
    "Machine learning allows computers to learn from data without programming.",
    "Deep learning uses neural networks inspired by the human brain.",
    "Neural networks have multiple layers that process information.",
    "Convolutional neural networks excel at image recognition tasks.",
    
    # Data Science
    "Data is the foundation of modern artificial intelligence systems.",
    "Big data requires distributed processing and advanced analytics.",
    "Data visualization helps us understand complex patterns.",
    "Statistical analysis is crucial for data-driven decision making.",
    "Data privacy and security are paramount in the digital age.",
    
    # Programming & Technology
    "Python is a versatile language for data science and AI development.",
    "Open source software drives innovation in technology communities.",
    "Cloud computing provides scalable infrastructure for applications.",
    "APIs enable different software systems to communicate effectively.",
    "Version control with Git is essential for collaborative development.",
    
    # Innovation & Future
    "Quantum computing may revolutionize computational capabilities.",
    "Blockchain technology offers distributed ledger solutions.",
    "Edge computing brings computation closer to data sources.",
    "The Internet of Things connects billions of devices worldwide.",
    "5G networks enable faster communication and real-time applications.",
]

# Expand corpus for better training
training_corpus = training_corpus * 5  # Replicate 5 times

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Train Model
# ════════════════════════════════════════════════════════════════════════════

print("\n[1] TRAINING PHASE")
print("-" * 70)

model.train_on_texts(training_corpus, num_merges=64)

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Generation with Reasoning
# ════════════════════════════════════════════════════════════════════════════

print("\n[2] GENERATION PHASE")
print("-" * 70)

prompts = [
    "Artificial intelligence",
    "Machine learning is",
    "Data science helps",
    "Python programming",
    "The future of technology",
]

for prompt in prompts:
    print(f"\nPrompt: {prompt}")
    output, thinking = model.generate(prompt, max_length=50, thinking=True)
    
    print(f"\nGenerated: {output}")
    
    if thinking:
        print(f"\nReasoning Chain ({len(thinking.thoughts)} steps):")
        for i, thought in enumerate(thinking.thoughts[:4], 1):
            print(f"  [{i}] {thought.kind.upper()}: {thought.content[:70]}")
            if thought.confidence:
                print(f"      Confidence: {thought.confidence:.2f}")

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Evaluation & Improvement
# ════════════════════════════════════════════════════════════════════════════

print("\n[3] EVALUATION & LEARNING PHASE")
print("-" * 70)

test_prompt = "Artificial intelligence is"
test_output = "Artificial intelligence is transforming modern technology through machine learning and deep neural networks"

quality_score = model.evaluate_response(test_prompt, test_output)
print(f"\nTest Prompt: {test_prompt}")
print(f"Test Output: {test_output}")
print(f"Quality Score: {quality_score:.3f} (0-1)")

# Learn from feedback
print(f"\nLearning from quality score...")
model.improve(test_prompt, test_output, quality_score)

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Statistics
# ════════════════════════════════════════════════════════════════════════════

print("\n[4] MODEL STATISTICS")
print("-" * 70)

model.stats()

# ════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Save & Load
# ════════════════════════════════════════════════════════════════════════════

print("\n[5] PERSISTENCE")
print("-" * 70)

print(f"\nModel saved to: {model.model_dir}")
print(f"Files created:")
print(f"  - tokenizer/        (BPE vocabulary)")
print(f"  - embeddings/       (32D vectors)")
print(f"  - generator/        (evolutionary networks)")
print(f"  - metadata.json     (configuration)")

print("\n" + "="*70)
print("✓ Example Complete! LightBRX is running locally on your machine.")
print("="*70)
