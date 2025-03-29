# GEN-Models: Fine-Tuned GPT-Neo for Text Summarization

![GitHub Repo](https://img.shields.io/github/stars/Auth0r-C0dez/GEN-Models?style=social) 

🚀 **GEN-Models** is a repository showcasing fine-tuned **GPT-Neo** models for **abstractive text summarization** using the **CNN/DailyMail dataset**. The project involves training, evaluating, and optimizing GPT-Neo for improved text generation, leveraging **ROUGE scoring** for performance assessment.

## 🔥 Features
- **Fine-tuned GPT-Neo model** on news articles.
- **Abstractive summarization** for generating concise and meaningful summaries.
- **ROUGE metric evaluation** for accuracy assessment.
- **Optimized generation** using beam search, top-k sampling, and temperature scaling.
- **Visualization of results** using Matplotlib.

## 📂 Dataset
This model is trained on the **CNN/DailyMail dataset**, which contains long-form news articles and human-written highlights for summarization. The dataset is loaded using:
```python
from datasets import load_dataset
dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:1%]")  # 1% for quick testing
```

## 🛠️ Installation
To use this project, install the dependencies:
```bash
pip install transformers datasets torch evaluate rouge_score matplotlib
```

## 🚀 Fine-Tuning the Model
The model is fine-tuned using Hugging Face's `Trainer` with the following configuration:
```python
from transformers import Trainer, TrainingArguments
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    evaluation_strategy="steps",
    save_steps=500,
    num_train_epochs=3,
    logging_dir="./logs",
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset_test,
)
trainer.train()
```

## 🎯 Model Evaluation
The model’s summarization quality is assessed using **ROUGE metrics**:
```python
import evaluate
rouge = evaluate.load("rouge")
results = rouge.compute(predictions=generated_summaries, references=reference_summaries)
print("ROUGE scores:", results)
```

## 📊 Results
The ROUGE scores are visualized using Matplotlib:
```python
import matplotlib.pyplot as plt
scores = [results[key] * 100 for key in ["rouge1", "rouge2", "rougeL"]]
plt.bar(["ROUGE-1", "ROUGE-2", "ROUGE-L"], scores, color=["blue", "green", "red"])
plt.xlabel("Metric")
plt.ylabel("Score (%)")
plt.title("ROUGE Scores for Summarization Model")
plt.show()
```

## ⚡ Inference: Using the Fine-Tuned Model
To generate a summary using the fine-tuned model:
```python
prompt = "summarize: " + article_text
inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
output_tokens = model.generate(**inputs, max_length=150)
summary = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
print("Generated Summary:", summary)
```

## 📝 To-Do
- [ ] Experiment with larger datasets
- [ ] Fine-tune on custom datasets
- [ ] Deploy as an API

## 📜 License
This project is licensed under the **MIT License**. Feel free to contribute and improve the repository!

---
🚀 **Follow for more AI projects!**

🔗 GitHub Repo: [GEN-Models](https://github.com/Auth0r-C0dez/GEN-Models)  

