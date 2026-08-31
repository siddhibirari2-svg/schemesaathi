# SchemeSaathi — Architecture & Technical Design Specification

## 1. Executive Summary

**SchemeSaathi** is an AI-powered Government Benefit Execution Platform designed for Indian citizens. Unlike conventional discovery portals that merely display lists of welfare schemes, SchemeSaathi guides citizens through the **entire 8-stage lifecycle**:

$$\text{Discover} \longrightarrow \text{Understand} \longrightarrow \text{Check Eligibility} \longrightarrow \text{Verify Documents} \longrightarrow \text{Prepare Application} \longrightarrow \text{Apply on Official Portal} \longrightarrow \text{Track Application} \longrightarrow \text{Receive Benefit / Grievance AI}$$

---

## 2. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                              CITIZEN CLIENT (SPA)                                 |
|  - 8-Stage Benefit Journey Tracker  - Multilingual AI Assistant (EN/HI/MR)        |
|  - Private Vault & Gap Analyzer    - Dynamic Grievance Petition Generator         |
|  - Side-by-Side Comparison Matrix   - Pre-Submission Data Sheet & Checklist       |
+-----------------------------------------------------------------------------------+
                                         │  HTTPS / REST / JSON
                                         ▼
+-----------------------------------------------------------------------------------+
|                           SCHEMESAATHI API GATEWAY                                |
|  - Multi-Tenant Cryptographic Auth Layer (Argon2id / PBKDF2 + SHA-256)            |
|  - Strict Tenant-Isolated Data Access Controller (RBAC)                           |
|  - Government Domain Whitelist Enforcement (*.gov.in, *.nic.in)                   |
+-----------------------------------------------------------------------------------+
         │                               │                               │
         ▼                               ▼                               ▼
+--------------------+         +--------------------+         +--------------------+
| DETERMINISTIC RULE |         | BENEFIT KNOWLEDGE  |         | GROUNDED CITIZEN   |
| ENGINE (engine.py) |         | GRAPH (Neo4j / D3) |         | AI ASSISTANT       |
| - Zero Hallucinate |         | - Multi-Hop Family |         | - Strict Context   |
| - Age/Income/Caste |         | - Entity Relations |         | - Field Explainer  |
| - Rejection Risk   |         | - Document Reuse   |         | - CPGRAMS Petitions|
+--------------------+         +--------------------+         +--------------------+
         │                               │                               │
         └───────────────────────────────┼───────────────────────────────┘
                                         ▼
+-----------------------------------------------------------------------------------+
|                        DATABASE & REGISTRY LAYER                                  |
|  - SQLite (Local Embedded) / PostgreSQL 16+ with pgvector (Cloud Scaled)          |
|  - Scheme Versioning & Gazette Audit Trail (scheme_versions)                      |
|  - Document Vault & Inconsistency Registry (document_conflicts)                   |
|  - Application Lifecycle & Risk Scoring (applications, risk_scores)               |
+-----------------------------------------------------------------------------------+
```

---

## 3. Core Engine Components

### 3.1. Deterministic Eligibility & Gap Engine (`engine.py`)
- **Strict Rule Trees**: Evaluates citizen parameters against government gazette criteria (Age, Gender, Social Category, Annual Income, Landholding, Student Status, Area Type).
- **Zero-Hallucination Guarantee**: LLMs are never permitted to make eligibility verdicts; all decisions are computed using deterministic boolean expressions.
- **Dynamic Missing Document Guidance**: Produces step-by-step resolution pathways (issuing authority, turnaround time, required proofs, official portals) for missing prerequisites.

### 3.2. Benefit Knowledge Graph Engine (`graph_engine.py`)
- **Entity Model**:
  - `Citizen` (Primary user demographics)
  - `FamilyMember` (Dependents, daughters, senior citizens)
  - `GovernmentScheme` (Central and State welfare programs)
  - `Ministry` / `Department` (Issuing authorities)
  - `VaultDocument` & `RequiredDocument` (Proofs and certificates)
- **Multi-Hop Traversal**: Automatically detects family entitlements (e.g. girl child education schemes, agricultural subsidies for farmer parents).

### 3.3. Document Conflict & Inconsistency Detector
- Compares cross-document fields (Name spelling, DOB, Address, Validity dates).
- Categorizes inconsistencies as `Potential Inconsistency Detected` rather than declaring fraud, prompting human verification before official portal filing.

### 3.4. Application Rejection-Risk Model
- Evaluates 6 key failure vectors:
  1. *Aadhaar-Bank Passbook Name Matching*
  2. *NPCI Aadhaar DBT Seeding Status*
  3. *Certificate Expiry Timing (< 30 days)*
  4. *Income Slab Margin (< 10% from ceiling)*
  5. *Domicile / Caste Validity Documentation*
  6. *Application Mode & Scrutiny SLAs*

### 3.5. Grievance AI & Petition Generator
- Formulates formal administrative grievance petitions citing relevant department guidelines, SLA timelines, and escalation hierarchies (CPGRAMS / State CM Helplines).

---

## 4. Security & Privacy Architecture

1. **Multi-Tenant Isolation**: Every database query is parameterized with `WHERE user_id = ?`. Cross-tenant document tampering triggers immediate `403 Forbidden` and security audit logging.
2. **Cryptographic Protection**: Passwords hashed with salted PBKDF2/Argon2 with 100,000 iterations.
3. **DPDP Act Compliance**: Dedicated Privacy Dashboard supporting *Right to Access*, *Export My Data (JSON)*, and *Right to be Forgotten (Full Deletion)*.
