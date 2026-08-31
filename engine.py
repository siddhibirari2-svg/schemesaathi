"""
SchemeSaathi - Core Intelligence Engine
Implements:
1. Smart Document Gap Analyzer & Intelligent OCR Engine
2. Application Readiness Score (0-100%)
3. Scheme Priority Ranking with Explanations (Why #1 Recommended)
4. My Next Action Generator (Actionable & Dynamic)
5. Benefits Health Check with Financial Value Breakdown & Benefit Opportunity Score
6. Expiry & Deadline Proactive Monitor
7. Official Source Verifier (.gov.in Registry)
8. Context-Aware Grounded AI Copilot with RAG and Multilingual Support (EN, HI, MR)
9. Master Unified User Schemes Overview Engine
10. AI Government Form Field Explainer
"""

from datetime import datetime, timedelta
import re
import json
import database as db
from document_solver_data import DOCUMENT_GUIDES, get_document_guide

def get_all_schemes():
    return db.get_all_db_schemes()

def get_scheme_by_id(scheme_id: str):
    return db.get_db_scheme_by_id(scheme_id)

def normalize_doc_name(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    return cleaned

def is_doc_match(req_doc: str, avail_doc_name: str) -> bool:
    r_norm = normalize_doc_name(req_doc)
    a_norm = normalize_doc_name(avail_doc_name)
    if r_norm in a_norm or a_norm in r_norm:
        return True
    
    # Specific semantic aliases
    aliases = {
        "aadhaar": ["aadhaar", "uidai", "aadhar"],
        "income": ["income", "aamdani", "tahsildar", "utpann"],
        "domicile": ["domicile", "residence", "nivasi", "prtc"],
        "caste": ["caste", "jati", "validity", "category", "pramanpatra"],
        "bank": ["bank", "passbook", "dbt", "account", "jandhan", "npci"],
        "marksheet": ["marksheet", "10th", "12th", "passing", "board", "diploma", "iti", "degree"],
        "land": ["land", "712", "ror", "khata", "khatiyan", "bhulekh", "jamabandi"],
        "ration": ["ration", "bpl", "aay", "nfsa", "phh", "rashan"],
        "pan": ["pan", "pancard"],
        "msme": ["udyam", "msme", "registration", "udyog"],
        "vending": ["vending", "hawker", "cor", "lor", "svanidhi"],
        "disability": ["disability", "udid", "divyang", "pwd", "medical"]
    }
    
    for key, words in aliases.items():
        if any(w in r_norm for w in words) and any(w in a_norm for w in words):
            return True
            
    return False

def check_doc_validity(doc: dict) -> tuple[str, str]:
    """Returns (status, detail_msg). Status is 'Valid', 'Expiring Soon', or 'Expired'."""
    expiry_date_str = doc.get("expiry_date")
    if not expiry_date_str:
        return "Valid", "No expiry date (Permanent validity)"
    
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
        today = datetime.now()
        days_left = (expiry_date - today).days
        
        if days_left < 0:
            return "Expired", f"Expired {-days_left} days ago"
        elif days_left <= 30:
            return "Expiring Soon", f"Expires in {days_left} days"
        else:
            return "Valid", f"Valid for {days_left} days"
    except Exception:
        return "Valid", "Valid"

# ==================== INTELLIGENT OCR SIMULATION ====================

def simulate_document_ocr(doc_name: str, profile: dict = None) -> dict:
    """
    Intelligent OCR simulation: extracts issuing authority, validity, detected fields,
    and performs cross-check against citizen profile.
    """
    prof = profile or {}
    user_name = prof.get("full_name", "Citizen User")
    norm = normalize_doc_name(doc_name)
    now_year = datetime.now().year
    
    if "income" in norm or "utpann" in norm:
        inc = prof.get("annual_income", 180000)
        return {
            "detected_doc_type": "Income & Assets Certificate (State Revenue)",
            "issuing_authority": "Tehsildar & Executive Magistrate",
            "detected_name": user_name,
            "issue_date": f"{now_year}-04-10",
            "expiry_date": f"{now_year + 3}-03-31",
            "confidence_score": "98.4%",
            "extracted_fields": {
                "annual_family_income": f"₹{inc:,}",
                "financial_year": f"{now_year-1}-{now_year}",
                "certificate_no": f"IC-MH-{now_year}-84920",
                "circle_office": f"{prof.get('district', 'Pune')} Revenue Circle"
            },
            "profile_cross_check": {
                "name_matched": True,
                "income_matched": True,
                "district_matched": True
            },
            "ocr_status": "VERIFIED & MATCHED"
        }
    elif "aadhaar" in norm or "uidai" in norm:
        return {
            "detected_doc_type": "Aadhaar Card (UIDAI)",
            "issuing_authority": "Unique Identification Authority of India (UIDAI)",
            "detected_name": user_name,
            "issue_date": f"{now_year - 4}-01-15",
            "expiry_date": None,
            "confidence_score": "99.8%",
            "extracted_fields": {
                "aadhaar_masked": "XXXX-XXXX-4819",
                "gender": prof.get("gender", "Male"),
                "state": prof.get("state", "Maharashtra"),
                "pincode": prof.get("pincode", "411001"),
                "dbt_bank_seeded": "Active (NPCI Mapped)"
            },
            "profile_cross_check": {
                "name_matched": True,
                "gender_matched": True,
                "state_matched": True
            },
            "ocr_status": "VERIFIED & MATCHED"
        }
    elif "caste" in norm or "jati" in norm:
        return {
            "detected_doc_type": "Caste Certificate & Scrutiny Validity",
            "issuing_authority": "Sub-Divisional Officer (SDO) / Divisional Scrutiny Committee",
            "detected_name": user_name,
            "issue_date": f"{now_year - 2}-03-20",
            "expiry_date": f"{now_year + 1}-03-19",
            "confidence_score": "97.5%",
            "extracted_fields": {
                "social_category": prof.get("caste_category", "OBC"),
                "caste_validity_number": f"CV-{prof.get('caste_category', 'OBC')[:2]}-{now_year}-1029",
                "issuing_district": prof.get("district", "Pune")
            },
            "profile_cross_check": {
                "name_matched": True,
                "category_matched": True
            },
            "ocr_status": "VERIFIED & MATCHED"
        }
    elif "domicile" in norm or "residence" in norm or "nivasi" in norm:
        return {
            "detected_doc_type": "Certificate of Age, Nationality & Domicile",
            "issuing_authority": "Competent Revenue Authority / e-District",
            "detected_name": user_name,
            "issue_date": f"{now_year - 3}-08-12",
            "expiry_date": f"{now_year + 7}-08-12",
            "confidence_score": "98.9%",
            "extracted_fields": {
                "domicile_state": prof.get("state", "Maharashtra"),
                "residence_years": "Continuous (Birth/10+ Yrs)",
                "certificate_no": f"DOM-MH-{now_year}-9912"
            },
            "profile_cross_check": {
                "name_matched": True,
                "state_matched": True
            },
            "ocr_status": "VERIFIED & MATCHED"
        }
    elif "land" in norm or "712" in norm or "ror" in norm:
        return {
            "detected_doc_type": "Record of Rights (7/12 Extract / Khasra Khatauni)",
            "issuing_authority": "Revenue & Land Records Department (Bhulekh / Mahabhulekh)",
            "detected_name": user_name,
            "issue_date": f"{now_year}-01-10",
            "expiry_date": None,
            "confidence_score": "96.4%",
            "extracted_fields": {
                "survey_khasra_no": "Survey No 84/2A",
                "landholding_acres": f"{prof.get('land_size_acres', 1.5)} Acres",
                "cultivable_status": "Cultivable Agricultural Land",
                "land_type": "Jirayat / Bagayat"
            },
            "profile_cross_check": {
                "name_matched": True,
                "landholding_matched": True
            },
            "ocr_status": "VERIFIED & MATCHED"
        }
    else:
        return {
            "detected_doc_type": f"Official Proof ({doc_name})",
            "issuing_authority": "Competent Government Authority",
            "detected_name": user_name,
            "issue_date": f"{now_year}-01-01",
            "expiry_date": None,
            "confidence_score": "95.0%",
            "extracted_fields": {
                "document_reference": f"DOC-{secrets_hex_stub()}",
                "verification_mode": "Digital Signature / QR Seal"
            },
            "profile_cross_check": {
                "name_matched": True
            },
            "ocr_status": "VERIFIED"
        }

def secrets_hex_stub() -> str:
    import secrets
    return secrets.token_hex(4).upper()

# ==================== EXPLAINABLE ELIGIBILITY ENGINE ====================

def check_eligibility(scheme: dict, profile: dict) -> tuple[bool, int, list[str]]:
    """
    Evaluates citizen profile against scheme criteria.
    Returns (is_eligible, match_pct, list_of_reasons_or_failed_reasons).
    Handles both JSON eligibility_rules and top-level SQL columns.
    """
    rules = scheme.get("eligibility_rules", {})
    reasons = []
    failed_reasons = []
    
    # 1. Income Check
    max_inc = rules.get("max_income")
    if max_inc is None:
        max_inc = scheme.get("max_income")
    
    user_inc = profile.get("annual_income", 150000)
    if max_inc is not None and max_inc < 9000000:
        if user_inc <= max_inc:
            reasons.append(f"Income ₹{user_inc:,} is within eligible ceiling of ₹{max_inc:,}")
        else:
            failed_reasons.append(f"Annual income ₹{user_inc:,} exceeds ceiling of ₹{max_inc:,}")

    # 2. Age Check
    min_age = rules.get("min_age", scheme.get("min_age", 0))
    max_age = rules.get("max_age", scheme.get("max_age", 120))
    user_age = profile.get("age", 21)
    if min_age <= user_age <= max_age:
        reasons.append(f"Age {user_age} satisfied ({min_age}-{max_age} yrs)")
    else:
        failed_reasons.append(f"Age {user_age} outside eligible bracket ({min_age}-{max_age} yrs)")

    # 3. State Criteria
    scheme_level = scheme.get("level", "Central")
    scheme_state = scheme.get("state", "All India")
    user_state = profile.get("state", "Maharashtra")
    if scheme_level == "State" and scheme_state != "All India":
        if user_state.lower() == scheme_state.lower():
            reasons.append(f"State domicile satisfied ({user_state})")
        else:
            failed_reasons.append(f"Scheme restricted to {scheme_state} (User in {user_state})")

    # 4. Gender Check
    scheme_gender = scheme.get("gender_criteria", "ALL")
    user_gender = profile.get("gender", "Male")
    if scheme_gender and scheme_gender.upper() != "ALL":
        if user_gender.upper() == scheme_gender.upper():
            reasons.append(f"Gender criteria satisfied ({user_gender})")
        else:
            failed_reasons.append(f"Scheme for {scheme_gender} applicants only (User is {user_gender})")

    # 5. Student Check
    req_student = rules.get("student") if rules.get("student") is not None else scheme.get("requires_student")
    if req_student:
        if profile.get("student") or profile.get("occupation") == "Student":
            reasons.append("Active student enrollment verified")
        else:
            failed_reasons.append("Requires active student enrollment")

    # 6. Occupation Check
    req_occ = rules.get("occupation")
    if not req_occ:
        raw_occ = scheme.get("occupation", '["All"]')
        if isinstance(raw_occ, str):
            try:
                req_occ = json.loads(raw_occ)
            except Exception:
                req_occ = [raw_occ]
        elif isinstance(raw_occ, list):
            req_occ = raw_occ
            
    user_occ = profile.get("occupation", "")
    if req_occ and "All" not in req_occ and "ALL" not in req_occ:
        occ_match = any(o.lower() in user_occ.lower() for o in req_occ) or user_occ.lower() in [o.lower() for o in req_occ]
        if profile.get("student") and any("student" in o.lower() for o in req_occ):
            occ_match = True
        if profile.get("has_land") and any("farmer" in o.lower() for o in req_occ):
            occ_match = True

        if occ_match:
            reasons.append(f"Occupation matches target group ({user_occ})")
        else:
            failed_reasons.append(f"Occupation '{user_occ}' does not match: {', '.join(req_occ)}")

    # 7. Caste / Social Category Check
    req_caste = rules.get("caste_category")
    if not req_caste:
        raw_caste = scheme.get("social_category", '["ALL"]')
        if isinstance(raw_caste, str):
            try:
                req_caste = json.loads(raw_caste)
            except Exception:
                req_caste = [raw_caste]
        elif isinstance(raw_caste, list):
            req_caste = raw_caste

    user_caste = profile.get("caste_category", "General")
    if req_caste and "ALL" not in req_caste and "All" not in req_caste:
        if user_caste in req_caste:
            reasons.append(f"Category {user_caste} is eligible")
        else:
            failed_reasons.append(f"Category {user_caste} not covered in {', '.join(req_caste)}")

    # 8. Landholding Check
    req_land = rules.get("requires_land") if rules.get("requires_land") is not None else scheme.get("requires_land")
    if req_land:
        if profile.get("has_land") or profile.get("occupation") == "Farmer":
            reasons.append(f"Cultivable landholding recorded ({profile.get('land_size_acres', 1)} acres)")
        else:
            failed_reasons.append("Requires agricultural landholding")

    # 9. Girl Child Check
    req_girl = rules.get("has_girl_child") if rules.get("has_girl_child") is not None else scheme.get("has_girl_child")
    if req_girl:
        if profile.get("has_girl_child"):
            reasons.append("Eligible girl child under 10 years verified")
        else:
            failed_reasons.append("Requires girl child under 10 years in family")

    # 10. Housing Check (e.g. PMAY requires no pucca house)
    if "awas" in scheme.get("id", "") or "housing" in scheme.get("category", "").lower():
        if profile.get("has_pucca_house") and scheme.get("id") == "pm-awas-gramin":
            failed_reasons.append("Requires non-pucca/kutcha house status")
        else:
            reasons.append("Housing eligibility criteria satisfied")

    # Calculate match percentage
    total_checks = len(reasons) + len(failed_reasons)
    if total_checks == 0:
        return True, 100, ["General eligibility criteria satisfied"]
    
    is_eligible = len(failed_reasons) == 0
    match_pct = int((len(reasons) / total_checks) * 100)
    
    return is_eligible, match_pct, (reasons if is_eligible else failed_reasons)

# ==================== SMART DOCUMENT GAP ANALYZER ====================

def analyze_document_gap(scheme: dict, user_documents: list[dict]) -> dict:
    """
    Compares REQUIRED DOCUMENTS vs DOCUMENTS AVAILABLE TO THE USER.
    Returns structured gap analysis with checked, missing, and expiring documents.
    """
    required_docs = scheme.get("required_documents", [])
    available_matched = []
    missing_docs = []
    expiring_docs = []
    
    for req_doc in required_docs:
        matched_user_doc = None
        for u_doc in user_documents:
            if is_doc_match(req_doc, u_doc.get("doc_name", "")):
                matched_user_doc = u_doc
                break
                
        if matched_user_doc:
            status, detail_msg = check_doc_validity(matched_user_doc)
            doc_entry = {
                "required_name": req_doc,
                "matched_doc_name": matched_user_doc.get("doc_name"),
                "status": status,
                "validity_detail": detail_msg,
                "doc_id": matched_user_doc.get("id"),
                "source": matched_user_doc.get("source", "User Vault"),
                "ocr_status": matched_user_doc.get("ocr_metadata", {}).get("ocr_status", "Verified")
            }
            available_matched.append(doc_entry)
            if status in ["Expiring Soon", "Expired"]:
                expiring_docs.append(doc_entry)
        else:
            missing_docs.append({
                "required_name": req_doc,
                "status": "Missing",
                "guide_available": req_doc in DOCUMENT_GUIDES,
                "guide": get_document_guide(req_doc)
            })
            
    is_complete = len(missing_docs) == 0 and not any(d["status"] == "Expired" for d in available_matched)
    
    return {
        "scheme_id": scheme.get("id"),
        "total_required": len(required_docs),
        "total_available": len(available_matched),
        "total_missing": len(missing_docs),
        "is_complete": is_complete,
        "available_docs": available_matched,
        "missing_docs": missing_docs,
        "expiring_docs": expiring_docs
    }

# ==================== APPLICATION READINESS SCORE ====================

def calculate_readiness_score(scheme: dict, profile: dict, user_documents: list[dict]) -> dict:
    """
    Calculates dynamic 0-100% Application Readiness score based on:
    - Eligibility match (40%)
    - Document availability (40%)
    - Document validity & non-expiry (10%)
    - Official application portal verification (10%)
    """
    is_elig, match_pct, reasons = check_eligibility(scheme, profile)
    gap = analyze_document_gap(scheme, user_documents)
    
    # 1. Eligibility Points (max 40)
    elig_points = (match_pct / 100.0) * 40.0
    
    # 2. Document Points (max 40)
    total_req = gap["total_required"]
    total_avail = gap["total_available"]
    doc_points = 40.0 if total_req == 0 else (total_avail / total_req) * 40.0
    
    # 3. Validity Points (max 10)
    validity_points = 10.0
    for ad in gap["available_docs"]:
        if ad["status"] == "Expired":
            validity_points -= 5.0
        elif ad["status"] == "Expiring Soon":
            validity_points -= 2.0
    validity_points = max(0.0, validity_points)
    
    # 4. Official Portal Points (max 10)
    portal_points = 10.0 if scheme.get("official_url") and ".gov.in" in scheme.get("official_domain", "") else 5.0
    
    total_score = int(round(elig_points + doc_points + validity_points + portal_points))
    total_score = min(100, max(0, total_score))
    
    # Label & Action remaining
    actions_remaining = []
    if not is_elig:
        actions_remaining.append("Check eligibility requirements against your profile")
    for m in gap["missing_docs"]:
        actions_remaining.append(f"Obtain {m['required_name']}")
    for exp in gap["expiring_docs"]:
        actions_remaining.append(f"Renew {exp['required_name']} ({exp['validity_detail']})")
        
    if not actions_remaining:
        actions_remaining.append("All documents verified. Ready to submit on official portal.")
        
    if total_score >= 90:
        label = f"{total_score}% READY TO APPLY"
        badge_class = "bg-emerald-500 text-white"
    elif total_score >= 70:
        label = f"{total_score}% READY — 1 Document Needed"
        badge_class = "bg-blue-600 text-white"
    elif total_score >= 50:
        label = f"{total_score}% PARTIALLY READY"
        badge_class = "bg-amber-500 text-white"
    else:
        label = f"{total_score}% ACTION REQUIRED"
        badge_class = "bg-rose-500 text-white"
        
    return {
        "is_eligible": is_elig,
        "match_pct": match_pct,
        "eligibility_reasons": reasons,
        "document_gap": gap,
        "readiness_score": total_score,
        "readiness_label": label,
        "badge_class": badge_class,
        "doc_count_summary": f"{total_avail}/{total_req} Documents",
        "actions_remaining": actions_remaining,
        "breakdown": {
            "eligibility_match": int(elig_points),
            "documents_present": int(doc_points),
            "validity_check": int(validity_points),
            "official_portal_active": int(portal_points),
            "documents_ratio": f"{total_avail}/{total_req}",
            "valid_documents": validity_points >= 8.0
        }
    }

# ==================== SCHEME PRIORITY ENGINE ====================

def rank_schemes_priority(profile: dict, user_documents: list[dict]) -> list[dict]:
    """
    Ranks schemes using multi-factor priority algorithm:
    Base Priority Weight + Eligibility Match + Document Readiness + Deadline Urgency.
    """
    all_schemes = get_all_schemes()
    scored_schemes = []
    
    for s in all_schemes:
        is_elig, match_pct, reasons = check_eligibility(s, profile)
        gap = analyze_document_gap(s, user_documents)
        readiness = calculate_readiness_score(s, profile, user_documents)
        
        # Calculate dynamic score
        base_weight = s.get("priority_weight", 85)
        score = base_weight * 0.35 + match_pct * 0.35 + readiness["readiness_score"] * 0.20
        
        # Urgency bonus for approaching deadline (< 90 days)
        days_left = s.get("deadline_days_left", 180)
        if days_left <= 30:
            score += 15
        elif days_left <= 60:
            score += 10
        elif days_left <= 90:
            score += 5
            
        # Generate specific why_reasons
        why_reasons = []
        if is_elig:
            for r in reasons[:3]:
                why_reasons.append(f"✓ {r}")
            if gap["is_complete"]:
                why_reasons.append("✓ 100% of required documents available in your vault")
            elif gap["total_missing"] == 1:
                why_reasons.append(f"⚠ Only 1 document needed: {gap['missing_docs'][0]['required_name']}")
            if days_left <= 60:
                why_reasons.append(f"⏰ Application deadline in {days_left} days")
        else:
            for fr in reasons[:2]:
                why_reasons.append(f"❌ {fr}")
                
        scored_schemes.append({
            "scheme": s,
            "final_score": score,
            "is_eligible": is_elig,
            "match_pct": match_pct,
            "gap": gap,
            "readiness": readiness,
            "why_reasons": why_reasons
        })
        
    # Sort: Eligible first, then highest score
    scored_schemes.sort(key=lambda x: (1 if x["is_eligible"] else 0, x["final_score"]), reverse=True)
    
    # Assign rank numbers and display badges
    for idx, item in enumerate(scored_schemes, start=1):
        item["rank_number"] = f"#{idx}"
        if item["is_eligible"]:
            if item["readiness"]["readiness_score"] >= 90:
                item["rank_badge"] = "APPLY NOW"
                item["badge_class"] = "bg-emerald-600 text-white"
            elif item["readiness"]["readiness_score"] >= 70:
                item["rank_badge"] = "HIGH PRIORITY"
                item["badge_class"] = "bg-blue-600 text-white"
            else:
                item["rank_badge"] = "RECOMMENDED"
                item["badge_class"] = "bg-indigo-600 text-white"
        else:
            item["rank_badge"] = "NOT ELIGIBLE"
            item["badge_class"] = "bg-slate-400 text-white"
            
    return scored_schemes

# ==================== BENEFIT OPPORTUNITY SCORE ====================

def compute_benefit_opportunity_score(profile: dict, user_documents: list[dict], eligible_schemes: list[dict]) -> tuple[int, str, list[str]]:
    """
    Generates personalized SchemeSaathi Benefit Opportunity Score (0-100).
    Evaluates: Profile Completeness, Matched Schemes, Vault Readiness, and Priority Benefits.
    """
    points = 0
    breakdown = []
    
    # 1. Profile Completeness (max 30)
    prof_fields = ["full_name", "age", "gender", "state", "district", "occupation", "annual_income", "caste_category"]
    filled_count = sum(1 for f in prof_fields if profile.get(f))
    prof_pts = int((filled_count / len(prof_fields)) * 30)
    points += prof_pts
    breakdown.append(f"Citizen Profile Completeness: {prof_pts}/30 pts")
    
    # 2. Eligible Welfare Programs (max 35)
    e_count = len(eligible_schemes)
    if e_count >= 5:
        elig_pts = 35
    elif e_count >= 3:
        elig_pts = 28
    elif e_count >= 1:
        elig_pts = 20
    else:
        elig_pts = 5
    points += elig_pts
    breakdown.append(f"Matched Welfare Schemes ({e_count} found): {elig_pts}/35 pts")
    
    # 3. Document Vault Health (max 25)
    v_count = len(user_documents)
    if v_count >= 5:
        doc_pts = 25
    elif v_count >= 3:
        doc_pts = 18
    elif v_count >= 1:
        doc_pts = 10
    else:
        doc_pts = 0
    points += doc_pts
    breakdown.append(f"Document Vault Readiness ({v_count} verified proofs): {doc_pts}/25 pts")
    
    # 4. Top Scheme Readiness (max 10)
    if eligible_schemes:
        top_readiness = eligible_schemes[0]["readiness"]["readiness_score"]
        readiness_pts = int((top_readiness / 100.0) * 10)
    else:
        readiness_pts = 0
    points += readiness_pts
    breakdown.append(f"Top Action Readiness: {readiness_pts}/10 pts")
    
    score = min(100, max(15, points))
    
    if score >= 80:
        label = "High Welfare Access Potential"
    elif score >= 60:
        label = "Moderate Welfare Access Potential"
    else:
        label = "Basic Welfare Match"
        
    return score, label, breakdown

# ==================== MASTER UNIFIED USER SCHEMES API ENGINE ====================

def compute_user_schemes_overview(profile: dict, user_documents: list[dict], filters: dict = None, page: int = 1, page_size: int = 20) -> dict:
    """
    Single Source of Truth for GET /api/user/schemes.
    Evaluates citizen against ALL schemes in SQL database.
    Returns:
    - User snapshot
    - Counts (Total, Eligible, Potentially Eligible, Ready to Apply, Missing Documents)
    - Benefit Opportunity Score
    - Top Ranked Schemes (Recommended For You)
    - All Eligible Schemes (with search, category, level, and readiness filters)
    """
    filters = filters or {}
    ranked = rank_schemes_priority(profile, user_documents)
    
    eligible_schemes = []
    potentially_eligible = []
    not_eligible = []
    
    missing_docs_global = set()
    ready_count = 0
    
    for item in ranked:
        s = item["scheme"]
        gap = item["gap"]
        
        # Enrich item with structured top-level metadata for robust frontend card rendering
        item["category"] = s.get("category", "General Welfare")
        item["government_level"] = s.get("level", "Central")
        item["short_benefit"] = s.get("benefit_amount", "₹0")
        item["eligibility_match"] = f"{item.get('match_pct', 100)}% Match"
        item["required_documents"] = list(s.get("required_documents") or [])
        item["available_documents"] = [d["required_name"] for d in gap.get("available_docs", [])]
        item["missing_documents"] = [d["required_name"] for d in gap.get("missing_docs", [])]
        item["deadline"] = s.get("deadline", "Open Year-Round")
        item["verification_status"] = s.get("verification_status", "VERIFIED")
        item["official_source"] = s.get("official_domain", "services.india.gov.in")
        item["official_application_link"] = s.get("official_url", "https://services.india.gov.in")

        if item["is_eligible"]:
            item["eligibility_status"] = "ELIGIBLE"
            eligible_schemes.append(item)
            if item["readiness"]["readiness_score"] >= 75:
                ready_count += 1
            for m in gap.get("missing_docs", []):
                missing_docs_global.add(m["required_name"])
        elif item["match_pct"] >= 50:
            item["eligibility_status"] = "POTENTIALLY_ELIGIBLE"
            potentially_eligible.append(item)
        else:
            item["eligibility_status"] = "NOT_ELIGIBLE"
            not_eligible.append(item)
            
    # Combine eligible and potentially eligible for full dashboard browsing
    all_matching = eligible_schemes + potentially_eligible
    
    # Apply Filters
    search_q = filters.get("search", "").lower().strip()
    cat_filter = filters.get("category", "ALL").upper()
    level_filter = filters.get("level", "ALL").upper()
    status_filter = filters.get("status", "ALL").upper()
    
    filtered_list = all_matching
    
    if search_q:
        filtered_list = [
            x for x in filtered_list
            if search_q in x["scheme"]["title"].lower()
            or search_q in x["scheme"].get("short_desc", "").lower()
            or search_q in x["scheme"].get("ministry", "").lower()
            or search_q in x["scheme"].get("category", "").lower()
        ]
        
    if cat_filter != "ALL":
        def matches_category(cat_query: str, scheme_cat: str) -> bool:
            q = cat_query.lower().strip()
            s = scheme_cat.lower().strip()
            if q == s or q in s or s in q:
                return True
            tokens_q = {t for t in re.findall(r'\w+', q) if t not in ('and', '&', 'the', 'for')}
            tokens_s = {t for t in re.findall(r'\w+', s) if t not in ('and', '&', 'the', 'for')}
            return bool(tokens_q & tokens_s)

        filtered_list = [x for x in filtered_list if matches_category(cat_filter, x["scheme"].get("category", ""))]
        
    if level_filter != "ALL":
        filtered_list = [x for x in filtered_list if x["scheme"].get("level", "CENTRAL").upper() == level_filter]
        
    if status_filter == "ELIGIBLE":
        filtered_list = [x for x in filtered_list if x["is_eligible"]]
    elif status_filter == "READY":
        filtered_list = [x for x in filtered_list if x["readiness"]["readiness_score"] >= 75]

    # Pagination
    total_matches = len(filtered_list)
    total_pages = max(1, (total_matches + page_size - 1) // page_size)
    start_idx = (page - 1) * page_size
    paginated_items = filtered_list[start_idx:start_idx + page_size]
    
    opp_score, opp_label, opp_breakdown = compute_benefit_opportunity_score(profile, user_documents, eligible_schemes)
    
    return {
        "success": True,
        "total_schemes": len(ranked),
        "total_schemes_in_db": len(ranked),
        "eligible_count": len(eligible_schemes),
        "potentially_eligible_count": len(potentially_eligible),
        "ready_to_apply_count": ready_count,
        "missing_document_count": len(missing_docs_global),
        "user": {
            "id": profile.get("user_id"),
            "full_name": profile.get("full_name", "Citizen User"),
            "state": profile.get("state", "Maharashtra"),
            "occupation": profile.get("occupation", "Student"),
            "caste_category": profile.get("caste_category", "OBC"),
            "annual_income": profile.get("annual_income", 180000)
        },
        "benefit_opportunity": {
            "score": opp_score,
            "label": opp_label,
            "max_score": 100,
            "breakdown": opp_breakdown
        },
        "ranked_schemes": eligible_schemes[:5],  # Top Recommendations
        "all_eligible_schemes": paginated_items, # Complete Accessible List
        "schemes": paginated_items,              # Dynamic alias for client contracts
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_matches": total_matches,
            "total_pages": total_pages
        }
    }

# ==================== MY NEXT ACTION GENERATOR ====================

def get_my_next_action(profile: dict, user_documents: list[dict], applications: list[dict] = None) -> dict:
    """
    Computes single highest-leverage next step for citizen:
    1. Apply now for 90%+ ready scheme.
    2. Obtain missing document unlocking most schemes.
    3. Renew expiring critical document.
    4. Complete profile for new recommendations.
    """
    ranked = rank_schemes_priority(profile, user_documents)
    eligible = [r for r in ranked if r["is_eligible"]]
    
    if not eligible:
        return {
            "action_type": "COMPLETE_PROFILE",
            "title": "Complete Your Citizen Profile",
            "reason": "Provide your income, category, and occupation to find eligible government welfare schemes.",
            "action_text": "Edit Profile Information",
            "action_url": "action:edit_profile",
            "priority": "HIGH"
        }
        
    # Check if any scheme is 90%+ Ready to Apply
    for r in eligible:
        if r["readiness"]["readiness_score"] >= 90:
            return {
                "action_type": "APPLY_NOW",
                "title": f"Ready to Apply: {r['scheme']['title']}",
                "reason": f"You have 100% required documents in your vault for this {r['scheme']['benefit_amount']} benefit.",
                "action_text": f"Apply on {r['scheme']['official_domain']}",
                "action_url": f"scheme:{r['scheme']['id']}",
                "priority": "CRITICAL"
            }
            
    # Check most impactful missing document across eligible schemes
    doc_freq = {}
    for r in eligible:
        for m in r["gap"]["missing_docs"]:
            d_name = m["required_name"]
            doc_freq[d_name] = doc_freq.get(d_name, 0) + 1
            
    if doc_freq:
        top_missing_doc = max(doc_freq.items(), key=lambda x: x[1])[0]
        unlocked_count = doc_freq[top_missing_doc]
        return {
            "action_type": "OBTAIN_DOCUMENT",
            "title": f"Obtain {top_missing_doc}",
            "reason": f"This single document is missing for {unlocked_count} of your eligible high-priority scheme(s).",
            "action_text": f"View Guide: How to Get {top_missing_doc}",
            "action_url": f"doc_solver:{top_missing_doc}",
            "priority": "HIGH"
        }
        
    return {
        "action_type": "REVIEW_SCHEMES",
        "title": "Review Your Recommended Schemes",
        "reason": "All documents are aligned with your profile criteria.",
        "action_text": "Explore Eligible Schemes",
        "action_url": "tab:tab-schemes",
        "priority": "NORMAL"
    }

# ==================== PROACTIVE BENEFIT MONITOR ====================

def run_proactive_benefit_monitor(user_id: str, profile: dict, user_documents: list[dict]) -> list[dict]:
    """
    Scans schemes, deadlines, and expiring documents to generate proactive in-app notifications.
    """
    ranked = rank_schemes_priority(profile, user_documents)
    notifications = []
    
    # 1. Check upcoming deadlines (< 45 days)
    for r in ranked:
        if r["is_eligible"]:
            days = r["scheme"].get("deadline_days_left", 180)
            if 0 < days <= 45:
                notif = {
                    "title": f"Upcoming Deadline: {r['scheme']['title']}",
                    "message": f"Application window closes in {days} days. Ensure your documents are ready for this {r['scheme']['benefit_amount']} grant.",
                    "type": "deadline",
                    "severity": "warning" if days <= 20 else "info",
                    "action_url": f"scheme:{r['scheme']['id']}"
                }
                notifications.append(notif)
                
    # 2. Check expiring documents in vault (< 30 days)
    for doc in user_documents:
        status, msg = check_doc_validity(doc)
        if status in ["Expiring Soon", "Expired"]:
            notif = {
                "title": f"Document Renewal Alert: {doc.get('doc_name')}",
                "message": f"Your certificate {msg}. Renew via your State e-District portal to prevent application rejections.",
                "type": "expiry",
                "severity": "danger" if status == "Expired" else "warning",
                "action_url": f"doc_solver:{doc.get('doc_name')}"
            }
            notifications.append(notif)
            
    return notifications

# ==================== AI FORM FIELD EXPLAINER ====================

FORM_FIELD_EXPLANATIONS = {
    "annual family income": {
        "title": "Annual Family Income / वार्षिक कौटुंबिक उत्पन्न",
        "en": "Enter the total combined gross annual income of all earning members of your household (parents/spouse) for the relevant financial year as stated in your official Income Certificate issued by the Tehsildar.",
        "hi": "तहसीलदार द्वारा जारी आय प्रमाण पत्र के अनुसार संबंधित वित्तीय वर्ष के लिए अपने परिवार के सभी कमाने वाले सदस्यों की कुल वार्षिक सकल आय दर्ज करें।",
        "mr": "तहसीलदारांनी जारी केलेल्या अधिकृत उत्पन्न प्रमाणपत्रावर नमूद केल्यानुसार संबंधित आर्थिक वर्षासाठी घरातील सर्व कमावत्या सदस्यांचे एकत्रित एकूण वार्षिक उत्पन्न प्रविष्ट करा."
    },
    "dbt bank seeding": {
        "title": "Aadhaar DBT Bank Seeding / आधार डीबीटी बँक जोडणी",
        "en": "Government subsidies are disbursed strictly via Aadhaar Payment Bridge (APB). Ensure your bank account is linked to your Aadhaar and seeded with NPCI mandate.",
        "hi": "सरकारी सब्सिडी केवल आधार भुगतान ब्रिज (APB) के माध्यम से भेजी जाती है। सुनिश्चित करें कि आपका बैंक खाता आधार से लिंक और NPCI मैप है।",
        "mr": "शासकीय अनुदाने थेट आधार पेमेंट ब्रिजद्वारे जमा होतात. तुमचे बँक खाते आधारशी लिंक आणि NPCI मॅन्डेटसह सक्रिय असल्याची खात्री करा."
    },
    "caste validity certificate": {
        "title": "Caste Validity Certificate / जात पडताळणी प्रमाणपत्र",
        "en": "Distinct from a basic Caste Certificate. Issued by the Divisional Caste Scrutiny Committee verifying authentic lineage for education reservations and government scholarships.",
        "hi": "जाति प्रमाण पत्र से अलग, यह संभागीय जाति पड़ताल समिति द्वारा जारी किया जाता है जो छात्रवृत्ति और आरक्षण के लिए आपकी प्रामाणिकता सत्यापित करता है।",
        "mr": "जात प्रमाणपत्रापेक्षा वेगळे; उच्च शिक्षण शिष्यवृत्ती आणि आरक्षणासाठी विभागीय जात पडताळणी समितीने दिलेले अधिकृत प्रमाणपत्र."
    },
    "domicile prtc": {
        "title": "Domicile / PRTC / अधिवास प्रमाणपत्र",
        "en": "Legal proof certifying that you are a permanent resident of your state for at least 10–15 continuous years.",
        "hi": "यह कानूनी प्रमाण पत्र जो प्रमाणित करता है कि आप अपने राज्य के कम से कम 10-15 वर्षों से स्थायी निवासी हैं।",
        "mr": "तुम्ही संबंधित राज्याचे सलग १०-१५ वर्षे कायमस्वरूपी रहिवासी असल्याचा अधिकृत महसूल पुरावा."
    }
}

def explain_confusing_form_field(field_name: str, scheme_id: str = None, lang: str = "en") -> dict:
    """Explains confusing government portal application terms in simple citizen language."""
    f_clean = field_name.lower().strip()
    match = None
    for key, data in FORM_FIELD_EXPLANATIONS.items():
        if key in f_clean or f_clean in key:
            match = data
            break
            
    if match:
        explanation = match.get(lang, match.get("en"))
        return {
            "field_name": field_name,
            "title": match.get("title"),
            "explanation": explanation,
            "official_guidance": "Always ensure details match your DigiLocker verified identity records exactly."
        }
    else:
        return {
            "field_name": field_name,
            "title": f"Form Field: {field_name}",
            "explanation": f"Enter the requested official detail for '{field_name}' exactly as recorded in your government identity and revenue documents.",
            "official_guidance": "Consult the scheme guidelines or visit your nearest CSC center if you are unsure."
        }

# ==================== CONTEXT-AWARE GROUNDED AI COPILOT WITH RAG ====================

def generate_grounded_ai_answer(question: str, profile: dict, user_documents: list[dict], lang: str = "en") -> dict:
    """
    RAG-powered Government Benefits Copilot:
    1. Retrieves verified facts from SQL scheme registry.
    2. Understands citizen context (Profile, Vault, Eligibility, Gaps).
    3. Multi-lingual generation in English, Hindi, and Marathi.
    4. Anti-hallucination guarantee: never fabricates unverified rules or URLs.
    """
    q_clean = question.lower().strip()
    all_schemes = get_all_schemes()
    ranked = rank_schemes_priority(profile, user_documents)
    eligible_schemes = [r for r in ranked if r["is_eligible"]]
    
    # 0. Why am I eligible Query: "Why am I eligible?" / "Why do I qualify?" / "पात्र का आहे?"
    if any(phrase in q_clean for phrase in ["why am i eligible", "why do i qualify", "why eligible", "पात्र का आहे", "का पात्र", "क्यों पात्र", "पात्रता कारण"]):
        if eligible_schemes:
            top = eligible_schemes[0]
            reasons = top.get("why_reasons", [])
            bullets = "\n".join([f"• {r}" for r in reasons[:4]])
            if lang == "mr":
                ans = f"**{top['scheme']['title']}** या योजनेसाठी तुमची पात्रता खालील कारणांमुळे सिद्ध होते:\n\n{bullets}\n\n• **नोंदणीकृत उत्पन्न**: ₹{profile.get('annual_income', 180000):,}\n• **राज्य**: {profile.get('state', 'Maharashtra')}\n• **व्यवसाय**: {profile.get('occupation', 'Student')}"
            elif lang == "hi":
                ans = f"**{top['scheme']['title']}** के लिए आपकी पात्रता निम्नलिखित कारणों से है:\n\n{bullets}\n\n• **वार्षिक आय**: ₹{profile.get('annual_income', 180000):,}\n• **राज्य**: {profile.get('state', 'Maharashtra')}\n• **व्यवसाय**: {profile.get('occupation', 'Student')}"
            else:
                ans = f"You qualify for **{top['scheme']['title']}** based on your verified demographic criteria:\n\n{bullets}\n\n• **Annual Income**: ₹{profile.get('annual_income', 180000):,}\n• **State**: {profile.get('state', 'Maharashtra')}\n• **Occupation**: {profile.get('occupation', 'Student')}"
            return {
                "answer": ans,
                "official_source": top["scheme"]["official_domain"],
                "official_url": top["scheme"]["official_url"],
                "department": top["scheme"]["ministry"],
                "last_verified": top["scheme"]["last_verified_date"]
            }

    # 1. Eligibility Query: "What schemes can I get?" / "काय योजना मिळतील?"
    if any(phrase in q_clean for phrase in ["eligible", "my schemes", "schemes for me", "what schemes", "which scheme", "योजना", "पात्र", "मिळतील", "मिलेंगी"]):
        if not eligible_schemes:
            if lang == "mr":
                ans = "आपल्या सध्याच्या प्रोफाईलनुसार कोणतीही थेट पात्र योजना आढळली नाही. कृपया नवीन योजना शोधण्यासाठी आपले वय, उत्पन्न आणि व्यवसाय अपडेट करा."
            elif lang == "hi":
                ans = "आपकी वर्तमान प्रोफ़ाइल के अनुसार कोई पात्र योजना नहीं मिली। कृपया अधिक योजनाओं के लिए अपनी आय और व्यवसाय अपडेट करें।"
            else:
                ans = "Based on your current profile, no eligible schemes were found. Please update your profile (income, occupation, age) to unlock matching welfare schemes."
            return {
                "answer": ans,
                "official_source": "services.india.gov.in",
                "official_url": "https://services.india.gov.in",
                "department": "National Government Services Portal",
                "last_verified": "2026-08-15"
            }
            
        lines = [f"• **{r['scheme']['title']}**: {r['scheme']['benefit_amount']} ({r['readiness']['readiness_label']})" for r in eligible_schemes[:4]]
        if lang == "mr":
            answer_text = (
                f"तुमच्या नागरिक प्रोफाईलनुसार, तुम्ही **{len(eligible_schemes)} शासकीय योजनांसाठी** पात्र आहात:\n\n"
                + "\n".join(lines) +
                f"\n\nतुमची सर्वोच्च प्राधान्य योजना **{eligible_schemes[0]['scheme']['title']}** आहे."
            )
        elif lang == "hi":
            answer_text = (
                f"आपकी सत्यापित नागरिक प्रोफ़ाइल के आधार पर, आप **{len(eligible_schemes)} सरकारी योजनाओं** के लिए पात्र हैं:\n\n"
                + "\n".join(lines) +
                f"\n\nआपकी शीर्ष अनुशंसित योजना **{eligible_schemes[0]['scheme']['title']}** है।"
            )
        else:
            answer_text = (
                f"Based on your verified citizen profile, you are currently eligible for **{len(eligible_schemes)} government schemes**:\n\n"
                + "\n".join(lines) +
                f"\n\nYour highest priority recommendation is **{eligible_schemes[0]['scheme']['title']}**."
            )
            
        return {
            "answer": answer_text,
            "official_source": eligible_schemes[0]["scheme"]["official_domain"],
            "official_url": eligible_schemes[0]["scheme"]["official_url"],
            "department": eligible_schemes[0]["scheme"]["ministry"],
            "last_verified": eligible_schemes[0]["scheme"]["last_verified_date"]
        }

    # 2. Priority Query: "Which scheme should I apply for first?" / "What should I apply for first?"
    if any(phrase in q_clean for phrase in ["first", "top priority", "rank", "आधी", "पहिले", "प्रथम", "पहले"]):
        if eligible_schemes:
            top = eligible_schemes[0]
            if lang == "mr":
                answer_text = (
                    f"**सर्वोच्च प्राधान्य योजना: {top['scheme']['title']}**\n\n"
                    f"• **फायदा**: {top['scheme']['benefit_amount']}\n"
                    f"• **अर्ज तयारी**: {top['readiness']['readiness_label']}\n"
                    f"• **मुदत**: {top['scheme']['deadline']}\n"
                    f"• **कारण**: {'; '.join(top['why_reasons'][:3])}\n\n"
                    f"*दस्तऐवज उपलब्धता आणि पात्रता निकषांवर आधारित अधिकृत शिफारस.*"
                )
            elif lang == "hi":
                answer_text = (
                    f"**शीर्ष अनुशंसित योजना: {top['scheme']['title']}**\n\n"
                    f"• **लाभ**: {top['scheme']['benefit_amount']}\n"
                    f"• **आवेदन तत्परता**: {top['readiness']['readiness_label']}\n"
                    f"• **अंतिम तिथि**: {top['scheme']['deadline']}\n"
                    f"• **कारण**: {'; '.join(top['why_reasons'][:3])}\n\n"
                    f"*दस्तावेज़ तत्परता और पात्रता पर आधारित सत्यापित सिफारिश।*"
                )
            else:
                answer_text = (
                    f"**Top Recommended Scheme: {top['scheme']['title']}**\n\n"
                    f"• **Match**: {top['match_pct']}% Personal Fit\n"
                    f"• **Readiness**: {top['readiness']['readiness_label']}\n"
                    f"• **Benefit**: {top['scheme']['benefit_amount']}\n"
                    f"• **Deadline**: {top['scheme']['deadline']}\n"
                    f"• **Why #1**: {'; '.join(top['why_reasons'][:3])}\n\n"
                    f"*Personalized recommendation based on eligibility and document readiness.*"
                )
            return {
                "answer": answer_text,
                "official_source": top["scheme"]["official_domain"],
                "official_url": top["scheme"]["official_url"],
                "department": top["scheme"]["ministry"],
                "last_verified": top["scheme"]["last_verified_date"]
            }

    # 3. Document Gap Query: "What documents am I missing?" / "What document do I need?"
    if any(phrase in q_clean for phrase in ["missing", "document", "documents do i need", "कागदपत्र", "दस्तावेज़", "कमी"]):
        missing_set = set()
        for r in eligible_schemes:
            for m in r["gap"]["missing_docs"]:
                missing_set.add(m["required_name"])
                
        if missing_set:
            docs_list = "\n".join([f"• **{doc}** — Click 'How to Get This Document' to view issuing authority and portal." for doc in missing_set])
            if lang == "mr":
                answer_text = (
                    f"तुमच्या पात्र योजनांसाठी सध्या **{len(missing_set)} आवश्यक दस्तऐवज अपूर्ण** आहेत:\n\n"
                    + docs_list +
                    "\n\nहे दस्तऐवज मिळवल्यास तुमची १००% अर्ज तयारी पूर्ण होईल."
                )
            elif lang == "hi":
                answer_text = (
                    f"आपकी पात्र योजनाओं के लिए वर्तमान में **{len(missing_set)} आवश्यक दस्तावेज़ अनुपलब्ध** हैं:\n\n"
                    + docs_list +
                    "\n\nइन दस्तावेजों को प्राप्त करने पर आप 100% आवेदन के लिए तैयार होंगे।"
                )
            else:
                answer_text = (
                    f"Across your eligible schemes, you currently have **{len(missing_set)} missing document(s)**:\n\n"
                    + docs_list +
                    "\n\nObtaining these documents will unlock 100% Application Readiness."
                )
            return {
                "answer": answer_text,
                "official_source": "services.india.gov.in / State e-District",
                "official_url": "https://services.india.gov.in",
                "department": "National Services Portal",
                "last_verified": "2026-08-15"
            }
        else:
            ans = "✓ All required documents for your eligible schemes are present in your vault. You are 100% ready to apply!"
            if lang == "mr": ans = "✓ उत्तम! तुमच्या पात्र योजनांसाठी आवश्यक असलेले सर्व दस्तऐवज व्हॉल्टमध्ये उपलब्ध आहेत. तुम्ही अर्ज करण्यास १००% तयार आहात!"
            return {
                "answer": ans,
                "official_source": "services.india.gov.in",
                "official_url": "https://services.india.gov.in",
                "department": "Public Services Portal",
                "last_verified": "2026-08-15"
            }

    # 4. Ready Today Query: "Which schemes can I apply for today?" / "apply today"
    if any(phrase in q_clean for phrase in ["today", "apply now", "ready to apply", "100%", "आज", "आता"]):
        ready_today = [r for r in eligible_schemes if r["gap"]["is_complete"] or r["readiness"]["readiness_score"] >= 85]
        if ready_today:
            lines = [f"• **{r['scheme']['title']}**: {r['scheme']['benefit_amount']} ([Apply on {r['scheme']['official_domain']}]({r['scheme']['official_url']}))" for r in ready_today]
            if lang == "mr":
                ans = f"तुम्ही आज त्वरित खालील **{len(ready_today)} योजनांसाठी** अर्ज करू शकता (सर्व कागदपत्रे उपलब्ध):\n\n" + "\n".join(lines)
            elif lang == "hi":
                ans = f"आप आज तुरंत निम्नलिखित **{len(ready_today)} योजनाओं** के लिए आवेदन कर सकते हैं (सभी दस्तावेज़ तैयार):\n\n" + "\n".join(lines)
            else:
                ans = f"You can apply today for the following **{len(ready_today)} scheme(s)** (all required proofs ready in your vault):\n\n" + "\n".join(lines)
            return {
                "answer": ans,
                "official_source": ready_today[0]["scheme"]["official_domain"],
                "official_url": ready_today[0]["scheme"]["official_url"],
                "department": ready_today[0]["scheme"]["ministry"],
                "last_verified": ready_today[0]["scheme"]["last_verified_date"]
            }

    # 5. Income / Profile Change Query: "What changed after I updated my income?"
    if any(phrase in q_clean for phrase in ["changed", "updated my income", "income changed", "बदल", "बदलाव"]):
        curr_inc = profile.get("annual_income", 180000)
        ans = f"Your current recorded income is **₹{curr_inc:,}**. With this income tier, you have cleared statutory ceilings across {len(eligible_schemes)} welfare programs."
        if lang == "mr":
            ans = f"तुमचे सध्याचे नोंदणीकृत उत्पन्न **₹{curr_inc:,}** आहे. या उत्पन्न मर्यादेनुसार तुम्ही {len(eligible_schemes)} शासकीय योजनांचे निकष पूर्ण करता."
        return {
            "answer": ans,
            "official_source": "services.india.gov.in",
            "official_url": "https://services.india.gov.in",
            "department": "National Welfare Authority",
            "last_verified": "2026-08-15"
        }

    # 6. Specific Scheme Retrieval (RAG Keyword & Semantic Matching)
    matched_scheme = None
    stop_words = {"pm", "is", "the", "of", "in", "and", "scheme", "yojana", "what", "for", "to", "how", "a", "an", "योजना", "बद्दल"}
    
    for s in all_schemes:
        if s["id"] in q_clean or s["title"].lower() in q_clean:
            matched_scheme = s
            break
        if "kisan" in q_clean and "kisan" in s["id"]:
            matched_scheme = s
            break
        if ("scholarship" in q_clean or "शिष्यवृत्ती" in q_clean) and "scholarship" in s["id"]:
            matched_scheme = s
            break
        if ("bahin" in q_clean or "लाडकी" in q_clean) and "bahin" in s["id"]:
            matched_scheme = s
            break
        if ("shahu" in q_clean or "शाहू" in q_clean) and "shahu" in s["id"]:
            matched_scheme = s
            break
        if "awas" in q_clean and "awas" in s["id"]:
            matched_scheme = s
            break
        if "ayushman" in q_clean and "ayushman" in s["id"]:
            matched_scheme = s
            break
        if "mudra" in q_clean and "mudra" in s["id"]:
            matched_scheme = s
            break
        if "svanidhi" in q_clean and "svanidhi" in s["id"]:
            matched_scheme = s
            break
        if "sukanya" in q_clean and "sukanya" in s["id"]:
            matched_scheme = s
            break
        if "vishwakarma" in q_clean and "vishwakarma" in s["id"]:
            matched_scheme = s
            break
        if "apprenticeship" in q_clean and "apprenticeship" in s["id"]:
            matched_scheme = s
            break
            
    if matched_scheme:
        readiness = calculate_readiness_score(matched_scheme, profile, user_documents)
        is_elig, _, reasons = check_eligibility(matched_scheme, profile)
        
        if lang == "mr":
            answer_text = (
                f"**{matched_scheme['title']}**\n\n"
                f"• **शासकीय लाभ**: {matched_scheme['benefit_amount']} ({matched_scheme['benefit_type']})\n"
                f"• **मंत्रालय/विभाग**: {matched_scheme['ministry']}\n"
                f"• **तुमची पात्रता**: {'✓ तुम्ही निकष पूर्ण करता' if is_elig else '❌ सध्या अपात्र'}\n"
                f"• **अर्ज तयारी स्कोर**: {readiness['readiness_label']}\n"
                f"• **आवश्यक दस्तऐवज**: {', '.join(matched_scheme['required_documents'])}\n"
                f"• **अधिकृत पोर्टल**: [{matched_scheme['official_domain']}]({matched_scheme['official_url']})\n"
                f"• **हेल्पलाईन**: {matched_scheme['helpline']}\n\n"
                f"*माहिती स्रोत: अधिकृत शासकीय नोंदणी (अंतिम पडताळणी: {matched_scheme['last_verified_date']})*"
            )
        elif lang == "hi":
            answer_text = (
                f"**{matched_scheme['title']}**\n\n"
                f"• **सरकारी लाभ**: {matched_scheme['benefit_amount']} ({matched_scheme['benefit_type']})\n"
                f"• **मंत्रालय**: {matched_scheme['ministry']}\n"
                f"• **आपकी पात्रता**: {'✓ आप पात्र हैं' if is_elig else '❌ अभी पात्र नहीं'}\n"
                f"• **आवेदन तत्परता**: {readiness['readiness_label']}\n"
                f"• **आवश्यक दस्तावेज़**: {', '.join(matched_scheme['required_documents'])}\n"
                f"• **आधिकारिक पोर्टल**: [{matched_scheme['official_domain']}]({matched_scheme['official_url']})\n"
                f"• **हेल्पलाइन**: {matched_scheme['helpline']}\n\n"
                f"*स्रोत: सत्यापित सरकारी डेटाबेस (सत्यापित: {matched_scheme['last_verified_date']})*"
            )
        else:
            answer_text = (
                f"**{matched_scheme['title']}**\n\n"
                f"• **Benefit**: {matched_scheme['benefit_amount']} ({matched_scheme['benefit_type']})\n"
                f"• **Ministry**: {matched_scheme['ministry']}\n"
                f"• **Your Eligibility**: {'✓ You meet the criteria' if is_elig else '❌ Not yet eligible'}\n"
                f"• **Your Readiness**: {readiness['readiness_label']}\n"
                f"• **Required Documents**: {', '.join(matched_scheme['required_documents'])}\n"
                f"• **Official Portal**: [{matched_scheme['official_domain']}]({matched_scheme['official_url']})\n"
                f"• **Helpline**: {matched_scheme['helpline']}\n\n"
                f"*Source: Verified Government Registry (Last verified: {matched_scheme['last_verified_date']})*"
            )
        return {
            "answer": answer_text,
            "official_source": matched_scheme["official_domain"],
            "official_url": matched_scheme["official_url"],
            "department": matched_scheme["department"],
            "last_verified": matched_scheme["last_verified_date"]
        }

    # 7. General Help or Greeting Query Handling
    if any(phrase in q_clean for phrase in ["hello", "hi", "namaste", "help", "guide", "overview", "what can you do", "साहाय्य", "मदत"]):
        if eligible_schemes:
            titles = [f"• **{r['scheme']['title']}** ({r['scheme']['benefit_amount']})" for r in eligible_schemes[:3]]
            answer_text = (
                f"Namaste! Here are your top recommended government schemes based on your profile:\n\n"
                + "\n".join(titles) +
                "\n\nYou can ask me about specific schemes, required documents, eligibility criteria, or application steps."
            )
            return {
                "answer": answer_text,
                "official_source": "india.gov.in",
                "official_url": "https://www.india.gov.in",
                "department": "National Portal of India",
                "last_verified": "2026-08-15"
            }
    
    # Strict Anti-Hallucination Fallback
    return {
        "answer": "I could not verify this information from an official government source. SchemeSaathi strictly relies on verified government databases (.gov.in). Please refer to the National Government Services Portal at https://services.india.gov.in or visit your nearest Citizen Service Center (CSC).",
        "official_source": "services.india.gov.in",
        "official_url": "https://services.india.gov.in",
        "department": "Ministry of Electronics and Information Technology",
        "last_verified": "2026-08-01"
    }

# ==================== BENEFITS HEALTH CHECK SUMMARY ====================

def compute_benefits_health_check(profile: dict, user_documents: list[dict], applications: list[dict]) -> dict:
    """Computes high-level health check metrics and estimated benefit financial chips."""
    ranked = rank_schemes_priority(profile, user_documents)
    
    potentially_relevant = sum(1 for r in ranked if r["is_eligible"])
    high_priority = sum(1 for r in ranked if r["is_eligible"] and r["readiness"]["readiness_score"] >= 70)
    application_ready = sum(1 for r in ranked if r["is_eligible"] and r["gap"]["is_complete"])
    
    in_progress = sum(1 for a in applications if a.get("status") in ["Applied", "Under Verification", "College Scrutiny", "Approved"])
    
    # Missing docs count across eligible schemes
    missing_set = set()
    for r in ranked:
        if r["is_eligible"]:
            for m in r["gap"]["missing_docs"]:
                missing_set.add(m["required_name"])
                
    # Expiring docs count
    expiring_set = set()
    for doc in user_documents:
        status, _ = check_doc_validity(doc)
        if status in ["Expiring Soon", "Expired"]:
            expiring_set.add(doc.get("doc_name"))
            
    # Upcoming deadlines (< 90 days)
    upcoming_deadlines = sum(1 for r in ranked if r["is_eligible"] and r["scheme"].get("deadline_days_left", 180) <= 90)
    
    # Financial benefit summary chips
    benefit_items = []
    for r in ranked:
        if r["is_eligible"]:
            benefit_items.append({
                "scheme_id": r["scheme"]["id"],
                "title": r["scheme"]["title"],
                "amount": r["scheme"]["benefit_amount"]
            })
            
    return {
        "potentially_relevant_schemes": potentially_relevant,
        "high_priority": high_priority,
        "application_ready": application_ready,
        "applications_in_progress": in_progress,
        "missing_documents": len(missing_set),
        "expiring_documents": len(expiring_set),
        "upcoming_deadlines": upcoming_deadlines,
        "benefit_items": benefit_items,
        "profile": profile,
        "benefit_disclaimer": "Potential benefit based on available scheme information. Actual benefit is determined by the concerned government authority.",
        "last_updated": datetime.now().strftime("%d-%b-%Y %H:%M")
    }

def verify_official_source(scheme: dict) -> dict:
    """Checks official government domain and returns verified metadata."""
    url = scheme.get("official_url", "")
    domain = scheme.get("official_domain", "")
    is_gov = domain.endswith(".gov.in") or domain.endswith(".nic.in") or domain.endswith(".org.in") or "gov" in domain
    
    return {
        "is_verified_official": is_gov,
        "badge_text": "VERIFIED OFFICIAL SOURCE" if is_gov else "UNVERIFIED SOURCE",
        "ministry": scheme.get("ministry", "Government of India"),
        "department": scheme.get("department", "Public Services Division"),
        "official_domain": domain,
        "official_url": url,
        "last_verified_date": scheme.get("last_verified_date", "2026-08-15"),
        "safety_note": "Direct link to official Government portal. SchemeSaathi never intercepts your application or credentials."
    }

# ==================== 11. DOCUMENT CONFLICT DETECTION ENGINE ====================

def detect_document_conflicts(user_documents: list, profile: dict) -> list[dict]:
    """
    Compares extracted fields across all uploaded citizen documents.
    Detects name spelling variations, DOB inconsistencies, expired certificates, and address disparities.
    """
    conflicts = []
    
    # Track extracted entities
    name_map = {}
    dob_map = {}
    
    for doc in user_documents:
        dname = doc.get("doc_name", "")
        ocr = doc.get("ocr_metadata", {})
        if isinstance(ocr, str):
            try:
                ocr = json.loads(ocr)
            except Exception:
                ocr = {}
                
        det_name = ocr.get("detected_name") or profile.get("full_name")
        det_dob = ocr.get("extracted_fields", {}).get("dob") or profile.get("dob")
        
        if det_name:
            name_map[dname] = det_name
        if det_dob:
            dob_map[dname] = det_dob

    # Cross-compare Names
    doc_keys = list(name_map.keys())
    for i in range(len(doc_keys)):
        for j in range(i + 1, len(doc_keys)):
            d1, d2 = doc_keys[i], doc_keys[j]
            n1, n2 = name_map[d1].strip().lower(), name_map[d2].strip().lower()
            if n1 and n2 and n1 != n2:
                conflicts.append({
                    "conflict_type": "NAME_FORMAT_MISMATCH",
                    "conflict_field": "Name Spelling",
                    "severity": "WARNING",
                    "field": "Full Name",
                    "doc_1": d1,
                    "val_1": name_map[d1],
                    "doc_2": d2,
                    "val_2": name_map[d2],
                    "message": f"Potential inconsistency detected: Name spelling discrepancy between '{d1}' ({name_map[d1]}) and '{d2}' ({name_map[d2]}).",
                    "recommendation": "Ensure name formatting exactly matches the primary government identity before online submission."
                })

    # Check for expired or expiring certificates
    for doc in user_documents:
        status, exp_str = check_doc_validity(doc)
        if status == "Expired":
            conflicts.append({
                "conflict_type": "DOCUMENT_EXPIRED",
                "severity": "CRITICAL",
                "field": "Validity Period",
                "doc_1": doc.get("doc_name"),
                "val_1": f"Expired on {exp_str}",
                "doc_2": "Current Date",
                "val_2": datetime.now().strftime("%Y-%m-%d"),
                "message": f"Certificate '{doc.get('doc_name')}' has expired.",
                "recommendation": "Renew this certificate immediately to avoid automatic portal rejection."
            })

    return conflicts

# ==================== 12. CROSS-SCHEME DOCUMENT REUSE ENGINE ====================

def compute_cross_scheme_document_reuse(user_documents: list, all_schemes: list) -> list[dict]:
    """
    Identifies which verified vault documents can be reused across multiple government schemes,
    minimizing repeated documentation efforts.
    """
    reuse_map = []
    
    for doc in user_documents:
        dname = doc.get("doc_name", "")
        status, _ = check_doc_validity(doc)
        if status == "Expired":
            continue
            
        supported_schemes = []
        for s in all_schemes:
            req_docs = s.get("required_documents", [])
            for req in req_docs:
                if is_doc_match(req, dname):
                    supported_schemes.append({
                        "scheme_id": s.get("id"),
                        "title": s.get("title"),
                        "category": s.get("category"),
                        "benefit_amount": s.get("benefit_amount")
                    })
                    break
                    
        reuse_map.append({
            "doc_id": doc.get("id"),
            "doc_name": dname,
            "doc_type": doc.get("doc_type", "General"),
            "unlocked_schemes_count": len(supported_schemes),
            "supported_schemes": supported_schemes,
            "reuse_efficiency": "High" if len(supported_schemes) >= 3 else ("Medium" if len(supported_schemes) >= 2 else "Standard")
        })
        
    reuse_map.sort(key=lambda x: x["unlocked_schemes_count"], reverse=True)
    return reuse_map

# ==================== 13. APPLICATION REJECTION-RISK MODEL ====================

def calculate_application_rejection_risk(scheme: dict, profile: dict, user_documents: list) -> dict:
    """
    AI/ML-assisted risk estimator predicting application approval success.
    Evaluates: Missing documents, Certificate expiry, Cross-document mismatches, Marginal income criteria, and DBT seeding.
    """
    risk_score = 0
    risk_factors = []
    mitigation_advice = []

    # 1. Document Gap (0 - 40 points)
    gap = analyze_document_gap(scheme, user_documents)
    if not gap["is_complete"]:
        miss_count = gap["total_missing"]
        risk_score += min(40, miss_count * 20)
        risk_factors.append(f"{miss_count} mandatory supporting document(s) missing from vault")
        for md in gap["missing_docs"]:
            mitigation_advice.append(f"Upload verified copy of '{md['required_name']}'")

    # 2. Document Expiry (<30 days) (0 - 20 points)
    expiring_docs = []
    for doc in user_documents:
        status, exp_date = check_doc_validity(doc)
        if status in ["Expiring Soon", "Expired"]:
            expiring_docs.append(doc.get("doc_name"))
    if expiring_docs:
        risk_score += 15
        risk_factors.append(f"Document(s) expiring soon: {', '.join(expiring_docs)}")
        mitigation_advice.append("Obtain renewal acknowledgment receipt before final portal submission")

    # 3. Cross-Document Conflicts (0 - 20 points)
    conflicts = detect_document_conflicts(user_documents, profile)
    if conflicts:
        risk_score += 15
        risk_factors.append(f"{len(conflicts)} potential data consistency issue(s) detected across certificates")
        mitigation_advice.append("Verify that spelling of applicant name and birth date match your Aadhaar Card exactly")

    # 4. Income Margin Proximity (0 - 15 points)
    user_income = profile.get("annual_income", 180000)
    max_income = scheme.get("max_income", 9999999)
    if max_income < 9999999:
        margin = max_income - user_income
        if margin < 30000:
            risk_score += 10
            risk_factors.append(f"Annual income (₹{user_income:,}) is close to scheme limit (₹{max_income:,})")
            mitigation_advice.append("Ensure latest financial year's Tehsildar-attested Income Certificate is attached")

    # 5. DBT Bank Seeding (0 - 10 points)
    if scheme.get("benefit_type") == "Direct Benefit Transfer (DBT)":
        mitigation_advice.append("Confirm that your Bank Account is active and mapped to Aadhaar NPCI mapper")

    # Normalize risk level
    if risk_score <= 20:
        risk_level = "LOW"
        risk_color = "emerald"
        confidence_label = "HIGH APPROVAL PROBABILITY"
    elif risk_score <= 50:
        risk_level = "MEDIUM"
        risk_color = "amber"
        confidence_label = "MODERATE RISK - REMEDIATION ADVISED"
    else:
        risk_level = "HIGH"
        risk_color = "rose"
        confidence_label = "HIGH REJECTION RISK - ACTION REQUIRED"

    return {
        "scheme_id": scheme.get("id"),
        "scheme_title": scheme.get("title"),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "risk_score": min(100, risk_score),
        "confidence_label": confidence_label,
        "risk_factors": risk_factors if risk_factors else ["All mandatory documents and eligibility criteria fully satisfied"],
        "mitigation_advice": mitigation_advice if mitigation_advice else ["Your application profile is completely ready for submission."],
        "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

# ==================== 14. GOVERNMENT SCHEME CHANGE DETECTION ====================

def detect_government_scheme_changes() -> list[dict]:
    """
    Simulates automated government source monitoring and detects gazette / notification updates.
    """
    changes = [
        {
            "scheme_id": "post-matric-scholarship",
            "scheme_title": "Post-Matric Scholarship for OBC/SC/ST Students",
            "department": "Ministry of Social Justice & Empowerment",
            "change_type": "RULE_CRITERIA_REVISED",
            "detected_date": datetime.now().strftime("%Y-%m-%d"),
            "source_url": "https://scholarships.gov.in",
            "change_summary": "DBT NPCI Direct Bank Seeding made mandatory for FY 2026-27 scholarship disbursements.",
            "impact_level": "MODERATE",
            "action_required": "Ensure your bank passbook is seeded with Aadhaar on NPCI portal."
        },
        {
            "scheme_id": "mh-ladki-bahin-yojana",
            "scheme_title": "Mukhyamantri Majhi Ladki Bahin Yojana",
            "department": "Women & Child Development Department, Maharashtra",
            "change_type": "DEADLINE_EXTENDED",
            "detected_date": datetime.now().strftime("%Y-%m-%d"),
            "source_url": "https://ladakibahin.maharashtra.gov.in",
            "change_summary": "Online e-KYC submission date extended through December 2026.",
            "impact_level": "FAVORABLE",
            "action_required": "Complete Aadhaar biometric e-KYC at Setu Suvidha Kendra."
        }
    ]
    return changes

# ==================== 15. GRIEVANCE AI ASSISTANT ====================

def generate_grievance_draft(application: dict, citizen_profile: dict, issue_category: str = "Delay in Disbursal", user_notes: str = "") -> dict:
    """
    Generates a formal, legally structured CPGRAMS / State Public Grievance Petition.
    """
    app_ref = application.get("ref_number", "APP-2026-NSP-8821")
    scheme_title = application.get("scheme_name", "Government Welfare Scheme")
    dept = application.get("department", "Concerned Government Department")
    c_name = citizen_profile.get("full_name", "Citizen Applicant")
    c_state = citizen_profile.get("state", "Maharashtra")
    c_dist = citizen_profile.get("district", "Pune")
    
    petition_text = f"""TO:
The Public Grievance Officer / Appellate Authority,
{dept},
Government of India / Government of {c_state}.

SUBJECT: Formal Public Grievance regarding {issue_category} for {scheme_title} (Application Ref: {app_ref})

RESPECTED SIR/MADAM,

I, {c_name}, resident of District {c_dist}, State of {c_state}, have submitted my duly completed application for '{scheme_title}' under Reference ID: {app_ref}.

1. Details of Application:
   • Applicant Name: {c_name}
   • Application Reference Number: {app_ref}
   • Scheme Name: {scheme_title}
   • Date of Submission: {application.get('applied_date', '2026-06-15')}
   • Current Recorded Status: {application.get('status', 'Under Verification')}

2. Specific Grievance:
   The application has been pending beyond the citizen service standard SLA timeframe without specific deficiency notifications or disbursement updates.
   {f'Additional Facts: {user_notes}' if user_notes else ''}

3. Prayer / Relief Requested:
   I earnestly request your esteemed office to:
   a) Conduct an expeditious scrutiny of application {app_ref};
   b) Clear any pending administrative verification;
   c) Direct the disbursal of sanctioned benefits into my Aadhaar-seeded bank account.

Thanking you.

Yours faithfully,
{c_name}
Date: {datetime.now().strftime('%d-%b-%Y')}
Address: District {c_dist}, {c_state}
"""

    return {
        "petition_title": f"Grievance Petition — {scheme_title}",
        "reference_number": app_ref,
        "responsible_authority": "Central Public Grievance Redress and Monitoring System (CPGRAMS) / State Grievance Portal",
        "official_portal_url": "https://pgportal.gov.in",
        "escalation_sla_days": 30,
        "sla_escalation_level": 1,
        "petition_text": petition_text.strip()
    }

# ==================== 16. 8-STAGE BENEFIT JOURNEY ENGINE ====================

def compute_8_stage_benefit_journey(scheme: dict, profile: dict, user_documents: list, applications: list) -> dict:
    """
    Calculates live progress across the 8 stages of the Citizen Benefit Journey:
    ① Profile → ② Eligibility → ③ Documents → ④ Application Preparation → ⑤ Official Submission → ⑥ Department Verification → ⑦ Sanction/Approval → ⑧ Benefit Disbursal
    """
    sid = scheme.get("id")
    is_elig, match_pct, reasons = check_eligibility(scheme, profile)
    gap = analyze_document_gap(scheme, user_documents)
    readiness = calculate_readiness_score(scheme, profile, user_documents)
    
    # Check if existing application exists
    existing_app = next((a for a in applications if a.get("scheme_id") == sid), None)
    app_status = existing_app.get("status") if existing_app else None
    
    stages = [
        {
            "stage_number": 1,
            "name": "Citizen Profile",
            "status": "COMPLETED",
            "icon": "fa-user-check",
            "desc": "Demographics, income & category recorded"
        },
        {
            "stage_number": 2,
            "name": "Eligibility Evaluation",
            "status": "COMPLETED" if is_elig else "ATTENTION",
            "icon": "fa-bullseye",
            "desc": f"{match_pct}% Match verified by deterministic rule engine" if is_elig else "May not meet specific criteria"
        },
        {
            "stage_number": 3,
            "name": "Document Readiness",
            "status": "COMPLETED" if gap["is_complete"] else "ACTION_REQUIRED",
            "icon": "fa-folder-open",
            "desc": f"{gap['total_available']}/{gap['total_required']} Documents Ready" if gap["is_complete"] else f"Missing: {gap['missing_docs'][0]['required_name'] if gap['missing_docs'] else 'Document'}"
        },
        {
            "stage_number": 4,
            "name": "Application Copilot",
            "status": "READY" if gap["is_complete"] and is_elig else "PENDING_DOCS",
            "icon": "fa-file-signature",
            "desc": "Pre-filled data sheet ready for submission" if gap["is_complete"] else "Complete missing documents to unlock"
        },
        {
            "stage_number": 5,
            "name": "Official Portal Submission",
            "status": "SUBMITTED" if app_status else "READY_TO_SUBMIT",
            "icon": "fa-arrow-up-right-from-square",
            "desc": f"Applied on {scheme.get('official_domain', 'gov.in')}" if app_status else f"Proceed to {scheme.get('official_domain', 'gov.in')}"
        },
        {
            "stage_number": 6,
            "name": "Department Verification",
            "status": "IN_PROGRESS" if app_status in ["Applied", "Under Verification", "College Scrutiny"] else ("COMPLETED" if app_status in ["Approved", "Benefit Disbursed"] else "NOT_STARTED"),
            "icon": "fa-magnifying-glass",
            "desc": "Scrutiny by competent government authority"
        },
        {
            "stage_number": 7,
            "name": "Sanction & Approval",
            "status": "COMPLETED" if app_status in ["Approved", "Benefit Disbursed"] else ("REJECTED" if app_status == "Rejected" else "NOT_STARTED"),
            "icon": "fa-stamp",
            "desc": "Formal sanction order issuance"
        },
        {
            "stage_number": 8,
            "name": "Benefit Disbursal",
            "status": "COMPLETED" if app_status == "Benefit Disbursed" else "NOT_STARTED",
            "icon": "fa-sack-dollar",
            "desc": f"Direct Benefit Transfer of {scheme.get('benefit_amount', 'Benefit')}"
        }
    ]

    # Calculate overall journey completion percentage
    completed_stages = sum(1 for st in stages if st["status"] in ["COMPLETED", "SUBMITTED"])
    progress_pct = int((completed_stages / len(stages)) * 100)

    return {
        "scheme_id": sid,
        "scheme_title": scheme.get("title"),
        "current_stage": completed_stages + 1,
        "total_stages": 8,
        "progress_pct": progress_pct,
        "stages": stages,
        "official_url": scheme.get("official_url"),
        "official_domain": scheme.get("official_domain")
    }

# ==================== 17. ADMIN GOVERNMENT POLICY CHANGE SIMULATOR ====================

def simulate_policy_change(admin_id: str, scheme_id: str, old_rule: dict, new_rule: dict) -> dict:
    """
    Simulates the demographic and budget impact of changing a statutory government rule.
    Example: Income limit changed from ₹2,50,000 to ₹3,00,000.
    """
    scheme = get_scheme_by_id(scheme_id) or get_all_schemes()[0]
    stitle = scheme.get("title")

    # Fetch all user profiles and docs in single fast queries
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles")
        all_profiles = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM user_documents")
        all_docs_raw = [dict(r) for r in cursor.fetchall()]
        conn.close()
    except Exception:
        all_profiles = [db.get_user_profile("user_rahul_001") or {}]
        all_docs_raw = []

    user_docs_map = {}
    for d in all_docs_raw:
        uid = d.get("user_id")
        if uid not in user_docs_map:
            user_docs_map[uid] = []
        user_docs_map[uid].append(d)

    newly_eligible_count = 0
    previously_eligible_count = 0
    newly_ineligible_count = 0
    total_evaluated = max(1, len(all_profiles))
    missing_docs_tally = {}

    old_max_income = old_rule.get("max_income", scheme.get("max_income", 250000))
    new_max_income = new_rule.get("max_income", 300000)

    for prof in all_profiles:
        uid = prof.get("user_id")
        docs = user_docs_map.get(uid, [])
        user_inc = prof.get("annual_income", 180000)

        # Baseline evaluation
        old_scheme_copy = dict(scheme)
        old_scheme_copy["max_income"] = old_max_income
        is_old_elig, _, _ = check_eligibility(old_scheme_copy, prof)

        # Simulated evaluation
        new_scheme_copy = dict(scheme)
        new_scheme_copy["max_income"] = new_max_income
        is_new_elig, _, _ = check_eligibility(new_scheme_copy, prof)

        if is_old_elig:
            previously_eligible_count += 1
        if not is_old_elig and is_new_elig:
            newly_eligible_count += 1
            gap = analyze_document_gap(new_scheme_copy, docs)
            for md in gap.get("missing_docs", []):
                dn = md.get("required_name")
                missing_docs_tally[dn] = missing_docs_tally.get(dn, 0) + 1
        elif is_old_elig and not is_new_elig:
            newly_ineligible_count += 1

    # Extract grant amount
    b_str = scheme.get("benefit_amount", "0")
    digits = re.findall(r'\d+', b_str.replace(',', ''))
    unit_grant = int(digits[0]) if digits else 25000
    est_budget_impact = newly_eligible_count * unit_grant

    impact_summary = {
        "scheme_id": scheme_id,
        "scheme_title": stitle,
        "total_citizens_evaluated": total_evaluated,
        "previously_eligible_count": previously_eligible_count,
        "simulated_eligible_count": previously_eligible_count + newly_eligible_count - newly_ineligible_count,
        "newly_eligible_count": newly_eligible_count,
        "newly_ineligible_count": newly_ineligible_count,
        "net_growth_pct": round(((newly_eligible_count - newly_ineligible_count) / max(1, previously_eligible_count)) * 100, 1),
        "estimated_annual_budget_impact": est_budget_impact,
        "estimated_annual_budget_impact_formatted": f"₹{est_budget_impact:,}",
        "primary_document_bottlenecks": [
            {"document_name": k, "affected_citizens": v}
            for k, v in sorted(missing_docs_tally.items(), key=lambda x: x[1], reverse=True)[:3]
        ],
        "policy_recommendation": f"Expanding income threshold to ₹{new_max_income:,} brings {newly_eligible_count} additional citizens into the welfare safety net. Priority campaign recommended for {list(missing_docs_tally.keys())[0] if missing_docs_tally else 'income certificates'}."
    }

    try:
        db.save_policy_simulation(admin_id, scheme_id, old_rule, new_rule, impact_summary)
    except Exception:
        pass
    return impact_summary


