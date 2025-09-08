import random
import csv
import pandas as pd
import os

class GhanaExpenseDataGenerator:
    """Generate Ghana-specific training data for expense categorization"""
    
    GHANA_CATEGORIES = {
        'food': [
            'waakye', 'kenkey', 'banku', 'jollof', 'fufu', 'chop bar', 'papaye', 
            'kfc accra', 'shoprite food', 'melcom snacks', 'local restaurant'
        ],
        'transport': [
            'trotro fare', 'bolt ride', 'uber accra', 'shs bus', 'vip transport',
            'goil fuel', 'shell petrol', 'total fuel', 'taxi fare', 'metro mass'
        ],
        'shopping': [
            'shoprite', 'melcom', 'game stores', 'palace shopping', 'accra mall',
            'west hills mall', 'makola market', 'kaneshie market', 'clothing'
        ],
        'entertainment': [
            'silverbird cinema', 'dstv subscription', 'gotv payment', 'netflix',
            'spotify premium', 'concert ticket', 'movie night'
        ],
        'bills': [
            'ecg bill', 'gwcl water', 'vodafone airtime', 'mtn mobile money',
            'airteltigo data', 'rent payment', 'insurance premium'
        ],
        'healthcare': [
            'korle bu hospital', 'ridge hospital', 'pharmacy', 'nhis payment',
            'doctor consultation', 'medical checkup', 'clinic visit'
        ],
        'education': [
            'legon fees', 'knust tuition', 'ucc payment', 'school fees',
            'textbook purchase', 'stationery', 'library fine'
        ],
        'travel': [
            'kotoka airport', 'flight to kumasi', 'hotel booking', 'cape coast trip',
            'tamale travel', 'vacation expenses', 'transport fare'
        ]
    }
    
    def generate_training_data(self, num_samples=5000, output_file='ghana_expenses.csv'):
        """Generate Ghana-specific expense descriptions"""
        data = []
        
        for _ in range(num_samples):
            category = random.choice(list(self.GHANA_CATEGORIES.keys()))
            base_desc = random.choice(self.GHANA_CATEGORIES[category])
            
            # Add variations
            variations = [
                f"{base_desc}",
                f"{base_desc} payment",
                f"paid for {base_desc}",
                f"{base_desc} - GH₵{random.randint(10, 500)}",
                f"monthly {base_desc}",
            ]
            
            description = random.choice(variations)
            
            data.append({
                'description': description,
                'category': category
            })
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Generated {len(data)} Ghana-specific samples")
        return output_file