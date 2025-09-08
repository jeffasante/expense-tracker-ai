from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np
from ..interfaces.categorizer import CategorizerInterface

class MLCategorizer(CategorizerInterface):
    """ML-based categorizer using scikit-learn (example for future enhancement)"""
    
    def __init__(self, random_seed=42):
        # Fix random seed for deterministic testing
        np.random.seed(random_seed)
        self.random_seed = random_seed
        self.pipeline = None
        self.categories = ['food', 'transport', 'shopping', 'entertainment', 'bills', 'healthcare', 'education', 'travel', 'other']
        self._build_model()
    
    def _build_model(self):
        """Build ML pipeline (placeholder - would need training data)"""
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', LogisticRegression(random_state=self.random_seed))
        ])
    
    def predict(self, description: str) -> Dict[str, Any]:
        """Predict using ML model (fallback to rule-based for now)"""
        # For demo purposes, return a mock ML prediction
        # In production, this would use trained model
        return {
            'predicted_category': 'other',
            'confidence': 0.6,
            'method': 'ml_model',
            'model_type': 'logistic_regression'
        }
    
    def get_supported_categories(self) -> list:
        """Return supported categories"""
        return self.categories