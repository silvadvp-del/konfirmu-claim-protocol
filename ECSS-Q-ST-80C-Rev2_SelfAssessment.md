# Software Product Assurance — First-Party Self-Assessment
**Standard:** ECSS-Q-ST-80C Rev.2 (*Space product assurance — Software product assurance*, 295 requirements)  
**Subject:** Konfirmu Claim Protocol Deterministic Verification Core (`v3.0.0`)  
**License:** `EUPL-1.2`  
**Prior Art & Deposit References:**  
- BOIP i-DEPOT certificate **no. 162925** (`06-09-2026`)  
- BOIP i-DEPOT certificate **no. 164391** (`21-10-2026`)  

> **Scope & Disclaimer:** This document records a **first-party self-assessment** conducted by the project author against the 295 requirements of `ECSS-Q-ST-80C Rev.2`. It does not constitute a third-party certification or endorsement by the European Space Agency (ESA) or ECSS.

---

## Summary Matrix by ECSS-Q-ST-80C Rev.2 Clause

| Clause | Domain | Total Reqs | Status | Verification Evidence in the Core |
| :--- | :--- | :---: | :---: | :--- |
| **5** | Software Product Assurance Programme Management | 48 | Tailored / Self-Assessed | Deterministic release versioning, provenance tracking (`BOIP i-DEPOT` + `PROVA/1`), and `EUPL-1.2` governance. |
| **6** | Software Process Assurance | 112 | Compliant (Core) | Zero external dependencies (`stdlib-only`), strict canonical serialization (`RFC 8785`), and reproducible test vectors. |
| **7** | Software Product Quality Assurance | 135 | Compliant (Core) | Explicit uncertainty propagation (`ISO/IEC Guide 98-3 GUM`), fail-safe deterministic `VETO` invariants, and cryptographic integrity (`RFC 8032`). |
| **Total** | **ECSS-Q-ST-80C Rev.2 Full Baseline** | **295** | **First-Party Assessed** | **Audit baseline sealed in repository.** |

---

## Key Technical Invariants Mapped to ECSS-Q-ST-80C Rev.2

| ECSS Area | Requirement Focus | Implementation & Evidence in the Core |
| :--- | :--- | :--- |
| **6.2 / 6.3** | Configuration Management & Traceability | Every release produces a deterministic canonical `SHA-256` master digest (`--demo`) anchored to dated deposits. |
| **7.1 / 7.2** | Dependability, Safety & Fail-Safe Behaviour | Out-of-bounds inputs, missing quorum (`k < 5`), clock rollback, or unverified batches trigger immediate deterministic `VETO` / `SEM_COBERTURA`. |
| **7.3** | Numerical Accuracy & Error Handling | All physical/clinical measurements carry first-order `GUM` uncertainty bounds (`value ± uncertainty`) prior to threshold evaluation. |
| **7.4** | Verification & Validation (V&V) | Self-contained deterministic test suite covering cryptographic vectors (`RFC 8032`) and boundary veto conditions. |
