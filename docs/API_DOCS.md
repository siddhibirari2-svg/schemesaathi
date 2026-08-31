# SchemeSaathi — REST API Documentation Reference

Base URL: `http://localhost:8000` or Cloudflare live tunnel.
Authorization: Bearer token or `X-User-Id` header (multi-tenant isolation enforced on all user routes).

---

## 1. Authentication & Onboarding Endpoints

### `POST /api/auth/register`
Registers a new citizen user.
- **Request Body**:
  ```json
  {
    "full_name": "Rahul Patil",
    "email": "rahul.patil@example.com",
    "mobile": "9876543210",
    "password": "SecurePassword123!",
    "confirm_password": "SecurePassword123!"
  }
  ```
- **Response**: `200 OK` with user object and session token.

### `POST /api/auth/login`
Authenticates an existing citizen or admin.
- **Request Body**: `{"identifier": "rahul.patil@example.com", "password": "..."}`
- **Response**: `200 OK` with user profile, session token, and redirect route.

---

## 2. Benefit Execution & Journey Endpoints

### `GET /api/benefit-journey?scheme_id={scheme_id}`
Returns the comprehensive 8-stage benefit journey for a specific scheme.
- **Response**:
  ```json
  {
    "scheme_id": "post-matric-scholarship",
    "scheme_title": "Post-Matric Scholarship for OBC/SC/ST Students",
    "current_stage": 5,
    "progress_pct": 62,
    "stages": [
      {"stage_number": 1, "name": "Citizen Discovery", "status": "COMPLETED", "icon": "fa-magnifying-glass"},
      {"stage_number": 2, "name": "Demographic Eligibility", "status": "COMPLETED", "icon": "fa-id-card-clip"},
      {"stage_number": 3, "name": "Document Verification", "status": "COMPLETED", "icon": "fa-file-shield"},
      {"stage_number": 4, "name": "Application Preparation", "status": "COMPLETED", "icon": "fa-list-check"},
      {"stage_number": 5, "name": "Official Submission", "status": "SUBMITTED", "icon": "fa-arrow-up-right-from-square"},
      {"stage_number": 6, "name": "Department Scrutiny", "status": "IN_PROGRESS", "icon": "fa-building-columns"},
      {"stage_number": 7, "name": "Sanction & Approval", "status": "PENDING", "icon": "fa-file-signature"},
      {"stage_number": 8, "name": "Benefit Disbursal", "status": "PENDING", "icon": "fa-hand-holding-dollar"}
    ]
  }
  ```

### `POST /api/applications/risk-estimate`
Computes pre-submission application rejection risk.
- **Request Body**: `{"scheme_id": "post-matric-scholarship"}`
- **Response**:
  ```json
  {
    "risk_level": "LOW",
    "risk_score": 12,
    "confidence_score": 94,
    "risk_factors": ["Income ceiling is within safe margin"],
    "mitigation_advice": ["Verify bank account NPCI Aadhaar seeding at local branch"]
  }
  ```

---

## 3. Document Vault & Inconsistency Endpoints

### `GET /api/documents/conflicts`
Scans the citizen's private vault for cross-document inconsistencies.
- **Response**: List of detected discrepancies (Name spelling, DOB, Address).

### `GET /api/documents/reuse`
Returns cross-scheme document reuse metrics.
- **Response**: Shows how many welfare schemes each verified vault document unlocks.

---

## 4. Grievance AI Endpoints

### `POST /api/grievance/draft`
Synthesizes a formal administrative grievance petition conforming to CPGRAMS standards.
- **Request Body**:
  ```json
  {
    "application_id": "app_001",
    "issue_category": "Delay in Disbursal beyond Standard SLA",
    "ref_number": "APP-2026-NSP-8821",
    "notes": "Submitted 60 days ago. Verified by college desk."
  }
  ```
- **Response**: Structured formal petition letter, responsible authority, and link to `https://pgportal.gov.in`.

---

## 5. Knowledge Graph Endpoints

### `GET /api/graph/benefit-universe`
Returns full directed graph topology (Nodes & Edges) for interactive visual exploration.
