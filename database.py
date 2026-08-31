"""
SchemeSaathi - Scalable Government Scheme Registry & Multi-Tenant Database Manager
Uses SQLite with normalized scheme registry, citizen audit trails, and strict tenant isolation.
"""

import sqlite3
import os
import hashlib
import secrets
import json
import re
from datetime import datetime, timedelta

DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "schemesaathi.db"))
DOC_VAULT_DIR = os.environ.get("DOC_VAULT_DIR", os.path.join(os.path.dirname(__file__), "private_vault"))

os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
os.makedirs(DOC_VAULT_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def validate_email(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.strip()))

def validate_mobile(mobile: str) -> bool:
    if not mobile:
        return False
    # Valid Indian mobile number: 10 digits starting with 6, 7, 8, 9
    cleaned = re.sub(r'[^0-9]', '', mobile.strip())
    return bool(re.match(r'^[6-9]\d{9}$', cleaned))

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        mobile TEXT UNIQUE,
        role TEXT DEFAULT 'citizen',
        is_onboarded BOOLEAN DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 3. Profiles Table (Rich Onboarding Attributes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        full_name TEXT,
        dob TEXT,
        age INTEGER DEFAULT 21,
        gender TEXT DEFAULT 'Male',
        state TEXT DEFAULT 'Maharashtra',
        district TEXT DEFAULT 'Pune',
        pincode TEXT,
        occupation TEXT DEFAULT 'Student',
        annual_income INTEGER DEFAULT 180000,
        caste_category TEXT DEFAULT 'OBC',
        area_type TEXT DEFAULT 'Rural',
        disability_status TEXT DEFAULT 'None',
        marital_status TEXT DEFAULT 'Single',
        education_level TEXT DEFAULT 'Higher Secondary',
        student BOOLEAN DEFAULT 0,
        course_stream TEXT,
        institution_type TEXT,
        has_land BOOLEAN DEFAULT 0,
        land_size_acres REAL DEFAULT 0,
        has_pucca_house BOOLEAN DEFAULT 0,
        has_girl_child BOOLEAN DEFAULT 0,
        family_size INTEGER DEFAULT 1,
        dependents_count INTEGER DEFAULT 0,
        senior_citizens_count INTEGER DEFAULT 0,
        has_bpl_card BOOLEAN DEFAULT 0,
        interest_categories TEXT DEFAULT '[]',
        onboarding_completed BOOLEAN DEFAULT 0,
        onboarding_step INTEGER DEFAULT 1,
        onboarding_draft TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Dynamic Column Migrations for Users & Profiles
    def _add_col_if_missing(table, col, col_type):
        try:
            cursor.execute(f"PRAGMA table_info({table})")
            cols = [r["name"] for r in cursor.fetchall()]
            if col not in cols:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
        except Exception:
            pass

    _add_col_if_missing("users", "mobile", "TEXT")
    _add_col_if_missing("users", "is_onboarded", "BOOLEAN DEFAULT 0")

    _add_col_if_missing("profiles", "dob", "TEXT")
    _add_col_if_missing("profiles", "district", "TEXT")
    _add_col_if_missing("profiles", "pincode", "TEXT")
    _add_col_if_missing("profiles", "disability_status", "TEXT DEFAULT 'None'")
    _add_col_if_missing("profiles", "marital_status", "TEXT DEFAULT 'Single'")
    _add_col_if_missing("profiles", "education_level", "TEXT")
    _add_col_if_missing("profiles", "course_stream", "TEXT")
    _add_col_if_missing("profiles", "institution_type", "TEXT")
    _add_col_if_missing("profiles", "land_size_acres", "REAL DEFAULT 0")
    _add_col_if_missing("profiles", "family_size", "INTEGER DEFAULT 1")
    _add_col_if_missing("profiles", "dependents_count", "INTEGER DEFAULT 0")
    _add_col_if_missing("profiles", "senior_citizens_count", "INTEGER DEFAULT 0")
    _add_col_if_missing("profiles", "has_bpl_card", "BOOLEAN DEFAULT 0")
    _add_col_if_missing("profiles", "interest_categories", "TEXT DEFAULT '[]'")
    _add_col_if_missing("profiles", "onboarding_completed", "BOOLEAN DEFAULT 0")
    _add_col_if_missing("profiles", "onboarding_step", "INTEGER DEFAULT 1")
    _add_col_if_missing("profiles", "onboarding_draft", "TEXT")

    _add_col_if_missing("user_documents", "ocr_metadata", "TEXT DEFAULT '{}'")
    conn.commit()

    # 4. User Documents Vault Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_documents (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        doc_name TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        file_name TEXT,
        file_path TEXT,
        issue_date TEXT,
        expiry_date TEXT,
        ocr_metadata TEXT DEFAULT '{}',
        is_verified BOOLEAN DEFAULT 1,
        source TEXT DEFAULT 'Manual Upload',
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 5. Normalized Government Scheme Registry Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schemes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        short_desc TEXT,
        detailed_desc TEXT,
        level TEXT DEFAULT 'Central',
        state TEXT DEFAULT 'All India',
        ministry TEXT,
        department TEXT,
        category TEXT,
        target_beneficiary TEXT,
        min_age INTEGER DEFAULT 0,
        max_age INTEGER DEFAULT 120,
        gender_criteria TEXT DEFAULT 'ALL',
        max_income INTEGER DEFAULT 9999999,
        social_category TEXT DEFAULT '["ALL"]',
        occupation TEXT DEFAULT '["All"]',
        area_criteria TEXT DEFAULT 'ALL',
        education_criteria TEXT DEFAULT 'None',
        disability_criteria TEXT DEFAULT 'None',
        requires_land BOOLEAN DEFAULT 0,
        requires_student BOOLEAN DEFAULT 0,
        has_girl_child BOOLEAN DEFAULT 0,
        other_conditions TEXT,
        benefit_amount TEXT,
        benefit_type TEXT,
        benefit_details TEXT,
        required_documents TEXT DEFAULT '[]',
        application_mode TEXT,
        application_process TEXT,
        official_url TEXT,
        info_url TEXT,
        official_domain TEXT,
        grievance_portal TEXT,
        helpline TEXT,
        start_date TEXT,
        deadline TEXT,
        deadline_days_left INTEGER DEFAULT 180,
        renewal_requirements TEXT,
        scheme_status TEXT DEFAULT 'ACTIVE',
        last_verified_date TEXT,
        source_authority TEXT,
        verification_status TEXT DEFAULT 'VERIFIED',
        priority_weight INTEGER DEFAULT 85,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 6. Citizen Missing Scheme Reports Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS missing_scheme_reports (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        scheme_name TEXT NOT NULL,
        department_or_ministry TEXT,
        state TEXT,
        official_link TEXT,
        description TEXT,
        status TEXT DEFAULT 'PENDING_REVIEW',
        reported_at TEXT NOT NULL
    )
    """)

    # 7. Scheme Synchronization Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheme_sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sync_source TEXT NOT NULL,
        schemes_count INTEGER,
        status TEXT,
        details TEXT,
        synced_at TEXT NOT NULL
    )
    """)

    # 8. Applications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        scheme_id TEXT NOT NULL,
        scheme_name TEXT NOT NULL,
        ref_number TEXT UNIQUE NOT NULL,
        applied_date TEXT NOT NULL,
        status TEXT NOT NULL,
        last_updated TEXT NOT NULL,
        next_action TEXT,
        rejection_reason TEXT,
        corrective_action TEXT,
        is_demo_data BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 9. Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        severity TEXT DEFAULT 'info',
        action_url TEXT,
        is_read BOOLEAN DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 10. Consent Permissions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consents (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        service_name TEXT NOT NULL,
        purpose TEXT NOT NULL,
        scopes TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        granted_at TEXT NOT NULL,
        revoked_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 11. Audit Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        action TEXT NOT NULL,
        ip_address TEXT,
        details TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    # 12. Scheme Versions Table (Change Detection & Revision Tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheme_versions (
        id TEXT PRIMARY KEY,
        scheme_id TEXT NOT NULL,
        version_number INTEGER NOT NULL,
        effective_year INTEGER DEFAULT 2026,
        source_url TEXT NOT NULL,
        source_title TEXT,
        detected_date TEXT NOT NULL,
        verified_date TEXT NOT NULL,
        verified_by_admin TEXT DEFAULT 'admin_gov_01',
        change_summary TEXT NOT NULL,
        previous_criteria TEXT DEFAULT '{}',
        new_criteria TEXT DEFAULT '{}',
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
    )
    """)

    # 13. Scheme Rules Table (Deterministic Rule Trees)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheme_rules (
        id TEXT PRIMARY KEY,
        scheme_id TEXT NOT NULL,
        rule_name TEXT NOT NULL,
        operator TEXT DEFAULT 'AND',
        condition_expression TEXT NOT NULL,
        parameters_json TEXT DEFAULT '{}',
        error_explanation TEXT NOT NULL,
        FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
    )
    """)

    # 14. Document Conflicts Table (Cross-Document Consistency Analysis)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_conflicts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        doc_id_1 TEXT NOT NULL,
        doc_id_2 TEXT NOT NULL,
        conflict_field TEXT NOT NULL,
        value_1 TEXT NOT NULL,
        value_2 TEXT NOT NULL,
        severity TEXT DEFAULT 'WARNING',
        status TEXT DEFAULT 'DETECTED',
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 15. Grievances Table (AI-Powered Citizen Grievance Assistance)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grievances (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        application_id TEXT,
        scheme_id TEXT NOT NULL,
        scheme_name TEXT NOT NULL,
        department TEXT NOT NULL,
        ref_number TEXT,
        issue_category TEXT NOT NULL,
        petition_text TEXT NOT NULL,
        responsible_authority TEXT NOT NULL,
        grievance_portal_url TEXT NOT NULL,
        escalation_level INTEGER DEFAULT 1,
        status TEXT DEFAULT 'DRAFTED',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 16. Life Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS life_events (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_date TEXT NOT NULL,
        details_json TEXT DEFAULT '{}',
        discovered_schemes_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 17. Application Risk Scores Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_scores (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        scheme_id TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        risk_score INTEGER NOT NULL,
        risk_factors TEXT DEFAULT '[]',
        mitigation_advice TEXT DEFAULT '[]',
        evaluated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 18. Family Members Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS family_members (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        relation TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        occupation TEXT,
        student BOOLEAN DEFAULT 0,
        annual_income INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 19. Citizen Benefit Twins Table (Derived Benefit State Cache)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benefit_twins (
        user_id TEXT PRIMARY KEY,
        twin_state_json TEXT NOT NULL,
        opportunity_score INTEGER DEFAULT 84,
        calculated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 20. Benefit Twin Events Table (Event-Driven Recalculation Audit Log)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benefit_twin_events (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_payload_json TEXT DEFAULT '{}',
        selective_nodes_recalculated TEXT DEFAULT '[]',
        execution_time_ms REAL DEFAULT 0.0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 21. Scenario Simulations Table (What-If Hypothetical Simulations)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scenario_simulations (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        scenario_title TEXT NOT NULL,
        parameters_json TEXT NOT NULL,
        results_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 22. Explainable Decision Traces Table (Rule Evaluation Traces)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_traces (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        scheme_id TEXT NOT NULL,
        trace_json TEXT NOT NULL,
        is_eligible BOOLEAN DEFAULT 0,
        is_ready BOOLEAN DEFAULT 0,
        evaluated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 23. Admin Policy Simulations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS policy_simulations (
        id TEXT PRIMARY KEY,
        admin_id TEXT NOT NULL,
        scheme_id TEXT,
        old_rule_json TEXT NOT NULL,
        new_rule_json TEXT NOT NULL,
        impact_summary_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    # Pre-seed verified scheme registry, versions, & demo users if not present
    seed_schemes_registry()
    seed_scheme_versions()
    seed_demo_data()

# ==================== USER AUTHENTICATION & ONBOARDING ====================

def register_user(full_name: str, email: str, mobile: str, password: str) -> tuple[dict, str]:
    """Registers a new citizen user securely with salted SHA256 password hash."""
    full_name = full_name.strip()
    email = email.strip().lower() if email else None
    mobile = re.sub(r'[^0-9]', '', mobile.strip()) if mobile else None

    if not full_name or len(full_name) < 2:
        raise ValueError("Please provide a valid full name.")
    if not validate_email(email):
        raise ValueError("Please provide a valid email address.")
    if not validate_mobile(mobile):
        raise ValueError("Please provide a valid 10-digit Indian mobile number.")
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")

    conn = get_db()
    cursor = conn.cursor()

    # Check for duplicate email
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("An account with this email address already exists. Please login instead.")

    # Check for duplicate mobile
    cursor.execute("SELECT id FROM users WHERE mobile = ?", (mobile,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("An account with this mobile number already exists. Please login instead.")

    user_id = "user_" + secrets.token_hex(6)
    pw_hash, salt = hash_password(password)
    now_str = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO users (id, username, password_hash, salt, full_name, email, mobile, role, is_onboarded, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'citizen', 0, ?)
    """, (user_id, email, pw_hash, salt, full_name, email, mobile, now_str))

    # Initialize empty profile for user with onboarding_completed = 0
    cursor.execute("""
    INSERT INTO profiles (
        user_id, full_name, dob, age, gender, state, district, pincode, occupation,
        annual_income, caste_category, area_type, disability_status, marital_status,
        education_level, student, course_stream, institution_type, has_land,
        land_size_acres, has_pucca_house, has_girl_child, family_size, dependents_count,
        senior_citizens_count, has_bpl_card, interest_categories, onboarding_completed,
        onboarding_step, updated_at
    ) VALUES (?, ?, '', 21, 'Male', 'Maharashtra', 'Pune', '', 'Student', 180000, 'General', 'Rural', 'None', 'Single', 'None', 0, '', '', 0, 0, 0, 0, 1, 0, 0, 0, '[]', 0, 1, ?)
    """, (user_id, full_name, now_str))

    # Generate session token (valid for 30 days)
    session_token = "ss_tok_" + secrets.token_hex(24)
    exp_str = (datetime.now() + timedelta(days=30)).isoformat()

    cursor.execute("""
    INSERT INTO sessions (token, user_id, created_at, expires_at)
    VALUES (?, ?, ?, ?)
    """, (session_token, user_id, now_str, exp_str))

    conn.commit()
    conn.close()

    user_safe = {
        "id": user_id,
        "full_name": full_name,
        "email": email,
        "mobile": mobile,
        "role": "citizen",
        "is_onboarded": False,
        "created_at": now_str
    }
    return user_safe, session_token

def login_user(identifier: str, password: str) -> tuple[dict, dict, str]:
    """Authenticates user via Email, Mobile number, or Username."""
    identifier = identifier.strip()
    if not identifier or not password:
        raise ValueError("Please provide your login email/mobile and password.")

    conn = get_db()
    cursor = conn.cursor()

    # Match against email, mobile, or username
    cleaned_mobile = re.sub(r'[^0-9]', '', identifier)
    cursor.execute("""
    SELECT * FROM users WHERE email = ? OR mobile = ? OR username = ?
    """, (identifier.lower(), cleaned_mobile, identifier))
    user_row = cursor.fetchone()

    if not user_row:
        conn.close()
        raise ValueError("Account not found with this email/mobile number.")

    stored_hash = user_row["password_hash"]
    stored_salt = user_row["salt"]

    check_hash, _ = hash_password(password, stored_salt)
    if check_hash != stored_hash:
        conn.close()
        raise ValueError("Incorrect password. Please verify and try again.")

    user_id = user_row["id"]
    now_str = datetime.now().isoformat()
    exp_str = (datetime.now() + timedelta(days=30)).isoformat()
    session_token = "ss_tok_" + secrets.token_hex(24)

    cursor.execute("""
    INSERT INTO sessions (token, user_id, created_at, expires_at)
    VALUES (?, ?, ?, ?)
    """, (session_token, user_id, now_str, exp_str))
    conn.commit()

    # Fetch profile
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    prof_row = cursor.fetchone()
    conn.close()

    profile_dict = dict(prof_row) if prof_row else {}
    if profile_dict and "interest_categories" in profile_dict:
        try:
            profile_dict["interest_categories"] = json.loads(profile_dict["interest_categories"] or "[]")
        except Exception:
            profile_dict["interest_categories"] = []

    user_safe = {
        "id": user_row["id"],
        "full_name": user_row["full_name"],
        "email": user_row["email"],
        "mobile": user_row["mobile"],
        "role": user_row["role"],
        "is_onboarded": bool(user_row["is_onboarded"]),
        "created_at": user_row["created_at"]
    }
    return user_safe, profile_dict, session_token

def get_all_users() -> list[dict]:
    """Returns all registered users for demographic policy simulation."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, mobile, role, is_onboarded, created_at FROM users")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_user_by_session_token(token: str) -> dict | None:
    """Validates session token and returns safe user record."""
    if not token:
        return None
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("""
    SELECT u.id, u.username, u.full_name, u.email, u.mobile, u.role, u.is_onboarded, u.created_at
    FROM sessions s
    JOIN users u ON s.user_id = u.id
    WHERE s.token = ? AND s.expires_at > ?
    """, (token, now_str))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def logout_session(token: str):
    """Deletes session token on logout."""
    if not token:
        return
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def save_user_onboarding_profile(user_id: str, data: dict):
    """Saves complete onboarding profile into SQLite and marks onboarding completed."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    interests_json = json.dumps(data.get("interest_categories", []))

    # Calculate age from DOB if given
    age = int(data.get("age") or 25)
    if data.get("dob"):
        try:
            dob_dt = datetime.strptime(data.get("dob"), "%Y-%m-%d")
            today = datetime.now()
            calc_age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
            if calc_age > 0:
                age = calc_age
        except Exception:
            pass

    cursor.execute("""
    INSERT INTO profiles (
        user_id, full_name, dob, age, gender, state, district, pincode, occupation,
        annual_income, caste_category, area_type, disability_status, marital_status,
        education_level, student, course_stream, institution_type, has_land,
        land_size_acres, has_pucca_house, has_girl_child, family_size, dependents_count,
        senior_citizens_count, has_bpl_card, interest_categories, onboarding_completed,
        onboarding_step, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 6, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        full_name = excluded.full_name,
        dob = excluded.dob,
        age = excluded.age,
        gender = excluded.gender,
        state = excluded.state,
        district = excluded.district,
        pincode = excluded.pincode,
        occupation = excluded.occupation,
        annual_income = excluded.annual_income,
        caste_category = excluded.caste_category,
        area_type = excluded.area_type,
        disability_status = excluded.disability_status,
        marital_status = excluded.marital_status,
        education_level = excluded.education_level,
        student = excluded.student,
        course_stream = excluded.course_stream,
        institution_type = excluded.institution_type,
        has_land = excluded.has_land,
        land_size_acres = excluded.land_size_acres,
        has_pucca_house = excluded.has_pucca_house,
        has_girl_child = excluded.has_girl_child,
        family_size = excluded.family_size,
        dependents_count = excluded.dependents_count,
        senior_citizens_count = excluded.senior_citizens_count,
        has_bpl_card = excluded.has_bpl_card,
        interest_categories = excluded.interest_categories,
        onboarding_completed = 1,
        onboarding_step = 6,
        updated_at = excluded.updated_at
    """, (
        user_id,
        data.get("full_name", ""),
        data.get("dob", ""),
        age,
        data.get("gender", "Male"),
        data.get("state", "Maharashtra"),
        data.get("district", "Pune"),
        data.get("pincode", ""),
        data.get("occupation", "Student"),
        int(data.get("annual_income") or 180000),
        data.get("caste_category", "General"),
        data.get("area_type", "Rural"),
        data.get("disability_status", "None"),
        data.get("marital_status", "Single"),
        data.get("education_level", "Higher Secondary"),
        1 if data.get("student") or data.get("occupation") == "Student" else 0,
        data.get("course_stream", ""),
        data.get("institution_type", "Government"),
        1 if data.get("has_land") else 0,
        float(data.get("land_size_acres") or 0),
        1 if data.get("has_pucca_house") else 0,
        1 if data.get("has_girl_child") else 0,
        int(data.get("family_size") or 1),
        int(data.get("dependents_count") or 0),
        int(data.get("senior_citizens_count") or 0),
        1 if data.get("has_bpl_card") else 0,
        interests_json,
        now_str
    ))

    # Mark user as onboarded
    cursor.execute("UPDATE users SET is_onboarded = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def save_onboarding_draft(user_id: str, step: int, data: dict):
    """Saves partial onboarding draft so citizen can resume seamlessly."""
    conn = get_db()
    cursor = conn.cursor()
    draft_json = json.dumps(data)
    cursor.execute("""
    UPDATE profiles SET onboarding_step = ?, onboarding_draft = ?, updated_at = ?
    WHERE user_id = ?
    """, (step, draft_json, datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()

# ==================== SCHEME REGISTRY METHODS ====================

def seed_schemes_registry(force: bool = False):
    """Seeds verified government schemes in SQLite registry if not already present."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as c FROM schemes")
    count = cursor.fetchone()["c"]
    conn.close()

    if count > 0 and not force:
        return

    from schemes_data import get_seed_schemes
    seed_schemes = get_seed_schemes()
    for s in seed_schemes:
        insert_or_update_scheme(s)

    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO scheme_sync_logs (sync_source, schemes_count, status, details, synced_at)
    VALUES (?, ?, ?, ?, ?)
    """, ("National & State Government Services Portal (.gov.in) Seed", len(seed_schemes), "SUCCESS", "Verified Central and State schemes synchronized with SQL registry", now_str))
    conn.commit()
    conn.close()

def _format_scheme_row(row: sqlite3.Row) -> dict:
    d = dict(row)
    try:
        d["required_documents"] = json.loads(d.get("required_documents") or "[]")
    except Exception:
        d["required_documents"] = []

    try:
        d["social_category"] = json.loads(d.get("social_category") or "[\"ALL\"]")
    except Exception:
        d["social_category"] = ["ALL"]

    try:
        d["occupation"] = json.loads(d.get("occupation") or "[\"All\"]")
    except Exception:
        d["occupation"] = ["All"]

    d["eligibility_rules"] = {
        "min_age": d.get("min_age", 0),
        "max_age": d.get("max_age", 120),
        "max_income": d.get("max_income", 9999999),
        "caste_category": d["social_category"],
        "occupation": d["occupation"],
        "student": bool(d.get("requires_student")),
        "requires_land": bool(d.get("requires_land")),
        "has_girl_child": bool(d.get("has_girl_child")),
        "area_type": d.get("area_criteria", "ALL"),
        "states": d.get("state", "All India")
    }
    return d

def get_all_db_schemes() -> list[dict]:
    """Dynamically queries all active schemes from the SQLite registry."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schemes WHERE scheme_status = 'ACTIVE' ORDER BY priority_weight DESC")
    rows = cursor.fetchall()
    conn.close()
    return [_format_scheme_row(r) for r in rows]

def get_db_scheme_by_id(scheme_id: str) -> dict | None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
    row = cursor.fetchone()
    conn.close()
    return _format_scheme_row(row) if row else None

def insert_or_update_scheme(s: dict) -> str:
    """Inserts or updates a scheme in the registry dynamically."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    scheme_id = s.get("id") or ("scheme_" + secrets.token_hex(4))

    req_docs_json = json.dumps(s.get("required_documents", []))
    social_cat_json = json.dumps(s.get("social_category", ["ALL"]))
    occ_json = json.dumps(s.get("occupation", ["All"]))

    cursor.execute("""
    INSERT INTO schemes (
        id, title, short_desc, detailed_desc, level, state, ministry, department, category,
        target_beneficiary, min_age, max_age, gender_criteria, max_income, social_category,
        occupation, area_criteria, education_criteria, disability_criteria, requires_land,
        requires_student, has_girl_child, other_conditions, benefit_amount, benefit_type,
        benefit_details, required_documents, application_mode, application_process, official_url,
        info_url, official_domain, grievance_portal, helpline, start_date, deadline,
        deadline_days_left, renewal_requirements, scheme_status, last_verified_date,
        source_authority, verification_status, priority_weight, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        title = excluded.title,
        short_desc = excluded.short_desc,
        detailed_desc = excluded.detailed_desc,
        level = excluded.level,
        state = excluded.state,
        ministry = excluded.ministry,
        department = excluded.department,
        category = excluded.category,
        target_beneficiary = excluded.target_beneficiary,
        min_age = excluded.min_age,
        max_age = excluded.max_age,
        gender_criteria = excluded.gender_criteria,
        max_income = excluded.max_income,
        social_category = excluded.social_category,
        occupation = excluded.occupation,
        area_criteria = excluded.area_criteria,
        education_criteria = excluded.education_criteria,
        disability_criteria = excluded.disability_criteria,
        requires_land = excluded.requires_land,
        requires_student = excluded.requires_student,
        has_girl_child = excluded.has_girl_child,
        other_conditions = excluded.other_conditions,
        benefit_amount = excluded.benefit_amount,
        benefit_type = excluded.benefit_type,
        benefit_details = excluded.benefit_details,
        required_documents = excluded.required_documents,
        application_mode = excluded.application_mode,
        application_process = excluded.application_process,
        official_url = excluded.official_url,
        info_url = excluded.info_url,
        official_domain = excluded.official_domain,
        grievance_portal = excluded.grievance_portal,
        helpline = excluded.helpline,
        deadline = excluded.deadline,
        deadline_days_left = excluded.deadline_days_left,
        renewal_requirements = excluded.renewal_requirements,
        scheme_status = excluded.scheme_status,
        last_verified_date = excluded.last_verified_date,
        source_authority = excluded.source_authority,
        verification_status = excluded.verification_status,
        priority_weight = excluded.priority_weight,
        updated_at = excluded.updated_at
    """, (
        scheme_id, s["title"], s.get("short_desc", ""), s.get("detailed_desc", ""), s.get("level", "Central"),
        s.get("state", "All India"), s.get("ministry", "Government of India"), s.get("department", ""), s.get("category", "General"),
        s.get("target_beneficiary", "All Citizens"), int(s.get("min_age", 0)), int(s.get("max_age", 120)), s.get("gender_criteria", "ALL"),
        int(s.get("max_income", 9999999)), social_cat_json, occ_json, s.get("area_criteria", "ALL"),
        s.get("education_criteria", "None"), s.get("disability_criteria", "None"), 1 if s.get("requires_land") else 0,
        1 if s.get("requires_student") else 0, 1 if s.get("has_girl_child") else 0, s.get("other_conditions", ""),
        s.get("benefit_amount", "Standard Benefit"), s.get("benefit_type", "Welfare Grant"), s.get("benefit_details", ""), req_docs_json,
        s.get("application_mode", "Online"), s.get("application_process", ""), s.get("official_url", ""),
        s.get("info_url", ""), s.get("official_domain", ""), s.get("grievance_portal", ""), s.get("helpline", ""),
        s.get("start_date", ""), s.get("deadline", "Open"), int(s.get("deadline_days_left", 180)),
        s.get("renewal_requirements", ""), s.get("scheme_status", "ACTIVE"), s.get("last_verified_date", datetime.now().strftime("%Y-%m-%d")),
        s.get("source_authority", "Government Department"), s.get("verification_status", "VERIFIED"),
        int(s.get("priority_weight", 85)), now_str, now_str
    ))
    conn.commit()
    conn.close()
    return scheme_id

def report_missing_scheme(user_id: str, data: dict) -> str:
    """Stores citizen reports of missing schemes for admin review."""
    report_id = "rep_" + secrets.token_hex(6)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO missing_scheme_reports (
        id, user_id, scheme_name, department_or_ministry, state, official_link, description, status, reported_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING_REVIEW', ?)
    """, (
        report_id, user_id, data.get("scheme_name", "Untitled Scheme"),
        data.get("department_or_ministry", "Central / State Department"),
        data.get("state", "All India"),
        data.get("official_link", ""),
        data.get("description", ""),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return report_id

def get_missing_scheme_reports() -> list[dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM missing_scheme_reports ORDER BY reported_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_scheme_stats() -> dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM schemes WHERE scheme_status = 'ACTIVE'")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM schemes WHERE verification_status = 'VERIFIED' AND scheme_status = 'ACTIVE'")
    verified = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM schemes WHERE level = 'Central' AND scheme_status = 'ACTIVE'")
    central = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM schemes WHERE level = 'State' AND scheme_status = 'ACTIVE'")
    state_cnt = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM missing_scheme_reports WHERE status = 'PENDING_REVIEW'")
    reported_pending = cursor.fetchone()[0]

    conn.close()
    return {
        "database_label": "DEMO SCHEME DATABASE",
        "total_active_schemes": total,
        "verified_schemes_count": verified,
        "central_schemes_count": central,
        "state_schemes_count": state_cnt,
        "reported_missing_pending": reported_pending,
        "architecture": "Scalable SQL-Backed Government Registry (Supports 10,000+ schemes)",
        "disclaimer": "Verified entries represent audited schemes with official .gov.in endpoints. Citizens can report missing schemes for registry inclusion."
    }

# ==================== DEMO PERSONA SEEDING ====================

def seed_demo_data():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", ("rahul_student",))
    if not cursor.fetchone():
        # 1. Rahul Sharma - Rural Student Persona
        u_id = "user_rahul_001"
        pw_h, salt = hash_password("demo123")
        cursor.execute("""
        INSERT INTO users (id, username, password_hash, salt, full_name, email, mobile, role, is_onboarded, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'citizen', 1, ?)
        """, (u_id, "rahul_student", pw_h, salt, "Rahul Sharma", "rahul.sharma@example.gov.in", "9876543210", datetime.now().isoformat()))

        cursor.execute("""
        INSERT INTO profiles (user_id, full_name, dob, age, gender, state, district, pincode, occupation, annual_income, caste_category, area_type, disability_status, marital_status, education_level, student, course_stream, institution_type, has_land, land_size_acres, has_pucca_house, has_girl_child, family_size, dependents_count, senior_citizens_count, has_bpl_card, interest_categories, onboarding_completed, onboarding_step, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 6, ?)
        """, (u_id, "Rahul Sharma", "2005-04-15", 21, "Male", "Maharashtra", "Pune", "411001", "Student", 180000, "OBC", "Rural", "None", "Single", "Undergraduate", 1, "B.Sc Computer Science", "Government Aided", 0, 0, 0, 0, 4, 1, 1, 0, json.dumps(["Education & Scholarships", "Skill Development & Employment", "Energy & Sustainability"]), datetime.now().isoformat()))

        # Documents for Rahul
        today = datetime.now()
        exp_caste = (today + timedelta(days=20)).strftime("%Y-%m-%d")
        
        docs = [
            ("doc_r1", u_id, "Aadhaar Card", "Identity", "aadhaar_rahul.enc", "2022-01-10", "2032-01-10", 1, "DigiLocker Verified"),
            ("doc_r2", u_id, "Bank Account / Passbook with DBT Seeding", "Financial", "bank_rahul.enc", "2023-04-01", "2030-01-01", 1, "Bank e-KYC"),
            ("doc_r3", u_id, "10th / 12th Marksheet", "Academic", "marksheet_rahul.enc", "2022-06-15", None, 1, "CBSE DigiLocker"),
            ("doc_r4", u_id, "Domicile Certificate", "Residence", "domicile_rahul.enc", "2023-08-12", "2033-08-12", 1, "e-District Portal"),
            ("doc_r5", u_id, "Caste Certificate & Validity", "Category", "caste_rahul.enc", "2022-03-20", exp_caste, 1, "Sub-Divisional Officer")
        ]

        for d in docs:
            cursor.execute("""
            INSERT INTO user_documents (id, user_id, doc_name, doc_type, file_name, issue_date, expiry_date, is_verified, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (*d, datetime.now().isoformat()))

        # Pre-seed sample application for Rahul
        cursor.execute("""
        INSERT INTO applications (id, user_id, scheme_id, scheme_name, ref_number, applied_date, status, last_updated, next_action, is_demo_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "app_rahul_001",
            u_id,
            "post-matric-scholarship",
            "Post-Matric Scholarship for SC / ST / OBC / EWS Students",
            "NSP-2026-MH-94820",
            (today - timedelta(days=7)).strftime("%Y-%m-%d"),
            "Under Verification",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "College Verification Completed → Awaiting District Social Welfare Approval",
            1
        ))

        # Seed Notifications for Rahul
        cursor.execute("""
        INSERT INTO notifications (id, user_id, title, message, type, severity, action_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "notif_r1",
            u_id,
            "Document Expiring Soon",
            "Your Caste Certificate & Validity renewal window is open (expires in 20 days). Renew to keep reservations active.",
            "expiry",
            "warning",
            "doc_solver:Caste Certificate & Validity",
            datetime.now().isoformat()
        ))

        cursor.execute("""
        INSERT INTO notifications (id, user_id, title, message, type, severity, action_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "notif_r2",
            u_id,
            "Upcoming Application Deadline",
            "Post-Matric Scholarship 2026 application window closes in 65 days. Obtain Income Certificate to complete application.",
            "deadline",
            "info",
            "scheme:post-matric-scholarship",
            datetime.now().isoformat()
        ))

        # Seed Consent
        cursor.execute("""
        INSERT INTO consents (id, user_id, service_name, purpose, scopes, status, granted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "con_r1",
            u_id,
            "DigiLocker National Depository (DEMO)",
            "Automatic document gap verification for Government Scheme Eligibility",
            "Aadhaar, Class X/XII Marksheets, Driving License",
            "ACTIVE",
            datetime.now().isoformat()
        ))

        # 2. Sunita Devi - Small Farmer Persona
        u_id2 = "user_sunita_002"
        pw_h2, salt2 = hash_password("demo123")
        cursor.execute("""
        INSERT INTO users (id, username, password_hash, salt, full_name, email, mobile, role, is_onboarded, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'citizen', 1, ?)
        """, (u_id2, "sunita_farmer", pw_h2, salt2, "Sunita Devi", "sunita.devi@example.gov.in", "9876543211", datetime.now().isoformat()))

        cursor.execute("""
        INSERT INTO profiles (user_id, full_name, dob, age, gender, state, district, pincode, occupation, annual_income, caste_category, area_type, disability_status, marital_status, education_level, student, course_stream, institution_type, has_land, land_size_acres, has_pucca_house, has_girl_child, family_size, dependents_count, senior_citizens_count, has_bpl_card, interest_categories, onboarding_completed, onboarding_step, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 6, ?)
        """, (u_id2, "Sunita Devi", "1988-08-12", 38, "Female", "Maharashtra", "Nashik", "422001", "Farmer", 120000, "SC", "Rural", "None", "Married", "School", 0, "", "", 1, 1.5, 0, 1, 5, 2, 1, 1, json.dumps(["Agriculture & Farmers", "Women & Child Welfare", "Housing & Infrastructure"]), datetime.now().isoformat()))

        docs_sunita = [
            ("doc_s1", u_id2, "Aadhaar Card", "Identity", "aadhaar_sunita.enc", "2021-05-12", "2031-05-12", 1, "DigiLocker Verified"),
            ("doc_s2", u_id2, "Bank Account / Passbook with DBT Seeding", "Financial", "bank_sunita.enc", "2022-08-10", "2030-01-01", 1, "Jan Dhan Account"),
            ("doc_s3", u_id2, "Land Records / 7/12 Extract / RoR", "Property", "land_sunita.enc", "2024-01-15", None, 1, "Bhulekh UP Portal"),
            ("doc_s4", u_id2, "Ration Card (BPL / AAY)", "Entitlement", "ration_sunita.enc", "2020-11-20", "2030-11-20", 1, "Food & Civil Supplies")
        ]
        for d in docs_sunita:
            cursor.execute("""
            INSERT INTO user_documents (id, user_id, doc_name, doc_type, file_name, issue_date, expiry_date, is_verified, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (*d, datetime.now().isoformat()))

        # Seed Application for Sunita
        cursor.execute("""
        INSERT INTO applications (id, user_id, scheme_id, scheme_name, ref_number, applied_date, status, last_updated, next_action, is_demo_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "app_sunita_001",
            u_id2,
            "pm-kisan",
            "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "PMK-2026-MH-88231",
            (today - timedelta(days=14)).strftime("%Y-%m-%d"),
            "Under Verification",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Land Record (7/12 1.5 Acres) Verified by Talathi → State Approval Pending",
            1
        ))

        # 3. User B (Test User for Multi-tenant isolation tests)
        u_id3 = "user_victim_003"
        pw_h3, salt3 = hash_password("secret456")
        cursor.execute("""
        INSERT INTO users (id, username, password_hash, salt, full_name, email, mobile, role, is_onboarded, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'citizen', 1, ?)
        """, (u_id3, "user_b_private", pw_h3, salt3, "Private Citizen B", "citizen_b@example.com", "9876543212", datetime.now().isoformat()))

        cursor.execute("""
        INSERT INTO user_documents (id, user_id, doc_name, doc_type, file_name, issue_date, expiry_date, is_verified, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("doc_private_b_999", u_id3, "Confidential Property Deed", "Private", "secret_b.enc", "2024-01-01", "2034-01-01", 1, "Confidential", datetime.now().isoformat()))

        conn.commit()

    conn.close()

# ==================== MULTI-TENANT USER METHODS ====================

def get_user_documents(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_documents WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = []
    for r in cursor.fetchall():
        d = dict(r)
        if "ocr_metadata" in d and d["ocr_metadata"]:
            try:
                d["ocr_metadata"] = json.loads(d["ocr_metadata"])
            except Exception:
                d["ocr_metadata"] = {}
        else:
            d["ocr_metadata"] = {}
        rows.append(d)
    conn.close()
    return rows

def get_document_by_id(doc_id: str, user_id: str):
    """Strictly checks owner_user_id. Returns None if owned by another user."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if "ocr_metadata" in d and d["ocr_metadata"]:
        try:
            d["ocr_metadata"] = json.loads(d["ocr_metadata"])
        except Exception:
            d["ocr_metadata"] = {}
    else:
        d["ocr_metadata"] = {}
    return d

def delete_user_document(doc_id: str, user_id: str) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def add_user_document(user_id: str, doc_name: str, doc_type: str, issue_date: str = None, expiry_date: str = None, source: str = "Manual Upload", ocr_metadata: dict = None):
    doc_id = "doc_" + secrets.token_hex(8)
    conn = get_db()
    cursor = conn.cursor()
    ocr_json = json.dumps(ocr_metadata or {})
    cursor.execute("""
    INSERT INTO user_documents (id, user_id, doc_name, doc_type, issue_date, expiry_date, ocr_metadata, is_verified, source, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
    """, (doc_id, user_id, doc_name, doc_type, issue_date, expiry_date, ocr_json, source, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return doc_id

def insert_notification(user_id: str, title: str, message: str, notif_type: str = "info", severity: str = "info", action_url: str = "") -> str:
    """Inserts a persistent notification for the user."""
    notif_id = "notif_" + secrets.token_hex(6)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO notifications (id, user_id, title, message, type, severity, action_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (notif_id, user_id, title, message, notif_type, severity, action_url, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return notif_id

def get_user_profile(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["interest_categories"] = json.loads(d.get("interest_categories") or "[]")
    except Exception:
        d["interest_categories"] = []
    return d

def get_user_by_id(user_id: str):
    """Returns safe user record without password hash/salt."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, mobile, role, is_onboarded, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_user_profile(user_id: str, data: dict):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO profiles (user_id, full_name, age, gender, occupation, annual_income, caste_category, state, area_type, student, has_land, land_size_acres, has_pucca_house, has_girl_child, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        full_name = excluded.full_name,
        age = excluded.age,
        gender = excluded.gender,
        occupation = excluded.occupation,
        annual_income = excluded.annual_income,
        caste_category = excluded.caste_category,
        state = excluded.state,
        area_type = excluded.area_type,
        student = excluded.student,
        has_land = excluded.has_land,
        land_size_acres = excluded.land_size_acres,
        has_pucca_house = excluded.has_pucca_house,
        has_girl_child = excluded.has_girl_child,
        updated_at = excluded.updated_at
    """, (
        user_id,
        data.get("full_name", ""),
        data.get("age", 25),
        data.get("gender", "Male"),
        data.get("occupation", "Unemployed"),
        data.get("annual_income", 150000),
        data.get("caste_category", "General"),
        data.get("state", "Maharashtra"),
        data.get("area_type", "Rural"),
        1 if data.get("student") else 0,
        1 if data.get("has_land") else 0,
        data.get("land_size_acres", 0),
        1 if data.get("has_pucca_house") else 0,
        1 if data.get("has_girl_child") else 0,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_user_applications(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY last_updated DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_application(user_id: str, scheme_id: str, scheme_name: str, status: str = "Draft", is_demo_data: bool = True):
    app_id = "app_" + secrets.token_hex(6)
    ref_num = f"SS-2026-{secrets.token_hex(4).upper()}"
    today = datetime.now().strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO applications (id, user_id, scheme_id, scheme_name, ref_number, applied_date, status, last_updated, next_action, is_demo_data)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (app_id, user_id, scheme_id, scheme_name, ref_num, today, status, now_str, "Application received. Document scrutiny in progress.", 1 if is_demo_data else 0))
    conn.commit()
    conn.close()
    return app_id, ref_num

def update_application_status(app_id: str, user_id: str, status: str, next_action: str = None, rejection_reason: str = None, corrective_action: str = None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE applications SET
        status = ?,
        last_updated = ?,
        next_action = COALESCE(?, next_action),
        rejection_reason = ?,
        corrective_action = ?
    WHERE id = ? AND user_id = ?
    """, (status, datetime.now().strftime("%Y-%m-%d %H:%M"), next_action, rejection_reason, corrective_action, app_id, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_user_notifications(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_user_consents(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consents WHERE user_id = ? ORDER BY granted_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def toggle_consent(user_id: str, service_name: str, enable: bool):
    conn = get_db()
    cursor = conn.cursor()
    if enable:
        cursor.execute("""
        INSERT INTO consents (id, user_id, service_name, purpose, scopes, status, granted_at)
        VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?)
        """, (
            "con_" + secrets.token_hex(6),
            user_id,
            service_name,
            "Automatic document verification for schemes",
            "Aadhaar, Marksheets, Certificates",
            datetime.now().isoformat()
        ))
    else:
        cursor.execute("""
        UPDATE consents SET status = 'REVOKED', revoked_at = ? WHERE user_id = ? AND service_name = ?
        """, (datetime.now().isoformat(), user_id, service_name))
    conn.commit()
    conn.close()

def delete_all_user_data(user_id: str):
    """Right to be forgotten - completely purges user profile, docs, apps, notifications."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_documents WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM applications WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM consents WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM profiles WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def log_audit(user_id: str, action: str, ip: str = "127.0.0.1", details: str = ""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO audit_logs (user_id, action, ip_address, details, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, action, ip, details, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_audit_logs(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

# ==================== SCHEME VERSIONING & CHANGE TRACKING ====================

def seed_scheme_versions():
    """Seeds historical version snapshots for government schemes."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scheme_versions")
    if cursor.fetchone()[0] == 0:
        versions = [
            ("ver_pms_01", "post-matric-scholarship", 1, 2025, "https://scholarships.gov.in", "NSP Portal Notification 2024-25", "2025-01-10", "2025-01-15", "admin_nsp_lead", "Annual income ceiling set at ₹2,50,000 for OBC/SC/ST students.", json.dumps({"max_income": 200000}), json.dumps({"max_income": 250000}), 1),
            ("ver_pms_02", "post-matric-scholarship", 2, 2026, "https://scholarships.gov.in", "MoSJE Gazette 2026", "2026-02-01", "2026-02-05", "admin_gov_01", "Mandatory DBT NPCI bank linking requirement enforced for direct disbursal.", json.dumps({"dbt_mandatory": False}), json.dumps({"dbt_mandatory": True}), 1),
            ("ver_pmk_01", "pm-kisan", 1, 2025, "https://pmkisan.gov.in", "MoA&FW Guidelines 2025", "2025-01-01", "2025-01-05", "admin_agri_01", "Direct cash support of ₹6,000/year in three ₹2,000 tranches with Aadhaar eKYC requirement.", json.dumps({"ekyc_required": False}), json.dumps({"ekyc_required": True}), 1),
            ("ver_pmjay_01", "ayushman-bharat-pmjay", 1, 2025, "https://beneficiary.nha.gov.in", "NHA Policy Update 2025", "2025-04-01", "2025-04-05", "admin_nha_lead", "Hospitalization coverage verified up to ₹5 Lakh per family per year.", json.dumps({"cover": 300000}), json.dumps({"cover": 500000}), 1)
        ]
        for v in versions:
            cursor.execute("SELECT id FROM schemes WHERE id = ?", (v[1],))
            if cursor.fetchone():
                cursor.execute("""
                INSERT OR IGNORE INTO scheme_versions (id, scheme_id, version_number, effective_year, source_url, source_title, detected_date, verified_date, verified_by_admin, change_summary, previous_criteria, new_criteria, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, v)
        conn.commit()
    conn.close()

def get_scheme_versions(scheme_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scheme_versions WHERE scheme_id = ? ORDER BY version_number DESC", (scheme_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def record_scheme_version(scheme_id: str, version_data: dict):
    conn = get_db()
    cursor = conn.cursor()
    v_id = version_data.get("id") or ("ver_" + secrets.token_hex(6))
    cursor.execute("""
    INSERT INTO scheme_versions (id, scheme_id, version_number, effective_year, source_url, source_title, detected_date, verified_date, verified_by_admin, change_summary, previous_criteria, new_criteria, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        v_id,
        scheme_id,
        version_data.get("version_number", 1),
        version_data.get("effective_year", 2026),
        version_data.get("source_url", "https://india.gov.in"),
        version_data.get("source_title", "Official Government Gazette"),
        version_data.get("detected_date", datetime.now().strftime("%Y-%m-%d")),
        version_data.get("verified_date", datetime.now().strftime("%Y-%m-%d")),
        version_data.get("verified_by_admin", "admin_gov_01"),
        version_data.get("change_summary", "Government criteria updated."),
        json.dumps(version_data.get("previous_criteria", {})),
        json.dumps(version_data.get("new_criteria", {})),
        1
    ))
    conn.commit()
    conn.close()
    return v_id

# ==================== GRIEVANCE ASSISTANCE DATABASE ====================

def get_user_grievances(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grievances WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_grievance(user_id: str, data: dict):
    conn = get_db()
    cursor = conn.cursor()
    g_id = data.get("id") or ("grv_" + secrets.token_hex(6))
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
    INSERT INTO grievances (id, user_id, application_id, scheme_id, scheme_name, department, ref_number, issue_category, petition_text, responsible_authority, grievance_portal_url, escalation_level, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DRAFTED', ?, ?)
    """, (
        g_id,
        user_id,
        data.get("application_id"),
        data.get("scheme_id", "general-grievance"),
        data.get("scheme_name", "Government Welfare Scheme"),
        data.get("department", "Ministry of Social Justice & Empowerment"),
        data.get("ref_number"),
        data.get("issue_category", "Application Delay / Pending Status"),
        data.get("petition_text", ""),
        data.get("responsible_authority", "Central Public Grievance Redress and Monitoring System (CPGRAMS)"),
        data.get("grievance_portal_url", "https://pgportal.gov.in"),
        data.get("escalation_level", 1),
        now_str,
        now_str
    ))
    conn.commit()
    conn.close()
    return g_id

# ==================== DOCUMENT CONFLICTS & REUSE ====================

def get_document_conflicts(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM document_conflicts WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def record_document_conflict(user_id: str, data: dict):
    conn = get_db()
    cursor = conn.cursor()
    c_id = data.get("id") or ("conf_" + secrets.token_hex(6))
    cursor.execute("""
    INSERT INTO document_conflicts (id, user_id, doc_id_1, doc_id_2, conflict_field, value_1, value_2, severity, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'DETECTED', ?)
    """, (
        c_id,
        user_id,
        data.get("doc_id_1", ""),
        data.get("doc_id_2", ""),
        data.get("conflict_field", "Name"),
        data.get("value_1", ""),
        data.get("value_2", ""),
        data.get("severity", "WARNING"),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return c_id

# ==================== LIFE EVENTS & RISK SCORES ====================

def record_life_event(user_id: str, event_type: str, details: dict, discovered_count: int = 0):
    conn = get_db()
    cursor = conn.cursor()
    ev_id = "ev_" + secrets.token_hex(6)
    cursor.execute("""
    INSERT INTO life_events (id, user_id, event_type, event_date, details_json, discovered_schemes_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        ev_id,
        user_id,
        event_type,
        datetime.now().strftime("%Y-%m-%d"),
        json.dumps(details),
        discovered_count,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return ev_id

def get_user_life_events(user_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM life_events WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def record_risk_score(user_id: str, scheme_id: str, risk_data: dict):
    conn = get_db()
    cursor = conn.cursor()
    r_id = "risk_" + secrets.token_hex(6)
    cursor.execute("""
    INSERT OR REPLACE INTO risk_scores (id, user_id, scheme_id, risk_level, risk_score, risk_factors, mitigation_advice, evaluated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        r_id,
        user_id,
        scheme_id,
        risk_data.get("risk_level", "LOW"),
        risk_data.get("risk_score", 15),
        json.dumps(risk_data.get("risk_factors", [])),
        json.dumps(risk_data.get("mitigation_advice", [])),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return r_id

# ==================== CITIZEN BENEFIT TWIN STORAGE & EVENTS ====================

def save_benefit_twin(user_id: str, twin_data: dict):
    conn = get_db()
    try:
        cursor = conn.cursor()
        opp_score = twin_data.get("benefit_opportunity_score", {}).get("total_score", 84)
        cursor.execute("""
        INSERT OR REPLACE INTO benefit_twins (user_id, twin_state_json, opportunity_score, calculated_at)
        VALUES (?, ?, ?, ?)
        """, (user_id, json.dumps(twin_data), int(opp_score), datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()

def get_benefit_twin(user_id: str) -> dict | None:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM benefit_twins WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return json.loads(row["twin_state_json"])
    except Exception:
        return None
    finally:
        conn.close()

def record_benefit_twin_event(user_id: str, event_type: str, payload: dict, affected_nodes: list = None, exec_ms: float = 0.0) -> str:
    evt_id = "evt_" + secrets.token_hex(6)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO benefit_twin_events (id, user_id, event_type, event_payload_json, selective_nodes_recalculated, execution_time_ms, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            evt_id,
            user_id,
            event_type,
            json.dumps(payload or {}),
            json.dumps(affected_nodes or []),
            float(exec_ms),
            datetime.now().isoformat()
        ))
        conn.commit()
        return evt_id
    finally:
        conn.close()

def get_benefit_twin_events(user_id: str) -> list[dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM benefit_twin_events WHERE user_id = ? ORDER BY created_at DESC LIMIT 30", (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    finally:
        conn.close()

def save_scenario_simulation(user_id: str, scenario_title: str, parameters: dict, results: dict) -> str:
    sim_id = "sim_" + secrets.token_hex(6)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO scenario_simulations (id, user_id, scenario_title, parameters_json, results_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sim_id,
            user_id,
            scenario_title,
            json.dumps(parameters or {}),
            json.dumps(results or {}),
            datetime.now().isoformat()
        ))
        conn.commit()
        return sim_id
    finally:
        conn.close()

def get_user_scenario_simulations(user_id: str) -> list[dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scenario_simulations WHERE user_id = ? ORDER BY created_at DESC LIMIT 10", (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        for r in rows:
            try:
                r["parameters"] = json.loads(r.get("parameters_json", "{}"))
                r["results"] = json.loads(r.get("results_json", "{}"))
            except Exception:
                pass
        return rows
    finally:
        conn.close()

def save_decision_trace(user_id: str, scheme_id: str, trace_data: dict, is_eligible: bool, is_ready: bool):
    tr_id = "trace_" + secrets.token_hex(6)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO decision_traces (id, user_id, scheme_id, trace_json, is_eligible, is_ready, evaluated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tr_id,
            user_id,
            scheme_id,
            json.dumps(trace_data or {}),
            1 if is_eligible else 0,
            1 if is_ready else 0,
            datetime.now().isoformat()
        ))
        conn.commit()
        return tr_id
    finally:
        conn.close()

def save_decision_traces_batch(user_id: str, traces: list[dict]):
    """Saves multiple scheme decision traces in a single fast atomic transaction."""
    if not traces:
        return
    conn = get_db()
    try:
        cursor = conn.cursor()
        now_str = datetime.now().isoformat()
        params = [
            (
                "trace_" + secrets.token_hex(6),
                user_id,
                t["scheme_id"],
                json.dumps(t.get("trace_data") or {}),
                1 if t.get("is_eligible") else 0,
                1 if t.get("is_ready") else 0,
                now_str
            )
            for t in traces
        ]
        cursor.executemany("""
        INSERT OR REPLACE INTO decision_traces (id, user_id, scheme_id, trace_json, is_eligible, is_ready, evaluated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, params)
        conn.commit()
    finally:
        conn.close()

def get_decision_trace(user_id: str, scheme_id: str) -> dict | None:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM decision_traces WHERE user_id = ? AND scheme_id = ? ORDER BY evaluated_at DESC LIMIT 1", (user_id, scheme_id))
        row = cursor.fetchone()
        if not row:
            return None
        return json.loads(row["trace_json"])
    except Exception:
        return None
    finally:
        conn.close()

def save_policy_simulation(admin_id: str, scheme_id: str, old_rule: dict, new_rule: dict, impact_summary: dict) -> str:
    pol_id = "pol_" + secrets.token_hex(6)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO policy_simulations (id, admin_id, scheme_id, old_rule_json, new_rule_json, impact_summary_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pol_id,
            admin_id,
            scheme_id,
            json.dumps(old_rule or {}),
            json.dumps(new_rule or {}),
            json.dumps(impact_summary or {}),
            datetime.now().isoformat()
        ))
        conn.commit()
        return pol_id
    finally:
        conn.close()

def get_policy_simulations() -> list[dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM policy_simulations ORDER BY created_at DESC LIMIT 20")
        rows = [dict(r) for r in cursor.fetchall()]
        for r in rows:
            try:
                r["old_rule"] = json.loads(r.get("old_rule_json", "{}"))
                r["new_rule"] = json.loads(r.get("new_rule_json", "{}"))
                r["impact_summary"] = json.loads(r.get("impact_summary_json", "{}"))
            except Exception:
                pass
        return rows
    finally:
        conn.close()

# Initialize on import
init_db()
