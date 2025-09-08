#!/usr/bin/env python
"""
Ghana-specific ML training pipeline with SmolVLM fallback
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from data_generation.ghana_data_generator import GhanaExpenseDataGenerator
from enhanced_categorizer import EnhancedExpenseCategorizer

def main():
    print("Ghana AI Expense Categorizer Training Pipeline")
    print("=" * 60)
    
    # Step 1: Generate Ghana-specific training data
    print("\nStep 1: Generating Ghana training data...")
    generator = GhanaExpenseDataGenerator()
    training_file = generator.generate_training_data(
        num_samples=3000, 
        output_file='data/ghana_expenses.csv'
    )
    
    # Step 2: Train enhanced categorizer
    print("\nStep 2: Training enhanced categorizer...")
    categorizer = EnhancedExpenseCategorizer()
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Train primary model
    results = categorizer.train(training_file)
    print(f"Training accuracy: {results['accuracy']:.4f}")
    
    # Save model
    model_path = 'models/ghana_expense_categorizer.pkl'
    categorizer.save_model(model_path)
    
    # Step 3: Test with Ghana examples
    print("\nStep 3: Testing with Ghana examples...")
    
    test_cases = [
        "Waakye at Auntie Muni chop bar",
        "Trotro fare to Kotoka Airport", 
        "Shopping at Shoprite East Legon",
        "ECG electricity bill payment",
        "Fuel at GOIL filling station",
        "Banku and tilapia at local restaurant",
        "MTN mobile money transfer",
        "DSTV subscription renewal"
    ]
    
    for description in test_cases:
        result = categorizer.predict(description)
        print(f"  '{description}'")
        print(f"    → {result['predicted_category']} ({result['method']}, confidence: {result.get('confidence', 0):.3f})")
    
    # Step 4: Test SmolVLM fallback
    print("\nStep 4: Testing SmolVLM fallback...")
    
    # Simulate primary model failure
    categorizer.pipeline = None
    
    fallback_test = "Kenkey and fish at Circle"
    result = categorizer.predict(fallback_test)
    print(f"  Fallback test: '{fallback_test}'")
    print(f"    → {result['predicted_category']} ({result['method']})")
    
    print("\n" + "=" * 60)
    print("GHANA ML PIPELINE COMPLETED!")
    print("=" * 60)
    print(f"Model saved: {model_path}")
    print(f"Accuracy: {results['accuracy']:.4f}")
    print("SmolVLM fallback ready")
    print("Ghana-specific categories supported")

if __name__ == "__main__":
    main()