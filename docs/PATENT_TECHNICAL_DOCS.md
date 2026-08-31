# Patent-Oriented Technical Specification

## Title of the Invention
**DYNAMIC CITIZEN BENEFIT TWIN AND GOVERNMENT RULE-GRAPH SYSTEM FOR CONTINUOUS ELIGIBILITY RECALCULATION, DOCUMENT READINESS ANALYSIS, AND NEXT-BEST BENEFIT ACTION OPTIMIZATION**

---

> **Patent Prototype Notice**: This document outlines the technical architecture of the *SchemeSaathi* patent-oriented prototype. Where live external government departmental endpoints are unavailable in local staging environments, operations are safely simulated with explicit mock tags (`DEMO / MOCK / SIMULATION`).

---

## 1. Field of the Invention
This invention relates to computational welfare informatics, semantic knowledge graphs, and reactive state-machine architectures. More specifically, it pertains to a **Dynamic Citizen Benefit Twin (CBT)** connected to a **16-Node Government Rule-Graph (GRG)** for event-driven eligibility recalculation, multi-factor document readiness optimization, explainable deterministic rule tracing, hypothetical scenario simulation, and policy amendment impact projection.

---

## 2. Technical Problems Addressed & Prior Art Deficiencies

| Deficiency in Prior Art | Failure Mode in Government Welfare | Technical Solution in SchemeSaathi |
| :--- | :--- | :--- |
| **Static Profile Silos** | Citizen profiles are static database rows; when a document expires or age increments, benefits are silently lost. | **Dynamic Citizen Benefit Twin (CBT)**: Derived, reactive state machine tracking continuous entitlement status across 15 discrete states. |
| **Brute-Force Periodic Scans** | Systems run $O(N \times M)$ full recalculations daily, resulting in excessive compute latency and stale cache states. | **Selective Event-Driven Dependency Recalculation**: Recalculates only downstream subgraphs in $O(\Delta k)$ upon lifecycle triggers, yielding **11.7x to 14.8x speedup**. |
| **LLM Hallucinations in Welfare** | Generative models fabricate qualification criteria, causing application rejection and citizen disenfranchisement. | **Deterministic Rule Graph + Machine-Readable Decision Traces**: 100% deterministic rule evaluations with verifiable per-rule boolean verdicts. |
| **Document Vault Blindness** | Portals check eligibility without verifying supporting proofs, leading citizens to apply without prerequisites. | **Document Dependency & Unlock Graph**: Identifies high-leverage document prerequisites unlocking multiple welfare programs simultaneously. |
| **Lack of Action Prioritization** | Citizens are presented with long lists of schemes with no guidance on which step offers the highest ROI. | **Optimized Next Best Action (NBA) Engine**: Ranks citizen tasks by mathematical benefit score, urgency, effort, and dependency value. |

---

## 3. Mathematical Models and System Formulations

### 3.1. 16-Node & 14-Relationship Knowledge Graph Ontology
The system models government welfare as an attributed multi-relational property graph:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{T}_v, \mathcal{T}_e)$$

Nodes: `Citizen`, `Attribute`, `Scheme`, `SchemeVersion`, `EligibilityRule`, `Document`, `DocumentType`, `Benefit`, `Ministry`, `Department`, `State`, `District`, `GovernmentPortal`, `Deadline`, `Application`, `LifeEvent`.

Relationships: `HAS_ATTRIBUTE`, `HAS_DOCUMENT`, `LIVES_IN`, `EXPERIENCED`, `HAS_VERSION`, `HAS_RULE`, `REQUIRES`, `PROVIDES`, `ADMINISTERED_BY`, `HAS_DEADLINE`, `HAS_PORTAL`, `SATISFIES`, `SUPPORTS`, `SUPERSEDES`.

### 3.2. 15-State Benefit Lifecycle State Machine
Each scheme in a citizen's Benefit Twin exists in exactly one deterministic state:
`UNKNOWN`, `POTENTIALLY_ELIGIBLE`, `ELIGIBLE`, `DOCUMENT_INCOMPLETE`, `APPLICATION_READY`, `APPLICATION_STARTED`, `SUBMITTED`, `UNDER_REVIEW`, `ADDITIONAL_INFORMATION_REQUIRED`, `APPROVED`, `BENEFIT_RECEIVED`, `NOT_ELIGIBLE`, `REJECTED`, `EXPIRED`, `SUSPENDED`.

### 3.3. Next Best Action (NBA) Optimization Formula
$$\text{Action Score}(a) = \frac{\text{Benefit Impact}(a) \times \text{Urgency}(a) \times \text{Confidence}(a) \times \text{Dependency Value}(a)}{\text{Estimated Effort}(a)}$$

### 3.4. Transparent Opportunity Guidance Score
$$\text{Opportunity Score} = 0.40 \cdot P_{\text{elig}} + 0.30 \cdot P_{\text{doc}} + 0.20 \cdot P_{\text{app}} + 0.10 \cdot P_{\text{urg}}$$

---

## 4. Key Patent Claims
1. A method for continuous Citizen Benefit Twin computation and selective event-driven graph recalculation.
2. A deterministic explainable decision trace engine providing machine-readable per-rule boolean evaluations grounded in official gazettes.
3. An in-memory hypothetical What-If scenario simulation method without mutating persistent citizen data.
4. A government policy change simulator forecasting demographic and budget impacts across multi-tenant citizen populations.
