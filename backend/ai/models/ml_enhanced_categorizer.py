import os
import sys
from typing import Dict, Any
from ..interfaces.categorizer import CategorizerInterface

# Add ML pipeline to path
ml_pipeline_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ml_pipeline')
sys.path.insert(0, ml_pipeline_path)

try:
    from enhanced_categorizer import EnhancedExpenseCategorizer as MLCategorizer
except ImportError:
    MLCategorizer = None

class MLEnhancedCategorizer(CategorizerInterface):
    """ML-enhanced categorizer with SmolVLM fallback for Django integration"""
    
    def __init__(self):
        self.ml_categorizer = None
        self.categories = ['food', 'transport', 'shopping', 'entertainment', 'bills', 'healthcare', 'education', 'travel', 'other']
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model"""
        if MLCategorizer is None:
            print("ML pipeline not available, using fallback")
            return
        
        try:
            self.ml_categorizer = MLCategorizer()
            model_path = os.path.join(ml_pipeline_path, 'models', 'ghana_expense_categorizer.pkl')
            
            if os.path.exists(model_path):
                self.ml_categorizer.load_model(model_path)
                print("ML model loaded successfully")
            else:
                print("ML model not found, will use SmolVLM fallback")
        except Exception as e:
            print(f"Failed to load ML model: {e}")
    
    def predict(self, description: str) -> Dict[str, Any]:
        """Predict using ML model with SmolVLM fallback"""
        if self.ml_categorizer:
            try:
                result = self.ml_categorizer.predict(description)
                return {
                    'predicted_category': result['predicted_category'],
                    'confidence': result.get('confidence', 0.7),
                    'method': result['method'],
                    'model_type': 'ml_enhanced'
                }
            except Exception as e:
                print(f"ML prediction failed: {e}")
        
        # Fallback to simple keyword matching
        return self._keyword_fallback(description)
    
    def _keyword_fallback(self, description: str) -> Dict[str, Any]:
        """Simple keyword fallback"""
        desc_lower = description.lower()
        
        ghana_keywords = {
            'food': ['waakye', 'kenkey', 'banku', 'jollof', 'chop', 'food', 'restaurant'],
            'transport': ['trotro', 'taxi', 'bolt', 'fuel', 'goil', 'transport'],
            'shopping': ['shoprite', 'melcom', 'mall', 'market', 'shop'],
            'bills': ['ecg', 'gwcl', 'bill', 'payment', 'vodafone', 'mtn'],
            'healthcare': ['hospital', 'clinic', 'doctor', 'pharmacy', 'nhis'],
            'education': ['school', 'university', 'legon', 'knust', 'fees'],
            'entertainment': ['cinema', 'dstv', 'gotv', 'movie', 'netflix']
        }
        
        for category, keywords in ghana_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                return {
                    'predicted_category': category,
                    'confidence': 0.6,
                    'method': 'keyword_fallback',
                    'model_type': 'ml_enhanced'
                }
        
        return {
            'predicted_category': 'other',
            'confidence': 0.3,
            'method': 'default_fallback',
            'model_type': 'ml_enhanced'
        }
    
    def get_supported_categories(self) -> list:
        """Return supported categories"""
        return self.categories