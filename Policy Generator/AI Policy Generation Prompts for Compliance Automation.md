# AI Policy Generation Prompts for Compliance Automation

This document outlines the strategy and examples for developing robust AI prompts to automate compliance policy generation. The goal is to enable the AI engine to produce accurate, comprehensive, and contextually relevant policies tailored to specific compliance frameworks, Australian industry requirements, and organizational profiles.

## Principles of Effective AI Policy Generation Prompts

Effective prompts for AI-driven policy generation must be clear, comprehensive, and structured to guide the AI model towards producing high-quality, actionable compliance policies. Key principles include:

1.  **Specificity:** Clearly define the scope, purpose, and target audience of the policy.
2.  **Contextualization:** Provide relevant organizational details, industry sector, and specific operational environment.
3.  **Framework Alignment:** Explicitly state the compliance framework(s) and specific controls the policy must address.
4.  **Output Format and Tone:** Specify the desired format (e.g., Markdown, plain text, section headings) and the required tone (e.g., formal, technical, accessible).
5.  **Constraint Definition:** Include any constraints or exclusions (e.g., 


avoiding certain jargon, adhering to specific word counts).
6.  **Iterative Refinement:** Acknowledge that prompt engineering is an iterative process, requiring testing and refinement based on AI output.

## General Prompt Structure for Policy Generation

A robust prompt for compliance policy generation should typically include the following sections:

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable compliance policy. Adhere strictly to the specified compliance frameworks and organizational context. Ensure the policy is clear, concise, and addresses all relevant controls.

