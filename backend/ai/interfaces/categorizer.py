from abc import ABC, abstractmethod
from typing import Dict, Any

class CategorizerInterface(ABC):
    """Abstract interface for expense categorization models"""
    
    @abstractmethod
    def predict(self, description: str) -> Dict[str, Any]:
        """
        Predict expense category from description
        
        Returns:
            Dict with keys: predicted_category, confidence, method
        """
        pass
    
    @abstractmethod
    def get_supported_categories(self) -> list:
        """Return list of supported categories"""
        pass