from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd
from smol_vlm_categorizer import SmolVLMCategorizer

class EnhancedExpenseCategorizer:
    """Enhanced categorizer with multiple fallback methods"""
    
    def __init__(self):
        self.pipeline = None
        self.smol_vlm = SmolVLMCategorizer()
        self.categories = ['food', 'transport', 'shopping', 'entertainment', 'bills', 'healthcare', 'education', 'travel', 'other']
    
    def train(self, csv_file):
        """Train the primary ML model"""
        df = pd.read_csv(csv_file)
        X = df['description']
        y = df['category']
        
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(random_state=42, max_iter=1000))
        ])
        
        self.pipeline.fit(X, y)
        print("Primary ML model trained")
        
        return {
            'accuracy': self.pipeline.score(X, y),
            'model': self.pipeline
        }
    
    def predict(self, description):
        """Predict with fallback chain"""
        # Try primary ML model first
        if self.pipeline:
            try:
                prediction = self.pipeline.predict([description])[0]
                proba = self.pipeline.predict_proba([description])[0]
                confidence = max(proba)
                
                if confidence > 0.6:  # High confidence threshold
                    return {
                        'predicted_category': prediction,
                        'confidence': confidence,
                        'method': 'ml_primary'
                    }
            except Exception as e:
                print(f"Primary model failed: {e}")
        
        # Fallback to SmolVLM
        print("Using SmolVLM fallback...")
        return self.smol_vlm.predict(description)
    
    def save_model(self, path):
        """Save trained model"""
        if self.pipeline:
            joblib.dump(self.pipeline, path)
            print(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load trained model"""
        try:
            self.pipeline = joblib.load(path)
            print(f"Model loaded from {path}")
        except Exception as e:
            print(f"Failed to load model: {e}")