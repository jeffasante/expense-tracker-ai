from django.test import TestCase
from ai.models.rule_based_categorizer import RuleBasedCategorizer
from ai.models.ml_categorizer import MLCategorizer
from ai.services.categorization_service import CategorizationService
import numpy as np

class DeterministicAITestCase(TestCase):
    """Ensure AI predictions are deterministic for testing"""
    
    def setUp(self):
        # Fix random seeds for deterministic results
        np.random.seed(42)
    
    def test_rule_based_deterministic(self):
        """Rule-based categorizer should always return same results"""
        categorizer = RuleBasedCategorizer()
        
        # Test same input multiple times
        results = []
        for _ in range(5):
            result = categorizer.predict('McDonald\'s lunch')
            results.append(result)
        
        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result['predicted_category'], first_result['predicted_category'])
            self.assertEqual(result['confidence'], first_result['confidence'])
            self.assertEqual(result['method'], first_result['method'])
    
    def test_keyword_matching_deterministic(self):
        """Test specific keyword matches are deterministic"""
        categorizer = RuleBasedCategorizer()
        
        test_cases = [
            ('uber ride', 'transport'),
            ('pizza dinner', 'food'),
            ('amazon purchase', 'shopping'),
            ('netflix subscription', 'entertainment'),
            ('doctor visit', 'healthcare'),
            ('random xyz expense', 'other')
        ]
        
        for description, expected_category in test_cases:
            result = categorizer.predict(description)
            self.assertEqual(result['predicted_category'], expected_category)
    
    def test_ml_categorizer_deterministic(self):
        """ML categorizer should be deterministic with fixed seed"""
        categorizer = MLCategorizer()
        
        # Test multiple predictions
        results = []
        for _ in range(3):
            result = categorizer.predict('test expense')
            results.append(result)
        
        # Should return consistent results
        for result in results:
            self.assertEqual(result['predicted_category'], 'other')
            self.assertEqual(result['method'], 'ml_model')
    
    def test_service_layer_deterministic(self):
        """Service layer should maintain deterministic behavior"""
        service = CategorizationService()
        
        # Test with rule-based categorizer
        result1 = service.categorize('Starbucks coffee')
        result2 = service.categorize('Starbucks coffee')
        
        self.assertEqual(result1['predicted_category'], result2['predicted_category'])
        self.assertEqual(result1['confidence'], result2['confidence'])
    
    def test_confidence_scores_consistent(self):
        """Confidence scores should be consistent"""
        categorizer = RuleBasedCategorizer()
        
        # Test confidence for matched keywords
        result = categorizer.predict('restaurant dinner')
        self.assertEqual(result['confidence'], 0.85)
        
        # Test confidence for fallback
        result = categorizer.predict('unknown expense xyz')
        self.assertEqual(result['confidence'], 0.3)