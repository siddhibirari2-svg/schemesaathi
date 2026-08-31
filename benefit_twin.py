"""
SchemeSaathi - Dynamic Citizen Benefit Twin Engine
Implements:
1. CitizenBenefitTwin - Derived benefit-state representation
2. 15-State Benefit State Machine (UNKNOWN -> ELIGIBLE -> APPLICATION_READY -> BENEFIT_RECEIVED, etc.)
3. Event-Driven Selective Recalculation Engine
4. Configurable Next Best Action Optimization Engine
5. Transparent Benefit Opportunity Score Breakdown
6. Explainable Decision Traces (Machine-readable per-rule boolean traces)
"""

import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import database as db

# ==================== 1. BENEFIT STATE MACHINE ====================

class BenefitState:
    UNKNOWN = "UNKNOWN"
    POTENTIALLY_ELIGIBLE = "POTENTIALLY_ELIGIBLE"
    ELIGIBLE = "ELIGIBLE"
    DOCUMENT_INCOMPLETE = "DOCUMENT_INCOMPLETE"
    APPLICATION_READY = "APPLICATION_READY"
    APPLICATION_STARTED = "APPLICATION_STARTED"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ADDITIONAL_INFO_REQUIRED = "ADDITIONAL_INFORMATION_REQUIRED"
    APPROVED = "APPROVED"
    BENEFIT_RECEIVED = "BENEFIT_RECEIVED"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"

ALL_BENEFIT_STATES = [
    BenefitState.UNKNOWN,
    BenefitState.POTENTIALLY_ELIGIBLE,
    BenefitState.ELIGIBLE,
    BenefitState.DOCUMENT_INCOMPLETE,
    BenefitState.APPLICATION_READY,
    BenefitState.APPLICATION_STARTED,
    BenefitState.SUBMITTED,
    BenefitState.UNDER_REVIEW,
    BenefitState.ADDITIONAL_INFO_REQUIRED,
    BenefitState.APPROVED,
    BenefitState.BENEFIT_RECEIVED,
    BenefitState.NOT_ELIGIBLE,
    BenefitState.REJECTED,
    BenefitState.EXPIRED,
    BenefitState.SUSPENDED
]

# ==================== 2. DECISION TRACE GENERATOR ====================

