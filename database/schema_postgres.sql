-- ====================================================================
-- SchemeSaathi - Production PostgreSQL & pgvector Database Schema DDL
-- Enterprise Benefit Execution Platform Database Design
-- Supports: Millions of citizens, 10,000+ schemes, document vaults,
-- deterministic rule trees, pgvector embeddings, and audit trails.
-- ====================================================================

-- Enable Required PostgreSQL Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Users Table (Multi-tenant Citizens, Admins, Reviewers)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(150) UNIQUE,
    email VARCHAR(255) UNIQUE,
    mobile VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(64) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'citizen' CHECK (role IN ('citizen', 'admin', 'scheme_reviewer', 'support_officer')),
    is_onboarded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_mobile ON users(mobile);

-- 2. Sessions Table (Cryptographic Session Storage)
CREATE TABLE IF NOT EXISTS sessions (
    token VARCHAR(255) PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);

-- 3. Citizen Profiles Table (Comprehensive Demographics)
CREATE TABLE IF NOT EXISTS citizen_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    dob DATE,
    age INT CHECK (age >= 0 AND age <= 125),
    gender VARCHAR(50) DEFAULT 'Male',
    state VARCHAR(100) DEFAULT 'Maharashtra',
    district VARCHAR(100) DEFAULT 'Pune',
    pincode VARCHAR(10),
    area_type VARCHAR(50) DEFAULT 'Rural' CHECK (area_type IN ('Rural', 'Urban', 'Semi-Urban')),
    caste_category VARCHAR(50) DEFAULT 'General' CHECK (caste_category IN ('General', 'OBC', 'SC', 'ST', 'EWS', 'Minority')),
    annual_income BIGINT DEFAULT 180000,
    occupation VARCHAR(100) DEFAULT 'Student',
    education_level VARCHAR(100),
    student BOOLEAN DEFAULT FALSE,
    course_stream VARCHAR(150),
    institution_type VARCHAR(100),
    has_land BOOLEAN DEFAULT FALSE,
    land_size_acres NUMERIC(8,2) DEFAULT 0.0,
    has_pucca_house BOOLEAN DEFAULT FALSE,
    has_bpl_card BOOLEAN DEFAULT FALSE,
    has_girl_child BOOLEAN DEFAULT FALSE,
    family_size INT DEFAULT 1,
    dependents_count INT DEFAULT 0,
    senior_citizens_count INT DEFAULT 0,
    disability_status VARCHAR(100) DEFAULT 'None',
    marital_status VARCHAR(50) DEFAULT 'Single',
    interest_categories JSONB DEFAULT '[]'::jsonb,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_step INT DEFAULT 1,
    onboarding_draft JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_profiles_state ON citizen_profiles(state);
CREATE INDEX IF NOT EXISTS idx_profiles_income ON citizen_profiles(annual_income);
CREATE INDEX IF NOT EXISTS idx_profiles_category ON citizen_profiles(caste_category);

-- 4. Family Members Table (Multi-Member Entitlement Traversal)
CREATE TABLE IF NOT EXISTS family_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    relation VARCHAR(50) NOT NULL,
    age INT,
    gender VARCHAR(50),
    occupation VARCHAR(100),
    student BOOLEAN DEFAULT FALSE,
    annual_income BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_family_user_id ON family_members(user_id);

