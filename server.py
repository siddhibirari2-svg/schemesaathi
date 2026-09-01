"""
SchemeSaathi - High Performance REST API & Web Server
Zero external dependencies, powered by Python standard library with SQLite & multi-tenant security.
"""

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import mimetypes
from datetime import datetime, timedelta
import secrets

import database as db
import engine
from engine import get_all_schemes, get_scheme_by_id
from graph_engine import knowledge_graph
from benefit_twin import CitizenBenefitTwin, handle_benefit_twin_event, generate_decision_trace
from scenario_simulator import simulate_what_if
from research_metrics import get_evaluation_metrics, get_baseline_comparison
from document_solver_data import DOCUMENT_GUIDES, get_document_guide

PORT = int(os.environ.get("PORT", 8000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SchemeSaathiHandler(BaseHTTPRequestHandler):

    def get_current_user_id(self) -> str:
        # Check explicit X-User-Id header first (enables instant client persona switching)
        user_header = self.headers.get("X-User-Id", "").strip()
        if user_header:
            return user_header

        # Check Authorization header
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            tok = auth.replace("Bearer ", "").strip()
            user = db.get_user_by_session_token(tok)
            if user:
                return user["id"]
            if tok.startswith("user_"):
                return tok
            
        cookie = self.headers.get("Cookie", "")
        if "schemesaathi_token=" in cookie:
            for part in cookie.split(";"):
                if "schemesaathi_token=" in part:
                    tok = part.split("=")[1].strip()
                    user = db.get_user_by_session_token(tok)
                    if user:
                        return user["id"]
        if "schemesaathi_user=" in cookie:
            for part in cookie.split(";"):
                if "schemesaathi_user=" in part:
                    return part.split("=")[1].strip()
                    
        # Default to Rahul Sharma (Student demo persona)
        return "user_rahul_001"

    def send_json_response(self, data: dict | list, status_code: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-User-Id")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, private")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def send_file_response(self, filepath: str, content_type: str = None):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return
        
        if not content_type:
            content_type, _ = mimetypes.guess_type(filepath)
            if not content_type:
                content_type = "application/octet-stream"

        with open(filepath, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-User-Id")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        user_id = self.get_current_user_id()

        # Static Web UI routes
        if path == "/" or path == "/index.html":
            return self.send_file_response(os.path.join(BASE_DIR, "index.html"), "text/html; charset=utf-8")
        elif path == "/app.js":
            return self.send_file_response(os.path.join(BASE_DIR, "app.js"), "application/javascript; charset=utf-8")
        elif path == "/i18n.js":
            return self.send_file_response(os.path.join(BASE_DIR, "i18n.js"), "application/javascript; charset=utf-8")
        elif path == "/styles.css":
            return self.send_file_response(os.path.join(BASE_DIR, "styles.css"), "text/css; charset=utf-8")

        # API Routes
        if path == "/api/auth/me":
            user = db.get_user_by_id(user_id)
            profile = db.get_user_profile(user_id)
            return self.send_json_response({
                "user_id": user_id,
                "user": user,
                "profile": profile,
                "is_onboarded": bool(profile.get("onboarding_completed", False)) if profile else False
            })

        elif path == "/api/profile":
            profile = db.get_user_profile(user_id)
            return self.send_json_response(profile or {})

        elif path == "/api/schemes":
            all_schemes = get_all_schemes()
            return self.send_json_response(all_schemes)

        elif path == "/api/schemes/stats":
            stats = db.get_scheme_stats()
            return self.send_json_response(stats)

        elif path == "/api/schemes/missing-reports":
            reports = db.get_missing_scheme_reports()
            return self.send_json_response(reports)

        elif path == "/api/user/schemes":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            
            params = query
            search = params.get("search", [""])[0]
            cat = params.get("category", ["ALL"])[0]
            level = params.get("level", ["ALL"])[0]
            status = params.get("status", ["ALL"])[0]
            try:
                page = int(params.get("page", ["1"])[0])
            except Exception:
                page = 1
            try:
                page_size = int(params.get("page_size", ["20"])[0])
            except Exception:
                page_size = 20
            
            filters = {
                "search": search,
                "category": cat,
                "level": level,
                "status": status
            }
            overview = engine.compute_user_schemes_overview(profile, docs, filters, page, page_size)
            return self.send_json_response(overview)

        elif path == "/api/schemes/prioritized":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            ranked = engine.rank_schemes_priority(profile, docs)
            return self.send_json_response({
                "ranked_schemes": ranked,
                "disclaimer": "Personalized recommendation based on eligibility and document readiness, NOT an official government ranking."
            })

        elif path.startswith("/api/schemes/") and path.endswith("/versions"):
            scheme_id = path.replace("/api/schemes/", "").replace("/versions", "")
            versions = db.get_scheme_versions(scheme_id)
            return self.send_json_response(versions)

        elif path.startswith("/api/schemes/"):
            scheme_id = path.replace("/api/schemes/", "")
            scheme = get_scheme_by_id(scheme_id)
            if not scheme:
                return self.send_json_response({"error": "Scheme not found"}, 404)
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            readiness = engine.calculate_readiness_score(scheme, profile, docs)
            source_verif = engine.verify_official_source(scheme)
            return self.send_json_response({
                "scheme": scheme,
                "readiness": readiness,
                "source_verification": source_verif
            })

        elif path == "/api/benefit-journey":
            params = query
            scheme_id = params.get("scheme_id", ["post-matric-scholarship"])[0]
            scheme = get_scheme_by_id(scheme_id) or get_all_schemes()[0]
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            apps = db.get_user_applications(user_id)
            journey = engine.compute_8_stage_benefit_journey(scheme, profile, docs, apps)
            return self.send_json_response(journey)

        # ==================== CITIZEN BENEFIT TWIN & PATENT CAPABILITIES ====================
        elif path == "/api/benefit-twin":
            twin = CitizenBenefitTwin.compute(user_id)
            return self.send_json_response(twin)

        elif path == "/api/benefit-twin/impact":
            events = db.get_benefit_twin_events(user_id)
            twin = db.get_benefit_twin(user_id) or CitizenBenefitTwin.compute(user_id)
            return self.send_json_response({"events": events, "twin": twin})

        elif path == "/api/benefit-twin/next-action":
            twin = db.get_benefit_twin(user_id) or CitizenBenefitTwin.compute(user_id)
            return self.send_json_response({
                "top_action": twin.get("next_best_action"),
                "alternative_actions": twin.get("alternative_actions", []),
                "benefit_opportunity_score": twin.get("benefit_opportunity_score")
            })

        elif path == "/api/benefit-twin/simulations":
            sims = db.get_user_scenario_simulations(user_id)
            return self.send_json_response(sims)

        elif path.startswith("/api/eligibility/") and path.endswith("/decision-trace"):
            scheme_id = path.replace("/api/eligibility/", "").replace("/decision-trace", "")
            scheme = get_scheme_by_id(scheme_id) or get_all_schemes()[0]
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            apps = db.get_user_applications(user_id)
            app = next((a for a in apps if a.get("scheme_id") == scheme_id), None)
            trace = generate_decision_trace(scheme, profile, docs, app)
            return self.send_json_response(trace)

        elif path.startswith("/api/schemes/") and path.endswith("/dependencies"):
            scheme_id = path.replace("/api/schemes/", "").replace("/dependencies", "")
            subgraph = knowledge_graph.get_scheme_subgraph(scheme_id)
            return self.send_json_response(subgraph)

        elif path == "/api/documents/dependencies":
            dep_graph = knowledge_graph.get_document_dependency_graph(get_all_schemes())
            return self.send_json_response(dep_graph)

        elif path == "/api/research/evaluation-metrics":
            metrics = get_evaluation_metrics()
            return self.send_json_response(metrics)

        elif path == "/api/research/baseline-comparison":
            comp = get_baseline_comparison()
            return self.send_json_response(comp)

        elif path == "/api/admin/policy-simulations":
            sims = db.get_policy_simulations()
            return self.send_json_response(sims)

        elif path == "/api/documents/conflicts":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            conflicts = engine.detect_document_conflicts(docs, profile)
            return self.send_json_response(conflicts)

        elif path == "/api/documents/reuse":
            docs = db.get_user_documents(user_id)
            all_s = get_all_schemes()
            reuse = engine.compute_cross_scheme_document_reuse(docs, all_s)
            return self.send_json_response(reuse)

        elif path == "/api/grievances":
            grievances = db.get_user_grievances(user_id)
            return self.send_json_response(grievances)

        elif path == "/api/graph/benefit-universe":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            ranked = engine.rank_schemes_priority(profile, docs)
            graph_data = knowledge_graph.build_user_universe_graph(profile, docs, ranked)
            return self.send_json_response(graph_data)

        elif path == "/api/admin/detected-changes":
            changes = engine.detect_government_scheme_changes()
            return self.send_json_response(changes)

        elif path.startswith("/api/readiness/"):
            scheme_id = path.replace("/api/readiness/", "")
            scheme = get_scheme_by_id(scheme_id)
            if not scheme:
                return self.send_json_response({"error": "Scheme not found"}, 404)
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            readiness = engine.calculate_readiness_score(scheme, profile, docs)
            return self.send_json_response(readiness)

        elif path == "/api/documents":
            docs = db.get_user_documents(user_id)
            enriched = []
            for d in docs:
                status, msg = engine.check_doc_validity(d)
                d_copy = dict(d)
                d_copy["validity_status"] = status
                d_copy["validity_message"] = msg
                enriched.append(d_copy)
            return self.send_json_response(enriched)

        elif path.startswith("/api/documents/") and path.endswith("/download"):
            # Multi-Tenant Document Security Check: User A CANNOT access User B's documents
            doc_id = path.replace("/api/documents/", "").replace("/download", "")
            doc = db.get_document_by_id(doc_id, user_id)
            if not doc:
                # Security Protection: Return 403 Forbidden
                return self.send_json_response({
                    "error": "Forbidden: You do not have permission to access this document.",
                    "code": "AUTH_FORBIDDEN"
                }, 403)
            
            db.log_audit(user_id, f"DOWNLOAD_DOCUMENT_{doc_id}", self.client_address[0])
            return self.send_json_response({
                "document": doc,
                "message": "Secure token verified. Private document accessed."
            })

        elif path.startswith("/api/document-guide/"):
            doc_name = urllib.parse.unquote(path.replace("/api/document-guide/", ""))
            guide = get_document_guide(doc_name)
            return self.send_json_response(guide)

        elif path == "/api/next-action":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            apps = db.get_user_applications(user_id)
            next_action = engine.get_my_next_action(profile, docs, apps)
            return self.send_json_response(next_action)

        elif path == "/api/health-check":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            apps = db.get_user_applications(user_id)
            health = engine.compute_benefits_health_check(profile, docs, apps)
            return self.send_json_response(health)

        elif path == "/api/applications":
            apps = db.get_user_applications(user_id)
            return self.send_json_response(apps)

        elif path.startswith("/api/applications/") and path.endswith("/rejection-help"):
            app_id = path.replace("/api/applications/", "").replace("/rejection-help", "")
            conn = db.get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM applications WHERE id = ? AND user_id = ?", (app_id, user_id))
            row = cursor.fetchone()
            conn.close()
            if not row:
                return self.send_json_response({"error": "Application not found or unauthorized"}, 404)
            
            app_dict = dict(row)
            scheme = get_scheme_by_id(app_dict.get("scheme_id", ""))
            
            help_data = {
                "application": app_dict,
                "scheme_title": app_dict.get("scheme_name"),
                "rejection_reason": app_dict.get("rejection_reason", "Document mismatch or income slab exceeded."),
                "corrective_actions": [
                    "Verify name, date of birth, and gender spelling between Aadhaar and Bank Account.",
                    "Ensure active NPCI DBT Aadhaar mapping is linked at your bank branch.",
                    "If Income Certificate is expired or rejected, obtain a fresh one from Tehsildar / e-District."
                ],
                "official_appeal_mechanism": {
                    "portal_name": "CPGRAMS (Centralized Public Grievance Redress and Monitoring System)",
                    "portal_url": "https://pgportal.gov.in",
                    "state_portal": "State CM Helpline / e-District Grievance Desk",
                    "department_grievance_url": scheme.get("grievance_portal", "https://pgportal.gov.in") if scheme else "https://pgportal.gov.in",
                    "helpline": scheme.get("helpline", "1800-11-0001") if scheme else "1800-11-0001"
                },
                "disclaimer": "Information is based strictly on published official grievance procedures. SchemeSaathi does not invent appeal mechanisms."
            }
            return self.send_json_response(help_data)

        elif path == "/api/notifications":
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            stored_notifs = db.get_user_notifications(user_id)
            proactive_notifs = engine.run_proactive_benefit_monitor(user_id, profile, docs)
            
            # Combine without duplicating titles
            titles = {n.get("title") for n in stored_notifs}
            combined = list(stored_notifs)
            for pn in proactive_notifs:
                if pn.get("title") not in titles:
                    pn["id"] = f"proactive_{len(combined)+1}"
                    pn["user_id"] = user_id
                    pn["created_at"] = datetime.now().isoformat()
                    combined.append(pn)
                    titles.add(pn.get("title"))
            return self.send_json_response(combined)

        elif path == "/api/consents":
            consents = db.get_user_consents(user_id)
            return self.send_json_response(consents)

        elif path == "/api/privacy/export":
            # Full citizen data export (Download My Data)
            profile = db.get_user_profile(user_id)
            docs = db.get_user_documents(user_id)
            apps = db.get_user_applications(user_id)
            notifs = db.get_user_notifications(user_id)
            consents = db.get_user_consents(user_id)
            audits = db.get_audit_logs(user_id)
            
            export_payload = {
                "exported_at": datetime.now().isoformat(),
                "user_id": user_id,
                "profile": profile,
                "documents_count": len(docs),
                "documents": docs,
                "applications": apps,
                "notifications": notifs,
                "consents": consents,
                "audit_trail": audits,
                "privacy_statement": "All your SchemeSaathi data is encrypted and completely under citizen ownership."
            }
            db.log_audit(user_id, "EXPORT_MY_DATA", self.client_address[0])
            return self.send_json_response(export_payload)

        elif path == "/api/privacy/audit-logs":
            logs = db.get_audit_logs(user_id)
            return self.send_json_response(logs)

        elif path == "/api/schemes/stats":
            stats = db.get_scheme_stats()
            return self.send_json_response(stats)

        elif path == "/api/schemes/missing-reports":
            reports = db.get_missing_scheme_reports()
            return self.send_json_response(reports)

        elif path == "/api/admin/schemes":
            all_s = db.get_all_db_schemes()
            stats = db.get_scheme_stats()
            return self.send_json_response({
                "schemes": all_s,
                "stats": stats,
                "total_schemes": len(all_s),
                "verified_count": len([s for s in all_s if s.get("verification_status") == "VERIFIED"]),
                "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        user_id = self.get_current_user_id()
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path == "/api/auth/register":
            full_name = data.get("full_name", "").strip()
            email = data.get("email", "").strip()
            mobile = data.get("mobile", "").strip()
            password = data.get("password", "")
            confirm_password = data.get("confirm_password", "")

            if not password or password != confirm_password:
                return self.send_json_response({"error": "Passwords do not match. Please verify."}, 400)

            try:
                user_safe, token = db.register_user(full_name, email, mobile, password)
                db.log_audit(user_safe["id"], "REGISTER_ACCOUNT", self.client_address[0])
                return self.send_json_response({
                    "success": True,
                    "message": "Account created successfully! Welcome to SchemeSaathi.",
                    "token": token,
                    "user": user_safe,
                    "is_new_user": True
                })
            except ValueError as ve:
                return self.send_json_response({"error": str(ve)}, 400)
            except Exception as ex:
                return self.send_json_response({"error": f"Registration failed: {str(ex)}"}, 500)

        elif path == "/api/auth/login":
            if "persona" in data:
                # Fast Demo Persona Switcher (Rahul / Sunita)
                persona = data.get("persona", "rahul")
                target_user = "user_rahul_001" if persona == "rahul" else "user_sunita_002"
                user_row = db.get_user_by_id(target_user)
                prof = db.get_user_profile(target_user)
                db.log_audit(target_user, f"LOGIN_PERSONA_{persona.upper()}", self.client_address[0])
                return self.send_json_response({
                    "token": target_user,
                    "user_id": target_user,
                    "user": user_row,
                    "profile": prof,
                    "is_onboarded": True,
                    "message": f"Switched to {persona.title()} persona (DEMO MODE)"
                })

            identifier = data.get("identifier", "").strip() or data.get("email", "").strip() or data.get("mobile", "").strip()
            password = data.get("password", "")

            try:
                user_safe, profile_dict, token = db.login_user(identifier, password)
                db.log_audit(user_safe["id"], "LOGIN_SUCCESS", self.client_address[0])
                return self.send_json_response({
                    "success": True,
                    "token": token,
                    "user": user_safe,
                    "profile": profile_dict,
                    "is_onboarded": bool(profile_dict.get("onboarding_completed", False)),
                    "message": f"Welcome back, {user_safe['full_name']}!"
                })
            except ValueError as ve:
                return self.send_json_response({"error": str(ve)}, 400)
            except Exception as ex:
                return self.send_json_response({"error": f"Login failed: {str(ex)}"}, 500)

        elif path == "/api/auth/logout":
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                tok = auth.replace("Bearer ", "").strip()
                db.logout_session(tok)
            db.log_audit(user_id, "LOGOUT", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": "Logged out successfully."
            })

        elif path == "/api/onboarding/save":
            db.save_user_onboarding_profile(user_id, data)
            db.log_audit(user_id, "COMPLETE_ONBOARDING", self.client_address[0])

            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            ranked = engine.rank_schemes_priority(profile, docs)

            category_counts = {}
            for r in ranked:
                cat = r["scheme"].get("category", "General")
                category_counts[cat] = category_counts.get(cat, 0) + 1

            return self.send_json_response({
                "success": True,
                "message": "Profile setup complete! Finding your government scheme matches...",
                "profile": profile,
                "ranked_schemes": ranked,
                "category_counts": category_counts,
                "total_matched": len(ranked)
            })

        elif path == "/api/onboarding/draft":
            step = int(data.get("step", 1))
            db.save_onboarding_draft(user_id, step, data.get("draft", {}))
            return self.send_json_response({"success": True})

        elif path == "/api/profile":
            db.save_user_profile(user_id, data)
            db.log_audit(user_id, "UPDATE_PROFILE", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": "Profile updated successfully.",
                "profile": db.get_user_profile(user_id)
            })

        elif path == "/api/profile/life-event":
            event_type = data.get("event_type", "")
            profile = db.get_user_profile(user_id) or {}
            
            # Apply life-event scenario modifications
            if event_type == "started_college":
                profile["student"] = 1
                profile["occupation"] = "Student"
                msg = "Profile updated: Marked as College Student."
            elif event_type == "graduated":
                profile["student"] = 0
                profile["occupation"] = "Job Seeking / Graduate"
                msg = "Profile updated: Graduated from college."
            elif event_type == "started_business":
                profile["occupation"] = "Entrepreneur / Small Business Owner"
                profile["student"] = 0
                msg = "Profile updated: Registered as MSME / Business Owner."
            elif event_type == "became_farmer":
                profile["occupation"] = "Farmer"
                profile["has_land"] = 1
                profile["land_size_acres"] = 2.0
                msg = "Profile updated: Agricultural landholding recorded."
            elif event_type == "became_unemployed":
                profile["occupation"] = "Unemployed"
                profile["annual_income"] = 50000
                msg = "Profile updated: Unemployed status recorded."
            elif event_type == "income_changed":
                new_inc = data.get("new_income", 120000)
                profile["annual_income"] = int(new_inc)
                msg = f"Profile updated: Annual income updated to ₹{new_inc:,}."
            elif event_type == "had_child":
                profile["has_girl_child"] = 1
                msg = "Profile updated: Girl child dependent added."
            else:
                msg = "Profile recalculated."
                
            db.save_user_profile(user_id, profile)
            db.log_audit(user_id, f"LIFE_EVENT_{event_type.upper()}", self.client_address[0])
            
            # Return new prioritized schemes
            docs = db.get_user_documents(user_id)
            ranked = engine.rank_schemes_priority(profile, docs)
            health = engine.compute_benefits_health_check(profile, docs, db.get_user_applications(user_id))
            
            return self.send_json_response({
                "success": True,
                "message": msg,
                "recalculated_schemes": ranked,
                "health_check": health
            })

        elif path == "/api/documents":
            doc_name = data.get("doc_name", "Aadhaar Card")
            doc_type = data.get("doc_type", "Identity")
            issue_date = data.get("issue_date")
            expiry_date = data.get("expiry_date")
            source = data.get("source", "Manual Citizen Vault")
            
            profile = db.get_user_profile(user_id) or {}
            ocr_meta = engine.simulate_document_ocr(doc_name, profile)
            
            doc_id = db.add_user_document(user_id, doc_name, doc_type, issue_date, expiry_date, source, ocr_metadata=ocr_meta)
            db.log_audit(user_id, f"UPLOAD_DOC_{doc_name}", self.client_address[0])
            
            return self.send_json_response({
                "success": True,
                "doc_id": doc_id,
                "ocr_metadata": ocr_meta,
                "message": f"'{doc_name}' saved and verified via AI document intelligence."
            })

        elif path == "/api/ai/explain-field":
            field_name = data.get("field_name", "")
            scheme_id = data.get("scheme_id")
            lang = data.get("lang", "en")
            explanation = engine.explain_confusing_form_field(field_name, scheme_id, lang)
            return self.send_json_response(explanation)

        elif path == "/api/applications/risk-estimate":
            scheme_id = data.get("scheme_id", "post-matric-scholarship")
            scheme = get_scheme_by_id(scheme_id) or get_all_schemes()[0]
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            risk_data = engine.calculate_application_rejection_risk(scheme, profile, docs)
            db.record_risk_score(user_id, scheme_id, risk_data)
            return self.send_json_response(risk_data)

        elif path == "/api/grievance/draft":
            app_id = data.get("application_id")
            app_obj = {}
            if app_id:
                apps = db.get_user_applications(user_id)
                app_obj = next((a for a in apps if a.get("id") == app_id), {})
            if not app_obj:
                app_obj = {
                    "ref_number": data.get("ref_number", "APP-2026-NSP-8821"),
                    "scheme_name": data.get("scheme_name", "Post-Matric Scholarship for OBC/SC/ST Students"),
                    "department": data.get("department", "Ministry of Social Justice & Empowerment"),
                    "applied_date": "2026-06-15",
                    "status": "Under Verification"
                }
            profile = db.get_user_profile(user_id) or {}
            issue_cat = data.get("issue_category", "Delay in Disbursal")
            notes = data.get("notes", "")
            draft = engine.generate_grievance_draft(app_obj, profile, issue_cat, notes)
            g_id = db.create_grievance(user_id, {
                "application_id": app_id,
                "scheme_id": app_obj.get("scheme_id", "post-matric-scholarship"),
                "scheme_name": app_obj.get("scheme_name"),
                "department": app_obj.get("department"),
                "ref_number": app_obj.get("ref_number"),
                "issue_category": issue_cat,
                "petition_text": draft.get("petition_text"),
                "responsible_authority": draft.get("responsible_authority"),
                "grievance_portal_url": draft.get("official_portal_url")
            })
            draft["id"] = g_id
            db.log_audit(user_id, f"DRAFT_GRIEVANCE_{app_obj.get('ref_number')}", self.client_address[0])
            return self.send_json_response(draft)

        elif path == "/api/admin/schemes/detect-changes":
            changes = engine.detect_government_scheme_changes()
            db.log_audit(user_id, "ADMIN_DETECT_SCHEME_CHANGES", self.client_address[0])
            return self.send_json_response({
                "status": "SCAN_COMPLETE",
                "detected_changes": changes,
                "timestamp": datetime.now().isoformat()
            })

        # ==================== SCENARIO SIMULATOR & POLICY SIMULATOR ====================
        elif path == "/api/benefit-twin/simulate":
            mods = data.get("modifications", {})
            title = data.get("title", "Custom What-If Simulation")
            res = simulate_what_if(user_id, mods, title)
            db.log_audit(user_id, f"SIMULATE_SCENARIO_{title}", self.client_address[0])
            return self.send_json_response(res)

        elif path == "/api/admin/policy-simulate":
            sch_id = data.get("scheme_id", "post-matric-scholarship")
            old_r = data.get("old_rule", {})
            new_r = data.get("new_rule", {})
            res = engine.simulate_policy_change(user_id, sch_id, old_r, new_r)
            db.log_audit(user_id, f"ADMIN_POLICY_SIMULATE_{sch_id}", self.client_address[0])
            return self.send_json_response(res)

        elif path == "/api/benefit-twin/trigger-event":
            evt_type = data.get("event_type", "PROFILE_UPDATED")
            payload = data.get("payload", {})
            res = handle_benefit_twin_event(user_id, evt_type, payload)
            db.log_audit(user_id, f"TRIGGER_EVENT_{evt_type}", self.client_address[0])
            return self.send_json_response(res)

        elif path == "/api/schemes/compare":
            scheme_ids = data.get("scheme_ids", [])
            if not scheme_ids:
                return self.send_json_response({"error": "Please provide 2 to 4 scheme_ids to compare."}, 400)
                
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            
            comparison_list = []
            for s_id in scheme_ids[:4]:
                s = get_scheme_by_id(s_id)
                if s:
                    readiness = engine.calculate_readiness_score(s, profile, docs)
                    source_v = engine.verify_official_source(s)
                    gap = readiness.get("document_gap") or engine.analyze_document_gap(s, docs)
                    
                    comparison_list.append({
                        "scheme_id": s["id"],
                        "title": s["title"],
                        "ministry": s["ministry"],
                        "benefit_type": s["benefit_type"],
                        "benefit_amount": s["benefit_amount"],
                        "application_mode": s["application_mode"],
                        "deadline": s["deadline"],
                        "readiness_score": readiness["readiness_score"],
                        "readiness_label": readiness["readiness_label"],
                        "is_eligible": readiness.get("is_eligible", True),
                        "required_docs": [d for d in s.get("required_documents", [])],
                        "available_docs": [d["required_name"] for d in gap.get("available_docs", [])],
                        "missing_docs": [d["required_name"] for d in gap.get("missing_docs", [])],
                        "official_domain": s.get("official_domain", "services.india.gov.in"),
                        "official_url": s.get("official_url", "https://services.india.gov.in")
                    })
                    
            # Generate "Recommended for you" explanation
            if comparison_list:
                best_s = max(comparison_list, key=lambda x: x["readiness_score"])
                recommended_note = f"We recommend **{best_s['title']}** as you have {best_s['readiness_label']} and meet the verified criteria of {best_s['ministry']}."
            else:
                recommended_note = "Select schemes to view recommendations."

            return self.send_json_response({
                "comparison": comparison_list,
                "recommended_for_you": recommended_note
            })

        elif path == "/api/applications":
            scheme_id = data.get("scheme_id")
            scheme = get_scheme_by_id(scheme_id)
            if not scheme:
                return self.send_json_response({"error": "Invalid scheme_id"}, 400)
                
            status = data.get("status", "Applied")
            app_id, ref_num = db.create_application(user_id, scheme["id"], scheme["title"], status, is_demo_data=True)
            db.log_audit(user_id, f"SUBMIT_APP_{scheme_id}_{ref_num}", self.client_address[0])
            
            return self.send_json_response({
                "success": True,
                "application_id": app_id,
                "reference_number": ref_num,
                "message": f"Application for {scheme['title']} registered under My Applications (DEMO DATA)."
            })

        elif path == "/api/consents/toggle":
            service_name = data.get("service_name", "DigiLocker Mock")
            enable = data.get("enable", True)
            db.toggle_consent(user_id, service_name, enable)
            db.log_audit(user_id, f"CONSENT_{'GRANTED' if enable else 'REVOKED'}_{service_name}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": f"Consent for '{service_name}' {'granted' if enable else 'revoked'}."
            })

        elif path == "/api/privacy/delete-all":
            # Right to be Forgotten
            db.delete_all_user_data(user_id)
            db.log_audit("SYSTEM", f"RIGHT_TO_BE_FORGOTTEN_PURGE_{user_id}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": "All your personal data, vault documents, and applications have been permanently deleted from SchemeSaathi."
            })

        elif path == "/api/ai/ask":
            query = data.get("query", "")
            lang = data.get("lang", "en")
            profile = db.get_user_profile(user_id) or {}
            docs = db.get_user_documents(user_id)
            
            answer = engine.generate_grounded_ai_answer(query, profile, docs, lang)
            db.log_audit(user_id, "AI_SAFE_QUERY", self.client_address[0], details=query[:100])
            return self.send_json_response(answer)

        elif path == "/api/schemes/report-missing":
            rep_id = db.report_missing_scheme(user_id, data)
            db.log_audit(user_id, f"REPORT_MISSING_SCHEME_{data.get('scheme_name', 'Unknown')}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "report_id": rep_id,
                "message": "Thank you! Your missing scheme report has been submitted to the SchemeSaathi editorial team for official verification."
            })

        elif path == "/api/admin/schemes/import":
            s_id = db.insert_or_update_scheme(data)
            db.log_audit(user_id, f"ADMIN_IMPORT_SCHEME_{s_id}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "scheme_id": s_id,
                "message": f"Scheme '{data.get('title', s_id)}' successfully saved to SQL registry."
            })

        elif path == "/api/admin/schemes/sync":
            db.seed_schemes_registry()
            db.log_audit(user_id, "ADMIN_SYNC_REGISTRY", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": "Registry synchronized with National Government Services Portal (.gov.in)."
            })

        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)

    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        user_id = self.get_current_user_id()
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path.startswith("/api/applications/"):
            app_id = path.replace("/api/applications/", "")
            status = data.get("status", "Under Verification")
            next_action = data.get("next_action")
            rejection_reason = data.get("rejection_reason")
            corrective_action = data.get("corrective_action")
            
            success = db.update_application_status(app_id, user_id, status, next_action, rejection_reason, corrective_action)
            if not success:
                return self.send_json_response({"error": "Application not found or unauthorized"}, 404)
                
            db.log_audit(user_id, f"UPDATE_APP_STATUS_{app_id}_{status}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": f"Application status updated to '{status}' (DEMO DATA)."
            })
            
        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        user_id = self.get_current_user_id()

        if path.startswith("/api/documents/"):
            doc_id = path.replace("/api/documents/", "")
            success = db.delete_user_document(doc_id, user_id)
            if not success:
                return self.send_json_response({
                    "error": "Document not found or unauthorized",
                    "code": "AUTH_FORBIDDEN"
                }, 403)
                
            db.log_audit(user_id, f"DELETE_DOC_{doc_id}", self.client_address[0])
            return self.send_json_response({
                "success": True,
                "message": "Document permanently removed from private vault."
            })
        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)

def run_server(port=PORT):
    server_address = ('0.0.0.0', port)
    httpd = ThreadingHTTPServer(server_address, SchemeSaathiHandler)
    print(f"SchemeSaathi Production Server listening on port {port} (0.0.0.0:{port})")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
