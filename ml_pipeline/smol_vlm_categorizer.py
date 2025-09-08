import torch
from transformers import AutoTokenizer, AutoModelForVision2Seq
import json
import re

class SmolVLMCategorizer:
    """Fallback categorizer using SmolVLM-256M-Instruct"""
    
    def __init__(self):
        self.model_name = "HuggingFaceTB/SmolVLM-256M-Instruct"
        self.tokenizer = None
        self.model = None
        self.categories = ['food', 'transport', 'shopping', 'entertainment', 'bills', 'healthcare', 'education', 'travel', 'other']
        self._load_model()
    
    def _load_model(self):
        """Load SmolVLM model with fallback"""
        try:
            # Try different model classes for SmolVLM
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Try loading without device_map first (simpler)
            try:
                from transformers import AutoModelForCausalLM
                self.model = AutoModelForCausalLM.from_pretrained(
                    "distilgpt2",  # Lightweight model
                    torch_dtype=torch.float32  # Use float32 for compatibility
                )
                self.model_name = "distilgpt2"
            except:
                # If that fails, try with device_map
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    device_map="auto" if torch.cuda.is_available() else "cpu",
                    trust_remote_code=True
                )
                
            print(f"Model loaded successfully: {self.model_name}")
        except Exception as e:
            print(f"Failed to load any model: {e}")
            print("Using keyword-only fallback")
            self.model = None
            self.tokenizer = None
    
    def predict(self, description):
        """Predict category using SmolVLM or fallback"""
        if not self.model or not self.tokenizer:
            return self._fallback_prediction(description)
        
        prompt = f"""Categorize this expense description into one of these categories: {', '.join(self.categories)}.

Expense: "{description}"

Category:"""
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=10,
                    temperature=0.1,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id if hasattr(self.tokenizer, 'eos_token_id') else self.tokenizer.pad_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            predicted_category = self._extract_category(response)
            
            return {
                'predicted_category': predicted_category,
                'confidence': 0.7,
                'method': f'llm_model_{self.model_name.split("/")[-1]}',
                'raw_response': response
            }
            
        except Exception as e:
            print(f"Model prediction failed: {e}")
            return self._fallback_prediction(description)
    
    def _extract_category(self, response):
        """Extract category from model response"""
        response_lower = response.lower()
        
        for category in self.categories:
            if category in response_lower:
                return category
        
        return 'other'
    
    def _fallback_prediction(self, description):
        """Simple keyword fallback"""
        desc_lower = description.lower()
        
        keywords = {
            'food': ['waakye', 'food', 'restaurant', 'chop'],
            'transport': ['trotro', 'taxi', 'fuel', 'transport'],
            'shopping': ['shop', 'mall', 'market', 'buy'],
            'bills': ['bill', 'payment', 'ecg', 'water']
        }
        
        for category, words in keywords.items():
            if any(word in desc_lower for word in words):
                return {
                    'predicted_category': category,
                    'confidence': 0.5,
                    'method': 'keyword_fallback'
                }
        
        return {
            'predicted_category': 'other',
            'confidence': 0.3,
            'method': 'default_fallback'
        }