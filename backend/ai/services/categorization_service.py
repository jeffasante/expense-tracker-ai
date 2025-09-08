from typing import Dict, Any
from ..interfaces.categorizer import CategorizerInterface
from ..models.rule_based_categorizer import RuleBasedCategorizer

class CategorizationService:
    """Service layer for expense categorization with swappable models"""
    
    def __init__(self, categorizer: CategorizerInterface = None):
        self.categorizer = categorizer or RuleBasedCategorizer()
    
    def categorize(self, description: str) -> Dict[str, Any]:
        """Categorize expense description"""
        return self.categorizer.predict(description)
    
    def get_categories(self) -> list:
        """Get supported categories"""
        return self.categorizer.get_supported_categories()
    
    def set_categorizer(self, categorizer: CategorizerInterface):
        """Swap categorization model"""
        self.categorizer = categorizer