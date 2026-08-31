"""
SchemeSaathi - Automated Security, Authentication & Feature Test Suite
Tests:
1. Multi-Tenant Isolation (User A cannot access User B's documents -> 403 Forbidden)
2. Document Gap Analyzer accuracy (Missing Income Certificate for Student)
3. Application Readiness Score Engine (Dynamic % & Action checklist)
4. Document Expiry Detection (Expiring Soon warning)
5. Scheme Priority Engine ranking & Why Reasons
6. Official Source Safety (.gov.in registry)
7. Context-Aware Grounded AI Safety
8. Benefits Health Check with Financial Summary & Application States
9. Scalable Scheme Registry & Dynamic Import (SQL-backed)
10. Citizen Missing Scheme Reporting
11. User Registration & Validation (Indian mobile, email, password hashing)
12. User Login, Token Generation & Logout Invalidation
13. Personalized Multi-Step Onboarding Profile & Automatic Eligibility Analysis
14. Strict User-to-User Multi-Tenant Authorization Security
15. Profile Update & Dynamic Recalculation
"""

import unittest
import secrets
from datetime import datetime, timedelta
import database as db
import engine

class TestSchemeSaathiSecurityAndFeatures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.init_db()

    def test_01_multi_tenant_document_isolation(self):
        """CRITICAL SECURITY TEST: User A (Rahul) cannot access User B's private document."""
        user_a = "user_rahul_001"
        user_b = "user_victim_003"
        doc_b_id = "doc_private_b_999"

        # User B should be able to access their own document
        doc_for_b = db.get_document_by_id(doc_b_id, user_b)
        self.assertIsNotNone(doc_for_b, "User B should be able to access own document")
        self.assertEqual(doc_for_b["user_id"], user_b)

        # User A attempting to access User B's document MUST return None (leading to 403 in server)
        doc_for_a = db.get_document_by_id(doc_b_id, user_a)
        self.assertIsNone(doc_for_a, "SECURITY VIOLATION: User A was able to query User B's document!")

        # User A attempting to delete User B's document MUST fail
        delete_success = db.delete_user_document(doc_b_id, user_a)
        self.assertFalse(delete_success, "SECURITY VIOLATION: User A was able to delete User B's document!")

        # Document B should still exist in User B's vault
        still_exists = db.get_document_by_id(doc_b_id, user_b)
        self.assertIsNotNone(still_exists)

    def test_02_document_gap_analyzer(self):
        """Verifies Required Documents vs Available Documents comparison (Missing Income Certificate)."""
        scholarship_scheme = engine.get_scheme_by_id("post-matric-scholarship")
        self.assertIsNotNone(scholarship_scheme)

        # User Rahul has Aadhaar, Bank, Marksheet, Domicile, Caste (Missing Income Certificate intentionally)
        rahul_docs = db.get_user_documents("user_rahul_001")
        gap = engine.analyze_document_gap(scholarship_scheme, rahul_docs)

        self.assertGreater(gap["total_required"], 0)
        self.assertGreater(gap["total_available"], 0)
        self.assertFalse(gap["is_complete"], "Gap analysis should identify missing Income Certificate")
        
        missing_names = [m["required_name"] for m in gap["missing_docs"]]
        self.assertIn("Income Certificate", missing_names, "Income Certificate should be listed as missing")

    def test_03_application_readiness_score(self):
        """Verifies Application Readiness Score calculation and action breakdown."""
        scholarship_scheme = engine.get_scheme_by_id("post-matric-scholarship")
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")

        readiness = engine.calculate_readiness_score(scholarship_scheme, profile, docs)
        
        self.assertGreaterEqual(readiness["readiness_score"], 70)
        self.assertLessEqual(readiness["readiness_score"], 100)
        self.assertIn("% READY", readiness["readiness_label"])
        self.assertTrue(len(readiness["actions_remaining"]) >= 1)
        
        has_income_action = any("Income" in act for act in readiness["actions_remaining"])
        self.assertTrue(has_income_action, "Should list obtaining Income Certificate as next action")

    def test_04_document_expiry_detection(self):
        """Verifies document expiry detection logic (Valid, Expiring Soon, Expired)."""
        rahul_docs = db.get_user_documents("user_rahul_001")
        caste_doc = next((d for d in rahul_docs if "Caste" in d["doc_name"]), None)
        self.assertIsNotNone(caste_doc)

        status, msg = engine.check_doc_validity(caste_doc)
        self.assertEqual(status, "Expiring Soon")
        self.assertIn("Expires in", msg)

    def test_05_scheme_priority_engine_and_why_reasons(self):
        """Verifies that schemes are intelligently ranked and have why_reasons."""
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")

        ranked = engine.rank_schemes_priority(profile, docs)
        self.assertGreater(len(ranked), 0)
        self.assertEqual(ranked[0]["rank_number"], "#1")
        self.assertTrue(len(ranked[0]["why_reasons"]) > 0, "Ranked scheme must provide explicit why_reasons")
        
        top_scheme_id = ranked[0]["scheme"]["id"]
        self.assertIn(top_scheme_id, ["post-matric-scholarship", "naps-apprenticeship", "ayushman-bharat-pmjay", "mh-mahadbt-shahu-maharaj"])

    def test_06_official_source_safety(self):
        """Verifies official .gov.in domain verification and safety notice."""
        scheme = engine.get_scheme_by_id("pm-kisan")
        verif = engine.verify_official_source(scheme)

        self.assertTrue(verif["is_verified_official"])
        self.assertIn(".gov.in", verif["official_domain"])
        self.assertEqual(verif["badge_text"], "VERIFIED OFFICIAL SOURCE")

    def test_07_context_aware_grounded_ai(self):
        """Verifies AI response uses verified database and recognizes user context."""
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")

        # 1. Scheme specific query
        res = engine.generate_grounded_ai_answer("What is the benefit of PM Kisan?", profile, docs)
        self.assertIn("pmkisan.gov.in", res["official_source"])
        self.assertIn("₹6,000", res["answer"])
        
        # 2. Context query: "What document am I missing?"
        res2 = engine.generate_grounded_ai_answer("What document am I missing?", profile, docs)
        self.assertIn("missing", res2["answer"].lower())
        self.assertIn("Income Certificate", res2["answer"])

    def test_08_benefits_health_check_financial_summary(self):
        """Verifies health check metrics and financial benefits summary."""
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")
        apps = db.get_user_applications("user_rahul_001")

        hc = engine.compute_benefits_health_check(profile, docs, apps)
        self.assertGreater(hc["potentially_relevant_schemes"], 0)
        self.assertGreater(len(hc["benefit_items"]), 0)
        self.assertIsNotNone(hc["benefit_disclaimer"])

    def test_09_dynamic_scheme_import_and_querying(self):
        """Verifies that new schemes can be dynamically inserted into SQL without altering source code."""
        new_scheme_payload = {
            "id": "test-dynamic-scheme-101",
            "title": "National Green Energy Rooftop Solar Scheme",
            "short_desc": "Subsidies up to ₹78,000 for installing grid-connected solar panels on residential rooftops.",
            "level": "Central",
            "state": "All India",
            "ministry": "Ministry of New and Renewable Energy",
            "category": "Energy & Sustainability",
            "benefit_amount": "₹78,000 Direct Subsidy",
            "official_url": "https://pmsuryaghar.gov.in",
            "official_domain": "pmsuryaghar.gov.in",
            "required_documents": ["Aadhaar Card", "Electricity Bill", "Bank Account / Passbook with DBT Seeding"],
            "verification_status": "VERIFIED",
            "priority_weight": 88
        }
        
        # Insert dynamically into SQLite registry
        scheme_id = db.insert_or_update_scheme(new_scheme_payload)
        self.assertEqual(scheme_id, "test-dynamic-scheme-101")

        # Query dynamically via engine
        queried = engine.get_scheme_by_id("test-dynamic-scheme-101")
        self.assertIsNotNone(queried)
        self.assertEqual(queried["title"], "National Green Energy Rooftop Solar Scheme")
        self.assertEqual(len(queried["required_documents"]), 3)

        # Check in all schemes list
        all_s = engine.get_all_schemes()
        self.assertTrue(any(s["id"] == "test-dynamic-scheme-101" for s in all_s))

    def test_10_citizen_missing_scheme_reporting(self):
        """Verifies that citizens can report missing schemes for registry inclusion."""
        report_data = {
            "scheme_name": "Maharashtra Ladki Bahin Yojana",
            "department_or_ministry": "Women & Child Development Department",
            "state": "Maharashtra",
            "official_link": "https://ladakibahin.maharashtra.gov.in",
            "description": "Monthly financial assistance of ₹1,500 for eligible women aged 21-65 years."
        }

        rep_id = db.report_missing_scheme("user_rahul_001", report_data)
        self.assertIsNotNone(rep_id)
        self.assertTrue(rep_id.startswith("rep_"))

        # Verify audit retrieval
        reports = db.get_missing_scheme_reports()
        self.assertTrue(any(r["id"] == rep_id for r in reports))
        matching_rep = next(r for r in reports if r["id"] == rep_id)
        self.assertEqual(matching_rep["scheme_name"], "Maharashtra Ladki Bahin Yojana")
        self.assertEqual(matching_rep["status"], "PENDING_REVIEW")

    def test_11_user_registration_and_validation(self):
        """Verifies registration validation, Indian mobile validation, password hashing, and duplicate prevention."""
        unique_suffix = secrets.token_hex(3)
        email = f"test_citizen_{unique_suffix}@example.com"
        mobile = f"98765{secrets.randbelow(90000) + 10000}"

        # 1. Successful registration
        user_safe, token = db.register_user("Amitabh Rao", email, mobile, "StrongPassword@123")
        self.assertIsNotNone(user_safe["id"])
        self.assertTrue(user_safe["id"].startswith("user_"))
        self.assertNotIn("password_hash", user_safe)
        self.assertNotIn("salt", user_safe)
        self.assertFalse(user_safe["is_onboarded"])
        self.assertTrue(token.startswith("ss_tok_"))

        # 2. Duplicate email rejection
        with self.assertRaises(ValueError) as ctx:
            db.register_user("Another User", email, f"9{secrets.randbelow(899999999) + 100000000}", "Pass123456")
        self.assertIn("email address already exists", str(ctx.exception))

        # 3. Duplicate mobile rejection
        with self.assertRaises(ValueError) as ctx:
            db.register_user("Another User", f"unique_{unique_suffix}@test.com", mobile, "Pass123456")
        self.assertIn("mobile number already exists", str(ctx.exception))

        # 4. Invalid Indian mobile number rejection
        with self.assertRaises(ValueError) as ctx:
            db.register_user("Bad Mobile", f"bad_{unique_suffix}@test.com", "12345", "Pass123456")
        self.assertIn("10-digit Indian mobile", str(ctx.exception))

        # Valid registration
        unique_suffix = secrets.token_hex(4)
        email = f"citizen_{unique_suffix}@example.com"
        mobile = f"9{secrets.randbelow(899999999) + 100000000}"
        password = "SecurePassword@123"
        user_safe, token = db.register_user("Anita Roy", email, mobile, password)
        self.assertIsNotNone(user_safe["id"])
        self.assertEqual(user_safe["email"], email)

        # Invalid Email rejection
        with self.assertRaises(ValueError) as ctx:
            db.register_user("Bad Email", "invalid-email-address", f"9{secrets.randbelow(899999999) + 100000000}", "Pass123456")
        self.assertIn("valid email address", str(ctx.exception))

    def test_12_user_login_token_and_logout(self):
        """Verifies login via email or mobile, password check, session generation, and logout."""
        unique_suffix = secrets.token_hex(4)
        email = f"login_user_{unique_suffix}@example.com"
        mobile = f"9{secrets.randbelow(899999999) + 100000000}"
        password = "SecurePassword@123"

        user_safe, token = db.register_user("Kavita Deshmukh", email, mobile, password)

        # 1. Login with Email
        login_u, prof, login_tok = db.login_user(email, password)
        self.assertEqual(login_u["id"], user_safe["id"])
        self.assertTrue(login_tok.startswith("ss_tok_"))

        # 2. Login with Mobile Number
        login_u2, prof2, login_tok2 = db.login_user(mobile, password)
        self.assertEqual(login_u2["id"], user_safe["id"])

        # 3. Verify session token resolves user
        resolved = db.get_user_by_session_token(login_tok)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved["id"], user_safe["id"])

        # 4. Login with Wrong Password fails
        with self.assertRaises(ValueError) as ctx:
            db.login_user(email, "WrongPassword999")
        self.assertIn("Incorrect password", str(ctx.exception))

        # 5. Logout deletes session token
        db.logout_session(login_tok)
        logged_out_resolved = db.get_user_by_session_token(login_tok)
        self.assertIsNone(logged_out_resolved, "Session token must be invalid after logout")

    def test_13_first_time_onboarding_and_eligibility_flow(self):
        """Tests complete onboarding flow: registration -> multi-step profile -> dynamic scheme matches."""
        unique_suffix = secrets.token_hex(3)
        email = f"onboard_{unique_suffix}@example.com"
        mobile = f"98765{secrets.randbelow(90000) + 10000}"

        user_safe, token = db.register_user("Anjali Patil", email, mobile, "AnjaliPass@123")
        uid = user_safe["id"]

        # Initial onboarding status is False
        prof_init = db.get_user_profile(uid)
        self.assertEqual(prof_init["onboarding_completed"], 0)

        # Complete 6-step onboarding payload for Maharashtra female student
        onboarding_payload = {
            "full_name": "Anjali Patil",
            "dob": "2002-05-10",
            "age": 24,
            "gender": "Female",
            "state": "Maharashtra",
            "district": "Pune",
            "pincode": "411004",
            "caste_category": "OBC",
            "annual_income": 150000,
            "area_type": "Rural",
            "disability_status": "None",
            "marital_status": "Single",
            "education_level": "Undergraduate",
            "student": True,
            "course_stream": "B.A Economics",
            "institution_type": "Government Aided",
            "occupation": "Student",
            "has_land": False,
            "land_size_acres": 0,
            "has_pucca_house": False,
            "has_bpl_card": False,
            "has_girl_child": False,
            "family_size": 4,
            "interest_categories": ["Education & Scholarships", "Women & Child Welfare", "Healthcare & Wellness"]
        }

        # Save profile
        db.save_user_onboarding_profile(uid, onboarding_payload)

        # Verify profile is marked complete
        updated_prof = db.get_user_profile(uid)
        self.assertEqual(updated_prof["onboarding_completed"], 1)
        self.assertEqual(updated_prof["state"], "Maharashtra")
        self.assertEqual(updated_prof["gender"], "Female")

        # Run eligibility engine
        docs = db.get_user_documents(uid)
        ranked = engine.rank_schemes_priority(updated_prof, docs)

        self.assertGreater(len(ranked), 0)
        matched_ids = [r["scheme"]["id"] for r in ranked]
        
        # Should match Maharashtra Higher Education and Women schemes
        self.assertTrue(
            "post-matric-scholarship" in matched_ids or 
            "mh-mahadbt-shahu-maharaj" in matched_ids or 
            "mh-ladki-bahin-yojana" in matched_ids,
            "Onboarded Maharashtra female student should match state education/women welfare schemes"
        )

    def test_14_user_a_cannot_access_user_b_profile_and_data(self):
        """SECURITY ISOLATION: User A cannot query or mutate User B's data."""
        # Create User A
        uA_safe, _ = db.register_user("User A", f"user_a_{secrets.token_hex(4)}@test.com", f"9{secrets.randbelow(899999999) + 100000000}", "PassA123")
        # Create User B
        uB_safe, _ = db.register_user("User B", f"user_b_{secrets.token_hex(4)}@test.com", f"9{secrets.randbelow(899999999) + 100000000}", "PassB123")

        # User B uploads a private document
        doc_b_id = db.add_user_document(uB_safe["id"], "Confidential B Document", "Private")

        # User A attempts to access User B document -> None
        self.assertIsNone(db.get_document_by_id(doc_b_id, uA_safe["id"]))

        # User A attempts to delete User B document -> False
        self.assertFalse(db.delete_user_document(doc_b_id, uA_safe["id"]))

        # User B can still access their document
        self.assertIsNotNone(db.get_document_by_id(doc_b_id, uB_safe["id"]))

    def test_15_profile_recalculation_on_change(self):
        """Verifies that changing income or status updates scheme eligibility dynamically."""
        unique_suffix = secrets.token_hex(4)
        user_safe, _ = db.register_user("Rajesh Sharma", f"rajesh_{unique_suffix}@example.com", f"9{secrets.randbelow(899999999) + 100000000}", "RajeshPass@123")
        uid = user_safe["id"]

        # Initial low income profile (eligible for scholarships and low-income schemes)
        prof_low = {
            "full_name": "Rajesh Sharma",
            "age": 21,
            "gender": "Male",
            "state": "Maharashtra",
            "annual_income": 120000,
            "caste_category": "OBC",
            "occupation": "Student",
            "student": True
        }
        db.save_user_onboarding_profile(uid, prof_low)
        docs = db.get_user_documents(uid)
        ranked_low = engine.rank_schemes_priority(prof_low, docs)

        pms_low = next((r for r in ranked_low if r["scheme"]["id"] == "post-matric-scholarship"), None)
        self.assertIsNotNone(pms_low)
        self.assertGreaterEqual(pms_low["match_pct"], 80)

        # High income change (> ₹2.5L limit)
        prof_high = dict(prof_low)
        prof_high["annual_income"] = 850000
        db.save_user_onboarding_profile(uid, prof_high)

        scheme = engine.get_scheme_by_id("post-matric-scholarship")
        is_eligible, match_pct, reasons = engine.check_eligibility(scheme, prof_high)
        self.assertFalse(is_eligible, "Income > 2.5L must disqualify from Post-Matric Scholarship")
        self.assertTrue(any("exceeds" in r for r in reasons))

    def test_16_unified_user_schemes_overview_api(self):
        """Tests compute_user_schemes_overview returning user overview, opportunity score, and filterable catalog."""
        prof = {
            "user_id": "user_rahul_001",
            "full_name": "Rahul Sharma",
            "age": 21,
            "gender": "Male",
            "state": "Maharashtra",
            "district": "Pune",
            "annual_income": 180000,
            "caste_category": "OBC",
            "occupation": "Student",
            "student": 1
        }
        docs = [
            {"doc_name": "Aadhaar Card", "expiry_date": None},
            {"doc_name": "Domicile Certificate", "expiry_date": "2028-06-01"},
            {"doc_name": "10th Marksheet", "expiry_date": None}
        ]

        overview = engine.compute_user_schemes_overview(prof, docs, filters={"category": "ALL"}, page=1, page_size=10)
        self.assertTrue(overview.get("success"))
        self.assertIn("user", overview)
        self.assertIn("benefit_opportunity", overview)
        self.assertGreaterEqual(overview["benefit_opportunity"]["score"], 50)
        self.assertIn("ranked_schemes", overview)
        self.assertIn("all_eligible_schemes", overview)
        self.assertIn("schemes", overview)
        self.assertGreater(len(overview["all_eligible_schemes"]), 0)
        self.assertGreaterEqual(overview["total_schemes"], 10)
        self.assertGreaterEqual(overview["eligible_count"], 1)
        self.assertIn("pagination", overview)
        self.assertEqual(overview["pagination"]["page"], 1)

    def test_17_multilingual_rag_copilot_safety(self):
        """Tests RAG Copilot in English, Hindi, and Marathi with anti-hallucination source verification."""
        prof = {
            "full_name": "Rahul Sharma",
            "age": 21,
            "gender": "Male",
            "state": "Maharashtra",
            "occupation": "Student",
            "student": 1,
            "annual_income": 180000
        }
        docs = [{"doc_name": "Aadhaar Card"}]

        # 1. English Query
        en_res = engine.generate_grounded_ai_answer("What schemes am I eligible for?", prof, docs, lang="en")
        self.assertIn("eligible", en_res["answer"].lower())
        self.assertTrue(".gov.in" in en_res["official_source"] or "services.india.gov.in" in en_res["official_source"])

        # 2. Hindi Query
        hi_res = engine.generate_grounded_ai_answer("मुझे कौन सी योजनाएं मिल सकती हैं?", prof, docs, lang="hi")
        self.assertIn("योजनाओं", hi_res["answer"])
        self.assertIsNotNone(hi_res["official_source"])

        # 3. Marathi Query
        mr_res = engine.generate_grounded_ai_answer("मला कोणत्या योजना मिळतील?", prof, docs, lang="mr")
        self.assertIn("योजनांसाठी", mr_res["answer"])
        self.assertIsNotNone(mr_res["official_source"])

        # 4. Anti-hallucination verification
        fake_res = engine.generate_grounded_ai_answer("Can you give me free bitcoin cryptocurrency subsidy?", prof, docs, lang="en")
        self.assertIn("could not verify", fake_res["answer"].lower())

    def test_18_intelligent_ocr_simulation_and_cross_check(self):
        """Tests document AI / OCR simulation extracting fields and matching profile."""
        prof = {
            "full_name": "Sunita Devi",
            "state": "Maharashtra",
            "district": "Solapur",
            "annual_income": 140000,
            "land_size_acres": 2.5
        }

        # Test Income Certificate OCR
        ocr_income = engine.simulate_document_ocr("Income Certificate", prof)
        self.assertEqual(ocr_income["detected_name"], "Sunita Devi")
        self.assertEqual(ocr_income["ocr_status"], "VERIFIED & MATCHED")
        self.assertTrue(ocr_income["profile_cross_check"]["name_matched"])
        self.assertTrue(ocr_income["profile_cross_check"]["income_matched"])

        # Test 7/12 Land Record OCR
        ocr_land = engine.simulate_document_ocr("7/12 Land Record Extract", prof)
        self.assertIn("2.5 Acres", ocr_land["extracted_fields"]["landholding_acres"])
        self.assertTrue(ocr_land["profile_cross_check"]["landholding_matched"])

    def test_19_ai_form_field_explainer(self):
        """Tests simplified citizen explanation of confusing government form fields."""
        res_en = engine.explain_confusing_form_field("Annual Family Income", lang="en")
        self.assertIn("combined gross annual income", res_en["explanation"])

        res_mr = engine.explain_confusing_form_field("DBT Bank Seeding", lang="mr")
        self.assertIn("आधार पेमेंट", res_mr["explanation"])

        res_hi = engine.explain_confusing_form_field("Caste Validity Certificate", lang="hi")
        self.assertIn("जाति", res_hi["explanation"])

    def test_20_proactive_benefit_monitor(self):
        """Tests scanner for upcoming application deadlines and expiring certificates."""
        prof = {
            "user_id": "user_rahul_001",
            "state": "Maharashtra",
            "occupation": "Student",
            "student": 1,
            "annual_income": 180000
        }
        docs = [
            {"doc_name": "Income Certificate", "expiry_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")},
            {"doc_name": "Aadhaar Card", "expiry_date": None}
        ]

        notifs = engine.run_proactive_benefit_monitor("user_rahul_001", prof, docs)
        self.assertGreater(len(notifs), 0)
        has_expiry = any(n["type"] == "expiry" for n in notifs)
        self.assertTrue(has_expiry, "Proactive monitor must catch document expiring in 15 days")

    def test_21_8_stage_benefit_journey_engine(self):
        """Tests the end-to-end 8-stage benefit journey calculation."""
        scheme = engine.get_scheme_by_id("post-matric-scholarship")
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")
        apps = db.get_user_applications("user_rahul_001")

        journey = engine.compute_8_stage_benefit_journey(scheme, profile, docs, apps)
        self.assertIn("stages", journey)
        self.assertEqual(len(journey["stages"]), 8)
        self.assertGreaterEqual(journey["current_stage"], 1)
        self.assertLessEqual(journey["current_stage"], 8)
        self.assertGreaterEqual(journey["progress_pct"], 0)
        self.assertLessEqual(journey["progress_pct"], 100)

        # Stage 1 and 2 should be COMPLETED for eligible Rahul
        self.assertEqual(journey["stages"][0]["status"], "COMPLETED")
        self.assertEqual(journey["stages"][1]["status"], "COMPLETED")

    def test_22_cross_document_conflict_detection(self):
        """Tests cross-document inconsistency detection (Name mismatch, DOB mismatch)."""
        profile = {"full_name": "Rahul Shinde Patil", "annual_income": 180000}
        docs_with_conflict = [
            {
                "id": "d1",
                "doc_name": "Aadhaar Card",
                "ocr_metadata": {"detected_name": "Rahul Shinde Patil", "extracted_fields": {"dob": "2003-05-14"}}
            },
            {
                "id": "d2",
                "doc_name": "Bank Passbook with DBT Seeding",
                "ocr_metadata": {"detected_name": "Rahul S. Patil", "extracted_fields": {"dob": "2003-05-14"}}
            }
        ]

        conflicts = engine.detect_document_conflicts(docs_with_conflict, profile)
        self.assertGreater(len(conflicts), 0)
        self.assertEqual(conflicts[0]["conflict_field"], "Name Spelling")
        self.assertEqual(conflicts[0]["severity"], "WARNING")
        self.assertIn("Potential inconsistency detected", conflicts[0]["message"])

    def test_23_cross_scheme_document_reuse_optimization(self):
        """Tests mapping showing how 1 verified document unlocks multiple welfare schemes."""
        docs = [
            {"doc_name": "Aadhaar Card"},
            {"doc_name": "Income Certificate"},
            {"doc_name": "Bank Passbook with DBT Seeding"}
        ]
        all_schemes = engine.get_all_schemes()

        reuse = engine.compute_cross_scheme_document_reuse(docs, all_schemes)
        self.assertGreater(len(reuse), 0)
        aadhaar_reuse = next((r for r in reuse if r["doc_name"] == "Aadhaar Card"), None)
        self.assertIsNotNone(aadhaar_reuse)
        self.assertGreaterEqual(aadhaar_reuse["unlocked_schemes_count"], 3)
        self.assertIn(aadhaar_reuse["reuse_efficiency"].upper(), ["HIGH", "VERY HIGH"])

    def test_24_application_rejection_risk_model(self):
        """Tests pre-submission rejection-risk score and mitigation recommendations."""
        scheme = engine.get_scheme_by_id("post-matric-scholarship")
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")

        risk = engine.calculate_application_rejection_risk(scheme, profile, docs)
        self.assertIn("risk_level", risk)
        self.assertIn(risk["risk_level"], ["LOW", "MEDIUM", "HIGH"])
        self.assertIn("risk_score", risk)
        self.assertIn("mitigation_advice", risk)
        self.assertGreater(len(risk["mitigation_advice"]), 0)

    def test_25_benefit_knowledge_graph_multi_hop_traversal(self):
        """Tests Knowledge Graph entity modeling and multi-hop relationship traversals."""
        from graph_engine import knowledge_graph

        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")
        ranked = engine.rank_schemes_priority(profile, docs)

        graph = knowledge_graph.build_user_universe_graph(profile, docs, ranked)
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)
        self.assertGreater(len(graph["nodes"]), 5)
        self.assertGreater(len(graph["edges"]), 5)

        # Test multi-hop family discovery (e.g. Daughter / Sukanya Samriddhi)
        family_results = knowledge_graph.multi_hop_family_discovery(profile, engine.get_all_schemes())
        self.assertIsInstance(family_results, list)
        self.assertGreater(len(family_results), 0)
        self.assertIn("relationship_path", family_results[0])

    def test_26_scheme_versioning_and_gazette_audit(self):
        """Tests scheme historical versions, gazette tracking, and criteria changes."""
        versions = db.get_scheme_versions("post-matric-scholarship")
        self.assertGreaterEqual(len(versions), 1)
        latest_v = versions[0]
        self.assertIn("version_number", latest_v)
        self.assertIn("effective_year", latest_v)
        self.assertIn("source_url", latest_v)
        self.assertTrue(latest_v["source_url"].startswith("http"))
        self.assertIn("change_summary", latest_v)

    def test_27_grievance_ai_petition_generator(self):
        """Tests legal grievance petition draft conforming to CPGRAMS standards."""
        app_obj = {
            "ref_number": "APP-2026-NSP-8821",
            "scheme_name": "Post-Matric Scholarship for OBC Students",
            "department": "Ministry of Social Justice & Empowerment",
            "applied_date": "2026-06-15",
            "status": "Under Verification"
        }
        profile = {"full_name": "Rahul Patil", "state": "Maharashtra", "district": "Pune"}

        draft = engine.generate_grievance_draft(app_obj, profile, "Delay in Disbursal beyond SLA", "Submitted 60 days ago.")
        self.assertIn("petition_text", draft)
        self.assertIn("APP-2026-NSP-8821", draft["petition_text"])
        self.assertIn("CPGRAMS", draft["responsible_authority"])
        self.assertEqual(draft["official_portal_url"], "https://pgportal.gov.in")
        self.assertEqual(draft["sla_escalation_level"], 1)

    def test_28_government_scheme_change_detection(self):
        """Tests periodic simulated government portal change scanner."""
        changes = engine.detect_government_scheme_changes()
        self.assertIsInstance(changes, list)
        self.assertGreater(len(changes), 0)
        for ch in changes:
            self.assertIn("scheme_id", ch)
            self.assertIn("change_type", ch)
            self.assertIn("change_summary", ch)
            self.assertIn("action_required", ch)

    def test_29_citizen_benefit_twin_state_machine(self):
        """Tests derived CitizenBenefitTwin state calculation and 15-state lifecycle machine."""
        from benefit_twin import CitizenBenefitTwin, BenefitState
        twin = CitizenBenefitTwin.compute("user_rahul_001")
        self.assertIn("user_id", twin)
        self.assertIn("benefit_opportunity_score", twin)
        opp = twin["benefit_opportunity_score"]
        self.assertGreaterEqual(opp["total_score"], 50)
        self.assertIn("eligibility_potential_pct", opp)
        self.assertIn("document_readiness_pct", opp)
        self.assertIn("application_readiness_pct", opp)
        self.assertIn("scheme_states", twin)
        
        # Check that state machine transitions exist
        post_matric_state = twin["scheme_states"].get("post-matric-scholarship", {})
        self.assertIn("state", post_matric_state)
        self.assertIn(post_matric_state["state"], [BenefitState.ELIGIBLE, BenefitState.DOCUMENT_INCOMPLETE, BenefitState.APPLICATION_READY, BenefitState.SUBMITTED, BenefitState.UNDER_REVIEW])

    def test_30_event_driven_selective_recalculation(self):
        """Tests event-driven selective dependency recalculation and audit logging."""
        from benefit_twin import handle_benefit_twin_event
        res = handle_benefit_twin_event("user_rahul_001", "INCOME_CHANGED", {"new_income": 220000})
        self.assertEqual(res["status"], "PROCESSED")
        self.assertIn("IncomeThresholdRule", res["affected_nodes"])
        self.assertGreater(res["execution_time_ms"], 0.0)
        events = db.get_benefit_twin_events("user_rahul_001")
        self.assertGreaterEqual(len(events), 1)

    def test_31_explainable_decision_trace_evaluation(self):
        """Tests deterministic machine-readable decision traces for scheme eligibility."""
        from benefit_twin import generate_decision_trace
        scheme = engine.get_scheme_by_id("post-matric-scholarship")
        profile = db.get_user_profile("user_rahul_001")
        docs = db.get_user_documents("user_rahul_001")
        trace = generate_decision_trace(scheme, profile, docs)
        self.assertIn("rules_evaluated", trace)
        self.assertGreater(len(trace["rules_evaluated"]), 3)
        self.assertTrue(any(r["verdict"] == "PASS" for r in trace["rules_evaluated"]))
        self.assertIn("why_eligible_summary", trace)

    def test_32_scenario_what_if_simulation_without_side_effects(self):
        """Tests What-If Scenario simulation on cloned Twin without persistent side-effects."""
        from scenario_simulator import simulate_what_if
        profile_before = db.get_user_profile("user_rahul_001")
        income_before = profile_before.get("annual_income")

        sim = simulate_what_if("user_rahul_001", {"annual_income": 400000}, "High Income Test")
        self.assertTrue(sim["is_simulated"])
        self.assertIn("summary", sim)
        self.assertIn("financial_delta", sim["summary"])

        # Confirm real profile has NOT been mutated
        profile_after = db.get_user_profile("user_rahul_001")
        self.assertEqual(profile_after.get("annual_income"), income_before)

    def test_33_admin_policy_change_simulator(self):
        """Tests Admin Government Policy Change demographic and budget simulation."""
        impact = engine.simulate_policy_change("user_rahul_001", "post-matric-scholarship", {"max_income": 250000}, {"max_income": 350000})
        self.assertIn("total_citizens_evaluated", impact)
        self.assertIn("newly_eligible_count", impact)
        self.assertIn("estimated_annual_budget_impact", impact)
        self.assertIn("policy_recommendation", impact)

    def test_34_research_metrics_and_baseline_comparison(self):
        """Tests empirical benchmark metrics and static vs dynamic architecture comparison."""
        from research_metrics import get_evaluation_metrics, get_baseline_comparison
        metrics = get_evaluation_metrics()
        self.assertIn("eligibility_accuracy", metrics["metrics"])
        self.assertGreaterEqual(metrics["metrics"]["eligibility_accuracy"]["score"], 95.0)

        comp = get_baseline_comparison()
        self.assertIn("dimensions", comp)
        self.assertGreaterEqual(len(comp["dimensions"]), 5)

    def test_35_reproducible_patent_4_step_demonstration(self):
        """
        Executes the complete 4-step patent demonstration workflow:
        Step 1: Student missing Domicile -> 4 schemes blocked
        Step 2: Upload Domicile -> Document graph updated, schemes unlocked
        Step 3: What-If simulation (Income ₹3.1L) -> Ripple calculated
        Step 4: Admin changes rule (₹2.5L -> ₹3.0L) -> Selective citizen recalculation
        """
        from benefit_twin import CitizenBenefitTwin
        from scenario_simulator import simulate_what_if

        # Step 1: Baseline Student with missing Domicile
        prof = {"user_id": "user_rahul_001", "full_name": "Test Student", "state": "Maharashtra", "annual_income": 240000, "occupation": "Student", "caste_category": "OBC", "age": 20}
        docs_step1 = [{"doc_name": "Aadhaar Card", "validity_status": "Valid"}]
        twin1 = CitizenBenefitTwin.compute("user_rahul_001", prof, docs_step1, [])
        incomplete_count_1 = twin1["scheme_states_summary"]["document_incomplete_count"]
        self.assertGreaterEqual(incomplete_count_1, 2)

        # Step 2: Upload Domicile Certificate and supporting documents
        docs_step2 = [
            {"doc_name": "Aadhaar Card", "validity_status": "Valid"},
            {"doc_name": "Domicile Certificate", "validity_status": "Valid"},
            {"doc_name": "Income Certificate", "validity_status": "Valid"},
            {"doc_name": "Caste Certificate", "validity_status": "Valid"},
            {"doc_name": "Bank Passbook with DBT Seeding", "validity_status": "Valid"},
            {"doc_name": "Previous Year Marksheet", "validity_status": "Valid"},
            {"doc_name": "College Admission Fee Receipt", "validity_status": "Valid"},
            {"doc_name": "Bonafide Student Certificate", "validity_status": "Valid"},
            {"doc_name": "Class 10th & 12th Marksheet", "validity_status": "Valid"},
            {"doc_name": "Passport Size Photographs", "validity_status": "Valid"}
        ]
        twin2 = CitizenBenefitTwin.compute("user_rahul_001", prof, docs_step2, [])
        ready_count_2 = twin2["scheme_states_summary"]["ready_to_apply_count"]
        self.assertGreater(ready_count_2, twin1["scheme_states_summary"]["ready_to_apply_count"])

        # Step 3: What-If Simulation (Income ₹3.1 Lakh)
        sim_res = simulate_what_if("user_rahul_001", {"annual_income": 310000}, "Patent Step 3 Test")
        self.assertIn("newly_available_count", sim_res["summary"])

        # Step 4: Admin Policy Change Simulation
        pol_res = engine.simulate_policy_change("user_rahul_001", "post-matric-scholarship", {"max_income": 250000}, {"max_income": 300000})
        self.assertGreaterEqual(pol_res["total_citizens_evaluated"], 1)

if __name__ == '__main__':
    unittest.main()

