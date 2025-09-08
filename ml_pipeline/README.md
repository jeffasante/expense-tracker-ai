# Ghana ML Pipeline for Expense Categorization

Advanced machine learning pipeline with SmolVLM-256M-Instruct fallback for Ghana-specific expense categorization.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run training pipeline
python run_pipeline.py
```

## Architecture

```
ml_pipeline/
├── data_generation/          # Ghana-specific data generation
├── enhanced_categorizer.py   # ML model with SmolVLM fallback
├── smol_vlm_categorizer.py  # SmolVLM-256M-Instruct integration
└── run_pipeline.py          # Main training pipeline
```

## Fallback Chain

1. **Primary ML Model** (scikit-learn TF-IDF + Logistic Regression)
2. **SmolVLM-256M-Instruct** (Hugging Face transformer)
3. **Keyword Matching** (Ghana-specific keywords)
4. **Default Fallback** ('other' category)

## Ghana-Specific Features

- **Local Businesses**: Shoprite, Melcom, Papaye, KFC Accra
- **Transport**: Trotro, SHS, VIP, Bolt, GOIL, Shell
- **Food**: Waakye, Kenkey, Banku, Jollof, Chop bars
- **Bills**: ECG, GWCL, Vodafone, MTN, AirtelTigo
- **Healthcare**: Korle Bu, Ridge Hospital, NHIS
- **Education**: Legon, KNUST, UCC

## SmolVLM Integration

Uses HuggingFace's SmolVLM-256M-Instruct as intelligent fallback:
- 256M parameters (lightweight)
- Instruction-tuned for better categorization
- GPU acceleration when available
- Graceful CPU fallback

## Training Data

- **3000+ Ghana-specific samples**
- **Real merchant names and locations**
- **Local currency context (GHS)**
- **Cultural expense patterns**

## Django Integration

The ML pipeline integrates with the main Django app through:
- `backend/ai/models/ml_enhanced_categorizer.py`
- Automatic model loading
- Graceful fallback handling
- Production-ready error handling