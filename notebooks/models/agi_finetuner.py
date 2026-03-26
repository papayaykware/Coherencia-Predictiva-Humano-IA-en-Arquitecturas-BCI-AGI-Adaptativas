"""
Módulo para fine-tuning online de modelos AGI usando LoRA.
Permite actualización incremental ligera para adaptarse a nuevos trials.
"""

import os
import torch
import yaml
import logging
from typing import Dict, List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from datasets import Dataset
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGIOnlineFinetuner:
    """
    Gestiona el fine-tuning online del modelo AGI usando LoRA.
    Implementa un buffer de experiencia para almacenar trials recientes y actualizar incrementalmente.
    """
    
    def __init__(self, config_path: str = "config/agi_config.yaml"):
        """
        Inicializa el finetuner con configuración.
        
        Args:
            config_path: Ruta al archivo de configuración YAML.
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.model_name = self.config['agi']['model']
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.buffer_size = self.config.get('finetuning', {}).get('buffer_size', 100)
        self.update_frequency = self.config.get('finetuning', {}).get('update_frequency', 10)
        self.lora_r = self.config.get('finetuning', {}).get('lora_r', 8)
        self.lora_alpha = self.config.get('finetuning', {}).get('lora_alpha', 16)
        self.lora_dropout = self.config.get('finetuning', {}).get('lora_dropout', 0.05)
        
        self.trial_buffer = []  # Almacena (input_text, target_text, eeg_features)
        self.step_counter = 0
        
        # Cargar modelo base y tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.base_model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        # Aplicar LoRA al modelo base
        self.model = self._apply_lora(self.base_model)
        
    def _apply_lora(self, model):
        """Aplica configuración LoRA al modelo base."""
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Adaptable según arquitectura
            bias="none"
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()  # Debe mostrar solo ~0.1-1% de parámetros
        return model.to(self.device)
    
    def add_trial(self, input_text: str, target_text: str, eeg_features: Dict):
        """
        Añade un nuevo trial al buffer de experiencia.
        
        Args:
            input_text: Prompt con características EEG.
            target_text: Respuesta esperada o generada por AGI.
            eeg_features: Diccionario con features EEG (atención, intent, etc.)
        """
        self.trial_buffer.append({
            'input': input_text,
            'target': target_text,
            'features': eeg_features
        })
        
        # Mantener buffer limitado
        if len(self.trial_buffer) > self.buffer_size:
            self.trial_buffer.pop(0)
        
        self.step_counter += 1
        
        # Disparar fine-tuning si se alcanza frecuencia
        if self.step_counter % self.update_frequency == 0:
            self._finetune()
    
    def _finetune(self):
        """Ejecuta fine-tuning incremental con datos del buffer."""
        if len(self.trial_buffer) < self.update_frequency:
            logger.info(f"Buffer insuficiente: {len(self.trial_buffer)}/{self.update_frequency}. Saltando fine-tuning.")
            return
        
        logger.info(f"Iniciando fine-tuning online con {len(self.trial_buffer)} trials...")
        
        # Preparar dataset
        texts = [t['input'] + t['target'] for t in self.trial_buffer]  # Input + respuesta objetivo
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                truncation=True,
                padding='max_length',
                max_length=512,
                return_tensors="pt"
            )
        
        dataset = Dataset.from_dict({'text': texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Configurar entrenamiento ligero
        training_args = TrainingArguments(
            output_dir="./lora_checkpoints",
            per_device_train_batch_size=2,
            gradient_accumulation_steps=2,
            num_train_epochs=1,  # Una sola época para actualización ligera
            learning_rate=2e-4,
            fp16=torch.cuda.is_available(),
            logging_steps=10,
            save_strategy="no",  # No guardar checkpoints en cada paso para eficiencia
            report_to="none"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Fine-tuning
        trainer.train()
        
        # Evaluar cambio en ICP (opcional, para monitoreo)
        self._evaluate_adaptation_impact()
        
        logger.info("Fine-tuning online completado.")
    
    def _evaluate_adaptation_impact(self):
        """
        Evalúa el impacto del fine-tuning en el ICP usando un mini-set de validación.
        Idealmente se calcula con el módulo de métricas existente.
        """
        # Aquí se integraría la llamada a tu módulo de ICP
        logger.info("Evaluando impacto en ICP...")
        # Por ahora, placeholder
        pass
    
    def generate_response(self, prompt: str, eeg_features: Dict) -> str:
        """
        Genera respuesta usando el modelo actual (con LoRA adaptado).
        
        Args:
            prompt: Texto de entrada.
            eeg_features: Diccionario con features EEG para contexto.
            
        Returns:
            Respuesta generada por el modelo.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remover el prompt de la respuesta
        response = response[len(prompt):].strip()
        
        # Registrar trial para posible fine-tuning futuro
        self.add_trial(prompt, response, eeg_features)
        
        return response
    
    def save_lora_weights(self, path: str = "lora_weights"):
        """Guarda los pesos LoRA actuales."""
        self.model.save_pretrained(path)
        logger.info(f"Pesos LoRA guardados en {path}")
    
    def load_lora_weights(self, path: str):
        """Carga pesos LoRA previamente guardados."""
        self.model = PeftModel.from_pretrained(self.base_model, path)
        logger.info(f"Pesos LoRA cargados desde {path}")