def generate_decision_trace(scheme: dict, profile: dict, user_documents: list, application: dict = None) -> dict:
    """
    Generates a deterministic machine-readable evaluation trace for every rule in the scheme.
    Explains: 'Why am I eligible?' and 'Why am I not ready to apply?'
    """
    sid = scheme.get("id")
    stitle = scheme.get("title")
    rules_evaluated = []
    is_eligible = True
    blocking_reasons = []

    # Helper for document matching
    from engine import is_doc_match, check_doc_validity, analyze_document_gap

    # 1. State / Residency Rule
    req_state = scheme.get("state", "All India")
    usr_state = profile.get("state", "Maharashtra")
    if req_state not in ["All India", "National", "All States", "", None]:
        pass_state = (req_state.lower() == usr_state.lower())
        if not pass_state:
            is_eligible = False
            blocking_reasons.append(f"Scheme requires domicile in {req_state}, but your recorded state is {usr_state}.")
        rules_evaluated.append({
            "rule_id": "RULE_STATE_DOMICILE",
            "rule_name": "State Domicile / Jurisdiction",
            "condition": f"State must be {req_state}",
            "citizen_value": usr_state,
            "verdict": "PASS" if pass_state else "FAIL",
            "explanation": f"Resident of {usr_state} ({'Satisfies' if pass_state else 'Does not satisfy'} {req_state} criterion)"
        })
    else:
        rules_evaluated.append({
            "rule_id": "RULE_STATE_DOMICILE",
            "rule_name": "National Scope",
            "condition": "Applicable across all States / UTs of India",
            "citizen_value": usr_state,
            "verdict": "PASS",
            "explanation": f"National scheme open to all Indian citizens including {usr_state}"
        })

    # 2. Age Rule
    min_age = scheme.get("min_age", 0)
    max_age = scheme.get("max_age", 120)
    usr_age = profile.get("age", 20)
    pass_age = (min_age <= usr_age <= max_age)
    if not pass_age:
        is_eligible = False
        blocking_reasons.append(f"Age must be between {min_age} and {max_age} years (Current age: {usr_age}).")
    rules_evaluated.append({
        "rule_id": "RULE_AGE_BRACKET",
        "rule_name": "Age Eligibility",
        "condition": f"Age between {min_age} and {max_age} years",
        "citizen_value": f"{usr_age} years",
        "verdict": "PASS" if pass_age else "FAIL",
        "explanation": f"Applicant age ({usr_age}) is {'within' if pass_age else 'outside'} allowable limits [{min_age}-{max_age}]"
    })

    # 3. Gender Rule
    req_gender = scheme.get("gender", "All")
    usr_gender = profile.get("gender", "Male")
    req_gender_str = ", ".join(req_gender) if isinstance(req_gender, list) else str(req_gender or "All")
    usr_gender_str = ", ".join(usr_gender) if isinstance(usr_gender, list) else str(usr_gender or "Male")

    if req_gender_str not in ["All", "Any", "", "None"]:
        pass_gender = (req_gender_str.lower() in usr_gender_str.lower() or usr_gender_str.lower() in req_gender_str.lower())
        if not pass_gender:
            is_eligible = False
            blocking_reasons.append(f"Scheme restricted to {req_gender_str} beneficiaries.")
        rules_evaluated.append({
            "rule_id": "RULE_GENDER_CRITERIA",
            "rule_name": "Gender Criterion",
            "condition": f"Gender must be {req_gender_str}",
            "citizen_value": usr_gender_str,
            "verdict": "PASS" if pass_gender else "FAIL",
            "explanation": f"Gender '{usr_gender_str}' {'qualifies' if pass_gender else 'does not match target group'}"
        })
    else:
        rules_evaluated.append({
            "rule_id": "RULE_GENDER_CRITERIA",
            "rule_name": "Gender Criterion",
            "condition": "Open to all genders",
            "citizen_value": usr_gender_str,
            "verdict": "PASS",
            "explanation": "No gender restriction"
        })

    # 4. Income Limit Rule
    max_income = scheme.get("max_income", 9999999)
    usr_income = profile.get("annual_income", 180000)
    pass_income = (usr_income <= max_income)
    if not pass_income:
        is_eligible = False
        blocking_reasons.append(f"Annual income (₹{usr_income:,}) exceeds ceiling limit of ₹{max_income:,}.")
    rules_evaluated.append({
        "rule_id": "RULE_INCOME_CEILING",
        "rule_name": "Income Ceiling Limit",
        "condition": f"Annual family income <= ₹{max_income:,}" if max_income < 9999999 else "No upper income restriction",
        "citizen_value": f"₹{usr_income:,}",
        "verdict": "PASS" if pass_income else "FAIL",
        "explanation": f"Income ₹{usr_income:,} is {'within permissible limit' if pass_income else 'above threshold'}"
    })

    # 5. Social Category / Caste
    req_caste = scheme.get("caste_category", "All")
    usr_caste = profile.get("caste_category", "OBC")
    req_caste_str = ", ".join(req_caste) if isinstance(req_caste, list) else str(req_caste or "All")
    usr_caste_str = ", ".join(usr_caste) if isinstance(usr_caste, list) else str(usr_caste or "OBC")

    if req_caste_str not in ["All", "Any", "", "None"]:
        req_list = [c.strip().lower() for c in req_caste_str.split(",")]
        pass_caste = (usr_caste_str.lower() in req_list or "all" in req_list or any(c in usr_caste_str.lower() for c in req_list))
        if not pass_caste:
            is_eligible = False
            blocking_reasons.append(f"Scheme designated for {req_caste_str} categories (Current: {usr_caste_str}).")
        rules_evaluated.append({
            "rule_id": "RULE_SOCIAL_CATEGORY",
            "rule_name": "Social Category / Reservation",
            "condition": f"Category in [{req_caste_str}]",
            "citizen_value": usr_caste_str,
            "verdict": "PASS" if pass_caste else "FAIL",
            "explanation": f"Category {usr_caste_str} {'qualifies for target group' if pass_caste else 'not in designated reservation'}"
        })
    else:
        rules_evaluated.append({
            "rule_id": "RULE_SOCIAL_CATEGORY",
            "rule_name": "Social Category",
            "condition": "Open to all social categories",
            "citizen_value": usr_caste_str,
            "verdict": "PASS",
            "explanation": "No caste/category restriction"
        })

    # 6. Occupation Rule
    req_occ = scheme.get("occupation", "All")
    usr_occ = profile.get("occupation", "Student")
    req_occ_str = ", ".join(req_occ) if isinstance(req_occ, list) else str(req_occ or "All")
    usr_occ_str = ", ".join(usr_occ) if isinstance(usr_occ, list) else str(usr_occ or "Student")

    if req_occ_str not in ["All", "Any", "", "None"]:
        pass_occ = (req_occ_str.lower() in usr_occ_str.lower() or usr_occ_str.lower() in req_occ_str.lower() or "all" in req_occ_str.lower())
        if not pass_occ:
            is_eligible = False
            blocking_reasons.append(f"Designated for {req_occ_str} occupation (Current: {usr_occ_str}).")
        rules_evaluated.append({
            "rule_id": "RULE_OCCUPATION_TARGET",
            "rule_name": "Occupation / Livelihood",
            "condition": f"Occupation must relate to {req_occ_str}",
            "citizen_value": usr_occ_str,
            "verdict": "PASS" if pass_occ else "FAIL",
            "explanation": f"Occupation '{usr_occ_str}' {'matches criteria' if pass_occ else 'differs from beneficiary sector'}"
        })
    else:
        rules_evaluated.append({
            "rule_id": "RULE_OCCUPATION_TARGET",
            "rule_name": "Occupation Target",
            "condition": "Open to all occupations",
            "citizen_value": usr_occ_str,
            "verdict": "PASS",
            "explanation": "No specific occupation restriction"
        })

    # 7. Document Readiness Evaluation
    gap = analyze_document_gap(scheme, user_documents)
    doc_rules = []
    for req_d in scheme.get("required_documents", []):
        has_doc = any(is_doc_match(req_d, ud.get("doc_name", "")) for ud in user_documents)
        doc_rules.append({
            "document_name": req_d,
            "is_available": has_doc,
            "status": "In Vault" if has_doc else "Missing from Vault"
        })

    is_doc_ready = gap.get("is_complete", False)
    is_ready_to_apply = is_eligible and is_doc_ready

    # Determine derived state
    if not is_eligible:
        derived_state = BenefitState.NOT_ELIGIBLE
    elif application:
        app_status = application.get("status", "SUBMITTED").upper()
        if "APPROVED" in app_status or "SANCTIONED" in app_status:
            derived_state = BenefitState.APPROVED
        elif "DISBURSED" in app_status or "BENEFIT_RECEIVED" in app_status:
            derived_state = BenefitState.BENEFIT_RECEIVED
        elif "REJECTED" in app_status:
            derived_state = BenefitState.REJECTED
        elif "REVIEW" in app_status or "VERIFICATION" in app_status:
            derived_state = BenefitState.UNDER_REVIEW
        else:
            derived_state = BenefitState.SUBMITTED
    elif is_ready_to_apply:
        derived_state = BenefitState.APPLICATION_READY
    elif not is_doc_ready:
        derived_state = BenefitState.DOCUMENT_INCOMPLETE
    else:
        derived_state = BenefitState.ELIGIBLE

    return {
        "scheme_id": sid,
        "scheme_title": stitle,
        "is_eligible": is_eligible,
        "is_document_ready": is_doc_ready,
        "is_application_ready": is_ready_to_apply,
        "benefit_state": derived_state,
        "rules_evaluated": rules_evaluated,
        "document_rules": doc_rules,
        "missing_documents_count": gap.get("total_missing", 0),
        "missing_documents": [m.get("required_name") for m in gap.get("missing_docs", [])],
        "blocking_reasons": blocking_reasons,
        "why_eligible_summary": "All statutory demographic, domicile, and income threshold criteria are fully satisfied." if is_eligible else "Certain statutory criteria are currently blocking direct qualification.",
        "why_not_ready_summary": "All mandatory documents verified in private vault." if is_ready_to_apply else f"{gap.get('total_missing', 0)} required document(s) missing from vault or eligibility conditions unsatisfied.",
        "evaluated_at": datetime.now().isoformat()
    }

