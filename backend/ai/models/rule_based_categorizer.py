from typing import Dict, Any
from ..interfaces.categorizer import CategorizerInterface

class RuleBasedCategorizer(CategorizerInterface):
    """Rule-based expense categorizer using keyword matching"""
    
    CATEGORIES = {
        'food': ['restaurant', 'chop bar', 'waakye', 'kenkey', 'banku', 'jollof', 'kfc', 'papaye', 'food', 'dining', 'lunch', 'dinner', 'breakfast', 'pizza', 'burger', 'mcdonald', 'shoprite', 'melcom'],
        'transport': ['uber', 'bolt', 'taxi', 'trotro', 'bus', 'shs', 'vip', 'fuel', 'petrol', 'goil', 'shell', 'total', 'parking', 'transport'],
        'shopping': ['shoprite', 'melcom', 'game', 'palace', 'accra mall', 'west hills mall', 'store', 'mall', 'shop', 'clothing', 'electronics', 'purchase', 'market', 'makola'],
        'entertainment': ['silverbird', 'movie', 'cinema', 'game', 'concert', 'music', 'netflix', 'spotify', 'dstv', 'gotv', 'theater'],
        'bills': ['ecg', 'gwcl', 'vodafone', 'mtn', 'airteltigo', 'internet', 'phone', 'rent', 'insurance', 'utility', 'electric', 'water'],
        'healthcare': ['doctor', 'hospital', 'korle bu', 'ridge hospital', 'pharmacy', 'medical', 'dentist', 'clinic', 'nhis'],
        'education': ['university', 'legon', 'knust', 'ucc', 'school', 'course', 'book', 'tuition', 'education', 'library'],
        'travel': ['hotel', 'flight', 'kotoka', 'vacation', 'trip', 'booking', 'airline', 'kumasi', 'tamale', 'cape coast'],
    }
    
    def predict(self, description: str) -> Dict[str, Any]:
        """Predict category using keyword matching"""
        description_lower = description.lower()
        
        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return {
                        'predicted_category': category,
                        'confidence': 0.85,
                        'method': 'rule_based',
                        'matched_keyword': keyword
                    }
        
        return {
            'predicted_category': 'other',
            'confidence': 0.3,
            'method': 'fallback',
            'matched_keyword': None
        }
    
    def get_supported_categories(self) -> list:
        """Return list of supported categories"""
        return list(self.CATEGORIES.keys()) + ['other']