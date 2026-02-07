"""
Model loader and initialization.
Loads and initializes all ML models at startup.
"""

import logging
from app.ml.skill_extractor import load_nlp_model

logger = logging.getLogger(__name__)

_models_loaded = False


def load_models():
    """
    Load all ML models.
    Called during application startup.
    """
    global _models_loaded
    
    if _models_loaded:
        logger.info("Models already loaded")
        return
    
    try:
        # Load spaCy NLP model
        logger.info("Loading NLP model...")
        load_nlp_model()
        
        # Additional models would be loaded here
        # e.g., career prediction model, skill classifier, etc.
        
        _models_loaded = True
        logger.info("All models loaded successfully")
        
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise


def models_ready() -> bool:
    """Check if models are loaded and ready."""
    return _models_loaded