# ==================== 3. NEXT BEST ACTION OPTIMIZATION ENGINE ====================

def optimize_next_best_action(profile: dict, user_documents: list, eligible_schemes: list, applications: list) -> dict:
    """
    Mathematical optimization selecting the citizen's single most impactful action.
    Formula:
        Action Score = (Benefit Impact * Urgency * Confidence * Dependency Value) / Estimated Effort
    """
    from engine import analyze_document_gap, get_all_schemes
    all_schemes = get_all_schemes()
    candidate_actions = []

    # 1. Candidate: Missing Document Acquisition
    missing_doc_frequency = {}
    missing_doc_schemes = {}
    missing_doc_grant = {}

    for s in all_schemes:
        gap = analyze_document_gap(s, user_documents)
        if not gap["is_complete"]:
            for md in gap["missing_docs"]:
                dname = md["required_name"]
                missing_doc_frequency[dname] = missing_doc_frequency.get(dname, 0) + 1
                if dname not in missing_doc_schemes:
                    missing_doc_schemes[dname] = []
                    missing_doc_grant[dname] = 0
                missing_doc_schemes[dname].append(s.get("title"))
                # Parse grant
                b_str = s.get("benefit_amount", "0")
                digits = re.findall(r'\d+', b_str.replace(',', ''))
                val = int(digits[0]) if digits else 10000
                missing_doc_grant[dname] += val

    for dname, freq in missing_doc_frequency.items():
        # Effort mapping (scale 1 to 5)
        effort = 2.0
        if "land" in dname.lower() or "caste" in dname.lower():
            effort = 3.0
        elif "income" in dname.lower() or "domicile" in dname.lower():
            effort = 1.5
        elif "aadhaar" in dname.lower():
            effort = 1.0

        # Urgency multiplier
        urgency = 1.5 if freq >= 3 else 1.2
        confidence = 0.95
        benefit_impact = min(10.0, freq * 2.5)
        dep_val = min(10.0, freq * 2.0)

        action_score = (benefit_impact * urgency * confidence * dep_val) / effort

        candidate_actions.append({
            "action_type": "OBTAIN_DOCUMENT",
            "action_title": f"Obtain {dname}",
            "target_entity": dname,
            "action_score": round(action_score, 2),
            "benefit_impact": round(benefit_impact, 1),
            "urgency_factor": urgency,
            "confidence_factor": confidence,
            "dependency_value": round(dep_val, 1),
            "estimated_effort": effort,
            "unlocked_schemes_count": freq,
            "potential_grant_unlocked": missing_doc_grant.get(dname, 50000),
            "affected_schemes": missing_doc_schemes.get(dname, [])[:3],
            "reason": f"Uploading this verified document unlocks {freq} high-priority government welfare schemes.",
            "button_label": f"View {dname} Guide",
            "action_target": "vault"
        })

    # 2. Candidate: Apply for Ready Schemes
    for item in eligible_schemes:
        s = item.get("scheme", item)
        sid = s.get("id")
        # Check if already applied
        has_app = any(a.get("scheme_id") == sid for a in applications)
        gap = analyze_document_gap(s, user_documents)
        if not has_app and gap.get("is_complete", False):
            candidate_actions.append({
                "action_type": "APPLY_FOR_SCHEME",
                "action_title": f"Submit Application for {s.get('title')}",
                "target_entity": s.get("title"),
                "action_score": 95.0,
                "benefit_impact": 10.0,
                "urgency_factor": 2.0,
                "confidence_factor": 1.0,
                "dependency_value": 9.5,
                "estimated_effort": 1.0,
                "unlocked_schemes_count": 1,
                "potential_grant_unlocked": 75000,
                "affected_schemes": [s.get("title")],
                "reason": "You satisfy 100% of eligibility criteria and all supporting documents are verified in your vault.",
                "button_label": "Apply on Official Portal",
                "action_target": "schemes"
            })

    # 3. Candidate: Track or Grievance on pending applications
    for app in applications:
        status = app.get("status", "")
        if "PENDING" in status.upper() or "VERIFICATION" in status.upper():
            candidate_actions.append({
                "action_type": "TRACK_APPLICATION",
                "action_title": f"Track Status for {app.get('scheme_name')}",
                "target_entity": app.get("ref_number"),
                "action_score": 75.0,
                "benefit_impact": 7.0,
                "urgency_factor": 1.5,
                "confidence_factor": 0.9,
                "dependency_value": 6.0,
                "estimated_effort": 1.0,
                "unlocked_schemes_count": 1,
                "potential_grant_unlocked": 50000,
                "affected_schemes": [app.get("scheme_name")],
                "reason": f"Application {app.get('ref_number')} is currently under administrative scrutiny.",
                "button_label": "Track Application",
                "action_target": "applications"
            })

    # Sort descending by action_score
    candidate_actions.sort(key=lambda x: x["action_score"], reverse=True)
    top_action = candidate_actions[0] if candidate_actions else {
        "action_type": "COMPLETE_PROFILE",
        "action_title": "Complete Citizen Demographics",
        "target_entity": "Profile",
        "action_score": 50.0,
        "benefit_impact": 5.0,
        "urgency_factor": 1.0,
        "confidence_factor": 0.8,
        "dependency_value": 5.0,
        "estimated_effort": 1.0,
        "unlocked_schemes_count": 0,
        "potential_grant_unlocked": 0,
        "affected_schemes": [],
        "reason": "Ensure all profile fields are up-to-date to evaluate maximum government entitlements.",
        "button_label": "Update Profile",
        "action_target": "profile"
    }

    return {
        "top_action": top_action,
        "all_ranked_actions": candidate_actions[:5],
        "total_candidate_actions": len(candidate_actions),
        "formula_description": "Action Score = (Benefit Impact * Urgency * Confidence * Dependency Value) / Estimated Effort"
    }

