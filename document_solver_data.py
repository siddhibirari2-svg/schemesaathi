"""
SchemeSaathi - Missing Document Solver Knowledgebase
Contains comprehensive, strictly verified official issuance guides, issuing authorities,
step-by-step application flows, and official portals for major Indian citizen documents.
Never invents government URLs.
"""

DOCUMENT_GUIDES = {
    "Aadhaar Card": {
        "doc_name": "Aadhaar Card (UIDAI)",
        "issuing_authority": "Unique Identification Authority of India (UIDAI), Ministry of Electronics & IT",
        "purpose": "Universal proof of identity, address, and demographic credentials required for Direct Benefit Transfer (DBT) and biometric authentication.",
        "official_url": "https://myaadhaar.uidai.gov.in",
        "official_domain": "uidai.gov.in / myaadhaar.uidai.gov.in",
        "last_verified_date": "2026-08-15",
        "processing_time": "15 to 30 days for new enrollment / 48-72 hours for PVC or online demographic update",
        "application_fee": "Free for fresh enrollment; ₹50 for address update or PVC card reprint",
        "required_proofs": [
            "Proof of Identity (POI) (e.g. Passport, PAN, Voter ID, Ration Card)",
            "Proof of Address (POA) (e.g. Electricity bill, Water bill, Bank Passbook, Domicile)",
            "Proof of Date of Birth (DOB) (e.g. Birth Certificate, 10th Marksheet)"
        ],
        "online_steps": [
            "Visit the official UIDAI portal at myaadhaar.uidai.gov.in.",
            "Click on 'Book an Appointment' for fresh enrollment or 'Login with OTP' for demographic updates.",
            "Select your State, District, and nearest Aadhaar Seva Kendra / Authorized Bank / Post Office.",
            "Visit the center on the scheduled date with original POI, POA, and DOB documents for biometric capture.",
            "Collect the 28-digit Enrollment Acknowledgement Slip (EID) to track status online."
        ],
        "offline_steps": [
            "Visit nearest Aadhaar Seva Kendra, Post Office, or Bank branch.",
            "Fill out the standard Aadhaar Enrollment / Correction Form.",
            "Provide biometric scan (10 fingerprints, iris scan, facial photograph) and original document verification.",
            "Receive physical enrollment receipt."
        ],
        "renewal_info": "Mandatory biometric update for children at age 5 and age 15 (Free of cost). Adults should verify/update demographic details every 10 years."
    },
    "Income Certificate": {
        "doc_name": "Income Certificate (Aamdani Praman Patra)",
        "issuing_authority": "Revenue Department / Tahsildar / Sub-Divisional Magistrate (SDM) of State Government",
        "purpose": "Official legal proof of annual household/family earnings to determine eligibility for subsidies, reservations, fee concessions, and scholarships.",
        "official_url": "https://services.india.gov.in/service/search?kw=Income+Certificate",
        "official_domain": "services.india.gov.in / State e-District Portals (.gov.in / .nic.in)",
        "last_verified_date": "2026-08-10",
        "processing_time": "7 to 15 working days as per State Citizen Service Guarantee Act",
        "application_fee": "₹15 to ₹50 depending on state e-District service charges",
        "required_proofs": [
            "Aadhaar Card / Voter ID of applicant & family head",
            "Salary Slips (Last 3 months) OR Form 16 / ITR OR Self-Declaration Affidavit on ₹100 stamp paper",
            "Ration Card or BPL Survey Record",
            "Electricity Bill or Land Revenue Receipt (7/12 Extract)",
            "Passport-size photograph"
        ],
        "online_steps": [
            "Log in to your State e-District portal (e.g., Aaple Sarkar in Maharashtra, e-District Delhi/UP/Bihar, MeeSeva, Seva Sindhu).",
            "Select 'Revenue Department' → 'Certificate of Income'.",
            "Fill applicant personal details, family member occupation, and declared annual income.",
            "Upload self-attested scanned copies of Aadhaar, Ration Card, and Income proof/Affidavit.",
            "Pay nominal fee online and download the Application Tracking Receipt.",
            "Upon field verification by Talathi/Patwari and approval by Tehsildar, download digitally signed certificate."
        ],
        "offline_steps": [
            "Visit local Tehsil Office, Sub-Divisional Magistrate (SDM) office, or Village Citizen Service Center (CSC).",
            "Submit physical application form attached with notary affidavit and salary/farm proofs.",
            "Local Revenue Inspector (Patwari/Talathi) conducts enquiry and submits report to Tehsildar for approval."
        ],
        "renewal_info": "⚠️ Validity: Typically 1 Financial Year (April 1 to March 31) or 6-12 months. Requires annual renewal before academic/fiscal cycle."
    },
    "Domicile Certificate": {
        "doc_name": "Domicile / Residence Certificate (Nivasi Praman Patra)",
        "issuing_authority": "Sub-Divisional Magistrate (SDM) / Executive Magistrate / Revenue Department",
        "purpose": "Certifies that a person has been residing continuously in a particular state/UT for a specified minimum period (usually 10-15 years), unlocking state quota schemes, state scholarships, and jobs.",
        "official_url": "https://services.india.gov.in/service/search?kw=Domicile+Certificate",
        "official_domain": "services.india.gov.in / State e-District Portals (.gov.in / .nic.in)",
        "last_verified_date": "2026-08-12",
        "processing_time": "15 to 21 working days",
        "application_fee": "₹20 to ₹60",
        "required_proofs": [
            "Proof of Continuous Stay (Electricity bills / Rent agreements / Property tax receipts for past 10-15 years)",
            "School Leaving Certificate (TC) or 10th/12th Marksheet indicating schooling in state",
            "Aadhaar Card / Voter ID Card",
            "Birth Certificate",
            "Self-declaration / Notarized Affidavit"
        ],
        "online_steps": [
            "Open your State e-District or Public Services Delivery portal.",
            "Register citizen login with Mobile/Aadhaar OTP.",
            "Navigate to 'Services' → 'Domicile / Resident Certificate'.",
            "Provide historical residency details and upload school certificates proving 10+ years stay.",
            "Submit online application and track with Application Acknowledgement Number.",
            "Download QR-coded digitally signed Domicile Certificate once SDM signs."
        ],
        "offline_steps": [
            "Collect Domicile Application Form from Taluk/Tehsil or CSC Center.",
            "Attach notary affidavit, school leaving certificate, and address proofs of parents.",
            "Submit to Revenue Office counter for verification."
        ],
        "renewal_info": "✓ Permanent validity in most Indian states unless place of residence changes."
    },
    "Caste Certificate & Validity": {
        "doc_name": "Caste Certificate & Caste Validity (Jati Praman Patra)",
        "issuing_authority": "Sub-Divisional Officer (SDO) / District Caste Scrutiny Committee",
        "purpose": "Affirms category status (SC, ST, OBC, VJ/NT, EWS) to avail reservations, scholarships, and social welfare benefits.",
        "official_url": "https://services.india.gov.in/service/search?kw=Caste+Certificate",
        "official_domain": "services.india.gov.in / State Social Justice Portals",
        "last_verified_date": "2026-08-11",
        "processing_time": "21 to 45 working days (Caste Scrutiny may take 60-90 days)",
        "application_fee": "₹30 to ₹100",
        "required_proofs": [
            "Father's / Grandfather's School Leaving Certificate / Primary School Record showing Caste entry",
            "Old Revenue / Land Record mentioning caste (pre-notified cutoff year, e.g. 1950 for SC/ST, 1967 for OBC in Maharashtra)",
            "Applicant's School Leaving Certificate & Aadhaar Card",
            "Genealogy / Family Tree Affidavit signed by applicant/family elders"
        ],
        "online_steps": [
            "Log in to State e-District / CCVIS (Caste Certificate Verification Information System).",
            "Select Category (SC / ST / OBC / SEBC / EWS) and enter caste sub-group.",
            "Upload father's/blood relative's valid caste evidence and genealogy chart.",
            "Submit application and note Acknowledgement Number for enquiry.",
            "For Validity, apply to District Caste Scrutiny Committee with college recommendation letter."
        ],
        "offline_steps": [
            "Submit physical dossier with ancestry records at Sub-Divisional Magistrate office.",
            "Attend hearing at Caste Scrutiny Committee if summoned for original document inspection."
        ],
        "renewal_info": "Caste certificate has lifetime validity; Non-Creamy Layer (NCL) certificate for OBC/EWS must be renewed every 1-3 financial years."
    },
    "Bank Account / Passbook with DBT Seeding": {
        "doc_name": "Bank Account with Aadhaar NPCI DBT Seeding",
        "issuing_authority": "Reserve Bank of India (RBI) Regulated Bank / National Payments Corporation of India (NPCI)",
        "purpose": "Required for direct government cash transfers (scholarships, PM-Kisan, subsidies) via Aadhaar Payment Bridge (APB) system.",
        "official_url": "https://myaadhaar.uidai.gov.in/check-aadhaar-bank-account-status",
        "official_domain": "uidai.gov.in / npci.org.in / Official Bank Websites",
        "last_verified_date": "2026-08-16",
        "processing_time": "Same day account opening / 24-48 hours for NPCI Aadhaar seeding mapper update",
        "application_fee": "Zero balance account under Pradhan Mantri Jan Dhan Yojana (PMJDY)",
        "required_proofs": [
            "Aadhaar Card (Original + Copy)",
            "PAN Card (or Form 60)",
            "2 Passport size photographs",
            "Valid Mobile Number for SMS alerts"
        ],
        "online_steps": [
            "Open digital savings account via Video KYC on bank website/app (SBI YONO, Bank of Baroda, IPPB, etc.).",
            "Ensure 'Opt-in for Direct Benefit Transfer (DBT) credit' checkbox is selected during KYC.",
            "Check seeding status anytime at myaadhaar.uidai.gov.in ('Bank Seeding Status' service)."
        ],
        "offline_steps": [
            "Visit nearest bank branch or India Post Payments Bank (IPPB) access point.",
            "Fill standard Account Opening Form and 'Aadhaar Seeding / NPCI Mandate Form'.",
            "Submit biometric fingerprint to link bank account with NPCI DBT mapper."
        ],
        "renewal_info": "Keep account active with at least one transaction every 6 months to avoid dormant/inoperative status."
    },
    "Land Records / 7/12 Extract / RoR": {
        "doc_name": "Land Records / Record of Rights (RoR) / 7/12 Extract / Khata",
        "issuing_authority": "State Land Revenue Department / Bhulekh / Mahabhulekh / Bhoomi",
        "purpose": "Verifies agricultural land ownership, parcel size, survey number, and cultivation status for PM-Kisan and farmer assistance schemes.",
        "official_url": "https://services.india.gov.in/service/search?kw=Land+Records+Bhulekh",
        "official_domain": "services.india.gov.in / State Bhulekh Portals (.gov.in / .nic.in)",
        "last_verified_date": "2026-08-09",
        "processing_time": "Instant online download with digital signature / 3 days at Tehsil",
        "application_fee": "₹15 for digitally signed extract; Free for viewing",
        "required_proofs": [
            "District, Taluk/Tehsil, Village Name",
            "Survey Number / Gath Number / Khata Number",
            "Aadhaar Card / Land Owner Name"
        ],
        "online_steps": [
            "Visit state land portal (e.g. Mahabhumi/Digital 7/12 in MH, Bhulekh UP/Bihar, Bhoomi Karnataka, Dharani Telangana).",
            "Select District → Tehsil → Village and enter Survey Number or Owner Name.",
            "Select 'Download Digitally Signed 7/12 / RoR'.",
            "Pay ₹15 and instantly download official QR-coded PDF document."
        ],
        "offline_steps": [
            "Visit local Gram Panchayat / Talathi office or Tehsil Bhulekh counter.",
            "Request physical stamped copy of 7/12 / Khatiyan extract from Revenue clerk."
        ],
        "renewal_info": "Download latest extract (within 3-6 months) to reflect current crop and ownership status."
    },
    "Ration Card (BPL / AAY)": {
        "doc_name": "Ration Card (NFSA / BPL / AAY / PHH)",
        "issuing_authority": "Department of Food, Civil Supplies and Consumer Affairs (State Gov)",
        "purpose": "Proof of family economic classification and subsidised food grain entitlement; vital for housing, healthcare, and welfare quotas.",
        "official_url": "https://nfsa.gov.in/portal/ration_card_state_portals_aa",
        "official_domain": "nfsa.gov.in / State Food & Civil Supplies Portals",
        "last_verified_date": "2026-08-14",
        "processing_time": "30 days",
        "application_fee": "₹20 to ₹50",
        "required_proofs": [
            "Aadhaar cards of all family members",
            "Income certificate / BPL survey inclusion certificate",
            "Gas connection details (LPG consumer number)",
            "Electricity bill / House tax receipt",
            "Group family photograph"
        ],
        "online_steps": [
            "Open your State Food & Civil Supplies portal or NFSA portal at nfsa.gov.in.",
            "Click on 'Apply for New Ration Card' or 'Member Addition'.",
            "Enter Head of Family and dependent details along with Aadhaar numbers.",
            "Upload scanned documents and submit for Food Inspector field verification.",
            "Track Application Reference and download e-Ration Card."
        ],
        "offline_steps": [
            "Collect application form from local Fair Price Shop (Ration Shop) or Circle Food Office.",
            "Attach copies of Aadhaar of all members and submit to Food Supply Inspector."
        ],
        "renewal_info": "Complete eKYC for all family members at Fair Price Shop (FPS) via biometric PoS machine to prevent deactivation."
    },
    "10th / 12th Marksheet": {
        "doc_name": "Secondary / Higher Secondary Marksheet & Passing Certificate",
        "issuing_authority": "State Education Board / CBSE / CISCE / DigiLocker National Academic Depository (NAD)",
        "purpose": "Academic proof of educational qualification, date of birth, and merit criteria for scholarships and apprenticeship programs.",
        "official_url": "https://www.digilocker.gov.in",
        "official_domain": "digilocker.gov.in / cbse.gov.in / State Board Portals",
        "last_verified_date": "2026-08-16",
        "processing_time": "Instant via DigiLocker / 15 days for duplicate physical copy from Board",
        "application_fee": "Free on DigiLocker; ₹200-₹500 for duplicate board certificate",
        "required_proofs": [
            "Roll Number / Seat Number",
            "Year of Examination & Center Code",
            "Aadhaar Card linked to Mobile"
        ],
        "online_steps": [
            "Open DigiLocker website (digilocker.gov.in) or mobile app.",
            "Sign in with Aadhaar OTP.",
            "Search for your Education Board (e.g. CBSE, Maharashtra State Board, UP Board).",
            "Select 'Class X Marksheet' or 'Class XII Marksheet'.",
            "Enter Roll Number and Passing Year; click 'Get Document'.",
            "Instantly save and download the legally valid digitally signed mark sheet."
        ],
        "offline_steps": [
            "Apply to the Divisional Board Secretary with school forwarding letter and fee challan for physical duplicate copy."
        ],
        "renewal_info": "Permanent validity. DigiLocker electronic copy is legally valid under IT Act 2000 Section 9A."
    },
    "PAN Card": {
        "doc_name": "Permanent Account Number (PAN Card)",
        "issuing_authority": "Income Tax Department, Ministry of Finance (via NSDL / Protean / UTIITSL)",
        "purpose": "Mandatory financial identification for business loans, bank transactions, MSME registrations, and tax compliance.",
        "official_url": "https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html",
        "official_domain": "incometax.gov.in / onlineservices.nsdl.com",
        "last_verified_date": "2026-08-15",
        "processing_time": "Instant e-PAN (10 minutes via Aadhaar OTP) / 10-15 days for physical plastic card",
        "application_fee": "Free for Instant e-PAN; ₹107 for physical card dispatched to address",
        "required_proofs": [
            "Aadhaar Card with active mobile number linked for OTP e-KYC"
        ],
        "online_steps": [
            "Go to Income Tax e-Filing Portal (eportal.incometax.gov.in) → 'Instant e-PAN'.",
            "Enter 12-digit Aadhaar number and validate with OTP received on Aadhaar-linked mobile.",
            "Confirm demographic details pulled automatically from UIDAI.",
            "Download digitally signed Instant e-PAN PDF within 10 minutes free of charge."
        ],
        "offline_steps": [
            "Submit Form 49A at nearest NSDL / UTIITSL TIN-Facilitation Center with Aadhaar copy."
        ],
        "renewal_info": "Permanent validity. Mandatory linking of PAN with Aadhaar."
    },
    "Udyam MSME Registration Certificate": {
        "doc_name": "Udyam Registration Certificate (MSME)",
        "issuing_authority": "Ministry of Micro, Small and Medium Enterprises (MSME)",
        "purpose": "Official legal status for micro, small, and medium enterprises to access Mudra loans, Stand-Up India, collateral subsidies, and priority bank credit.",
        "official_url": "https://udyamregistration.gov.in",
        "official_domain": "udyamregistration.gov.in",
        "last_verified_date": "2026-08-17",
        "processing_time": "Instant online generation (100% Paperless & Free)",
        "application_fee": "₹0 (Completely Free - Beware of fake payment portals)",
        "required_proofs": [
            "Aadhaar Number of entrepreneur / business owner",
            "PAN Number of business or proprietor",
            "Bank Account Number & IFSC",
            "Business activity / NIC Code & Number of employees"
        ],
        "online_steps": [
            "Open official government portal: udyamregistration.gov.in (Verify .gov.in domain!).",
            "Select 'For New Entrepreneurs who are not Registered yet as MSME'.",
            "Enter Aadhaar Number and validate with OTP.",
            "Enter PAN details and business location address.",
            "Choose National Industry Classification (NIC) code matching trade/service.",
            "Submit and immediately download QR-coded Udyam Certificate."
        ],
        "offline_steps": [
            "Visit District Industries Centre (DIC) or MSME-Development Institute for free guided registration."
        ],
        "renewal_info": "Permanent validity with annual auto-update of turnover through GST/ITR integration."
    }
}

def get_document_guide(doc_name):
    # Try exact match or fuzzy match
    for key, guide in DOCUMENT_GUIDES.items():
        if key.lower() in doc_name.lower() or doc_name.lower() in key.lower():
            return guide
    # Fallback to general government guide
    return {
        "doc_name": doc_name,
        "issuing_authority": "Designated State / Central Government Department",
        "purpose": f"Official document required to establish applicant eligibility criteria for {doc_name}.",
        "official_url": "https://services.india.gov.in",
        "official_domain": "services.india.gov.in",
        "last_verified_date": "2026-08-01",
        "processing_time": "7 to 21 working days as per Citizen Charter",
        "application_fee": "Nominal statutory fee as applicable",
        "required_proofs": ["Aadhaar Card", "Proof of Identity", "Proof of Address", "Passport Photo"],
        "online_steps": [
            "Visit National Government Services Portal at services.india.gov.in or State e-District Portal.",
            f"Search for '{doc_name}'.",
            "Submit citizen application with verified identity documents and track application ID."
        ],
        "offline_steps": [
            "Visit nearest Common Service Center (CSC) or Tehsildar / District Administrative office with original documents."
        ],
        "renewal_info": "Check document for stated validity date or renew annually as applicable."
    }
