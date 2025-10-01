## 2. n8n Workflow Outline

This section details a step-by-step n8n orchestration for automatically discovering distressed properties. The workflow is designed to be modular, allowing for easy expansion and maintenance.

### 2.1. Trigger

The workflow will be initiated on a recurring schedule to ensure timely data collection. Given the dynamic nature of property listings and public notices, a frequent schedule is recommended.

*   **Trigger Type:** Cron Schedule
*   **Frequency:** Daily (e.g., every morning at 08:00 AM AEST) or Weekly (e.g., every Monday at 08:00 AM AEST), depending on the update frequency of the sources and user preference. A daily trigger is preferred for capturing urgent opportunities.

### 2.2. Scraper/Fetcher Modules

Each data source will have a dedicated module or a set of nodes responsible for fetching or scraping the relevant information. The choice of method (webhook, RSS, scraping) will depend on the source's technical capabilities.

#### 2.2.1. AFSA's Bankruptcy Register (NPII)
*   **Method:** API (if business integration is established) or Web Scraper.
*   **Entry Point:** `https://www.afsa.gov.au/online-services-help/bankruptcy-register-search`
*   **Data to Extract:** Debtor name, insolvency type, date of insolvency. Property details are not directly available here but can be cross-referenced later.

#### 2.2.2. ASIC - Insolvency Notices
*   **Method:** Web Scraper.
*   **Entry Point:** `https://www.asic.gov.au/regulatory-resources/insolvency/more-insolvency-information/insolvency-notices/`
*   **Data to Extract:** Company name, ACN, notice type (e.g., 'Appointment of Liquidator'), date of notice, administrator/liquidator details. Property details are not directly available.

#### 2.2.3. Government Gazettes (Federal and State)
*   **Method:** Web Scraper (for search results pages).
*   **Entry Points:**
    *   Federal: `https://www.legislation.gov.au/gazettes`
    *   NSW: `https://legislation.nsw.gov.au/gazette`
    *   QLD: `https://www.forgov.qld.gov.au/communication-and-publishing/queensland-government-gazette/find-a-gazette`
    *   SA: `https://www.governmentgazette.sa.gov.au/gazette_archive`
    *   WA: `https://www.legislation.wa.gov.au/legislation/statutes.nsf/gazettes.html`
*   **Keywords for Search:** "property", "land", "sale", "mortgagee", "rates", "auction", "deceased estate".
*   **Data to Extract:** Notice title, publication date, relevant entities/names, any listed addresses or property descriptions, direct link to the gazette entry.

#### 2.2.4. Real Estate Portals (realestate.com.au, domain.com.au)
*   **Method:** Web Scraper.
*   **Entry Points:**
    *   `https://www.realestate.com.au/`
    *   `https://www.domain.com.au/`
*   **Search Filters/Keywords:** "mortgagee in possession", "urgent sale", "must sell", "deceased estate", "divorce", "forced sale", "bank says sell". These keywords will be applied to the search functionality of the portals.
*   **Data to Extract:** Property address, listing URL, price, number of bedrooms/bathrooms, land size, agent contact details, listing description (for keyword analysis).
*   **Example CSS Selectors (Illustrative for realestate.com.au - actual selectors may vary and require live inspection):**
    *   Property Address: `.residential-card__address`
    *   Price: `.residential-card__price`
    *   Listing URL: `.residential-card__link` (extract `href` attribute)
    *   Description: `.residential-card__description`

#### 2.2.5. Victorian Sheriff's Auctions
*   **Method:** Web Scraper.
*   **Entry Point:** `https://www.justice.vic.gov.au/sheriffrealestate`
*   **Data to Extract:** Property address, auction date/time, description, link to auction details.
*   **Example Regex for extracting address from text (Illustrative):** `\b\d+\s[A-Za-z]+\s(?:Street|Road|Avenue|Lane|Drive|Court|Parade|Place|Crescent|Way)\b` (This is a generic example and would need refinement based on actual text patterns).

#### 2.2.6. Council Public Notices (Sale of Land for Overdue Rates)
*   **Method:** Web Scraper (requires individual configuration for each council).
*   **Entry Points (Examples):**
    *   Gold Coast City Council: `https://www.goldcoast.qld.gov.au/Services/Rates-water/Payment-plans/Sale-of-land-for-overdue-rates`
    *   Clarence Valley Council: `https://www.clarence.nsw.gov.au/News-articles/Public-Notice-Sale-of-Land-for-Overdue-Rates`
*   **Data to Extract:** Property address, notice date, auction date (if applicable), council contact details, reason for sale (overdue rates).

### 2.3. Data Cleaner

After fetching, raw data will be processed to extract and standardize key information. This module will use a combination of text parsing, regular expressions, and conditional logic.

