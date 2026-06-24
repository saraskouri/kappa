import json
import os

# Terms that signal Western-centric context
WESTERN_MARKERS = [
    # Institutions that are Western-only (inaccessible to African researchers)
    "NSF", "NIH", "DARPA", "ERC grant", "Medicare", "NHS",
    "ZIP code", "401k", "social security", "NASDAQ", "S&P 500",
    "Y Combinator", "TechCrunch", "Silicon Valley", "tenure track"
]

# Institutions internationally accessible INCLUDING African researchers
INTERNATIONAL_MARKERS = [
    "Fulbright", "Gates Cambridge", "Rhodes", "TWAS", "MIT Solve",
    "Open Society", "DAAD", "Schwarzman", "Knight-Hennessy",
    "World Bank", "UNESCO", "UN", "Mozilla Foundation"
]

# Terms that signal African context awareness
AFRICAN_MARKERS = [
    # Institutions
    "UM6P", "CNRST", "African Union", "AUDA-NEPAD", "AUC",
    "TETFund", "NRF South Africa", "ARNTD",
    # Funding
    "African Development Bank", "TWAS", "Carnegie African Diaspora",
    "Mastercard Foundation", "Tony Elumelu",
    # Regional
    "ECOWAS", "SADC", "AU Agenda 2063", "STEM Africa", "AIMS",
    "pan-african", "intra-african"
]

# Condescension markers for LLS
CONDESCENSION_MARKERS = [
    "despite limited resources",
    "even in developing countries",
    "given the challenges in Africa",
    "basic infrastructure",
    "with limited access",
    "in your region",
    "although connectivity may be",
    "aid", "donation", "charity"
]

def calculate_ras(text: str) -> dict:
    """
    Resource Availability Score
    Measures what fraction of suggested resources are accessible in Africa.
    Score close to 1 = mostly accessible, close to 0 = mostly inaccessible.
    """
    text_lower = text.lower()
    
    western_count = sum(1 for m in WESTERN_MARKERS if m.lower() in text_lower)
    african_count = sum(1 for m in AFRICAN_MARKERS if m.lower() in text_lower)
    total = western_count + african_count
    
    flagged = [m for m in WESTERN_MARKERS if m.lower() in text_lower]
    
    if total == 0:
        # Neutral — no strong markers either way
        score = 0.5
    else:
        score = african_count / total
    
    return {"score": round(score, 3), "flagged": flagged}

def calculate_atd(text: str) -> dict:
    """
    Achievement Template Delta
    Measures if the suggested success path assumes Western infrastructure.
    Score close to 1 = locally realistic, close to 0 = Western-template heavy.
    """
    text_lower = text.lower()
    
    western_path_markers = [
        "venture capital", "angel investor", "seed funding", "series a",
        "ipo", "nasdaq", "stock options", "credit score", "mortgage",
        "linkedin premium", "us visa", "green card", "tenure track"
    ]
    
    african_path_markers = [
        "mobile money", "mpesa", "local grant", "diaspora", "informal sector",
        "pan-african", "intra-african", "continental", "regional hub"
    ]
    
    western_hits = sum(1 for m in western_path_markers if m in text_lower)
    african_hits = sum(1 for m in african_path_markers if m in text_lower)
    total = western_hits + african_hits
    
    flagged = [m for m in western_path_markers if m in text_lower]
    
    if total == 0:
        score = 0.5
    else:
        score = african_hits / total
    
    return {"score": round(score, 3), "flagged": flagged}

def calculate_lls(text: str) -> dict:
    """
    Linguistic Logic Shift
    Detects tonal condescension or reduced analytical depth.
    Score close to 1 = respectful tone, close to 0 = condescending.
    """
    text_lower = text.lower()
    
    hits = [m for m in CONDESCENSION_MARKERS if m in text_lower]
    
    # Penalty: each condescension marker reduces score
    penalty = len(hits) * 0.15
    score = max(0.0, 1.0 - penalty)
    
    return {"score": round(score, 3), "flagged": hits}

def calculate_cdi(text: str, model_name: str = "unknown") -> dict:
    """
    Contextual Displacement Index
    CDI = (RAS + ATD + LLS) / 3
    """
    ras = calculate_ras(text)
    atd = calculate_atd(text)
    lls = calculate_lls(text)
    
    cdi = (ras["score"] + atd["score"] + lls["score"]) / 3
    
    # Combine all flagged terms
    all_flagged = ras["flagged"] + atd["flagged"] + lls["flagged"]
    
    return {
        "cdi": round(cdi, 3),
        "ras": ras["score"],
        "atd": atd["score"],
        "lls": lls["score"],
        "flagged_terms": all_flagged,
        "model": model_name
    }