[POLICY CONTEXT]
- **Policy Title:** [e.g., Information Security Policy, Data Privacy Policy]
- **Policy Purpose:** [Briefly explain why this policy exists]
- **Target Audience:** [e.g., All Employees, IT Staff, Management]
- **Organizational Name:** [Client's Organization Name]
- **Industry Sector:** [e.g., Finance, Healthcare, Government, Education, Retail]
- **Organizational Profile:** [Brief description of the organization, its size, operations, and any specific characteristics relevant to compliance]
- **Existing Infrastructure/Technology Stack:** [e.g., AWS Cloud, Microsoft 365, On-premise servers, specific software]
- **Data Types Handled:** [e.g., Personal Identifiable Information (PII), Health Information, Payment Card Data, Classified Government Information, Intellectual Property]

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** [e.g., ISM, Essential 8, ISO 27001, PSPF, APRA CPS 234, Privacy Act 1988]
- **Specific Controls/Requirements to Address:** [List specific controls, clauses, or principles from the frameworks. For Essential 8, specify maturity level. For PSPF, specify relevant policies/guidelines.]
- **Cross-Framework Mappings (if applicable):** [Mention if the policy needs to satisfy requirements from multiple frameworks simultaneously]

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** [e.g., Introduction, Scope, Definitions, Roles and Responsibilities, Policy Statements, Procedures, Compliance and Enforcement, Review and Update, Related Documents]
- **Specific Policy Statements/Directives:** [Any specific directives or rules the policy must enforce]
- **Procedural Guidance:** [Indicate if the policy needs to include detailed procedural steps]
- **Reporting Requirements:** [e.g., Incident reporting, compliance reporting]
- **Training and Awareness:** [Requirements for staff training]

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** [e.g., Markdown, structured headings, bullet points for key requirements]
- **Tone:** [e.g., Formal, authoritative, clear, easy to understand]
- **Length:** [e.g., Approximately 1000-1500 words, concise]
- **Exclusions/Limitations:** [e.g., Do not include specific technical configurations, focus on policy principles]
- **Language:** English (Australian context)

[EXAMPLE OUTPUT (Optional - for fine-tuning or few-shot learning)]
[Provide a good example of a policy if available, to guide the AI's style and content.]
```

## Prompt Examples for Specific Frameworks and Industries

Below are examples of how to construct prompts for the AI engine, incorporating the research findings for ISM, Essential 8, ISO 27001, PSPF, and industry-specific requirements.

### Example 1: Australian Finance Industry - APRA CPS 234 & ISO 27001 Information Security Policy

**Goal:** Generate an Information Security Policy for an APRA-regulated financial institution, focusing on CPS 234 and ISO 27001 requirements.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Information Security Policy for an Australian financial institution. Adhere strictly to APRA CPS 234 and ISO 27001 requirements, ensuring the policy is clear, concise, and addresses all relevant controls for the finance sector. The policy must reflect a strong commitment to protecting sensitive customer and organizational data.

[POLICY CONTEXT]
- **Policy Title:** Information Security Policy
- **Policy Purpose:** To establish a framework for managing information security risks, protecting information assets, and ensuring compliance with regulatory and legal obligations for a financial institution.
- **Target Audience:** All employees, contractors, and third-party service providers of [Client's Organization Name].
- **Organizational Name:** [e.g., "SecureBank Australia Ltd."]
- **Industry Sector:** Finance (APRA-regulated entity)
- **Organizational Profile:** A medium-sized retail bank operating across Australia, handling customer deposits, loans, and investment services. Utilizes a hybrid cloud environment (AWS for customer-facing applications, on-premise for core banking systems).
- **Data Types Handled:** Personal Identifiable Information (PII), Financial Transaction Data, Payment Card Data, Customer Account Information, Sensitive Business Information.

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** APRA CPS 234 Information Security, ISO/IEC 27001:2022 (Information Security Management System)
- **Specific Controls/Requirements to Address:**
    - **APRA CPS 234:** All clauses, with particular emphasis on:
        - Clause 5: Information security policy framework
        - Clause 10: Information asset identification and classification
        - Clause 13: Information security capabilities
        - Clause 19: Incident management
        - Clause 24: Testing
        - Clause 34: Third-party arrangements
    - **ISO 27001 Annex A Controls:** A.5 Organizational controls, A.6 People controls, A.7 Physical controls, A.8 Technological controls, with specific focus on:
        - A.5.1.1 Policies for information security
        - A.5.1.2 Information security roles and responsibilities
        - A.5.7.1 Threat intelligence
        - A.5.23.1 Information security for use of cloud services
        - A.6.6.1 Contact with authorities
        - A.8.1.1 Inventory of information and other associated assets
        - A.8.1.2 Ownership of assets
        - A.8.2.1 Classification of information
        - A.8.2.3 Handling of assets
        - A.8.16.1 Monitoring, review and event logging
- **Cross-Framework Mappings:** The policy should demonstrate how ISO 27001 controls support and fulfill the requirements of APRA CPS 234.

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Summary, Scope, Definitions, Information Security Principles, Roles and Responsibilities (including Board/Senior Management accountability), Information Asset Management (Identification, Classification, Ownership), Risk Management, Information Security Controls (Logical, Physical, Personnel), Incident Management, Business Continuity and Disaster Recovery, Third-Party Security, Compliance and Review, Training and Awareness, Policy Enforcement.
- **Specific Policy Statements/Directives:** Explicit directives on data encryption, access control, secure system development, regular security assessments, and reporting of security incidents.
- **Procedural Guidance:** High-level procedural guidance for incident response, third-party security assessments, and data classification.
- **Reporting Requirements:** Requirements for reporting security incidents to internal stakeholders and APRA (as per CPS 234).
- **Training and Awareness:** Mandatory annual information security awareness training for all personnel.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings (H1, H2, H3). Use bullet points for lists of requirements or responsibilities.
- **Tone:** Formal, authoritative, and professional. Avoid overly technical jargon where possible, or provide clear definitions.
- **Length:** Comprehensive, approximately 2000-3000 words.
- **Exclusions/Limitations:** Do not include specific technical configurations (e.g., firewall rules). Focus on policy principles and high-level requirements.
- **Language:** English (Australian context).
```

### Example 2: Australian Healthcare Industry - Privacy Act & My Health Record Security Policy

**Goal:** Generate a Data Privacy and Security Policy for an Australian healthcare provider, focusing on the Privacy Act 1988 (APPs) and My Health Record Act requirements.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Data Privacy and Security Policy for an Australian healthcare provider. Adhere strictly to the Privacy Act 1988 (including Australian Privacy Principles) and the My Health Record Act 2012, ensuring the policy is clear, concise, and addresses all relevant controls for protecting sensitive health information.

[POLICY CONTEXT]
- **Policy Title:** Data Privacy and Security Policy
- **Policy Purpose:** To outline the organization's commitment and approach to protecting personal and health information, ensuring compliance with Australian privacy legislation, and maintaining the security of patient data, including My Health Record information.
- **Target Audience:** All employees, contractors, and volunteers of [Client's Organization Name] who handle personal or health information.
- **Organizational Name:** [e.g., "MediCare Clinic Group"]
- **Industry Sector:** Healthcare (Private Clinic Network)
- **Organizational Profile:** A network of private medical clinics providing general practice, specialist, and allied health services across several Australian states. Utilizes an electronic health record (EHR) system and participates in the My Health Record system.
- **Data Types Handled:** Health Information, Personal Identifiable Information (PII), Sensitive Information (e.g., genetic information, biometric data).

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** Privacy Act 1988 (Cth) (Australian Privacy Principles), My Health Record Act 2012
- **Specific Controls/Requirements to Address:**
    - **Privacy Act 1988 (APPs):** All 13 APPs, with particular emphasis on:
        - APP 1: Open and transparent management of personal information
        - APP 3: Collection of solicited personal information (especially sensitive information)
        - APP 6: Use or disclosure of personal information
        - APP 8: Cross-border disclosure of personal information
        - APP 11: Security of personal information
        - APP 12: Access to personal information
        - APP 13: Correction of personal information
    - **My Health Record Act 2012:** All relevant provisions for healthcare provider organizations, with emphasis on:
        - Obligations regarding patient consent for uploading information
        - Access controls and audit logging for My Health Record access
        - Security of My Health Record information
        - Incident reporting related to My Health Record
- **Supporting Frameworks (Implicit):** Essential Eight (for baseline cyber hygiene), ISO 27001 (for ISMS principles).

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Statement, Scope, Definitions (e.g., Personal Information, Health Information, Sensitive Information), Privacy Principles, Collection of Information, Use and Disclosure of Information, Data Quality, Data Security (including physical, technical, and administrative safeguards), My Health Record Obligations, Access and Correction, Data Breach Response, Roles and Responsibilities, Training and Awareness, Policy Review.
- **Specific Policy Statements/Directives:** Explicit directives on obtaining consent for health information handling, secure storage of patient records, strict access controls to EHR and My Health Record, mandatory data encryption, and procedures for handling patient requests regarding their data.
- **Procedural Guidance:** High-level procedural guidance for patient consent, My Health Record access protocols, data de-identification where appropriate, and incident response for privacy breaches.
- **Reporting Requirements:** Requirements for reporting privacy breaches to the OAIC (NDB scheme) and My Health Record incidents to the Australian Digital Health Agency.
- **Training and Awareness:** Mandatory privacy and data security training for all staff, with specific modules for My Health Record users.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings. Use bullet points for lists of responsibilities or key actions.
- **Tone:** Formal, empathetic, and clear. Emphasize patient trust and confidentiality.
- **Length:** Comprehensive, approximately 1800-2500 words.
- **Exclusions/Limitations:** Do not include specific technical configurations of EHR systems. Focus on policy principles and legislative compliance.
- **Language:** English (Australian context).
```

### Example 3: Australian Government Sector - PSPF & ISM Information Security Policy

**Goal:** Generate an Information Security Policy for an Australian Government entity, focusing on PSPF and ISM requirements.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Information Security Policy for an Australian Government entity. Adhere strictly to the Protective Security Policy Framework (PSPF) and the Information Security Manual (ISM), ensuring the policy is clear, concise, and addresses all relevant controls for protecting government information and systems.

[POLICY CONTEXT]
- **Policy Title:** Information Security Policy
- **Policy Purpose:** To establish the mandatory requirements and controls for protecting official information and systems of [Client's Organization Name] in accordance with the PSPF and ISM, ensuring the confidentiality, integrity, and availability of government information.
- **Target Audience:** All APS employees, contractors, and third-party service providers of [Client's Organization Name].
- **Organizational Name:** [e.g., "Department of Digital Services"]
- **Industry Sector:** Australian Government (Non-corporate Commonwealth entity)
- **Organizational Profile:** A federal government department responsible for developing and implementing digital policies and services for the Australian public. Handles PROTECTED and SECRET classified information. Operates primarily in an AWS cloud environment.
- **Data Types Handled:** Official Information (Unclassified, PROTECTED, SECRET), Personal Identifiable Information (PII) of citizens, Sensitive Business Information.

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** Protective Security Policy Framework (PSPF), Information Security Manual (ISM)
- **Specific Controls/Requirements to Address:**
    - **PSPF:** All relevant policies, with particular emphasis on:
        - Policy 8: Security of information
        - Policy 9: Access to information
        - Policy 10: Handling of information
        - Policy 11: Information communications technology (ICT) security
        - Policy 12: Security incidents
    - **ISM Controls:** All relevant controls from the ISM, including but not limited to:
        - Chapter 1: Governance
        - Chapter 2: Personnel Security
        - Chapter 3: Physical Security
        - Chapter 4: Information Security (e.g., Data encryption, Access control, System hardening, Patch management, Vulnerability management, Incident response)
        - Essential Eight mitigation strategies (Maturity Level 3 as a minimum baseline)
- **Cross-Framework Mappings:** The policy should clearly link ISM controls to the fulfillment of PSPF information security policies.

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Statement, Scope, Definitions (e.g., Official Information, Classification Levels), Information Security Principles, Roles and Responsibilities (including Agency Head accountability), Information Classification and Handling, ICT Security (including Cloud Security), Personnel Security (relevant to information access), Physical Security (relevant to information storage), Incident Management, Compliance and Reporting, Training and Awareness, Policy Review.
- **Specific Policy Statements/Directives:** Explicit directives on information classification, secure storage and transmission of classified information, mandatory implementation of Essential Eight controls, secure configuration of ICT systems, and strict access controls based on need-to-know and security clearances.
- **Procedural Guidance:** High-level procedural guidance for information classification, secure data handling, incident reporting to ACSC, and secure disposal of classified information.
- **Reporting Requirements:** Requirements for reporting security incidents to the ACSC and internal security advisors.
- **Training and Awareness:** Mandatory annual protective security and cybersecurity awareness training for all personnel, with specialized training for those handling classified information.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings. Use bullet points for lists of requirements or responsibilities.
- **Tone:** Formal, authoritative, and legally compliant. Use precise language as expected in government policy documents.
- **Length:** Comprehensive, approximately 2500-3500 words.
- **Exclusions/Limitations:** Do not include specific technical configurations or detailed implementation guides (refer to ISM for these). Focus on policy principles and mandatory requirements.
- **Language:** English (Australian context).
```

### Example 4: Australian Education Industry - Privacy Act & Essential Eight Cybersecurity Policy

**Goal:** Generate a Cybersecurity Policy for an Australian educational institution, focusing on the Privacy Act 1988 (APPs) and Essential Eight mitigation strategies.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Cybersecurity Policy for an Australian educational institution. Adhere strictly to the Privacy Act 1988 (including Australian Privacy Principles) and incorporate the ACSC Essential Eight mitigation strategies, ensuring the policy is clear, concise, and addresses all relevant controls for protecting student and staff data and maintaining secure IT environments.

[POLICY CONTEXT]
- **Policy Title:** Cybersecurity Policy
- **Policy Purpose:** To establish the organization's commitment and approach to managing cybersecurity risks, protecting IT systems and data (especially student and staff personal information), and ensuring compliance with Australian privacy legislation.
- **Target Audience:** All employees, students, contractors, and volunteers of [Client's Organization Name] who use the institution's IT systems or handle its data.
- **Organizational Name:** [e.g., "Innovate University"]
- **Industry Sector:** Education (University)
- **Organizational Profile:** A large public university with multiple campuses, offering undergraduate and postgraduate courses. Manages extensive student records, research data, and staff information. Utilizes a mix of on-premise and cloud-based learning management systems and administrative platforms.
- **Data Types Handled:** Student Personal Information (PII), Staff Personal Information (PII), Research Data (potentially sensitive), Academic Records, Financial Information.

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** Privacy Act 1988 (Cth) (Australian Privacy Principles), ACSC Essential Eight (Maturity Level 2 as a target)
- **Specific Controls/Requirements to Address:**
    - **Privacy Act 1988 (APPs):** Emphasis on:
        - APP 1: Open and transparent management of personal information
        - APP 11: Security of personal information
        - NDB Scheme requirements
    - **Essential Eight Mitigation Strategies:** All eight strategies, aiming for Maturity Level 2:
        - Application whitelisting
        - Patch applications
        - Configure Microsoft Office macro settings
        - Harden user applications
        - Restrict administrative privileges
        - Patch operating systems
        - Multi-factor authentication
        - Daily backups
- **Supporting Frameworks (Implicit):** ISO 27001 (for ISMS principles).

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Statement, Scope, Definitions, Cybersecurity Principles, Roles and Responsibilities, Information Asset Management, Risk Management, Essential Eight Implementation (detailed for each strategy), Data Privacy and Protection, Incident Response, Third-Party Security, Acceptable Use of IT Resources, Training and Awareness, Policy Review.
- **Specific Policy Statements/Directives:** Explicit directives on mandatory multi-factor authentication, regular patching cycles, secure configuration of all IT assets, data backup and recovery, and strict controls over administrative privileges. Policies for secure handling of student and staff PII.
- **Procedural Guidance:** High-level procedural guidance for implementing Essential Eight controls, incident reporting, and secure data handling practices.
- **Reporting Requirements:** Requirements for reporting cybersecurity incidents to relevant internal stakeholders and the OAIC (for NDB).
- **Training and Awareness:** Mandatory annual cybersecurity awareness training for all staff and students, with specific modules on data privacy and phishing.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings. Use bullet points for lists of requirements or responsibilities.
- **Tone:** Formal, educational, and protective. Balance technical requirements with user understanding.
- **Length:** Comprehensive, approximately 1500-2200 words.
- **Exclusions/Limitations:** Do not include highly technical implementation details (these should be in separate standards/procedures). Focus on policy principles and strategic directives.
- **Language:** English (Australian context).
```

### Example 5: Australian Retail Industry - PCI DSS & Privacy Act Data Protection Policy

**Goal:** Generate a Data Protection Policy for an Australian retail organization, focusing on PCI DSS and Privacy Act 1988 (APPs) requirements.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Data Protection Policy for an Australian retail organization. Adhere strictly to PCI DSS (Payment Card Industry Data Security Standard) and the Privacy Act 1988 (including Australian Privacy Principles), ensuring the policy is clear, concise, and addresses all relevant controls for protecting customer personal information and payment card data.

[POLICY CONTEXT]
- **Policy Title:** Data Protection Policy
- **Policy Purpose:** To establish the organization's commitment and approach to protecting customer personal information and payment card data, ensuring compliance with PCI DSS and Australian privacy legislation, and maintaining customer trust.
- **Target Audience:** All employees, contractors, and third-party service providers of [Client's Organization Name] who handle customer data or payment card information.
- **Organizational Name:** [e.g., "RetailMart Australia"]
- **Industry Sector:** Retail (Multi-channel retailer)
- **Organizational Profile:** A large multi-channel retailer operating physical stores and an e-commerce platform across Australia. Processes millions of credit card transactions annually and manages a loyalty program with extensive customer data.
- **Data Types Handled:** Payment Card Data (PCD), Personal Identifiable Information (PII) of customers (e.g., loyalty program data, purchase history, contact details), Employee PII.

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** PCI DSS (latest version), Privacy Act 1988 (Cth) (Australian Privacy Principles)
- **Specific Controls/Requirements to Address:**
    - **PCI DSS:** All 12 requirements, with particular emphasis on:
        - Requirement 1: Install and maintain a firewall configuration to protect cardholder data.
        - Requirement 3: Protect stored cardholder data.
        - Requirement 4: Encrypt transmission of cardholder data across open, public networks.
        - Requirement 6: Develop and maintain secure systems and applications.
        - Requirement 8: Identify and authenticate access to system components.
        - Requirement 10: Track and monitor all access to network resources and cardholder data.
        - Requirement 12: Maintain an information security policy for all personnel.
    - **Privacy Act 1988 (APPs):** Emphasis on:
        - APP 1: Open and transparent management of personal information
        - APP 3: Collection of solicited personal information
        - APP 6: Use or disclosure of personal information
        - APP 11: Security of personal information
        - NDB Scheme requirements
- **Supporting Frameworks (Implicit):** Essential Eight (for baseline cyber hygiene), ISO 27001 (for ISMS principles).

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Statement, Scope, Definitions (e.g., Cardholder Data, Personal Information), Data Protection Principles, PCI DSS Compliance Requirements (detailed for each of the 12 requirements), Privacy Act Compliance (APPs), Roles and Responsibilities, Data Classification and Handling, Network Security, System Security, Access Control, Incident Response, Third-Party Service Provider Management, Employee Training and Awareness, Policy Enforcement, Review and Update.
- **Specific Policy Statements/Directives:** Explicit directives on never storing sensitive authentication data, strong encryption for cardholder data, regular vulnerability scanning and penetration testing, secure development practices for e-commerce platforms, and strict access controls to systems handling PCD.
- **Procedural Guidance:** High-level procedural guidance for secure payment processing, data retention and disposal, incident response for cardholder data breaches, and privacy impact assessments for new data collection initiatives.
- **Reporting Requirements:** Requirements for reporting cardholder data breaches to payment brands and the OAIC (for NDB).
- **Training and Awareness:** Mandatory annual PCI DSS and privacy awareness training for all employees, especially those involved in payment processing or handling customer data.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings. Use bullet points for lists of requirements or responsibilities.
- **Tone:** Formal, protective, and business-oriented. Emphasize customer trust and regulatory adherence.
- **Length:** Comprehensive, approximately 2000-3000 words.
- **Exclusions/Limitations:** Do not include specific network diagrams or detailed technical configurations. Focus on policy principles and compliance requirements.
- **Language:** English (Australian context).
```

### Example 6: Australian Energy Industry - AESCSF & Essential Eight Cybersecurity Policy

**Goal:** Generate a Cybersecurity Policy for an Australian energy market participant, focusing on AESCSF and Essential Eight requirements.

```
[SYSTEM INSTRUCTION]
As an expert compliance policy writer and solution architect, your task is to generate a comprehensive and actionable Cybersecurity Policy for an Australian energy market participant. Adhere strictly to the Australian Energy Sector Cyber Security Framework (AESCSF) and incorporate the ACSC Essential Eight mitigation strategies, ensuring the policy is clear, concise, and addresses all relevant controls for protecting critical IT and OT systems and maintaining operational resilience.

[POLICY CONTEXT]
- **Policy Title:** Cybersecurity Policy
- **Policy Purpose:** To establish the organization's commitment and approach to managing cybersecurity risks, protecting critical IT and Operational Technology (OT) systems, and ensuring compliance with the AESCSF and other relevant Australian cybersecurity standards, thereby maintaining the security and reliability of energy supply.
- **Target Audience:** All employees, contractors, and third-party service providers of [Client's Organization Name] who interact with IT or OT systems.
- **Organizational Name:** [e.g., "PowerGrid Australia"]
- **Industry Sector:** Energy (Electricity Transmission and Distribution)
- **Organizational Profile:** A major electricity transmission and distribution network service provider operating critical infrastructure across multiple Australian states. Manages SCADA systems, substations, and a corporate IT network. Handles sensitive operational data and customer billing information.
- **Data Types Handled:** Operational Technology (OT) Data, SCADA Data, Customer Personal Information (PII), Sensitive Business Information, Critical Infrastructure Data.

[COMPLIANCE FRAMEWORKS AND CONTROLS]
- **Primary Framework(s):** Australian Energy Sector Cyber Security Framework (AESCSF), ACSC Essential Eight (Maturity Level 3 as a target)
- **Specific Controls/Requirements to Address:**
    - **AESCSF:** All relevant domains and controls, with particular emphasis on:
        - Governance and Risk Management
        - Asset Management (IT and OT assets)
        - Identity and Access Management
        - Threat Detection and Response
        - Supply Chain Risk Management
        - Resilience and Recovery
    - **Essential Eight Mitigation Strategies:** All eight strategies, aiming for Maturity Level 3:
        - Application whitelisting
        - Patch applications
        - Configure Microsoft Office macro settings
        - Harden user applications
        - Restrict administrative privileges
        - Patch operating systems
        - Multi-factor authentication
        - Daily backups
- **Supporting Frameworks (Implicit):** ISO 27001 (for ISMS principles), IEC 62443 (for OT security).

[POLICY CONTENT REQUIREMENTS]
- **Key Sections to Include:** Executive Statement, Scope, Definitions (e.g., IT, OT, SCADA), Cybersecurity Principles, Roles and Responsibilities (including Board/Senior Management oversight), Risk Management, Asset Management (IT and OT), Essential Eight Implementation, Operational Technology Security, Network Security, Access Control, Incident Response and Business Continuity, Supply Chain Security, Data Privacy (for customer PII), Training and Awareness, Policy Review.
- **Specific Policy Statements/Directives:** Explicit directives on segmentation of IT and OT networks, secure configuration of industrial control systems, mandatory multi-factor authentication for all systems, regular vulnerability assessments of OT environments, and robust incident response plans for operational disruptions.
- **Procedural Guidance:** High-level procedural guidance for implementing AESCSF controls, managing OT security, incident reporting to AEMO and other authorities, and secure remote access to critical infrastructure.
- **Reporting Requirements:** Requirements for reporting cybersecurity incidents to AEMO and other relevant regulatory bodies.
- **Training and Awareness:** Mandatory annual cybersecurity awareness training for all personnel, with specialized training for OT engineers and IT staff.

[OUTPUT FORMAT AND CONSTRAINTS]
- **Format:** Markdown with clear, hierarchical headings. Use bullet points for lists of requirements or responsibilities.
- **Tone:** Formal, authoritative, and focused on critical infrastructure protection. Use precise language.
- **Length:** Comprehensive, approximately 2500-3500 words.
- **Exclusions/Limitations:** Do not include highly technical configuration details of OT systems. Focus on policy principles and strategic directives.
- **Language:** English (Australian context).
```

## Conclusion

These prompt examples demonstrate how to leverage the AI engine to generate highly specific and compliant policies across various Australian industries and regulatory frameworks. By providing clear context, specifying relevant controls, and defining output requirements, the AI can act as a powerful tool for automating policy generation, significantly reducing manual effort and ensuring consistency and accuracy. Continuous refinement of these prompts based on AI output and expert review will further enhance the effectiveness of the compliance automation platform.