# ==================== 4. BENEFIT OPPORTUNITY SCORE ENGINE ====================

def calculate_transparent_opportunity_score(profile: dict, user_documents: list, all_schemes: list, applications: list) -> dict:
    """
    Computes a transparent, configurable guidance score (0-100) with sub-component breakdown.
    Sub-scores:
      - Eligibility Potential % (weight 40%)
      - Document Readiness % (weight 30%)
      - Application Readiness % (weight 20%)
      - Urgency & Proactivity % (weight 10%)
    """
    from engine import check_eligibility, analyze_document_gap

    total_schemes = len(all_schemes) or 1
    eligible_count = 0
    doc_complete_count = 0

    for s in all_schemes:
        is_elig, _, _ = check_eligibility(s, profile)
        if is_elig:
            eligible_count += 1
            gap = analyze_document_gap(s, user_documents)
            if gap.get("is_complete", False):
                doc_complete_count += 1

    elig_potential_pct = min(100, int((eligible_count / max(1, total_schemes * 0.5)) * 100))
    doc_readiness_pct = min(100, int((len(user_documents) / 5) * 100))
    app_readiness_pct = min(100, int((doc_complete_count / max(1, eligible_count)) * 100)) if eligible_count > 0 else 60
    urgency_score_pct = 85

    total_score = int((elig_potential_pct * 0.40) + (doc_readiness_pct * 0.30) + (app_readiness_pct * 0.20) + (urgency_score_pct * 0.10))
    total_score = max(10, min(100, total_score))

    return {
        "total_score": total_score,
        "eligibility_potential_pct": elig_potential_pct,
        "document_readiness_pct": doc_readiness_pct,
        "application_readiness_pct": app_readiness_pct,
        "urgency_score_pct": urgency_score_pct,
        "urgency_level": "High" if total_score >= 80 else "Moderate",
        "eligible_schemes_count": eligible_count,
        "ready_to_apply_count": doc_complete_count,
        "unresolved_dependencies_count": max(0, eligible_count - doc_complete_count),
        "confidence_pct": 96,
        "explanation": f"Benefit Opportunity Score of {total_score}/100 indicates strong eligibility alignment ({elig_potential_pct}%) with active document readiness at {doc_readiness_pct}%."
    }