*   **Nodes:** Text manipulation nodes, Regex nodes, Conditional nodes.
*   **Extraction & Standardization:**
    *   **Property Address:** Standardize format (e.g., "123 Main St, Suburb, State, Postcode"). Use geocoding APIs (e.g., Google Maps Geocoding API) to verify and enrich addresses with latitude/longitude.
    *   **Notice Type:** Categorize into predefined types: "Probate", "Insolvency", "Foreclosure/Mortgagee Sale", "Unpaid Rates", "Auction", "Distressed Listing (General)".
    *   **Date:** Extract and standardize dates (e.g., YYYY-MM-DD) for notice publication, auction, or last update.
    *   **Contact Details:** Extract names, phone numbers, and email addresses of relevant parties (e.g., real estate agents, solicitors, liquidators, council contacts).
    *   **Listing URL:** Ensure a clean, direct URL to the original source.
    *   **Keywords:** Extract relevant keywords from descriptions to aid in scoring.

### 2.4. Storage

The cleaned and structured data will be stored in a centralized database for easy access, querying, and further analysis.

*   **Options:** Google Sheets, Airtable, or PostgreSQL.
    *   **Google Sheets/Airtable:** Good for MVP due to ease of setup and visual interface.
    *   **PostgreSQL:** More robust for scaling, complex queries, and integration with other systems.
*   **Columns:**
    *   `Source` (e.g., "realestate.com.au", "AFSA", "NSW Gazette", "Gold Coast Council")
    *   `URL` (Link to the original notice/listing)
    *   `Address` (Standardized property address)
    *   `Latitude`
    *   `Longitude`
    *   `Notice_Type` (e.g., "Probate", "Insolvency", "Foreclosure")
    *   `Date_Published` (Date of the notice/listing)
    *   `Date_Updated` (Last updated date, if available)
    *   `Contact_Name`
    *   `Contact_Phone`
    *   `Contact_Email`
    *   `Price` (If available)
    *   `Bedrooms` (If available)
    *   `Bathrooms` (If available)
    *   `Land_Size` (If available)
    *   `Description_Keywords` (Keywords extracted from listing description)
    *   `Status` (e.g., "New", "Active", "Under Offer", "Sold")
    *   `Next_Action` (e.g., "Contact Agent", "Monitor Auction", "Research Probate")
    *   `Urgency_Score` (Calculated by Scoring Module)
    *   `Property_Type` (e.g., "House", "Apartment", "Land")
    *   `Location_Suburb`
    *   `Location_State`
    *   `Location_Postcode`

### 2.5. Alerting

Notifications will be sent for new or high-priority leads.

*   **Channels:** Slack, Telegram, Email.
*   **Trigger Conditions:**
    *   New property added to the database.
    *   Property with an `Urgency_Score` above a defined threshold.
    *   Change in `Status` for a monitored property (e.g., from "Active" to "Under Offer").
*   **Content:** Brief summary of the property (Address, Notice Type, Urgency Score), direct link to the record in the storage system, and key contact details.

### 2.6. Scoring Module

A dedicated module will assign a score to each property lead, helping users prioritize opportunities.

*   **Logic:** A combination of factors will contribute to the `Urgency_Score`.
    *   **Urgency:** Properties with upcoming auction dates, recent insolvency notices, or explicit "must sell" keywords will receive higher scores.
    *   **Property Type:** User-defined preferences (e.g., houses over apartments).
    *   **Location:** Proximity to user-defined areas of interest, or areas with high growth potential.
    *   **Sale Type:** Mortgagee sales and unpaid rates sales might be scored higher due to potential for discount.
    *   **Keyword Analysis:** Presence of specific keywords in the description (e.g., "renovator's delight", "development potential").
*   **Implementation:** A custom JavaScript or Python node within n8n can implement the scoring algorithm, assigning a numerical score (e.g., 1-100) to each lead.

### 2.7. Error Handling and Logging

Robust error handling and logging will be implemented to ensure the workflow's reliability.

*   **Error Notifications:** Send alerts (e.g., to Slack/email) if a scraper fails, data cleaning encounters unexpected formats, or API calls return errors.
*   **Logging:** Record workflow execution details, number of items processed, errors, and any skipped items for later review and debugging.

This structured approach ensures comprehensive coverage of data sources and a robust, automated process for lead generation.


### 2.8. Automation Research

This section details the recommended automation methods for each source and highlights those with APIs or structured feeds, along with examples of scraping techniques.

#### 2.8.1. Recommended Access Methods per Source