-- 5. Government Schemes Table (Normalized Registry)
CREATE TABLE IF NOT EXISTS schemes (
    id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    short_desc TEXT,
    detailed_desc TEXT,
    level VARCHAR(50) DEFAULT 'Central' CHECK (level IN ('Central', 'State', 'UT', 'District')),
    state VARCHAR(100) DEFAULT 'All India',
    ministry VARCHAR(255),
    department VARCHAR(255),
    category VARCHAR(100),
    target_beneficiary VARCHAR(255),
    min_age INT DEFAULT 0,
    max_age INT DEFAULT 120,
    gender_criteria VARCHAR(50) DEFAULT 'ALL',
    max_income BIGINT DEFAULT 999999999,
    social_category JSONB DEFAULT '["ALL"]'::jsonb,
    occupation JSONB DEFAULT '["All"]'::jsonb,
    area_criteria VARCHAR(50) DEFAULT 'ALL',
    education_criteria VARCHAR(100) DEFAULT 'None',
    disability_criteria VARCHAR(100) DEFAULT 'None',
    requires_land BOOLEAN DEFAULT FALSE,
    requires_student BOOLEAN DEFAULT FALSE,
    has_girl_child BOOLEAN DEFAULT FALSE,
    other_conditions TEXT,
    benefit_amount VARCHAR(150),
    benefit_type VARCHAR(100) DEFAULT 'Direct Benefit Transfer (DBT)',
    benefit_details TEXT,
    required_documents JSONB DEFAULT '[]'::jsonb,
    application_mode VARCHAR(50) DEFAULT 'Online',
    application_process TEXT,
    official_url VARCHAR(500),
    info_url VARCHAR(500),
    official_domain VARCHAR(255),
    grievance_portal VARCHAR(500),
    helpline VARCHAR(100),
    start_date DATE,
    deadline DATE,
    deadline_days_left INT DEFAULT 180,
    renewal_requirements TEXT,
    scheme_status VARCHAR(50) DEFAULT 'ACTIVE' CHECK (scheme_status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED', 'REVIEW_REQUIRED')),
    last_verified_date DATE,
    source_authority VARCHAR(255),
    verification_status VARCHAR(50) DEFAULT 'VERIFIED' CHECK (verification_status IN ('VERIFIED', 'PENDING_REVIEW', 'SUSPENDED')),
    priority_weight INT DEFAULT 85,
    embedding vector(1536), -- pgvector embeddings for RAG & semantic search
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_schemes_category ON schemes(category);
CREATE INDEX IF NOT EXISTS idx_schemes_state ON schemes(state);
CREATE INDEX IF NOT EXISTS idx_schemes_level ON schemes(level);

-- 6. Scheme Versions Table (Source Audit & Change Tracking)
CREATE TABLE IF NOT EXISTS scheme_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id VARCHAR(100) NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    effective_year INT DEFAULT 2026,
    source_url VARCHAR(500) NOT NULL,
    source_title VARCHAR(300),
    detected_date DATE NOT NULL,
    verified_date DATE NOT NULL,
    verified_by_admin VARCHAR(100) DEFAULT 'admin_gov_01',
    change_summary TEXT NOT NULL,
    previous_criteria JSONB DEFAULT '{}'::jsonb,
    new_criteria JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scheme_versions_scheme ON scheme_versions(scheme_id);

-- 7. Deterministic Scheme Rules Table
CREATE TABLE IF NOT EXISTS scheme_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id VARCHAR(100) NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    rule_name VARCHAR(150) NOT NULL,
    operator VARCHAR(20) DEFAULT 'AND' CHECK (operator IN ('AND', 'OR', 'NOT')),
    condition_expression TEXT NOT NULL,
    parameters_json JSONB DEFAULT '{}'::jsonb,
    error_explanation TEXT NOT NULL
);

-- 8. Citizen Documents Vault Table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doc_name VARCHAR(255) NOT NULL,
    doc_type VARCHAR(100) NOT NULL,
    storage_reference VARCHAR(500),
    file_name VARCHAR(255),
    file_size BIGINT,
    mime_type VARCHAR(100),
    file_hash VARCHAR(128),
    issue_date DATE,
    expiry_date DATE,
    ocr_metadata JSONB DEFAULT '{}'::jsonb,
    is_verified BOOLEAN DEFAULT TRUE,
    source VARCHAR(100) DEFAULT 'Manual Upload',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);