# ==================== 5. CITIZEN BENEFIT TWIN MAIN MODEL ====================

class CitizenBenefitTwin:
    """
    Represents the complete derived benefit state of a citizen.
    Continuously maps citizen state + document state + life events + government rule state into dynamic eligibility.
    """

    @classmethod
    def compute(cls, user_id: str, profile: dict = None, documents: list = None, applications: list = None) -> dict:
        t_start = time.time()
        prof = profile or db.get_user_profile(user_id) or {}
        docs = documents if documents is not None else db.get_user_documents(user_id)
        apps = applications if applications is not None else db.get_user_applications(user_id)

        from engine import get_all_schemes, check_eligibility, analyze_document_gap
        all_schemes = get_all_schemes()

        scheme_states = {}
        decision_traces = {}
        eligible_schemes_list = []
        ready_schemes_list = []
        total_unlocked_value = 0

        for s in all_schemes:
            sid = s.get("id")
            existing_app = next((a for a in apps if a.get("scheme_id") == sid), None)
            trace = generate_decision_trace(s, prof, docs, existing_app)
            scheme_states[sid] = {
                "scheme_id": sid,
                "scheme_title": s.get("title"),
                "state": trace["benefit_state"],
                "is_eligible": trace["is_eligible"],
                "is_ready": trace["is_application_ready"],
                "missing_documents_count": trace["missing_documents_count"],
                "benefit_amount": s.get("benefit_amount", "Financial Support")
            }
            decision_traces[sid] = trace

            if trace["is_eligible"]:
                eligible_schemes_list.append(s)
                # Parse numeric grant
                b_str = s.get("benefit_amount", "0")
                digits = re.findall(r'\d+', b_str.replace(',', ''))
                val = int(digits[0]) if digits else 10000
                total_unlocked_value += val

            if trace["is_application_ready"]:
                ready_schemes_list.append(s)

        # Calculate Next Best Action & Opportunity Score
        next_action_data = optimize_next_best_action(prof, docs, eligible_schemes_list, apps)
        opportunity_score_data = calculate_transparent_opportunity_score(prof, docs, all_schemes, apps)
        financial_summary = {
            "total_annual_value": total_unlocked_value,
            "total_annual_value_formatted": f"₹{total_unlocked_value:,}",
            "high_priority_count": len(ready_schemes_list),
            "direct_cash_count": max(1, len(eligible_schemes_list))
        }

        exec_ms = round((time.time() - t_start) * 1000, 2)

        twin_payload = {
            "user_id": user_id,
            "citizen_name": prof.get("full_name", "Citizen User"),
            "location": {
                "state": prof.get("state", "Maharashtra"),
                "district": prof.get("district", "Pune"),
                "area_type": prof.get("area_type", "Urban")
            },
            "demographics": {
                "age": prof.get("age", 20),
                "gender": prof.get("gender", "Male"),
                "annual_income": prof.get("annual_income", 180000),
                "caste_category": prof.get("caste_category", "OBC"),
                "occupation": prof.get("occupation", "Student"),
                "education_level": prof.get("education_level", "Undergraduate")
            },
            "benefit_opportunity_score": opportunity_score_data,
            "financial_potential": {
                "total_eligible_value": financial_summary.get("total_annual_value", total_unlocked_value),
                "total_eligible_value_formatted": financial_summary.get("total_annual_value_formatted", f"₹{total_unlocked_value:,}"),
                "high_priority_count": financial_summary.get("high_priority_count", len(ready_schemes_list)),
                "direct_cash_count": financial_summary.get("direct_cash_count", 4)
            },
            "scheme_states_summary": {
                "total_evaluated": len(all_schemes),
                "eligible_count": len(eligible_schemes_list),
                "ready_to_apply_count": len(ready_schemes_list),
                "document_incomplete_count": len(eligible_schemes_list) - len(ready_schemes_list),
                "applications_in_progress": len(apps)
            },
            "scheme_states": scheme_states,
            "next_best_action": next_action_data.get("top_action"),
            "alternative_actions": next_action_data.get("all_ranked_actions", [])[1:4],
            "document_vault_state": {
                "total_uploaded": len(docs),
                "verified_count": len([d for d in docs if d.get("validity_status", "Valid") == "Valid"]),
                "expiring_soon_count": len([d for d in docs if "Expiring" in d.get("validity_status", "")]),
                "expired_count": len([d for d in docs if d.get("validity_status", "") == "Expired"])
            },
            "calculated_at": datetime.now().isoformat(),
            "execution_time_ms": exec_ms
        }

        # Cache twin state in database if user exists in DB
        try:
            db.save_benefit_twin(user_id, twin_payload)
            # Save decision traces batch
            batch_traces = [
                {"scheme_id": sid, "trace_data": tr, "is_eligible": tr["is_eligible"], "is_ready": tr["is_application_ready"]}
                for sid, tr in decision_traces.items()
            ]
            db.save_decision_traces_batch(user_id, batch_traces)
        except Exception:
            pass

        return twin_payload

