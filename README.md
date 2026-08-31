# SchemeSaathi (स्कीम साथी) 🏛️
### Citizen Government Scheme Discovery & Action Platform

SchemeSaathi is an intelligent, citizen-centric government scheme action platform built to guide Indian citizens from discovery to actual application readiness, document gap resolution, application tracking, official source verification, fraud protection, and privacy control.

---

## Key Features Implemented

1. **Smart Document Gap Analyzer**: Compares required scheme documents against citizen documents in their private vault, displaying checked, expiring, and missing documents.
2. **Application Readiness Score (0–100%)**: Dynamic composite score evaluating Eligibility (40%), Document Availability (40%), Validity (10%), and Official Source/Deadline (10%) with actionable remaining steps.
3. **Missing Document Solver**: Interactive resolution guide providing Issuing Authority, Step-by-Step Online/Offline instructions, Required Proofs, and Verified `.gov.in`/`.nic.in` portal links.
4. **Document Expiry Detection**: Live validity tracking with amber badges (`Expiring Soon` within 30 days) and renewal alerts.
5. **Scheme Priority Engine**: Multi-factor ranking algorithm prioritizing schemes based on eligibility confidence, document readiness, deadline urgency, and benefit value (`#1 APPLY NOW`, `#2 APPLY NEXT`).
6. **Side-by-Side Scheme Comparison**: Compare 2 to 4 schemes with criteria matrices and personalized recommendations.
7. **"MY NEXT ACTION" Hero Widget**: Instant recommendation on the single action that unlocks the maximum number of schemes.
8. **Application Tracker & Visual Stepper**: Track submitted applications across 5 stages (`Applied` → `Document Verification` → `Department Verification` → `Approved` → `Benefit Disbursed`) with `DEMO DATA` watermark.
9. **Rejection Assistant ("What can I do next?")**: Official grievance mechanisms (CPGRAMS `pgportal.gov.in`, state CM helplines) and corrective actions for rejected applications.
10. **Deadline & Expiry Alerts Center**: Live notification banner for closing schemes and expiring documents.
11. **Life-Event Recheck ("Has anything changed?")**: Quick scenario recalculation (started college, graduated, started business, income changed, welcomed child, became farmer).
12. **Government Benefits Health Check**: Live dashboard summary metrics (Eligible Schemes, High Priority, Ready to Apply, Missing Docs, Expiring Docs, Deadlines).
13. **Official Source Safety Verifier**: Audits and displays verified government ministries, departments, and official `.gov.in` domains.
14. **Government Scheme Fraud Shield**: Anti-phishing guidelines, warnings against fake portals, and OTP/PIN sharing alerts.
15. **Privacy Dashboard & Consent Vault**: Download My Data (JSON export), document deletion, DigiLocker mock consent toggle, and Right to be Forgotten data purge.
16. **Multi-Tenant Document Security**: Complete data isolation. Automated test suite verifies User A cannot access User B's documents (HTTP 403 Forbidden).
17. **Grounded AI Safe Guide**: Accurate answers referencing verified knowledgebase without hallucinating non-existent schemes or fake links.
18. **Multilingual Support**: Seamless language toggle between **English**, **हिंदी (Hindi)**, and **मराठी (Marathi)**.
19. **Hackathon Demo Personas**: Pre-loaded personas for **Rahul Sharma** (Rural Student) and **Sunita Devi** (Small Farmer).

---

## How to Run

1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```bash
   cd C:\Users\Dell\.gemini\antigravity\scratch\schemesaathi
   ```
3. Run the server:
   ```bash
   python server.py
   ```
4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

---

## Running Automated Security Tests

Run the security test suite to verify multi-tenant isolation, readiness scoring, and document gap analysis:
```bash
python test_security.py
```
