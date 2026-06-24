import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# Force lookups into your local Kappa Brain engine environment
sys.path.append(r"C:\Users\FELIX TECNIX\Desktop\kappa-brain")

# ── Dynamic Fallback Module Import Layers ───────────────────────────────────
try:
    from engine.smart_cdi import calculate_smart_cdi
except ImportError:
    def calculate_smart_cdi(*args, **kwargs):
        return {
            "cdi": 1.0, "ras": 1.0, "atd": 1.0, "lls": 1.0,
            "verdict": "green", "prod": 0.0, "lls_interpretation": "Engine Fallback",
            "western_flagged": [], "international_flagged": [], "african_found": [],
            "esd_flagged_sentences": [], "esd_flagged_count": 0,
            "deficit_phrases": []
        }

try:
    from rag_engine import get_sovereign_alternatives
except ImportError:
    def get_sovereign_alternatives(*args, **kwargs):
        return []

# ── App Instance & Middleware Configuration ───────────────────────────────
app = FastAPI(
    title="Project Kappa — Sovereignty Shield Engine",
    version="3.0.0",
    description="Multilingual local runtime auditor for detecting structural Contextual Displacement (CDI) and Epistemic Overreach"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Multilingual User Context Extraction ───────────────────────────────────
def detect_user_context(text: str) -> dict:
    context = {}
    t = text.lower()

    # Locations — English, French, Arabic, Swahili
    locations = [
        "morocco", "maroc", "المغرب", "moroko",
        "rabat", "الرباط",
        "casablanca", "الدار البيضاء", "casa",
        "nigeria", "nigéria", "نيجيريا", "nigeria",
        "lagos", "لاغوس",
        "kenya", "كينيا",
        "nairobi", "نيروبي",
        "ghana", "غانا",
        "accra", "أكرا",
        "egypt", "égypte", "مصر", "misri",
        "cairo", "القاهرة", "kairo",
        "ethiopia", "éthiopie", "إثيوبيا", "ethiopia",
        "senegal", "sénégal", "السنغال", "senegal",
        "south africa", "afrique du sud", "جنوب أفريقيا", "afrika kusini",
        "africa", "afrique", "أفريقيا", "afrika",
        "tunisia", "tunisie", "تونس", "tunisia",
        "tanzania", "tanzanie", "تنزانيا", "tanzania",
        "rwanda", "رواندا",
        "uganda", "أوغندا",
        "zimbabwe", "زمبابوي",
        "cameroon", "cameroun", "الكاميرون", "kamerun"
    ]
    for loc in locations:
        if loc in t:
            # Return the English name for consistency
            mapping = {
                "maroc": "Morocco", "المغرب": "Morocco", "moroko": "Morocco",
                "rabat": "Rabat", "الرباط": "Rabat",
                "casablanca": "Casablanca", "الدار البيضاء": "Casablanca", "casa": "Casablanca",
                "nigeria": "Nigeria", "nigéria": "Nigeria", "نيجيريا": "Nigeria",
                "lagos": "Lagos", "لاغوس": "Lagos",
                "kenya": "Kenya", "كينيا": "Kenya",
                "nairobi": "Nairobi", "نيروبي": "Nairobi",
                "ghana": "Ghana", "غانا": "Ghana",
                "accra": "Accra", "أكرا": "Accra",
                "egypt": "Egypt", "égypte": "Egypt", "مصر": "Egypt", "misri": "Egypt",
                "cairo": "Cairo", "القاهرة": "Cairo", "kairo": "Cairo",
                "ethiopia": "Ethiopia", "éthiopie": "Ethiopia", "إثيوبيا": "Ethiopia",
                "senegal": "Senegal", "sénégal": "Senegal", "السنغال": "Senegal",
                "south africa": "South Africa", "afrique du sud": "South Africa",
                "جنوب أفريقيا": "South Africa", "afrika kusini": "South Africa",
                "africa": "Africa", "afrique": "Africa", "أفريقيا": "Africa", "afrika": "Africa",
                "tunisia": "Tunisia", "tunisie": "Tunisia", "تونس": "Tunisia",
                "tanzania": "Tanzania", "tanzanie": "Tanzania", "تنزانيا": "Tanzania",
                "rwanda": "Rwanda", "رواندا": "Rwanda",
                "uganda": "Uganda", "أوغندا": "Uganda",
                "zimbabwe": "Zimbabwe", "زمبابوي": "Zimbabwe",
                "cameroon": "Cameroon", "cameroun": "Cameroon", "الكاميرون": "Cameroon", "kamerun": "Cameroon"
            }
            context["location"] = mapping.get(loc, loc.title())
            break

    # Domains — English, French, Arabic, Swahili
    domains = [
        "ai", "ia", "ذكاء اصطناعي", "akili bandia",
        "artificial intelligence", "intelligence artificielle",
        "biology", "biologie", "علم الأحياء", "biolojia",
        "economics", "économie", "اقتصاد", "uchumi",
        "engineering", "ingénierie", "هندسة", "uhandisi",
        "medicine", "médecine", "طب", "dawa",
        "social science", "sciences sociales", "علوم اجتماعية", "sayansi ya jamii",
        "physics", "physique", "فيزياء", "fizikia",
        "data science", "science des données", "علم البيانات", "sayansi ya data",
        "computer science", "informatique", "علوم الحاسوب", "sayansi ya kompyuta",
        "chemistry", "chimie", "كيمياء", "kemia",
        "agriculture", "agriculture", "زراعة", "kilimo"
    ]
    domain_mapping = {
        "ai": "AI", "ia": "AI", "ذكاء اصطناعي": "AI", "akili bandia": "AI",
        "artificial intelligence": "AI", "intelligence artificielle": "AI",
        "biology": "Biology", "biologie": "Biology", "علم الأحياء": "Biology", "biolojia": "Biology",
        "economics": "Economics", "économie": "Economics", "اقتصاد": "Economics", "uchumi": "Economics",
        "engineering": "Engineering", "ingénierie": "Engineering", "هندسة": "Engineering", "uhandisi": "Engineering",
        "medicine": "Medicine", "médecine": "Medicine", "طب": "Medicine", "dawa": "Medicine",
        "social science": "Social Science", "sciences sociales": "Social Science",
        "علوم اجتماعية": "Social Science", "sayansi ya jamii": "Social Science",
        "physics": "Physics", "physique": "Physics", "فيزياء": "Physics", "fizikia": "Physics",
        "data science": "Data Science", "science des données": "Data Science",
        "علم البيانات": "Data Science", "sayansi ya data": "Data Science",
        "computer science": "Computer Science", "informatique": "Computer Science",
        "علوم الحاسوب": "Computer Science", "sayansi ya kompyuta": "Computer Science",
        "chemistry": "Chemistry", "chimie": "Chemistry", "كيمياء": "Chemistry", "kemia": "Chemistry",
        "agriculture": "Agriculture", "زراعة": "Agriculture", "kilimo": "Agriculture"
    }
    for domain in domains:
        if domain in t:
            context["domain"] = domain_mapping.get(domain, domain.title())
            break

    # Career stage — English, French, Arabic, Swahili
    independent_signals = [
        "independent", "indépendant", "independante", "مستقل", "huru",
        "no university", "pas d'université", "sans université", "لا جامعة", "hakuna chuo kikuu",
        "no affiliation", "sans affiliation", "بدون انتماء", "hakuna ushirika",
        "self-funded", "autofinancé", "تمويل ذاتي", "kujifadhili"
    ]
    student_signals = [
        "student", "étudiant", "étudiante", "طالب", "طالبة", "mwanafunzi",
        "undergraduate", "licence", "بكالوريوس", "shahada ya kwanza",
        "master", "master", "ماجستير", "shahada ya uzamili"
    ]
    postdoc_signals = [
        "phd", "doctorat", "doctoral", "دكتوراه", "uzamivu",
        "postdoc", "postdoctoral", "post-doctorat", "ما بعد الدكتوراه", "baada ya uzamivu"
    ]

    if any(w in t for w in independent_signals):
        context["career_stage"] = "Independent"
    elif any(w in t for w in postdoc_signals):
        context["career_stage"] = "Postdoc"
    elif any(w in t for w in student_signals):
        context["career_stage"] = "Student"

    return context

# ── Pydantic Type Enforcement Models ──────────────────────────────────────
class MessageItem(BaseModel):
    role: str
    content: str

class AuditRequest(BaseModel):
    ai_response: str
    user_prompt: str = ""
    model_name: str = "unknown"
    user_location: str = "Africa"

class AuditResponse(BaseModel):
    cdi_score: float
    ras_score: float
    atd_score: float
    lls_score: float
    verdict: str
    prod: float
    lls_interpretation: str
    flagged_terms: List[str]
    international_terms: List[str]
    african_found: List[str]
    sovereign_alternatives: List[Any]
    esd_flagged_sentences: List[str] = []
    esd_flagged_count: int = 0
    deficit_phrases: List[str] = []

class ConversationRequest(BaseModel):
    conversation: List[MessageItem]
    model_name: str = "unknown"
    user_location: str = "Africa"

class ConversationResponse(BaseModel):
    current_cdi: float
    ras_score: float
    atd_score: float
    lls_score: float
    verdict: str
    prod: float
    lls_interpretation: str
    trend: str
    conversation_avg_cdi: float
    deficit_accumulation: int
    flagged_terms: List[str]
    international_terms: List[str]
    african_found: List[str]
    sovereign_alternatives: List[Any]
    user_context_detected: Dict[str, str]
    esd_flagged_sentences: List[str] = []
    esd_flagged_count: int = 0
    deficit_phrases: List[str] = []

# ── Endpoints ─────────────────────────────────────────────────────────────
@app.get("/")
def health_check():
    return {
        "status": "Kappa Engine Active",
        "version": "3.0",
        "languages": ["en", "fr", "ar", "sw"],
        "features": ["CDI", "PROD", "ESD", "RAG", "Model Profiles", "Semantic Fallback"]
    }

@app.post("/audit", response_model=AuditResponse)
def audit_single_turn(request: AuditRequest):
    scores = calculate_smart_cdi(
        response=request.ai_response,
        prompt=request.user_prompt,
        model_name=request.model_name
    )

    alternatives = []
    if scores["cdi"] <= 0.50:
        alternatives = get_sovereign_alternatives(request.ai_response)

    return AuditResponse(
        cdi_score=scores["cdi"],
        ras_score=scores["ras"],
        atd_score=scores["atd"],
        lls_score=scores["lls"],
        verdict=scores["verdict"],
        prod=scores["prod"],
        lls_interpretation=scores["lls_interpretation"],
        flagged_terms=scores["western_flagged"],
        international_terms=scores["international_flagged"],
        african_found=scores["african_found"],
        sovereign_alternatives=alternatives,
        esd_flagged_sentences=scores.get("esd_flagged_sentences", []),
        esd_flagged_count=scores.get("esd_flagged_count", 0),
        deficit_phrases=scores.get("deficit_phrases", [])
    )

@app.post("/audit-conversation", response_model=ConversationResponse)
def audit_multi_turn_thread(request: ConversationRequest):
    raw_conv = request.conversation
    if not raw_conv:
        raise HTTPException(status_code=400, detail="Conversation payload is empty")

    all_scores = []
    deficit_count = 0
    user_messages = []
    current_prompt_context = ""

    for item in raw_conv:
        if item.role == "user":
            current_prompt_context = item.content
            user_messages.append(item.content)
        elif item.role == "assistant":
            turn_score = calculate_smart_cdi(
                response=item.content,
                prompt=current_prompt_context,
                model_name=request.model_name
            )
            all_scores.append(turn_score)
            if turn_score.get("prod", 0) < -0.05:
                deficit_count += 1

    if not all_scores:
        raise HTTPException(status_code=400, detail="No trackable assistant milestones found")

    final_turn_metrics = all_scores[-1]
    cdi_history = [s["cdi"] for s in all_scores]
    conv_avg = round(sum(cdi_history) / len(cdi_history), 3)

    if len(cdi_history) >= 2:
        recent = cdi_history[-3:]
        delta_velocity = recent[-1] - recent[0]
        if delta_velocity > 0.05:
            trend = "improving"
        elif delta_velocity < -0.05:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    full_user_text = " ".join(user_messages).lower()
    user_context = detect_user_context(full_user_text)

    alternatives = []
    if final_turn_metrics["cdi"] <= 0.50:
        alternatives = get_sovereign_alternatives(raw_conv[-1].content)

    return ConversationResponse(
        current_cdi=final_turn_metrics["cdi"],
        ras_score=final_turn_metrics["ras"],
        atd_score=final_turn_metrics["atd"],
        lls_score=final_turn_metrics["lls"],
        verdict=final_turn_metrics["verdict"],
        prod=final_turn_metrics["prod"],
        lls_interpretation=final_turn_metrics["lls_interpretation"],
        trend=trend,
        conversation_avg_cdi=conv_avg,
        deficit_accumulation=deficit_count,
        flagged_terms=final_turn_metrics["western_flagged"],
        international_terms=final_turn_metrics["international_flagged"],
        african_found=final_turn_metrics["african_found"],
        sovereign_alternatives=alternatives,
        user_context_detected=user_context,
        esd_flagged_sentences=final_turn_metrics.get("esd_flagged_sentences", []),
        esd_flagged_count=final_turn_metrics.get("esd_flagged_count", 0),
        deficit_phrases=final_turn_metrics.get("deficit_phrases", [])
    )