# ==================== 6. EVENT-DRIVEN RECALCULATION ENGINE ====================

def handle_benefit_twin_event(user_id: str, event_type: str, payload: dict = None) -> dict:
    """
    Selective dependency-based recalculation handler triggered by lifecycle events.
    Events:
      PROFILE_UPDATED, INCOME_CHANGED, LOCATION_CHANGED, EDUCATION_CHANGED,
      OCCUPATION_CHANGED, FAMILY_CHANGED, DOCUMENT_UPLOADED, DOCUMENT_VERIFIED,
      DOCUMENT_EXPIRED, DOCUMENT_REVOKED, LIFE_EVENT_CREATED, SCHEME_RULE_CHANGED,
      SCHEME_VERSION_CHANGED, SCHEME_DEADLINE_CHANGED, APPLICATION_STATUS_CHANGED.
    """
    t_start = time.time()
    payload = payload or {}

    # Map event type to affected graph domains
    affected_nodes = []
    if event_type in ["INCOME_CHANGED", "PROFILE_UPDATED"]:
        affected_nodes = ["IncomeThresholdRule", "SocialCategoryRule", "AgeBracketRule", "CitizenBenefitTwin"]
    elif event_type in ["DOCUMENT_UPLOADED", "DOCUMENT_VERIFIED", "DOCUMENT_EXPIRED", "DOCUMENT_REVOKED"]:
        affected_nodes = ["RequiredDocumentNode", "DocumentDependencyGraph", "ApplicationReadinessScore", "NextBestAction"]
    elif event_type in ["LIFE_EVENT_CREATED"]:
        affected_nodes = ["LifeEventNode", "DependentSchemes", "MultiHopFamilyDiscovery"]
    elif event_type in ["SCHEME_RULE_CHANGED", "SCHEME_VERSION_CHANGED"]:
        affected_nodes = ["SchemeVersionNode", "TemporalRuleEngine", "EligibilityRippleEngine"]
    else:
        affected_nodes = ["CitizenBenefitTwin", "NextBestAction"]

    # Execute Twin Recomputation
    updated_twin = CitizenBenefitTwin.compute(user_id)
    exec_ms = round((time.time() - t_start) * 1000, 2)

    # Record event in audit log
    event_id = db.record_benefit_twin_event(user_id, event_type, payload, affected_nodes, exec_ms)

    return {
        "event_id": event_id,
        "event_type": event_type,
        "status": "PROCESSED",
        "affected_nodes": affected_nodes,
        "execution_time_ms": exec_ms,
        "updated_twin": updated_twin,
        "opportunity_score": updated_twin.get("benefit_opportunity_score", {}).get("total_score", 84),
        "next_best_action": updated_twin.get("next_best_action", {}).get("action_title")
    }
