"""
SchemeSaathi - Scenario / What-If Simulation Engine
Implements:
1. Hypothetical Citizen Benefit Twin Cloning
2. What-If Attribute Modification & Graph Recomputation (Income, State, Occupation, Education)
3. Delta Comparison (Newly Available vs No Longer Available Schemes)
4. Financial Benefit Delta & Rule Ripple Tracing
"""

import time
import copy
from datetime import datetime
import database as db
from benefit_twin import CitizenBenefitTwin

def simulate_what_if(user_id: str, modifications: dict, scenario_title: str = "Custom What-If Simulation") -> dict:
    """
    Evaluates a hypothetical citizen state on a cloned Benefit Twin without altering real profile data.
    Supported modifications:
      - annual_income: int (e.g., 310000)
      - state: str (e.g., "Karnataka", "Delhi", "Maharashtra")
      - district: str (e.g., "Bengaluru Urban", "Pune")
      - occupation: str (e.g., "Farmer", "Student", "Unemployed", "Self-Employed / MSME")
      - education_level: str (e.g., "Postgraduate", "Undergraduate", "10th Pass")
      - caste_category: str (e.g., "SC", "ST", "OBC", "General / EWS")
      - age: int (e.g., 26)
    """
    t_start = time.time()
    real_profile = db.get_user_profile(user_id) or {}
    real_docs = db.get_user_documents(user_id)
    real_apps = db.get_user_applications(user_id)

    # 1. Compute baseline state
    baseline_twin = CitizenBenefitTwin.compute(user_id, real_profile, real_docs, real_apps)
    baseline_eligible_ids = set()
    for sid, sdata in baseline_twin.get("scheme_states", {}).items():
        if sdata.get("is_eligible", False):
            baseline_eligible_ids.add(sid)

    # 2. Clone and modify profile
    sim_profile = copy.deepcopy(real_profile)
    applied_changes = []
    for k, v in modifications.items():
        if k in sim_profile or k in ["annual_income", "state", "district", "occupation", "education_level", "caste_category", "age"]:
            old_val = sim_profile.get(k)
            sim_profile[k] = v
            applied_changes.append({
                "field": k,
                "old_value": old_val,
                "simulated_value": v
            })

    # 3. Compute simulated twin (in-memory only)
    from engine import get_all_schemes, check_eligibility, analyze_document_gap
    all_schemes = get_all_schemes()
    sim_eligible_schemes = []
    sim_eligible_ids = set()
    sim_ready_schemes = []

    for s in all_schemes:
        sid = s.get("id")
        is_elig, match_pct, reasons = check_eligibility(s, sim_profile)
        if is_elig:
            sim_eligible_ids.add(sid)
            sim_eligible_schemes.append(s)
            gap = analyze_document_gap(s, real_docs)
            if gap.get("is_complete", False):
                sim_ready_schemes.append(s)

    # 4. Compute Set Diffs
    newly_available_ids = sim_eligible_ids - baseline_eligible_ids
    no_longer_available_ids = baseline_eligible_ids - sim_eligible_ids

    newly_available_schemes = [
        {"id": s.get("id"), "title": s.get("title"), "benefit_amount": s.get("benefit_amount"), "category": s.get("category")}
        for s in all_schemes if s.get("id") in newly_available_ids
    ]
    no_longer_available_schemes = [
        {"id": s.get("id"), "title": s.get("title"), "benefit_amount": s.get("benefit_amount"), "category": s.get("category")}
        for s in all_schemes if s.get("id") in no_longer_available_ids
    ]

    # Calculate financial deltas
    def parse_val(sch_list):
        total = 0
        for s in sch_list:
            b_str = s.get("benefit_amount", "0")
            import re
            digits = re.findall(r'\d+', b_str.replace(',', ''))
            total += int(digits[0]) if digits else 15000
        return total

    base_val = baseline_twin.get("financial_potential", {}).get("total_eligible_value", 0)
    sim_val = parse_val(sim_eligible_schemes)
    financial_delta = sim_val - base_val

    exec_ms = round((time.time() - t_start) * 1000, 2)

    simulation_result = {
        "scenario_title": scenario_title,
        "user_id": user_id,
        "is_simulated": True,
        "applied_modifications": applied_changes,
        "summary": {
            "baseline_eligible_count": len(baseline_eligible_ids),
            "simulated_eligible_count": len(sim_eligible_ids),
            "net_scheme_change": len(sim_eligible_ids) - len(baseline_eligible_ids),
            "newly_available_count": len(newly_available_schemes),
            "no_longer_available_count": len(no_longer_available_schemes),
            "baseline_total_grant": base_val,
            "simulated_total_grant": sim_val,
            "financial_delta": financial_delta,
            "financial_delta_formatted": f"+₹{financial_delta:,}" if financial_delta >= 0 else f"-₹{abs(financial_delta):,}"
        },
        "newly_available_schemes": newly_available_schemes,
        "no_longer_available_schemes": no_longer_available_schemes,
        "simulated_ready_schemes_count": len(sim_ready_schemes),
        "execution_time_ms": exec_ms,
        "simulated_at": datetime.now().isoformat(),
        "disclaimer": "This is a temporary hypothetical simulation. Your persistent citizen profile and vault documents have NOT been changed."
    }

    # Save to history
    try:
        db.save_scenario_simulation(user_id, scenario_title, modifications, simulation_result)
    except Exception:
        pass

    return simulation_result