| Source Category | Specific Source | Recommended Method | Rationale |
|---|---|---|---|
| **Distressed Property Aggregators** | SQM Research, Real Estate Investar, REDA | Web Scraping (with caution) | These are paid platforms; scraping may violate ToS. API access might be available for enterprise clients. |
| **Probate Notices** | NSW Online Registry, PROV Victoria | Web Scraping | No direct APIs or RSS feeds found. Requires navigating search forms and parsing results. |
| **Insolvency Registers** | AFSA Bankruptcy Register (NPII) | API (preferred), Web Scraping | AFSA offers an API channel for businesses, which is the most reliable and efficient method. Web scraping is an alternative if API access is not feasible. |
| **Insolvency Registers** | ASIC - Insolvency Notices | Web Scraping | No direct APIs or RSS feeds found. |
| **Government Gazettes** | Federal Register of Legislation, State Gazettes | Web Scraping | Searchable web interfaces, but no structured feeds. |
| **Foreclosure/Mortgagee Sales** | Victorian Sheriff's Auctions | Web Scraping | Listings are presented on a web page. |
| **Auction Calendars** | realestate.com.au, domain.com.au, SQM Research Auctions | Web Scraping | Major portals with dynamic content, requiring robust scraping techniques. |
| **Council Public Notices** | Various Council Websites | Web Scraping | Highly fragmented; each council website needs a custom scraper. |

#### 2.8.2. Sources with APIs or Structured Feeds

1.  **AFSA Bankruptcy Register (NPII):** Offers an API channel for businesses to integrate their systems. This is the most structured and reliable source identified for insolvency data. [Source 3.1]
2.  **Federal Register of Legislation:** While not a traditional API, its gazette notices from October 2012 onwards are published as "individually searchable notices," implying a structured backend that might be more amenable to programmatic access than traditional scraping. [Source 4.1]
3.  **State Government Gazettes:** Similar to the Federal Register, some state gazettes (e.g., NSW Legislation Gazette) offer comprehensive search functions, which could indicate a more structured data access point. [Source 4.3]
4.  **Real Estate Portals (e.g., realestate.com.au, domain.com.au):** While primarily requiring web scraping for public listings, these platforms often have APIs for real estate agents or partners. Accessing these would likely require formal partnerships or paid subscriptions.
5.  **SQM Research:** As a data aggregator, they likely have internal APIs or structured data feeds that power their reports. Access would be via their paid subscription service. [Source 1.1]

#### 2.8.3. Examples of Regex / CSS Selectors for Scraping

**Scenario 1: Scraping a Probate Notice (Illustrative for a hypothetical public notice page)**

Assume a probate notice page has the following HTML structure:

```html
<div class="probate-notice">
    <h2>Notice of Intended Application for Probate</h2>
    <p><strong>Deceased Name:</strong> John Doe</p>
    <p><strong>Date of Death:</strong> 2025-09-01</p>
    <p><strong>Last Known Address:</strong> 123 Example Street, Suburb, NSW 2000</p>
    <p><strong>Applicant:</strong> Jane Doe (Solicitor for the Estate)</p>
    <p><strong>Contact:</strong> jane.doe@examplelaw.com</p>
</div>
```

*   **CSS Selectors:**
    *   Deceased Name: `.probate-notice p:nth-of-type(1) strong` (or more robustly, target `p` tags containing specific text if available)
    *   Date of Death: `.probate-notice p:nth-of-type(2)`
    *   Address: `.probate-notice p:nth-of-type(3)`
    *   Applicant: `.probate-notice p:nth-of-type(4)`
    *   Contact Email: `.probate-notice p:nth-of-type(5)`

*   **Regex for extracting specific data from the text content of the `p` tags:**
    *   For Deceased Name: `Deceased Name:\s*(.*?)(?=<br>|$)` (if `br` tags are used for line breaks)
    *   For Address: `Last Known Address:\s*(.*?)(?=<br>|$)`
    *   For Email: `Contact:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})`

**Scenario 2: Scraping an Auction Page (Illustrative for a real estate portal listing)**

Assume an auction listing card has the following HTML structure:

```html
<div class="auction-listing-card">
    <a href="/property/123-main-st-suburb-state-1234" class="listing-link">
        <h3 class="property-address">123 Main Street, Suburb, VIC 3000</h3>
        <span class="auction-date">Auction: Sat, 5 Oct 2025, 10:00 AM</span>
        <p class="property-description">Mortgagee in possession. Must sell!</p>
    </a>
    <div class="agent-contact">
        <span class="agent-name">John Smith</span>
        <span class="agent-phone">0412 345 678</span>
    </div>
</div>
```

*   **CSS Selectors:**
    *   Property Address: `.auction-listing-card .property-address`
    *   Listing URL: `.auction-listing-card .listing-link` (extract `href` attribute)
    *   Auction Date/Time: `.auction-listing-card .auction-date`
    *   Property Description: `.auction-listing-card .property-description`
    *   Agent Name: `.auction-listing-card .agent-contact .agent-name`
    *   Agent Phone: `.auction-listing-card .agent-contact .agent-phone`

*   **Regex for extracting date and time from `Auction: Sat, 5 Oct 2025, 10:00 AM`:**
    *   Date: `Auction:\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})`
    *   Time: `(\d{1,2}:\d{2}\s(?:AM|PM))`

These examples demonstrate how CSS selectors can pinpoint elements and regex can extract specific data points from text. Actual implementation would require inspecting the live HTML structure of each target website and adapting these patterns accordingly. Robust error handling for missing elements or changed structures is crucial for long-term maintenance of scrapers.

