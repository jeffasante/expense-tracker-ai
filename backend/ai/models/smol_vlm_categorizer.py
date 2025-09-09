import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re
from ai.interfaces.categorizer import CategorizerInterface

class SmolVLMCategorizer(CategorizerInterface):
    """AI-powered categorizer using DialoGPT-small with enhanced keyword fallback
    
    Originally designed for SmolVLM-256M-Instruct, but uses DialoGPT-small
    as a more compatible alternative with robust keyword-based fallback.
    """
    
    def __init__(self):
        # Use a more compatible model
        self.model_name = "microsoft/DialoGPT-small"  # Fallback to a working model
        self.tokenizer = None
        self.model = None
        self.categories = ['food', 'transport', 'shopping', 'entertainment', 'bills', 'healthcare', 'education', 'travel', 'other']
        self._load_model()
    
    def _load_model(self):
        """Load language model for categorization"""
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map="cpu"
            )
            
            # Set pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print(f"Model loaded successfully: {self.model_name}")
        except Exception as e:
            print(f"Failed to load model {self.model_name}: {e}")
            print("Trying GPT-2 as fallback...")
            try:
                self.model_name = "gpt2"
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                    
                print(f"Fallback model loaded: {self.model_name}")
            except Exception as e2:
                print(f"Fallback loading also failed: {e2}")
                print("Using keyword-only fallback")
                self.model = None
                self.tokenizer = None
    
    def predict(self, description):
        """Predict category using language model or fallback"""
        if not self.model or not self.tokenizer:
            return self._fallback_prediction(description)
        
        # Try multiple prompts to get better results
        prompts = [
            f"Expense: {description}\nCategory: bills",
            f"Expense: {description}\nCategory: food", 
            f"Expense: {description}\nCategory: transport",
            f"Expense: {description}\nCategory: shopping",
            f"Expense: {description}\nCategory: entertainment"
        ]
        
        try:
            best_category = 'other'
            best_score = -float('inf')
            
            for i, prompt in enumerate(prompts):
                category = ['bills', 'food', 'transport', 'shopping', 'entertainment'][i]
                
                inputs = self.tokenizer(prompt, return_tensors="pt", max_length=100, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    # Get the logits for the last token
                    logits = outputs.logits[0, -1, :]
                    score = torch.max(logits).item()
                    
                    if score > best_score:
                        best_score = score
                        best_category = category
            
            # Use enhanced fallback for better accuracy
            fallback_result = self._enhanced_fallback(description)
            if fallback_result['confidence'] > 0.7:
                return {
                    'predicted_category': fallback_result['predicted_category'],
                    'confidence': 0.8,
                    'method': 'enhanced_model_fallback',
                    'raw_response': f'model_enhanced_{fallback_result["predicted_category"]}'
                }
            
            return {
                'predicted_category': best_category,
                'confidence': 0.7,
                'method': 'language_model',
                'raw_response': f'model_selected_{best_category}'
            }
            
        except Exception as e:
            print(f"Model prediction failed: {e}")
            return self._fallback_prediction(description)
    
    def _extract_category(self, response):
        """Extract category from model response"""
        response_lower = response.lower().strip()
        
        # Direct match first
        if response_lower in self.categories:
            return response_lower
            
        # Partial match
        for category in self.categories:
            if category in response_lower:
                return category
        
        return 'other'
    
    def _calculate_confidence(self, response, predicted_category):
        """Calculate confidence based on response quality"""
        response_lower = response.lower().strip()
        
        # High confidence for exact matches
        if response_lower == predicted_category:
            return 0.9
        
        # Medium confidence for partial matches
        if predicted_category in response_lower and len(response_lower) < 20:
            return 0.75
            
        # Lower confidence for longer or unclear responses
        return 0.6
    
    def _enhanced_fallback(self, description):
        """Enhanced keyword-based categorization"""
        desc_lower = description.lower()
        
        # High confidence keywords
        high_confidence_keywords = {
            'bills': ['bill', 'payment', 'ecg', 'electricity', 'water', 'internet', 'mtn', 'vodafone', 'airtel', 'subscription'],
            'food': ['waakye', 'food', 'restaurant', 'chop', 'bar', 'eat', 'lunch', 'dinner', 'breakfast'],
            'transport': ['trotro', 'taxi', 'uber', 'bolt', 'fuel', 'petrol', 'transport', 'fare', 'airport'],
            'shopping': ['shop', 'mall', 'market', 'buy', 'purchase', 'shoprite', 'store'],
            'entertainment': ['movie', 'cinema', 'ticket', 'game', 'entertainment', 'club']
        }
        
        for category, words in high_confidence_keywords.items():
            matches = sum(1 for word in words if word in desc_lower)
            if matches > 0:
                confidence = min(0.9, 0.6 + (matches * 0.1))
                return {
                    'predicted_category': category,
                    'confidence': confidence,
                    'method': 'enhanced_keyword'
                }
        
        return {
            'predicted_category': 'other',
            'confidence': 0.4,
            'method': 'default_enhanced'
        }
    
    def _fallback_prediction(self, description):
        """Simple keyword fallback"""
        return self._enhanced_fallback(description)
    
    def get_supported_categories(self) -> list:
        """Return list of supported categories"""
        return self.categories