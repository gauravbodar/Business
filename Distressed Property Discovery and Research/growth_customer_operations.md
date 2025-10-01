## 5. Growth & Customer Operations

This section outlines the operational strategies for managing customer growth, ensuring retention, and automating key customer-facing processes. The focus is on leveraging n8n for automation and integrating various platforms to maintain a cohesive customer relationship management system.

**Who does this:** [Growth], [Ops], [Founder]

### 5.1. How to Set Up Weekly PDF Digest Automation Inside n8n for Subscribers

**Goal:** Provide value to premium subscribers through automated, personalized weekly PDF digests of new high-priority leads.

**Steps:**
1.  **n8n Workflow Trigger:**
    *   **Trigger Type:** Cron Schedule.
    *   **Frequency:** Weekly (e.g., every Friday at 06:00 AM AEST).
2.  **Fetch Subscriber Data:**
    *   **Database Node (PostgreSQL/Google Sheets/Airtable):** Query your app database to retrieve a list of all active premium subscribers.
    *   **Data to Fetch:** User ID, Email Address, Preferred Location Filters (if stored), Preferred Property Type Filters (if stored).
3.  **Iterate Through Subscribers:**
    *   **Split In Batches Node:** Process each subscriber individually to generate personalized digests.
4.  **Fetch Personalized Leads:**
    *   **Database Node (PostgreSQL/Google Sheets/Airtable):** For each subscriber, query the main property leads database.
    *   **Filters:** Apply the subscriber's preferred location, property type, and a date filter (e.g., leads added in the last 7 days) to retrieve relevant high-priority leads (e.g., `urgency_score > 70`).
5.  **Generate PDF Digest:**
    *   **Function Node (or Custom Code Node):** This is the most complex step and might require a custom Python or JavaScript script to generate a well-formatted PDF.
        *   **Input:** The list of personalized leads for the current subscriber.
        *   **Process:** Use a library like `ReportLab` (Python) or `jsPDF` (JavaScript, potentially run in a custom n8n node or external service) to dynamically create a PDF document.
        *   **Content:** Include property details (Address, Notice Type, Urgency Score, URL), a brief description, and potentially small map snippets (if geocoding is integrated).
        *   **Templating:** Use a template to ensure consistent branding and layout.
    *   **Alternative (Simpler MVP):** Generate a Markdown file with the digest content and then use `manus-md-to-pdf` (if available in the sandbox or a similar external tool) or a cloud PDF generation API (e.g., HTML to PDF API) to convert it.
6.  **Upload PDF:**
    *   **Cloud Storage Node (e.g., Google Drive, S3):** Upload the generated PDF to a cloud storage service. This provides a persistent URL for the attachment.
7.  **Send Email:**
    *   **Email Node (SMTP/Gmail/SendGrid):** Send an email to the subscriber.
    *   **Subject:** "Your Weekly Distressed Property Digest - [Date]"
    *   **Body:** Personalized greeting, brief summary, and a link to download the PDF digest from cloud storage.
    *   **Attachment:** Attach the generated PDF directly if the email service supports it, or include the download link.

### 5.2. Steps for Managing CRM Data Flow Between Apollo.io, Instantly.ai, and App Database

**Goal:** Ensure a unified view of customer interactions and lead status across all platforms.

**Data Flow Strategy:**

1.  **Apollo.io to Instantly.ai (Outbound Leads):**
    *   **Method:** Manual CSV export/import (as detailed in Section 4.2) or direct integration if available (e.g., Zapier/Make.com).
    *   **Frequency:** As needed, when new outbound campaigns are launched.
2.  **Instantly.ai to CRM (e.g., HubSpot, Pipedrive):**
    *   **Method:** Webhooks or native integrations.
    *   **n8n Workflow:** Create an n8n workflow triggered by Instantly.ai webhooks (e.g., `Lead Replied`, `Meeting Booked`).
    *   **CRM Node:** Use the appropriate CRM node (e.g., HubSpot, Pipedrive) to:
        *   Create new contacts/leads in the CRM.
        *   Update existing contact records with engagement data (e.g., `last_email_reply_date`, `campaign_name`).
        *   Create tasks for sales team members (e.g., "Follow up with [Lead Name]").
3.  **App Database to CRM (User Signups/Subscription Status):**
    *   **Method:** Webhooks from your Replit backend or n8n workflow triggered by database changes.
    *   **n8n Workflow:** Triggered when a new user signs up or a subscription status changes in your app database.
    *   **CRM Node:**
        *   Create a new contact in the CRM for new signups.
        *   Update contact records with subscription status (`Free`, `Premium`, `Cancelled`), plan details, and last login date.
4.  **CRM to App Database (Customer Feedback/Support):**
    *   **Method:** Webhooks from CRM or periodic sync via n8n.
    *   **n8n Workflow:** Triggered by specific events in the CRM (e.g., `Support Ticket Closed`, `Customer Feedback Received`).
    *   **Database Node:** Update relevant user records in your app database with customer feedback or support notes.

### 5.3. Retention Operations: Churn Prevention, Renewal Workflows

**Goal:** Proactively manage customer lifecycle to reduce churn and encourage renewals.

**Churn Prevention:**
1.  **Identify At-Risk Users:**
    *   **n8n Workflow (Scheduled):** Daily/weekly check of app database for users exhibiting churn indicators:
        *   Low feature usage (e.g., `last_login_date` > 14 days).
        *   No leads accessed in a week.
        *   Negative sentiment from support interactions (if tracked in CRM).
    *   **Scoring:** Assign a "churn risk score" to users.
2.  **Proactive Engagement:**
    *   **n8n Workflow (Triggered by Churn Risk):** If a user's churn risk score crosses a threshold:
        *   Send a personalized email (via Instantly.ai or email node) offering support, new feature highlights, or a special offer.
        *   Create a task in the CRM for a customer success manager to reach out.

**Renewal Workflows:**
1.  **Subscription Expiry Notifications:**
    *   **n8n Workflow (Scheduled):** Weekly check for premium subscribers whose subscriptions are due to expire in 30, 7, and 1 day(s).
    *   **Email Node:** Send automated, personalized emails:
        *   **30 Days Out:** Reminder of upcoming renewal, highlight value received, link to manage subscription.
        *   **7 Days Out:** Stronger call to action to renew, emphasize benefits of continued access.
        *   **1 Day Out:** Last chance reminder before service interruption.
2.  **Failed Payment Handling:**
    *   **n8n Workflow (Triggered by Payment Gateway Webhook):** Listen for `invoice.payment_failed` events from Stripe/PayPal.
    *   **Email Node:** Send automated emails to users with failed payments, providing instructions to update payment details.
    *   **Database Update:** Temporarily downgrade user access or mark subscription as `delinquent` in your app database.
3.  **Win-Back Campaigns:**
    *   **n8n Workflow (Scheduled):** Identify users whose subscriptions have lapsed (e.g., 30 days after expiry).
    *   **Instantly.ai Integration:** Add these users to a targeted win-back email sequence with special re-engagement offers.

By implementing these growth and customer operations, the SaaS product can effectively manage its user base, foster loyalty, and drive sustainable revenue.
