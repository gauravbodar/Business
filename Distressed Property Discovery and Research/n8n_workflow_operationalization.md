## 2. n8n Workflow Operationalization

This section provides practical instructions for deploying and configuring n8n workflows to automate the discovery and processing of distressed property data. The focus is on creating a robust, error-resistant, and scalable data pipeline.

**Who does this:** [Ops], [Dev]

### 2.1. Practical Instructions for Deploying n8n

**Goal:** Set up n8n for production use with proper configuration and monitoring.

**Deployment Options:**

#### Option A: Local Deployment (Development/Testing)
1.  **Install n8n locally:**
    ```bash
    npm install -g n8n
    ```
2.  **Start n8n:**
    ```bash
    n8n start
    ```
3.  **Access the interface:** Open `http://localhost:5678` in your browser.

#### Option B: Cloud Deployment (Production Recommended)
1.  **n8n Cloud:** Use [n8n Cloud](https://n8n.io/cloud/) for a managed solution. This is the simplest option for production deployment.
2.  **Self-hosted on Cloud Provider:**
    *   Deploy n8n on a cloud provider like [DigitalOcean](https://www.digitalocean.com/), [AWS](https://aws.amazon.com/), or [Render](https://render.com/).
    *   Use Docker for containerized deployment:
        ```bash
        docker run -it --rm \
          --name n8n \
          -p 5678:5678 \
          -v ~/.n8n:/home/node/.n8n \
          n8nio/n8n
        ```
    *   Configure environment variables for database connection, webhook URLs, and API keys.

**Configuration:**
*   **Database:** Configure n8n to use PostgreSQL for production (instead of the default SQLite) to ensure data persistence and scalability.
*   **Environment Variables:** Set up environment variables for sensitive information:
    *   `N8N_BASIC_AUTH_ACTIVE=true` (enable basic authentication)
    *   `N8N_BASIC_AUTH_USER=admin`
    *   `N8N_BASIC_AUTH_PASSWORD=your_secure_password`
    *   `DB_TYPE=postgresdb`
    *   `DB_POSTGRESDB_HOST=your_postgres_host`
    *   `DB_POSTGRESDB_DATABASE=n8n`
    *   `DB_POSTGRESDB_USER=n8n_user`
    *   `DB_POSTGRESDB_PASSWORD=your_db_password`

### 2.2. Node-by-Node Guide for Connecting Scrapers

**Goal:** Create specific n8n workflows for each data source identified in the product design.

#### Workflow 1: AFSA Bankruptcy Register (NPII)

**Nodes:**
1.  **Cron Trigger:** Schedule daily execution at 08:00 AM AEST.
2.  **HTTP Request Node (AFSA API):**
    *   **Method:** GET or POST (depending on AFSA API requirements)
    *   **URL:** `https://www.afsa.gov.au/online-services-help/api-channel` (or specific API endpoint)
    *   **Authentication:** Configure API key if required for business integration.
    *   **Parameters:** Include search criteria (e.g., recent insolvencies, specific regions).
3.  **Function Node (Data Processing):**
    *   Extract relevant fields: `debtor_name`, `insolvency_type`, `date_of_insolvency`, `location`.
    *   Standardize date format to YYYY-MM-DD.
    *   Add `source` field with value "AFSA".
4.  **Google Sheets Node (Storage):**
    *   **Operation:** Append
    *   **Sheet ID:** Your Google Sheets ID for the property database.
    *   **Range:** A:Z (or specific columns)
    *   **Values:** Mapped from the processed data.

#### Workflow 2: Real Estate Portal Scraper (realestate.com.au)

**Nodes:**
1.  **Cron Trigger:** Schedule daily execution at 09:00 AM AEST.
2.  **HTTP Request Node (Search Page):**
    *   **Method:** GET
    *   **URL:** `https://www.realestate.com.au/buy/with-keywords-mortgagee+in+possession/list-1`
    *   **Headers:** Include `User-Agent` to mimic a browser request.
3.  **HTML Extract Node:**
    *   **CSS Selector for Property Cards:** `.residential-card` (adjust based on actual HTML structure)
    *   **Extract Multiple:** Yes
4.  **Function Node (Data Extraction):**
    *   For each property card, extract:
        *   Address: `.residential-card__address`
        *   Price: `.residential-card__price`
        *   URL: `.residential-card__link` (href attribute)
        *   Description: `.residential-card__description`
    *   Add `source` field with value "realestate.com.au".
    *   Add `notice_type` field with value "Distressed Listing".
5.  **Google Maps Geocoding Node (Address Enrichment):**
    *   **Input:** Extracted address
    *   **Output:** Latitude and longitude
6.  **Google Sheets Node (Storage):** Same configuration as Workflow 1.

#### Workflow 3: Victorian Sheriff's Auctions

**Nodes:**
1.  **Cron Trigger:** Schedule weekly execution on Mondays at 10:00 AM AEST.
2.  **HTTP Request Node:**
    *   **URL:** `https://www.justice.vic.gov.au/sheriffrealestate`
3.  **HTML Extract Node:**
    *   **CSS Selector:** Target auction listing containers (inspect the page to determine exact selectors).
4.  **Function Node (Data Processing):**
    *   Extract property address, auction date, description.
    *   Use regex to parse addresses: `/\b\d+\s[A-Za-z\s]+(?:Street|Road|Avenue|Lane|Drive|Court|Parade|Place|Crescent|Way)\b/`
    *   Add `source` field with value "Victorian Sheriff".
    *   Add `notice_type` field with value "Sheriff Auction".
5.  **Google Sheets Node (Storage):** Same configuration as previous workflows.

### 2.3. Error Handling, Retries, and Logging Setup

**Goal:** Ensure workflow reliability and provide visibility into execution status.

**Error Handling:**
1.  **Error Workflow:** Create a dedicated error handling workflow that can be triggered by other workflows when errors occur.
2.  **Try-Catch Logic:** Use n8n's error handling features to catch errors in individual nodes and route them to the error workflow.
3.  **Conditional Nodes:** Add conditional logic to handle different types of errors (e.g., network timeouts, parsing errors, API rate limits).

**Retries:**
1.  **HTTP Request Node Settings:** Configure retry settings for HTTP requests:
    *   **Retry on Fail:** Yes
    *   **Max Retries:** 3
    *   **Retry Interval:** 5 seconds
2.  **Exponential Backoff:** Implement exponential backoff for API requests to avoid overwhelming target servers.

**Logging:**
1.  **Slack/Discord Notifications:** Set up nodes to send notifications to a Slack channel or Discord server for:
    *   Workflow start/completion
    *   Errors and failures
    *   Daily summary of processed items
2.  **Database Logging:** Create a separate table or sheet to log workflow executions:
    *   Workflow name, execution time, status (success/failure), number of items processed, error messages.

### 2.4. Data Pipeline Operations: Storage, Scoring, Notifications

**Goal:** Implement the complete data processing pipeline from raw data to actionable leads.

#### Storage Operations:
1.  **Database Schema:** Ensure your Google Sheets or PostgreSQL database has the following columns:
    *   `id`, `source`, `url`, `address`, `latitude`, `longitude`, `notice_type`, `date_published`, `contact_name`, `contact_phone`, `contact_email`, `price`, `bedrooms`, `bathrooms`, `land_size`, `description_keywords`, `status`, `urgency_score`, `property_type`, `location_suburb`, `location_state`, `location_postcode`, `created_at`, `updated_at`.
2.  **Data Validation:** Add validation nodes to check for required fields and data quality before storage.
3.  **Deduplication:** Implement logic to avoid storing duplicate entries (e.g., check if a property with the same address and source already exists).

#### Scoring Operations:
1.  **Scoring Function Node:** Create a JavaScript function node that calculates the `urgency_score` based on:
    *   **Keywords:** Higher score for "must sell", "mortgagee", "urgent".
    *   **Date:** Higher score for recent listings or upcoming auctions.
    *   **Property Type:** User-defined preferences.
    *   **Location:** Proximity to high-value areas.
2.  **Sample Scoring Logic:**
    ```javascript
    // Sample scoring algorithm
    let score = 0;
    const keywords = $json.description_keywords.toLowerCase();
    
    // Keyword scoring
    if (keywords.includes('mortgagee')) score += 30;
    if (keywords.includes('must sell')) score += 25;
    if (keywords.includes('urgent')) score += 20;
    if (keywords.includes('deceased estate')) score += 15;
    
    // Date scoring (recent listings get higher scores)
    const daysOld = (new Date() - new Date($json.date_published)) / (1000 * 60 * 60 * 24);
    if (daysOld <= 7) score += 20;
    else if (daysOld <= 30) score += 10;
    
    // Property type scoring
    if ($json.property_type === 'House') score += 10;
    
    return { urgency_score: Math.min(score, 100) };
    ```

#### Notification Operations:
1.  **High-Priority Alerts:** Set up conditional nodes to send immediate notifications for properties with `urgency_score > 70`.
2.  **Daily Digest:** Create a separate workflow that runs daily to compile and send a summary of new leads to subscribers.
3.  **Notification Channels:**
    *   **Slack:** Use Slack webhook nodes for internal team notifications.
    *   **Email:** Use SMTP or email service nodes for user notifications.
    *   **In-App:** Store notifications in the database for display in the user dashboard.

### 2.5. Scheduling & Monitoring Workflows

**Goal:** Ensure workflows run reliably and provide operational visibility.

**Scheduling:**
1.  **Cron Expressions:** Use appropriate cron expressions for different data sources:
    *   High-frequency sources (real estate portals): Daily at 08:00 AM AEST (`0 8 * * *`)
    *   Medium-frequency sources (government gazettes): Every 2 days at 10:00 AM AEST (`0 10 */2 * *`)
    *   Low-frequency sources (sheriff auctions): Weekly on Mondays at 12:00 PM AEST (`0 12 * * 1`)
2.  **Timezone Configuration:** Ensure n8n is configured to use Australian Eastern Standard Time (AEST) for consistent scheduling.

**Monitoring:**
1.  **Workflow Status Dashboard:** Use n8n's built-in execution history to monitor workflow performance.
2.  **External Monitoring:** Set up external monitoring tools (e.g., [UptimeRobot](https://uptimerobot.com/), [Pingdom](https://www.pingdom.com/)) to check if n8n is accessible and responsive.
3.  **Performance Metrics:** Track key metrics:
    *   Workflow execution time
    *   Success/failure rates
    *   Number of properties discovered per source
    *   Data quality metrics (e.g., percentage of records with valid addresses)
4.  **Alerting:** Configure alerts for:
    *   Workflow failures
    *   Unusual execution times
    *   Significant drops in data volume (indicating potential source issues)