-- 9. Document Conflicts Table (Inconsistency Analysis)
CREATE TABLE IF NOT EXISTS document_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doc_id_1 UUID REFERENCES documents(id) ON DELETE CASCADE,
    doc_id_2 UUID REFERENCES documents(id) ON DELETE CASCADE,
    conflict_field VARCHAR(100) NOT NULL,
    value_1 TEXT NOT NULL,
    value_2 TEXT NOT NULL,
    severity VARCHAR(50) DEFAULT 'WARNING' CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
    status VARCHAR(50) DEFAULT 'DETECTED' CHECK (status IN ('DETECTED', 'RESOLVED', 'IGNORED')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 10. Citizen Applications Table (8-Stage Benefit Lifecycle)
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheme_id VARCHAR(100) NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    scheme_name VARCHAR(300) NOT NULL,
    ref_number VARCHAR(100) UNIQUE NOT NULL,
    applied_date DATE NOT NULL,
    status VARCHAR(100) NOT NULL CHECK (status IN ('Draft', 'Applied', 'Under Verification', 'Documents Required', 'Approved', 'Rejected', 'Benefit Disbursed', 'Closed')),
    current_stage INT DEFAULT 5 CHECK (current_stage >= 1 AND current_stage <= 8),
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    next_action TEXT,
    rejection_reason TEXT,
    corrective_action TEXT,
    is_demo_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);

-- 11. Application Rejection Risk Scores Table
CREATE TABLE IF NOT EXISTS risk_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheme_id VARCHAR(100) NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    risk_level VARCHAR(50) DEFAULT 'LOW' CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    risk_score INT CHECK (risk_score >= 0 AND risk_score <= 100),
    risk_factors JSONB DEFAULT '[]'::jsonb,
    mitigation_advice JSONB DEFAULT '[]'::jsonb,
    evaluated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 12. Citizen Grievance Assistance Table
CREATE TABLE IF NOT EXISTS grievances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    application_id UUID REFERENCES applications(id) ON DELETE SET NULL,
    scheme_id VARCHAR(100) NOT NULL,
    scheme_name VARCHAR(300) NOT NULL,
    department VARCHAR(255) NOT NULL,
    ref_number VARCHAR(100),
    issue_category VARCHAR(255) NOT NULL,
    petition_text TEXT NOT NULL,
    responsible_authority VARCHAR(255) NOT NULL,
    grievance_portal_url VARCHAR(500) NOT NULL,
    escalation_level INT DEFAULT 1,
    status VARCHAR(50) DEFAULT 'DRAFTED' CHECK (status IN ('DRAFTED', 'FILED', 'IN_REVIEW', 'RESOLVED')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 13. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(50) DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'critical', 'success')),
    action_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 14. Consents Table
CREATE TABLE IF NOT EXISTS consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    service_name VARCHAR(150) NOT NULL,
    purpose TEXT NOT NULL,
    scopes VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'REVOKED')),
    granted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMPTZ
);

-- 15. Audit Logs Table (Full System Access Trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(150) NOT NULL,
    ip_address VARCHAR(50),
    details TEXT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(timestamp DESC);

-- 16. Citizen Benefit Twin State Table (Derived In-Memory & Relational State)
CREATE TABLE IF NOT EXISTS benefit_twins (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    twin_state_json JSONB NOT NULL,
    opportunity_score INT DEFAULT 84,
    calculated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 17. Benefit Twin Lifecycle Events Table (Event-Driven Dependency Logging)
CREATE TABLE IF NOT EXISTS benefit_twin_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    event_payload_json JSONB NOT NULL,
    selective_nodes_recalculated JSONB DEFAULT '[]'::jsonb,
    execution_time_ms NUMERIC(8, 2) DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_twin_events_user ON benefit_twin_events(user_id);

-- 18. Hypothetical What-If Scenario Simulations Table
CREATE TABLE IF NOT EXISTS scenario_simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scenario_title VARCHAR(255) NOT NULL,
    parameters_json JSONB NOT NULL,
    results_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 19. Explainable Deterministic Decision Traces Table
CREATE TABLE IF NOT EXISTS decision_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheme_id VARCHAR(100) NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    trace_json JSONB NOT NULL,
    is_eligible BOOLEAN DEFAULT FALSE,
    is_ready BOOLEAN DEFAULT FALSE,
    evaluated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_traces_user_scheme ON decision_traces(user_id, scheme_id);

-- 20. Government Policy Change Simulations Table (Admin Sandbox)
CREATE TABLE IF NOT EXISTS policy_simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheme_id VARCHAR(100) REFERENCES schemes(id) ON DELETE SET NULL,
    old_rule_json JSONB NOT NULL,
    new_rule_json JSONB NOT NULL,
    impact_summary_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
