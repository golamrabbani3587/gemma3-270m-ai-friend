# improved_fine_tune.py
import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import os

# Check if we're on Apple Silicon
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✅ Using Apple Silicon GPU (MPS)")
else:
    device = torch.device("cpu")
    print("⚠️  Using CPU")

# 1. Load expanded dataset
def load_dataset(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Use the expanded dataset
dataset = load_dataset('./training_data/expanded_train.json')
texts = [item['text'] for item in dataset]

print(f"Loaded {len(texts)} training examples")

# 2. Load model and tokenizer
model_id = "google/gemma-3-270m-it"
print(f"Loading model: {model_id}")

tokenizer = AutoTokenizer.from_pretrained(model_id, token=True)
tokenizer.pad_token = tokenizer.eos_token

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float32,
    token=True
)

# 3. Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples, truncation=True, padding=True, max_length=512)

# Tokenize our texts
encodings = tokenize_function(texts)

# Convert to torch dataset
class ChatDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings
        
    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
    
    def __len__(self):
        return len(self.encodings['input_ids'])

train_dataset = ChatDataset(encodings)

# 4. Set up LoRA with better parameters
peft_config = LoraConfig(
    lora_alpha=32,  # Increased from 16
    lora_dropout=0.1,
    r=16,  # Increased from 8
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]  # Added more modules
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# 5. Training arguments with better parameters
training_args = TrainingArguments(
    output_dir="./model_checkpoints",
    num_train_epochs=5,  # Increased from 3
    per_device_train_batch_size=2,
    warmup_steps=50,
    logging_steps=5,
    save_steps=50,
    learning_rate=5e-4,  # Slightly increased
    weight_decay=0.01,
    fp16=False,
    bf16=False,
    dataloader_pin_memory=False,
    gradient_accumulation_steps=4,  # Added gradient accumulation
    save_total_limit=3,  # Keep only 3 checkpoints
    remove_unused_columns=False,
)

# 6. Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

# 7. Train the model
print("Starting training...")
trainer.train()

# 8. Save the model
print("Saving model...")
trainer.save_model("./trained_model")

print("Training completed! Model saved to ./trained_model")
