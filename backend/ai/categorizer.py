import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle
import os

class ExpenseCategorizer:
    def __init__(self):
        self.model = None
        self.categories = {
            'food': ['restaurant', 'cafe', 'grocery', 'food', 'dining', 'lunch', 'dinner', 'breakfast', 'pizza', 'burger'],
            'transport': ['uber', 'taxi', 'bus', 'train', 'gas', 'fuel', 'parking', 'metro', 'subway'],
            'shopping': ['amazon', 'store', 'mall', 'shop', 'clothing', 'electronics', 'purchase'],
            'entertainment': ['movie', 'cinema', 'game', 'concert', 'music', 'netflix', 'spotify'],
            'bills': ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'insurance'],
            'healthcare': ['doctor', 'hospital', 'pharmacy', 'medical', 'dentist', 'clinic'],
            'education': ['school', 'university', 'course', 'book', 'tuition', 'education'],
            'travel': ['hotel', 'flight', 'vacation', 'trip', 'airbnb', 'booking'],
        }
        self._build_model()

    def _build_model(self):
        # Simple rule-based + ML hybrid approach
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', LogisticRegression(random_state=42))
        ])

    def _rule_based_predict(self, description):
        description_lower = description.lower()
        for category, keywords in self.categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category, 0.8
        return None, 0.0

    def predict(self, description):
        # First try rule-based approach
        category, confidence = self._rule_based_predict(description)
        if category:
            return {
                'predicted_category': category,
                'confidence': confidence,
                'method': 'rule_based'
            }
        
        # Fallback to 'other' category
        return {
            'predicted_category': 'other',
            'confidence': 0.5,
            'method': 'fallback'
        }