## 6. Compliance & Risk Operations

This section outlines the operational checks and procedures required to ensure the Distressed Property Discovery SaaS complies with Australian privacy laws, data scraping rules, and conveyancing regulations. It also details how disclaimers should be displayed and data retention policies implemented.

**Who does this:** [Founder], [Dev], [Ops]

### 6.1. Operational Checks Before Launch

**Goal:** Ensure legal and ethical compliance before the product goes live.

**Checklist:**

*   **Privacy Act Compliance (Privacy Act 1988 (Cth)):**
    *   **Privacy Policy:** Draft and publish a comprehensive Privacy Policy on the Replit-hosted application. This policy must clearly state:
        *   What personal information is collected (e.g., user registration data, contact details from scraped leads).
        *   How it is collected (e.g., user input, web scraping).
        *   The purpose of collection (e.g., lead generation, service delivery, marketing).
        *   How it is stored and secured.
        *   How individuals can access or correct their personal information.
        *   Details of any third parties with whom data is shared (e.g., Instantly.ai, Apollo.io).
        *   Contact details for privacy inquiries.
    *   **Data Minimization:** Verify that only necessary personal information is collected and stored. Regularly audit data fields.
    *   **Consent:** Ensure explicit consent is obtained for any processing of personal information beyond what is reasonably expected for the service, especially for marketing communications.
    *   **Data Security Audit:** Conduct a basic security audit of the Replit environment, n8n instance, and database to ensure data is protected against unauthorized access or breaches.
*   **Data Scraping Terms of Service (ToS) Checks:**
    *   **Source-Specific ToS Review:** For each data source (websites, APIs), review their respective Terms of Service and `robots.txt` files.
    *   **Compliance Strategy:** Document how the scraping strategy for each source aligns with its ToS. If a ToS explicitly prohibits scraping, either seek permission, find an alternative source, or exclude that source.
    *   **Rate Limiting:** Implement and verify rate-limiting in n8n scrapers to prevent overloading target servers and to comply with fair use policies.
*   **Disclaimers:**
    *   **Legal Disclaimer:** Prepare a clear legal disclaimer stating that the service provides information and leads, not legal, financial, or property advice. Emphasize the need for independent verification.
    *   **Data Accuracy Disclaimer:** Include a disclaimer that while efforts are made to ensure data accuracy, the information is sourced from public records and third-party websites, and its veracity cannot be guaranteed.

### 6.2. Where and How to Display Disclaimers in the App (Replit UI)

**Goal:** Ensure users are fully aware of the product's limitations and their responsibilities.

**Implementation:**

*   **Website Footer:** Display a link to the full Privacy Policy and Terms of Service in the footer of every page of the Replit-hosted application.
*   **Registration/Login Pages:** Require users to explicitly agree to the Terms of Service and Privacy Policy during the registration process (e.g., via a checkbox).
*   **Dashboard Banner/Pop-up (Initial Login):** Upon a user's first login, display a prominent, dismissible banner or pop-up with the core legal and data accuracy disclaimers. This ensures immediate visibility.
*   **Lead Detail View:** On each property lead's detailed view, include a small, clear note reminding users that the information requires independent verification and is not legal advice.
*   **Export Functionality:** When users export data (CSV, vCard), include a reminder about data usage and privacy obligations, especially if the export contains personal information.

### 6.3. Data Retention Policy: How Long to Keep Scraped Leads

**Goal:** Define and implement a clear data retention policy to comply with privacy regulations and manage storage costs.

**Policy Guidelines:**

*   **Personal Information:**
    *   **Probate/Insolvency Notices:** Personal information (e.g., names of deceased, insolvents, contact details of agents) should be retained only as long as necessary for the purpose for which it was collected (i.e., identifying distressed property leads). A retention period of **12-24 months** from the date of collection is generally reasonable, after which it should be anonymized or securely deleted.
    *   **Contact Details:** Contact details of agents/liquidators obtained from public sources can be retained longer if they are regularly engaged with (e.g., through CRM). However, if no engagement occurs within a defined period (e.g., 12 months), they should be reviewed for deletion or anonymization.
*   **Property Data (Non-Personal):**
    *   Property addresses, notice types, urgency scores, and other non-personal data can be retained for longer periods (e.g., **5-7 years**) for historical analysis, trend identification, and product improvement, provided it cannot be linked back to identifiable individuals.
*   **User Data:**
    *   User account information (email, hashed password, subscription status) should be retained as long as the user maintains an active account. Upon account deletion, all associated personal data should be securely removed, with exceptions for legally required retention (e.g., financial transaction records).

**Operational Steps for Implementation:**

1.  **Automated Deletion/Anonymization Workflow (n8n):** Create a scheduled n8n workflow that runs periodically (e.g., monthly).
    *   **Database Query:** Identify records in the property leads database that exceed their defined retention period for personal information.
    *   **Action:** For these records, either:
        *   **Anonymize:** Remove or replace personal identifiers (names, specific contact details) with generic placeholders.
        *   **Delete:** Securely delete the entire record if it primarily consists of personal information and is no longer needed.
2.  **User Account Deletion Process:** Implement a clear process for users to request account deletion, ensuring all their personal data is removed from the system (app database, CRM, etc.) within a reasonable timeframe (e.g., 30 days).
3.  **Regular Audits:** Periodically audit the database to ensure the retention policy is being adhered to and that no unnecessary personal data is being stored.

By meticulously following these operational procedures, the Distressed Property Discovery SaaS can maintain a strong posture regarding compliance and risk management, fostering user trust and avoiding potential legal issues.
