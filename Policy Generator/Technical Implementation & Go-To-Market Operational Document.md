# Technical Implementation & Go-To-Market Operational Document

This document outlines a step-by-step, execution-ready technical plan for building, launching, and monetizing the "Policy Genesis Suite" SaaS product. It is designed for a small development and growth team, prioritizing rapid MVP delivery, low infrastructure costs, and scalability.

## 1. Development & Infrastructure Setup

This section details the foundational steps for setting up the backend and frontend infrastructure, authentication, and membership management. The focus is on leveraging managed services and cost-effective solutions to accelerate development and minimize operational overhead, aligning with an MVP-first approach.

### 1.1 Backend Setup: API Orchestration, AI Model Integration, and Database Design

#### 1.1.1 API Orchestration with AWS API Gateway and Lambda

**Objective:** Establish a serverless, scalable, and secure API layer to expose backend functionalities and integrate with AI models and data storage.

**Instructions:**

1.  **[Dev] Create an AWS Account and Configure IAM:**
    *   Set up a new AWS account (if not already available).
    *   Create an IAM user with programmatic access and attach policies for API Gateway, Lambda, Bedrock, RDS, and S3. Store credentials securely.
    *   Configure AWS CLI locally with these credentials.

2.  **[Dev] Set up AWS API Gateway:**
    *   Navigate to API Gateway in the AWS Console.
    *   Create a new REST API (or HTTP API for simpler use cases).
    *   Define API resources and methods (e.g., `/policies` for policy generation).
    *   Integrate methods with AWS Lambda functions (to be created in the next step).
    *   Enable CORS for frontend access.
    *   Deploy the API to a stage (e.g., `dev`, `prod`).

3.  **[Dev] Implement AWS Lambda Functions for Business Logic:**
    *   For the policy generation API endpoint, create a corresponding Lambda function (e.g., `generatePolicyLambda`). Other Lambda functions for tender analysis and compliance dashboards will be implemented in later stages`).
    *   Use Python 3.9+ runtime.
    *   Each Lambda function will contain the business logic for its respective API, including:
        *   Input validation.
        *   Calling AI models (via Bedrock or SageMaker).
        *   Interacting with the database (RDS).
        *   Storing/retrieving files (S3).
    *   Configure appropriate IAM roles for Lambda functions to access Bedrock, RDS, and S3.
    *   Set up environment variables for database connection strings, S3 bucket names, etc.

**Example API Routes:**

*   `POST /policies/generate`: Triggers AI policy generation.
*   `GET /policies/{policy_id}`: Retrieves a generated policy.

#### 1.1.2 AI Model Integration with Amazon Bedrock

**Objective:** Integrate with Amazon Bedrock to leverage powerful Foundation Models for policy generation, ensuring scalability and access to state-of-the-art AI capabilities.

**Instructions:**

1.  **[Dev] Enable Amazon Bedrock Access:**
    *   Request access to the desired Foundation Models (e.g., Anthropic Claude, AI21 Labs Jurassic, Amazon Titan) within the AWS Bedrock console.
    *   Ensure the IAM role for Lambda functions has permissions to invoke Bedrock models (`bedrock:InvokeModel`).

2.  **[Dev] Implement AI Calls within Lambda Functions:**
    *   Within the `generatePolicyLambda` function, use the AWS SDK (Boto3 for Python) to call Bedrock models.
    *   Construct prompts dynamically based on user input and compliance framework requirements.
    *   Parse the AI model's response and integrate it into the application workflow.

**Example Python Snippet (within Lambda):**

```python
import boto3
import json

def invoke_bedrock_model(prompt_text, model_id='anthropic.claude-v2'):
    client = boto3.client('bedrock-runtime', region_name='us-east-1') # Use your desired region
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt_text}\n\nAssistant:",
        "max_tokens_to_sample": 2000,
        "temperature": 0.7,
        "top_p": 0.9
    })
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')

def generate_policy_handler(event, context):
    # Extract input from event (e.g., compliance framework, industry, client details)
    user_input = json.loads(event['body'])
    framework = user_input.get('framework')
    industry = user_input.get('industry')
    # ... construct a detailed prompt using the principles from the previous document
    
    prompt = f"Generate a {framework} compliant policy for the {industry} industry..."
    policy_content = invoke_bedrock_model(prompt)
    
    # Store policy_content in S3 and metadata in RDS
    # ...
    
    return {
        'statusCode': 200,
        'body': json.dumps({'policy_id': 'generated_id', 'content_preview': policy_content[:200]})
    }
```

#### 1.1.3 Database Design for Policies, Tenders, and Compliance Dashboards

**Objective:** Design a robust and scalable database schema using Amazon RDS for PostgreSQL to store structured data related to policies, tenders, compliance frameworks, and client information.

**Instructions:**

1.  **[Dev] Set up Amazon RDS for PostgreSQL:**
    *   Navigate to RDS in the AWS Console.
    *   Create a new PostgreSQL instance (e.g., `db.t3.micro` for MVP to keep costs low).
    *   Configure security groups to allow inbound traffic only from Lambda functions and potentially a bastion host for direct access.
    *   Enable automated backups.

2.  **[Dev] Design Database Schema:**
    *   **`users` table:** Stores user authentication details (linked to Cognito IDs), roles, and client organization ID.
        ```sql
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            cognito_id VARCHAR(255) UNIQUE NOT NULL,
            organization_id UUID REFERENCES organizations(id),
            email VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(50) NOT NULL, -- e.g., 'admin', 'compliance_manager', 'user'
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ```
    *   **`organizations` table:** Stores client organization details.
        ```sql
        CREATE TABLE organizations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(100),
            subscription_plan VARCHAR(50) NOT NULL, -- e.g., 'free', 'paid', 'enterprise'
            stripe_customer_id VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ```
    *   **`compliance_frameworks` table:** Stores metadata about supported frameworks.
        ```sql
        CREATE TABLE compliance_frameworks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) UNIQUE NOT NULL, -- e.g., 'ISM', 'Essential Eight', 'ISO 27001'
            description TEXT,
            version VARCHAR(50),
            controls JSONB -- Store control details as JSONB for flexibility
        );
        ```
    *   **`policies` table:** Stores metadata about generated policies.
        ```sql
        CREATE TABLE policies (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID REFERENCES organizations(id),
            title VARCHAR(255) NOT NULL,
            framework_id UUID REFERENCES compliance_frameworks(id),
            status VARCHAR(50) NOT NULL, -- e.g., 'draft', 'review', 'approved', 'published'
            s3_key VARCHAR(255) NOT NULL, -- Path to policy content in S3
            generated_by_ai BOOLEAN DEFAULT TRUE,
            version_history JSONB, -- Store versioning metadata
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ```


3.  **[Dev] Implement Data Access Layer:**
    *   Use a lightweight ORM or direct SQL queries within Lambda functions to interact with RDS.
    *   Implement connection pooling to manage database connections efficiently.

#### 1.1.4 File Storage with Amazon S3

**Objective:** Provide scalable, durable, and secure storage for policy documents, tender documents, AI-generated responses, and compliance evidence.

**Instructions:**

1.  **[Dev] Create S3 Buckets:**
    *   Create an S3 bucket for policy storage (e.g., `policy-genesis-policies`).
    *   Configure bucket policies to restrict access to only authorized IAM roles (Lambda, etc.).
    *   Enable server-side encryption (SSE-S3 or SSE-KMS).
    *   Enable versioning on buckets to maintain a history of document changes.

2.  **[Dev] Integrate S3 with Lambda Functions:**
    *   Lambda functions will use Boto3 to upload and download files from S3.
    *   When a policy or tender response is generated, store the content in S3 and the S3 key (path) in the RDS database.
    *   When a user requests to download a document, generate a pre-signed URL for secure, temporary access to the S3 object.

### 1.2 Frontend Setup: React.js and Hosting

**Objective:** Develop a responsive, intuitive, and performant client-facing dashboard using React.js and deploy it to a cost-effective hosting solution.

**Instructions:**

1.  **[Dev] Initialize React Project:**
    *   Use `create-react-app` or Vite to scaffold a new React project with TypeScript.
    *   Install necessary dependencies (e.g., React Router, state management library like Redux Toolkit or Zustand, UI library like Material-UI or Ant Design).

2.  **[Dev] Develop Core UI Components:**
    *   **Authentication Pages:** Login, Signup, Forgot Password (integrate with AWS Cognito UI components or custom forms).
    *   **Dashboard Layout:** Navigation, header, footer, main content area.
    *   **Policy Management:** List policies, view policy details, edit/approve workflow, export options.

    *   **User/Organization Settings:** Profile management, subscription details.

3.  **[Dev] Integrate with Backend APIs:**
    *   Use `fetch` API or a library like `axios` to make requests to the AWS API Gateway endpoints.
    *   Handle authentication tokens (JWT from Cognito) for API calls.
    *   Implement error handling and loading states for all API interactions.

4.  **[Dev] Frontend Hosting and Deployment:**
    *   **Option 1 (Recommended for MVP): Vercel or Netlify:**
        *   Connect the React project Git repository (e.g., GitHub, GitLab) to Vercel/Netlify.
        *   Configure build commands (`npm run build`) and output directory (`build` or `dist`).
        *   Vercel/Netlify automatically deploys on every push to the main branch, providing a CDN and SSL certificate.
        *   This offers excellent developer experience and low-cost hosting for an MVP.
    *   **Option 2 (AWS Native): AWS Amplify:**
        *   Connect the Git repository to AWS Amplify Console.
        *   Amplify handles continuous deployment, hosting, and CDN (CloudFront).
        *   Integrates seamlessly with AWS Cognito for authentication.
        *   Provides a unified platform for frontend and backend development.

**Recommended Stack:**
*   **Frontend:** React.js, TypeScript, Material-UI/Ant Design, React Router, Redux Toolkit/Zustand, React Query.
*   **Hosting:** Vercel (for simplicity and speed) or AWS Amplify (for deeper AWS integration).

### 1.3 Authentication and Membership Management

**Objective:** Implement secure user authentication and manage subscription plans, integrating with a payment gateway.

**Instructions:**

1.  **[Dev] Set up AWS Cognito User Pool:**
    *   Create a new User Pool in AWS Cognito.
    *   Configure sign-up and sign-in attributes (e.g., email, password).
    *   Enable Multi-Factor Authentication (MFA) for enhanced security.
    *   Create an App Client for the frontend application.
    *   Configure a hosted UI or integrate directly with the Cognito SDK in the React app.
    *   Set up User Pool groups (e.g., `FreeTierUsers`, `PaidTierUsers`, `EnterpriseUsers`, `Admins`) to manage roles.

2.  **[Dev] Integrate with Stripe for Subscription Management:**
    *   Create a Stripe account.
    *   Define subscription products and pricing plans in the Stripe Dashboard (e.g., Free, Paid, Enterprise).
    *   **Frontend Integration:**
        *   Use Stripe Checkout or Stripe Elements to handle payment collection securely on the frontend.
        *   When a user subscribes, create a customer in Stripe and subscribe them to a plan.
    *   **Backend Integration (Webhook Handler Lambda):**
        *   Create a Lambda function (`stripeWebhookHandler`) to receive Stripe webhooks (e.g., `customer.subscription.updated`, `invoice.payment_succeeded`).
        *   This Lambda function will update the `organizations` table in RDS with the client's `subscription_plan` and `stripe_customer_id` based on webhook events.
        *   Secure the webhook endpoint using Stripe's webhook signing secrets.

3.  **[Dev] Implement Role-Based Access Control (RBAC):**
    *   **Cognito Groups:** Map Cognito User Pool groups to roles in the `users` table (e.g., `FreeTierUsers` -> `user`, `PaidTierUsers` -> `compliance_manager`).
    *   **API Gateway Authorizers:** Use Cognito User Pool authorizers in API Gateway to protect API endpoints based on user authentication and group membership.
    *   **Frontend Logic:** Implement conditional rendering and feature access based on the user's role and subscription plan (fetched from the backend or JWT claims).

### 1.4 Recommended Stack and Deployment Strategy (MVP Speed > Heavy Infra)

**Objective:** Prioritize rapid development and low operational costs for the Minimum Viable Product (MVP), while laying the groundwork for future scalability.

**Recommended Stack:**

*   **Backend:** AWS Lambda (Python), AWS API Gateway, Amazon Bedrock, Amazon RDS for PostgreSQL, Amazon S3.
*   **Frontend:** React.js (TypeScript), Material-UI/Ant Design, Vercel/AWS Amplify.
*   **Authentication/Payments:** AWS Cognito, Stripe.
*   **Orchestration:** N8N (self-hosted on a small EC2 instance or managed service if budget allows, otherwise manual Lambda orchestration for MVP).

**Deployment Strategy (MVP-focused):**

1.  **Serverless First:** Leverage AWS Lambda for all backend logic to minimize server management and scale automatically. This keeps compute costs low, especially during early stages.
2.  **Managed Database:** Amazon RDS for PostgreSQL provides a managed database solution, reducing administrative overhead. Start with a small instance type (`db.t3.micro`) and scale up as needed.
3.  **Static Frontend Hosting:** Vercel or AWS Amplify for frontend hosting offers CI/CD, global CDN, and SSL out-of-the-box with minimal configuration, enabling fast deployments.
4.  **N8N for Workflows:** For MVP, N8N can be self-hosted on a small EC2 instance to keep costs down, or even start with manual Lambda orchestrations if N8N integration proves too complex initially. As the product matures, consider a managed N8N service or a more robust serverless workflow solution like AWS Step Functions.
5.  **Cost Optimization:** Utilize AWS Free Tier where applicable. Implement cost monitoring and alerts from day one. Focus on optimizing Lambda memory and execution times.
6.  **Infrastructure as Code (IaC):** While not strictly MVP, consider using AWS CloudFormation or Terraform for managing infrastructure from the outset. This ensures consistency, repeatability, and easier management as the platform grows. For MVP, manual setup might be faster, but document everything thoroughly.

This setup provides a lean, agile foundation that can be rapidly iterated upon, allowing the team to focus on core product features and market feedback rather than infrastructure complexities.



## 2. Core Feature Implementation

This section details the technical implementation of the core product features: Policy Generation Engine, Tender Auto-Writing, and the Compliance Dashboard. Each feature outlines the workflow, technical considerations, and integration points.

### 2.1 Policy Generation Engine

**Objective:** Enable users to generate compliance policies automatically based on selected frameworks and organizational context, with options for review, editing, and export.

**Workflow for Policy Generation:**

1.  **User Input [Frontend]:**
    *   User selects desired compliance framework(s) (e.g., ISM, Essential Eight, ISO 27001, PSPF).
    *   User provides organizational context (industry, size, existing tech stack, data types handled) via a structured form. This data is stored in the `organizations` table in RDS.
    *   User specifies policy title and purpose.

2.  **API Call [Frontend → Backend]:**
    *   Frontend makes a `POST` request to `/policies/generate` endpoint on AWS API Gateway.
    *   The request body includes selected frameworks, organizational context, and policy details.

3.  **Lambda Orchestration [Backend]:**
    *   The `generatePolicyLambda` function is invoked.
    *   It retrieves the full details of the selected compliance frameworks from the `compliance_frameworks` table in RDS.
    *   It constructs a detailed prompt for the AI model, incorporating the user's organizational context and the specific controls/requirements of the chosen frameworks (as per the prompt engineering strategy outlined in the previous architecture document).

4.  **AI Model Invocation [Backend]:**
    *   The Lambda function invokes the Amazon Bedrock service with the constructed prompt.
    *   The Bedrock model (e.g., Anthropic Claude) generates the policy content in Markdown format.

5.  **Output Processing and Storage [Backend]:**
    *   The generated policy content is received by the Lambda function.
    *   The content is stored as a Markdown file in an S3 bucket (e.g., `s3://policy-genesis-policies/{organization_id}/{policy_id}.md`).
    *   Metadata about the policy (title, framework, status='draft', S3 key, generated_by_ai=TRUE) is stored in the `policies` table in RDS.
    *   An initial version entry is added to the `version_history` JSONB column.

6.  **User Notification [Backend → Frontend]:**
    *   The Lambda function returns a `policy_id` to the frontend.
    *   The frontend displays a notification to the user that the policy has been generated and is available for review.

7.  **Review and Edit [Frontend]:**
    *   User navigates to the policy details page using the `policy_id`.
    *   The frontend fetches the policy content from S3 (via a pre-signed URL generated by a Lambda function) and displays it in an editable text area or rich-text editor.
    *   Users can make edits, which are saved back to S3 (creating a new version) and updated in the `policies` table (updating `updated_at` and `version_history`).

8.  **Export Options [Frontend]:**
    *   Users can export the policy in various formats:
        *   **Word (.docx):** Frontend can use a client-side library (e.g., `mammoth.js` for Markdown to HTML, then `docx` library for HTML to DOCX conversion) or a backend Lambda function can use a headless browser (e.g., `Playwright` with `pandoc` or similar) to convert Markdown to DOCX.
        *   **PDF (.pdf):** Similar to Word, client-side (e.g., `jsPDF`) or backend Lambda (e.g., `WeasyPrint` or `Puppeteer` to render HTML to PDF) conversion from Markdown.

**Technical Details:**

*   **API Endpoint:** `POST /policies/generate`
    *   **Request Body:** `{ 


            "frameworks": ["ISM", "Essential Eight"],
            "organization_context": {
                "industry": "Government",
                "size": "SME",
                "data_types": ["PII", "Official Information"],
                "tech_stack": ["AWS Cloud", "Microsoft 365"]
            },
            "policy_title": "Cybersecurity Policy"
        }`
    *   **Response:** `{ "policy_id": "uuid-of-generated-policy", "status": "draft" }`
*   **API Endpoint:** `GET /policies/{policy_id}`
    *   **Response:** `{ "policy_id": "...", "title": "...", "content": "# Policy Content...", "status": "...", "versions": [...] }`
*   **Storage Schema (RDS `policies` table):**
    ```sql
    CREATE TABLE policies (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        organization_id UUID REFERENCES organizations(id),
        title VARCHAR(255) NOT NULL,
        framework_id UUID REFERENCES compliance_frameworks(id), -- Can be array of UUIDs for multiple frameworks
        status VARCHAR(50) NOT NULL, -- e.g., 'draft', 'review', 'approved', 'published'
        s3_key VARCHAR(255) NOT NULL, -- Path to policy content in S3
        generated_by_ai BOOLEAN DEFAULT TRUE,
        version_history JSONB, -- Store versioning metadata: [{version: 1, s3_key: '...', timestamp: '...'}]
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    ```
This robust implementation of core features ensures that the Policy Genesis Suite provides comprehensive functionality for automated policy generation, all within a user-friendly and scalable architecture.



## 3. Workflow Orchestration (n8n or equivalent)

This section outlines the strategic use of n8n (or an equivalent workflow automation tool) to orchestrate various processes within the Policy Genesis Suite. n8n's visual workflow builder and extensive integrations make it an ideal choice for connecting different services, automating tasks, and enabling advanced logic flows without extensive custom coding. For MVP, n8n can be self-hosted on a small EC2 instance to manage costs, with a clear path to a managed service or AWS Step Functions as the product scales.

### 3.1 Where to Use n8n for Automation

n8n will serve as the central nervous system for event-driven automation, connecting the core AI agents, external services, and internal data management. Its primary applications will be:

1.  **Generating and Storing Policy Drafts:** Automating the trigger for policy generation based on user input and managing the subsequent storage and notification processes.
2.  **Future Feature - Tender Updates:** (To be implemented in later stages) Monitoring external procurement portals or internal tender statuses and notifying users of changes or upcoming deadlines.
3.  **Future Feature - Compliance Reminders:** (To be implemented in later stages) Proactively reminding users about overdue compliance tasks, evidence submissions, or policy reviews.
4.  **Client Onboarding and Offboarding Workflows:** Automating the setup of new client accounts, subscription management, and data archival upon client departure.
5.  **Data Synchronization:** Periodically pulling data from integrated client systems (e.g., HR, asset management) and pushing it to the platform's data ingestion APIs.
6.  **Reporting and Analytics Triggers:** Initiating scheduled report generation or data aggregation tasks for the compliance dashboard.

### 3.2 Node-by-Node Operational Design (Example: Policy Generation Workflow)

This example illustrates a typical n8n workflow for policy generation, detailing the sequence of nodes and their functions. This pattern can be adapted for other automation scenarios.

**Workflow Name:** `Policy_Generation_Request`

**Trigger:**
*   **Node Type:** `Webhook`
*   **Configuration:** Listens for `POST` requests from the frontend API Gateway (`/n8n/webhook/policy-generate`). This webhook is invoked by a Lambda function after initial user input is validated and basic metadata is stored in RDS.
*   **Purpose:** Initiates the policy generation process upon user request.

**Data Retrieval (from RDS):**
*   **Node Type:** `PostgreSQL`
*   **Configuration:** Connects to the Amazon RDS PostgreSQL instance.
*   **Operation:** `SELECT` query to retrieve detailed organizational context, selected compliance frameworks, and any specific policy parameters from the `organizations` and `compliance_frameworks` tables using the `organization_id` and `framework_ids` passed in the webhook payload.
*   **Purpose:** Gathers all necessary information to construct a comprehensive AI prompt.

**AI Prompt Construction:**
*   **Node Type:** `Code` (or `Function` node)
*   **Configuration:** Python or JavaScript code to dynamically construct the AI prompt. This node will take the retrieved data (organizational context, framework controls) and format it into a detailed prompt string, following the prompt engineering guidelines.
*   **Purpose:** Prepares the input for the AI model, ensuring it receives all relevant context.

**AI Model Invocation (Amazon Bedrock):**
*   **Node Type:** `AWS Bedrock` (if a custom n8n node is developed or available, otherwise `HTTP Request`)
*   **Configuration (if `HTTP Request`):**
    *   **Method:** `POST`
    *   **URL:** AWS Bedrock runtime endpoint for the chosen model (e.g., Anthropic Claude).
    *   **Headers:** `x-api-key`, `Content-Type: application/json` (with appropriate AWS authentication headers if not using a dedicated Bedrock node).
    *   **Body:** JSON payload containing the constructed prompt and model parameters (e.g., `max_tokens_to_sample`, `temperature`).
*   **Purpose:** Sends the prompt to the Foundation Model and receives the generated policy content.

**Data Cleaning and Formatting:**
*   **Node Type:** `Code` (or `Function` node)
*   **Configuration:** Processes the raw output from the AI model. This might involve:
    *   Removing any conversational filler from the AI response.
    *   Ensuring the output is in the desired Markdown format.
    *   Extracting key sections or metadata if the AI provides them.
*   **Purpose:** Refines the AI output into a clean, usable policy draft.

**Storage (S3):**
*   **Node Type:** `AWS S3`
*   **Configuration:**
    *   **Operation:** `Upload`
    *   **Bucket:** `policy-genesis-policies`
    *   **Key:** Dynamically generated path (e.g., `{organization_id}/{policy_id}.md`)
    *   **Content:** The cleaned policy draft from the previous node.
*   **Purpose:** Persists the generated policy content in durable object storage.

**Metadata Update (RDS):**
*   **Node Type:** `PostgreSQL`
*   **Configuration:** Connects to the Amazon RDS PostgreSQL instance.
*   **Operation:** `UPDATE` or `INSERT` query to update the `policies` table with the S3 key, status (`draft`), and any other relevant metadata for the newly generated policy.
*   **Purpose:** Keeps the database synchronized with the latest policy information.

**Notification (Email/Dashboard):**
*   **Node Type:** `Email` (e.g., `SMTP` or `SendGrid`) or `Webhook` (to trigger a frontend notification).
*   **Configuration:** Sends an email to the user (or relevant compliance manager) notifying them that the policy draft is ready for review. Alternatively, triggers a frontend event to display an in-app notification.
*   **Purpose:** Informs the user about the completion of the policy generation process.

**Error Handling:**
*   **Node Type:** `Error Trigger` and `Email` or `Slack`
*   **Configuration:** Catches errors at any stage of the workflow. Sends an alert to the operations team (e.g., via email or Slack) with details of the error, allowing for manual intervention and debugging.
*   **Purpose:** Ensures that failures are detected and addressed promptly, maintaining system reliability.

### 3.3 n8n JSON Skeletons (Example for Policy Generation)

Below is a simplified JSON skeleton for the policy generation workflow in n8n. This structure can be imported directly into n8n and customized.

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "policy-generate",
        "httpMethod": "POST",
        "responseMode": "lastNode",
        "options": {}
      },
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "executeOnReceived": true,
      "webhookId": "policy-generate-webhook",
      "id": "1"
    },
    {
      "parameters": {
        "database": "{{ $json.body.databaseName || 'policy_genesis' }}",
        "authentication": "credentials",
        "credentials": "aws_rds_postgresql_credentials",
        "query": "SELECT * FROM organizations WHERE id = '{{ $json.body.organization_id }}'; SELECT * FROM compliance_frameworks WHERE id IN ({{ $json.body.framework_ids.join(',') }});",
        "options": {}
      },
      "name": "Get Org & Framework Data",
      "type": "n8n-nodes-base.postgreSql",
      "typeVersion": 1,
      "id": "2"
    },
    {
      "parameters": {
        "functionCode": "return [ { json: { prompt: `Generate a ${$node["Get Org & Framework Data"].json[1].name} compliant policy for the ${$node["Get Org & Framework Data"].json[0].industry} industry, considering the following controls: ${JSON.stringify($node["Get Org & Framework Data"].json[1].controls)}.` } } ];",
        "options": {}
      },
      "name": "Construct AI Prompt",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "id": "3"
    },
    {
      "parameters": {
        "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
        "method": "POST",
        "body": "={{ JSON.stringify({ prompt: `\n\nHuman: ${$node['Construct AI Prompt'].json.prompt}\n\nAssistant:`, max_tokens_to_sample: 2000, temperature: 0.7, top_p: 0.9 }) }}",
        "jsonParameters": true,
        "options": {
          "headerParameters": [
            {
              "name": "X-Amz-Target",
              "value": "AmazonBedrockRuntime.InvokeModel"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "authentication": "awsApi",
        "awsApi": {
          "region": "us-east-1",
          "service": "bedrock"
        }
      },
      "name": "Invoke Bedrock Model",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "id": "4"
    },
    {
      "parameters": {
        "functionCode": "return [ { json: { policyContent: $node['Invoke Bedrock Model'].json.completion.replace(/\n\nAssistant:/g, '').trim() } } ];",
        "options": {}
      },
      "name": "Clean AI Output",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "id": "5"
    },
    {
      "parameters": {
        "bucketName": "policy-genesis-policies",
        "fileName": "={{ $json.body.organization_id }}/{{ $json.body.policy_id }}.md",
        "fileContent": "={{ $node['Clean AI Output'].json.policyContent }}",
        "options": {}
      },
      "name": "Upload to S3",
      "type": "n8n-nodes-base.awsS3",
      "typeVersion": 1,
      "id": "6"
    },
    {
      "parameters": {
        "database": "{{ $json.body.databaseName || 'policy_genesis' }}",
        "authentication": "credentials",
        "credentials": "aws_rds_postgresql_credentials",
        "query": "UPDATE policies SET s3_key = '{{ $node['Upload to S3'].json.key }}', status = 'draft', updated_at = CURRENT_TIMESTAMP WHERE id = '{{ $json.body.policy_id }}';",
        "options": {}
      },
      "name": "Update Policy Metadata",
      "type": "n8n-nodes-base.postgreSql",
      "typeVersion": 1,
      "id": "7"
    },
    {
      "parameters": {
        "fromEmail": "no-reply@policygenesis.com",
        "toEmail": "{{ $json.body.userEmail }}",
        "subject": "Your Policy Draft is Ready!",
        "text": "Hi {{ $json.body.userName }},\n\nYour policy draft for '{{ $json.body.policy_title }}' is ready for review in the Policy Genesis Suite.\n\nBest regards,\nThe Policy Genesis Team",
        "options": {}
      },
      "name": "Send Email Notification",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "id": "8"
    }
  ],
  "connections": {
    "Webhook Trigger": [
      [ { "node": "Get Org & Framework Data", "type": "main", "index": 0 } ]
    ],
    "Get Org & Framework Data": [
      [ { "node": "Construct AI Prompt", "type": "main", "index": 0 } ]
    ],
    "Construct AI Prompt": [
      [ { "node": "Invoke Bedrock Model", "type": "main", "index": 0 } ]
    ],
    "Invoke Bedrock Model": [
      [ { "node": "Clean AI Output", "type": "main", "index": 0 } ]
    ],
    "Clean AI Output": [
      [ { "node": "Upload to S3", "type": "main", "index": 0 } ]
    ],
    "Upload to S3": [
      [ { "node": "Update Policy Metadata", "type": "main", "index": 0 } ]
    ],
    "Update Policy Metadata": [
      [ { "node": "Send Email Notification", "type": "main", "index": 0 } ]
    ]
  }
}
```

**Role Tags:**
*   **[Dev]** Responsible for implementing n8n nodes, custom code, and ensuring API integrations.
*   **[Ops]** Responsible for monitoring n8n workflows, troubleshooting, and managing n8n infrastructure.

This approach to workflow orchestration with n8n provides a flexible, scalable, and cost-effective way to automate complex processes within the Policy Genesis Suite, enabling the small team to deliver powerful features efficiently.



## 4. Membership & SaaS Layer

This section details the technical implementation of the membership and SaaS layer, focusing on subscription plan management, rate limiting, and robust integration with Stripe for billing. The goal is to provide a flexible and scalable system that supports various tiers while ensuring fair usage and revenue generation.

### 4.1 Technical Guide for Subscription Plans

The Policy Genesis Suite will offer a tiered subscription model to cater to different client needs, from individual users exploring basic policy templates to large enterprises requiring comprehensive compliance dashboards and advanced features. Each tier will have distinct access levels and feature sets.

**Subscription Tiers:**

1.  **Free Tier (Basic Policy Templates):**
    *   **Features:** Access to a limited set of basic policy templates, manual policy generation (without AI assistance), and basic document storage.
    *   **Purpose:** Attracts new users, allows them to experience the platform's value proposition, and serves as a lead generation mechanism.
    *   **Technical Implementation:**
        *   Users are assigned to the `FreeTierUsers` Cognito group upon signup.
        *   Frontend logic restricts access to AI-driven features and advanced dashboards.
        *   Backend API Gateway authorizers check user's group membership to enforce feature access.
        *   Rate limits are applied to prevent abuse (e.g., number of policy template downloads per month).

2.  **Paid Tier (AI-Driven Custom Policies + Tender Writing):**
    *   **Features:** Unlimited AI-driven custom policy generation, advanced policy management tools, and increased storage limits. (Tender Auto-Writing feature to be enabled in later stages for this tier).
    *   **Purpose:** Converts free users into paying customers by offering significant value through automation and advanced capabilities.
    *   **Technical Implementation:**
        *   Users subscribe via Stripe, and the `stripeWebhookHandler` Lambda updates their `organization_id`'s `subscription_plan` to `paid` in RDS.
        *   The user's Cognito group is updated to `PaidTierUsers` (can be automated via a Lambda triggered by RDS changes or Stripe webhook).
        *   Frontend and backend logic grant access to AI policy generation, tender auto-writing, and associated features.
        *   Higher rate limits are applied for AI calls and document storage.

3.  **Enterprise Tier (Compliance Dashboards + Dedicated Support):**
    *   **Features:** All Paid Tier features, role-based access for multiple team members, dedicated account manager, priority support, and custom integrations. (Comprehensive Compliance Dashboard with real-time insights to be enabled in later stages for this tier).
    *   **Purpose:** Caters to larger organizations with complex compliance needs, offering a complete compliance management solution.
    *   **Technical Implementation:**
        *   Typically involves direct sales and manual onboarding.
        *   `organization_id`'s `subscription_plan` is set to `enterprise` in RDS.
        *   User's Cognito group is updated to `EnterpriseUsers`.
        *   Frontend and backend logic unlock the full Compliance Dashboard, multi-user management, and advanced reporting.
        *   Highest rate limits and custom quotas are applied.

**Database Schema Outline (RDS `organizations` table - updated):**

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    subscription_plan VARCHAR(50) NOT NULL, -- e.g., 'free', 'paid', 'enterprise'
    stripe_customer_id VARCHAR(255), -- Stores Stripe Customer ID for billing
    stripe_subscription_id VARCHAR(255), -- Stores Stripe Subscription ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 Rate Limits / Quotas by Tier

To ensure fair usage, prevent abuse, and manage infrastructure costs, rate limits and quotas will be enforced at both the API Gateway and application levels. These limits will vary by subscription tier.

**Implementation Strategy:**

1.  **API Gateway Throttling:**
    *   **[Dev/Ops]** Configure API Gateway usage plans for each subscription tier.
    *   Define default request limits (e.g., requests per second) and burst limits.
    *   Associate API keys (generated per organization or user) with specific usage plans.
    *   This provides a first line of defense against excessive requests.

2.  **Application-Level Quotas (within Lambda/Database):**
    *   **[Dev]** Implement logic within relevant Lambda functions to check against quotas stored in the `organizations` table or a dedicated `quotas` table.
    *   **Examples:**
        *   **AI Policy Generations:** Free Tier: 5/month; Paid Tier: Unlimited; Enterprise: Unlimited.
        *   **Tender Analyses:** Free Tier: N/A; Paid Tier: 10/month; Enterprise: Unlimited.
        *   **Document Storage (S3):** Free Tier: 1GB; Paid Tier: 10GB; Enterprise: 100GB+.
        *   **User Seats:** Free Tier: 1; Paid Tier: 5; Enterprise: Custom.
    *   When a user attempts an action that exceeds their quota, the Lambda function returns an appropriate error message (e.g., HTTP 429 Too Many Requests).

3.  **Monitoring and Alerts:**
    *   **[Ops]** Set up AWS CloudWatch alarms to monitor API Gateway usage and application-level quota consumption.
    *   Alert the operations team and potentially the user when quotas are nearing their limits.

### 4.3 Integration with Stripe + Webhook Handling in Backend

Stripe will be the primary payment gateway for managing subscriptions. Robust integration, particularly webhook handling, is crucial for keeping the platform's subscription status synchronized with Stripe.

**Integration Steps:**

1.  **[Dev] Stripe Account Setup:**
    *   Create a Stripe account and configure products and pricing plans for Free, Paid, and Enterprise tiers.
    *   Obtain Stripe API keys (publishable and secret).

2.  **[Dev] Frontend (Client-Side) Integration:**
    *   Use Stripe.js and Stripe Elements to securely collect payment information and manage subscriptions.
    *   When a user initiates a subscription, create a Stripe Customer object and subscribe them to the chosen plan.
    *   The frontend will typically redirect the user to Stripe Checkout or embed payment forms using Elements.

3.  **[Dev] Backend Webhook Handler (AWS Lambda):**
    *   **Purpose:** To listen for events from Stripe (e.g., `customer.subscription.updated`, `invoice.payment_succeeded`, `customer.subscription.deleted`) and update the platform's database accordingly.
    *   **Implementation:**
        *   Create an AWS Lambda function (e.g., `stripeWebhookHandler`) triggered by an API Gateway endpoint (`POST /stripe/webhook`).
        *   This Lambda function will:
            *   Verify the webhook signature using Stripe's secret to ensure authenticity.
            *   Parse the incoming Stripe event.
            *   Based on the event type, update the `organizations` table in RDS (e.g., change `subscription_plan`, update `stripe_customer_id`, `stripe_subscription_id`).
            *   Potentially trigger other actions, such as updating the user's Cognito group.
        *   **Example Event Handling (within `stripeWebhookHandler` Lambda):**
            ```python
            import json
            import os
            import stripe
            import psycopg2 # or your ORM

            stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
            WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

            def handler(event, context):
                payload = event["body"]
                sig_header = event["headers"].get("stripe-signature")

                try:
                    event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
                except ValueError as e:
                    # Invalid payload
                    return {"statusCode": 400, "body": json.dumps({"error": "Invalid payload"})}
                except stripe.error.SignatureVerificationError as e:
                    # Invalid signature
                    return {"statusCode": 400, "body": json.dumps({"error": "Invalid signature"})}

                # Handle the event
                if event["type"] == "customer.subscription.updated":
                    subscription = event["data"]["object"]
                    customer_id = subscription["customer"]
                    status = subscription["status"]
                    # Logic to update RDS for organization with customer_id and new status
                    # e.g., update subscription_plan based on subscription.items.data[0].plan.id
                    print(f"Subscription updated for customer {customer_id}: {status}")
                elif event["type"] == "invoice.payment_succeeded":
                    invoice = event["data"]["object"]
                    customer_id = invoice["customer"]
                    # Logic to record successful payment
                    print(f"Payment succeeded for customer {customer_id}")
                # ... handle other event types

                return {"statusCode": 200, "body": json.dumps({"received": True})}
            ```

4.  **[Ops] Configure Stripe Webhooks:**
    *   In the Stripe Dashboard, add the API Gateway endpoint (`POST /stripe/webhook`) as a webhook endpoint.
    *   Select the events to send (at minimum: `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_succeeded`, `invoice.payment_failed`).
    *   Store the generated webhook secret in AWS Secrets Manager or as an environment variable for the Lambda function.

This robust membership and SaaS layer, powered by AWS Cognito and Stripe, ensures that the Policy Genesis Suite can effectively manage user access, monetize its features through flexible subscription plans, and maintain accurate billing records, all while minimizing operational overhead for the small team.



## 5. Sales & Marketing Integration

This section outlines the operational playbook for integrating sales and marketing efforts, focusing on leveraging tools like Instantly.ai and Apollo.io for outbound campaigns. The strategy is designed to efficiently acquire target customers, nurture leads, and drive product adoption, all while being executable by a small growth team.

### 5.1 Operational Playbook for Instantly.ai + Apollo.io Campaigns

**Objective:** Systematize outbound lead generation and outreach to target customer personas using a combination of data enrichment, email automation, and CRM integration.

**Tools:**
*   **Apollo.io:** For B2B data enrichment, lead sourcing, and contact information.
*   **Instantly.ai:** For cold email outreach, campaign management, and deliverability optimization.
*   **CRM/Lead Tracker:** A simple CRM (e.g., HubSpot Free, Pipedrive, or even a well-structured Google Sheet for MVP) to manage leads and track interactions.

**Instructions:**

1.  **[Growth] Define Target Customer Personas (see 5.2):** Clearly articulate the ideal customer profiles, including industry, company size, job titles, pain points, and compliance needs. This is the foundation for effective lead sourcing.

2.  **[Growth] Lead Sourcing with Apollo.io:**
    *   Use Apollo.io's extensive database to identify companies and contacts that match the defined customer personas.
    *   Filter by industry (e.g., Finance, Healthcare, Government contractors), company size, geography (Australia-focused), and job titles (e.g., Compliance Manager, Head of Risk, IT Security Manager, Procurement Officer, CEO/Founder of SME).
    *   Export lists of qualified leads, including email addresses, LinkedIn profiles, and company details.

3.  **[Growth] Campaign Setup in Instantly.ai:**
    *   Import the segmented lead lists from Apollo.io into Instantly.ai.
    *   Create new email campaigns tailored to each persona and their specific pain points (e.g., 


        "Automate ISM Compliance", "Streamline Tender Responses").
    *   Design multi-step email sequences with personalized merge tags (e.g., `{{first_name}}`, `{{company_name}}`).
    *   Include clear Calls-to-Action (CTAs) such as "Book a Demo" or "Try Free Tier".
    *   Set up follow-up emails and conditional logic based on recipient engagement (opens, clicks, replies).

4.  **[Growth] Deliverability Optimization in Instantly.ai:**
    *   Utilize Instantly.ai's features for email warm-up, sender rotation, and spam testing to maximize deliverability and avoid blacklisting.
    *   Monitor bounce rates, open rates, and reply rates to continuously optimize campaigns.

5.  **[Growth] CRM/Lead Tracker Integration:**
    *   Automatically log all email activities (sends, opens, replies) from Instantly.ai into the CRM/lead tracker.
    *   When a lead expresses interest (e.g., replies, books a demo), update their status in the CRM for sales follow-up.

### 5.2 Target Customer Personas

**Objective:** Clearly define the ideal customer profiles to focus sales and marketing efforts, ensuring high conversion rates and product-market fit.

**Key Personas:**

1.  **SMEs Applying for Government Tenders (Primary Target):**
    *   **Job Titles:** Business Owners, CEOs, Sales Directors, Bid Managers.
    *   **Pain Points:** Lack of internal compliance expertise, time-consuming manual tender responses, difficulty meeting government compliance requirements (PSPF, ISM, Essential Eight), missed tender opportunities due to compliance gaps.
    *   **Value Proposition:** Automate policy generation, streamline tender writing, increase tender win rates, ensure compliance with Australian government standards.

2.  **Compliance-Heavy Industries (e.g., Finance, Healthcare, Energy):**
    *   **Job Titles:** Compliance Managers, Risk Officers, CISOs, Legal Counsel.
    *   **Pain Points:** Managing multiple complex compliance frameworks (ISO 27001, APRA CPS 234, AESCSF), manual policy updates, difficulty demonstrating continuous compliance, audit fatigue.
    *   **Value Proposition:** Centralized compliance management, automated policy updates, real-time compliance dashboards, audit-readiness, human-in-the-loop oversight.

3.  **Consultants (IT Security, Compliance, Business Advisory):**
    *   **Job Titles:** Consulting Partners, Senior Consultants, Practice Leads.
    *   **Pain Points:** Manual client compliance assessments, time-consuming policy drafting for clients, difficulty scaling compliance services, lack of a standardized tool for client engagements.
    *   **Value Proposition:** Enhance service delivery, automate client policy generation, provide value-added compliance monitoring, scale consulting practice efficiently.

### 5.3 Campaign Workflow: Apollo.io → Instantly.ai → CRM/Lead Tracker → Booked Demo

**Objective:** Establish a clear, automated workflow for lead generation to demo booking.

**Workflow Steps:**

1.  **[Growth] Lead Identification (Apollo.io):**
    *   Use Apollo.io filters to build targeted lists based on persona criteria.
    *   Export leads with verified email addresses and relevant company/contact data.

2.  **[Growth] Outreach Automation (Instantly.ai):**
    *   Import Apollo.io leads into Instantly.ai.
    *   Assign leads to relevant multi-step email sequences (e.g., 3-5 emails over 10-14 days).
    *   Personalize emails using merge tags.
    *   Monitor engagement (opens, clicks, replies).

3.  **[Growth] Lead Qualification & CRM Update:**
    *   **Positive Reply:** If a lead replies positively or expresses interest, Instantly.ai (or a connected Zapier/Make.com automation) triggers an update in the CRM/lead tracker, changing the lead status to 


        `Interested` or `Warm`. A task is created for a sales representative to follow up.
    *   **No Reply/Negative Reply:** Leads are moved to a `Nurture` sequence or marked as `Unqualified`.

4.  **[Growth] Booked Demo:**
    *   When a lead expresses interest in a demo, they are directed to a scheduling tool (e.g., Calendly, Chili Piper) integrated with the sales team's calendars.
    *   Upon successful booking, the CRM is updated, and automated reminders are sent to both the lead and the sales representative.

### 5.4 Email Template Examples

**Objective:** Provide ready-to-use, high-converting email templates for various campaign stages, designed to resonate with target personas.

**Template 1: Cold Outreach - Policy Automation (SME Focus)**

**Subject:** Automate Your Compliance Policies & Win More Gov Tenders

```
Hi {{first_name}},

Are you an SME struggling with the complexity and time commitment of generating compliance policies for government tenders?

Many Australian businesses like yours find it challenging to meet requirements like ISM, Essential Eight, or PSPF, often losing out on lucrative government contracts.

Our new platform, Policy Genesis Suite, uses AI to automatically draft compliant policies tailored to your business, saving you countless hours and boosting your tender success rate.

Would you be open to a quick 15-minute chat next week to see how we can help you streamline this process?

Best regards,
{{your_name}}
Policy Genesis Suite
```

**Template 2: Cold Outreach - Tender Support (Bid Manager Focus)**

**Subject:** Boost Your Tender Win Rate with AI-Powered Drafting

```
Hi {{first_name}},

As a Bid Manager, you know how demanding and time-sensitive tender responses can be, especially when navigating complex compliance requirements.

What if you could cut down drafting time by 50% and ensure every response is perfectly aligned with standards like ISO 27001 or Essential Eight?

Policy Genesis Suite offers an AI-powered tender auto-writing feature that drafts compliant responses, allowing your team to focus on strategy and customization.

Let's connect for a brief call to explore how this can transform your tender process. Are you available for a quick chat this Thursday or Friday?

Thanks,
{{your_name}}
Policy Genesis Suite
```

**Template 3: Follow-up - Value Proposition**

**Subject:** Re: Automate Your Compliance Policies

```
Hi {{first_name}},

Just wanted to follow up on my previous email. I understand you're busy, but I truly believe Policy Genesis Suite can be a game-changer for {{company_name}} in managing compliance and securing government contracts.

Our clients typically see:
- 80% reduction in policy drafting time
- Significant improvement in tender compliance scores
- Enhanced audit-readiness

If you're looking to simplify compliance and gain a competitive edge, I'd love to show you a quick demo. You can book a time directly here: [Link to Calendly]

Looking forward to hearing from you,
{{your_name}}
Policy Genesis Suite
```

### 5.5 How to Integrate Lead Capture into the App

**Objective:** Seamlessly capture leads from the website and within the application, funneling them into the sales and marketing automation systems.

**Instructions:**

1.  **[Growth/Dev] Landing Page Integration:**
    *   **Free Trial Signup:** The primary lead capture mechanism will be the 


        `Free Tier` signup form on the landing page.
    *   When a user signs up, their details (email, company name) are captured and stored in the `organizations` and `users` tables in RDS.
    *   This action also triggers an n8n workflow to:
        *   Add the new user/organization to the CRM/lead tracker.
        *   Initiate a welcome email sequence (via Instantly.ai or a transactional email service like AWS SES) that introduces the platform and guides them to their first policy generation.
        *   Tag the lead as `Free Tier User` for segmentation.

2.  **[Dev] In-App Lead Capture (Upgrade Prompts):**
    *   Within the Free Tier experience, strategically place prompts and calls-to-action (CTAs) to encourage users to upgrade to the Paid or Enterprise tiers.
    *   Examples:
        *   When a Free Tier user attempts to use an AI-driven feature (e.g., Tender Auto-Writing), display a modal explaining the benefits of the Paid Tier and a link to the subscription page.
        *   Display banners or notifications highlighting advanced features available in higher tiers.
    *   Clicks on these CTAs can trigger n8n workflows to notify the sales team (for Enterprise leads) or initiate a targeted email nurture sequence.

3.  **[Dev] Contact Us / Demo Request Forms:**
    *   Implement simple contact forms or demo request forms on the website and within the app.
    *   Submissions from these forms trigger n8n workflows to:
        *   Create a new lead in the CRM.
        *   Assign the lead to a sales representative.
        *   Send an automated confirmation email to the user.
        *   Notify the sales team via Slack or email.

4.  **[Growth/Dev] Analytics Integration:**
    *   Integrate web analytics (e.g., Google Analytics, Mixpanel) to track user behavior, conversion funnels, and identify drop-off points.
    *   This data informs optimization of lead capture forms, in-app prompts, and marketing campaigns.

This integrated sales and marketing approach ensures that every touchpoint, from initial outreach to in-app experience, is optimized for lead capture, nurturing, and conversion, driving sustainable growth for the Policy Genesis Suite.



## 6. Compliance & Risk

This section addresses the critical aspects of operational compliance and risk management for the Policy Genesis Suite. Given the sensitive nature of compliance data and AI-generated content, robust measures are essential to ensure data privacy, legal adherence, and transparency. This framework is designed to build trust with clients and mitigate potential liabilities.

### 6.1 Operational Compliance: Handling of Client Data

**Objective:** Ensure all client data handling practices comply with relevant Australian privacy laws and international standards, fostering trust and minimizing legal exposure.

**Key Regulations and Standards:**

*   **Australian Privacy Act 1988 (including Australian Privacy Principles - APPs):** Governs the collection, use, storage, and disclosure of personal information by Australian government agencies and most private sector organizations. The platform must adhere to the 13 APPs.
*   **ISO 27001 (Information Security Management System):** While not a direct regulatory requirement, adherence to ISO 27001 principles demonstrates a commitment to information security best practices, which is crucial for handling sensitive client data.
*   **PSPF (Protective Security Policy Framework):** For clients dealing with Australian government information, adherence to PSPF guidelines (especially for data classification and handling) is critical.

**Instructions:**

1.  **[Ops/Dev] Data Classification and Handling Policy:**
    *   Develop an internal policy for classifying client data based on sensitivity (e.g., Public, Internal, Confidential, Secret).
    *   Define strict procedures for handling each data classification, including storage locations, access controls, and transmission methods.
    *   Ensure that all data processing aligns with the principles of data minimization and purpose limitation as per the Privacy Act.

2.  **[Dev] Encryption in Transit and At Rest:**
    *   **In Transit:** All data exchanged between the frontend, backend APIs, and external services (e.g., Stripe, Bedrock) MUST use TLS 1.2 or higher. AWS API Gateway and Load Balancers automatically enforce this.
    *   **At Rest:** All data stored in Amazon RDS (PostgreSQL), Amazon S3, and any other persistent storage MUST be encrypted at rest using AWS KMS. Client-specific encryption keys should be considered for Enterprise clients.

3.  **[Dev] Access Control and Segregation:**
    *   Implement strict Role-Based Access Control (RBAC) using AWS IAM and Cognito for all internal and external users/systems.
    *   Ensure logical multi-tenancy: each client's data is strictly segregated and inaccessible to other clients. This is achieved through `organization_id` filtering at the database and application layers.
    *   Regularly review IAM policies and user permissions to enforce the principle of least privilege.

4.  **[Ops] Data Processing Agreements (DPAs):**
    *   For all third-party service providers (e.g., AWS, Stripe, n8n hosting), ensure appropriate DPAs are in place that align with Australian privacy requirements.

5.  **[Ops] Privacy Policy and Terms of Service:**
    *   Develop clear, concise, and legally compliant Privacy Policy and Terms of Service documents that explicitly outline how client data is collected, used, stored, and protected.
    *   Ensure these documents are easily accessible on the platform's website.

6.  **[Ops] Incident Response Plan:**
    *   Establish a comprehensive data breach response plan in accordance with the Notifiable Data Breaches (NDB) scheme under the Privacy Act.
    *   This plan should cover detection, containment, assessment, notification (to affected individuals and the OAIC), and review.

### 6.2 Clear Disclaimers: 


"AI-generated policies require legal review"

**Objective:** Clearly communicate the limitations of AI-generated content and the necessity of human oversight to manage client expectations and legal liabilities.

**Instructions:**

1.  **[Growth/Dev] Prominent In-App Disclaimers:**
    *   Display clear and unavoidable disclaimers at key points within the application, especially when AI-generated content (policies, tender responses) is presented to the user.
    *   **Example Wording:**
        *   "**Important:** This policy has been generated by Artificial Intelligence. While designed for compliance, it is a draft and **requires review and validation by a qualified legal or compliance professional** to ensure accuracy, completeness, and applicability to your specific organizational context and current regulatory requirements. Policy Genesis Suite is not a law firm and does not provide legal advice."
        *   "**AI-Assisted Draft:** The content below is an AI-generated draft response. It is crucial to **review, edit, and customize** this content to accurately reflect your organization's capabilities and fully address the tender requirements. Always verify against the original tender document."

2.  **[Growth] Website and Marketing Material Disclaimers:**
    *   Include similar disclaimers on the product website, in marketing collateral, and during sales presentations.
    *   Emphasize that the platform is a tool to assist and accelerate compliance efforts, not a replacement for human expertise.

3.  **[Legal/Founder] Terms of Service and User Agreements:**
    *   Ensure the Terms of Service and User Agreements explicitly state the limitations of the AI, the user's responsibility for reviewing and validating generated content, and that the platform does not provide legal advice.

### 6.3 Data Retention and Audit Logging for Generated Documents

**Objective:** Implement robust data retention policies and comprehensive audit logging to meet regulatory requirements, support forensic analysis, and ensure accountability.

**Instructions:**

1.  **[Ops/Dev] Data Retention Policy:**
    *   Define a clear data retention policy for all types of data, especially AI-generated documents (policies, tender responses) and client-uploaded evidence.
    *   **Example:**
        *   **AI-Generated Policies/Tender Responses:** Retain for 7 years (or as required by specific compliance frameworks like ISO 27001 or client contracts).
        *   **Client-Uploaded Evidence:** Retain for 7 years or as long as the client maintains an active subscription, plus a grace period.
        *   **Audit Logs:** Retain for 1-3 years in active storage (CloudWatch Logs) and archive to S3 Glacier for long-term retention (7+ years).
    *   Implement automated lifecycle rules for S3 buckets to transition older data to lower-cost storage tiers (e.g., S3 Glacier) and eventually delete it after the retention period.

2.  **[Dev] Comprehensive Audit Logging:**
    *   **User Actions:** Log every significant user action within the platform (e.g., login, logout, policy generation, policy edit, tender upload, evidence submission, subscription change).
        *   **Details to Log:** User ID, organization ID, timestamp, action type, affected resource ID (e.g., `policy_id`), IP address, outcome (success/failure).
    *   **AI Agent Actions:** Log every invocation of an AI agent, including input prompts, model used, and output summary.
        *   **Details to Log:** Agent type, timestamp, `policy_id`/`tender_id` (if applicable), model ID, prompt hash (or truncated prompt), response hash (or truncated response), duration, outcome.
    *   **System Events:** Log critical system events (e.g., API calls, database changes, webhook receptions, errors).

3.  **[Dev] Audit Log Storage and Access:**
    *   Store all audit logs in **Amazon CloudWatch Logs** for real-time monitoring and short-term retention.
    *   Configure CloudWatch Logs to export logs to **Amazon S3** for long-term archival and analysis.
    *   Ensure audit logs are immutable and protected from unauthorized modification.
    *   Provide authorized users (e.g., Compliance Managers, Auditors) with secure, read-only access to audit logs via the Compliance Dashboard or dedicated reporting tools.

4.  **[Ops] Regular Audit Log Review:**
    *   Establish a process for regular review of audit logs to detect suspicious activities, unauthorized access attempts, or system anomalies.
    *   Utilize AWS CloudWatch Alarms and Dashboards to visualize log data and trigger alerts for predefined security events.

This robust compliance and risk framework ensures that the Policy Genesis Suite operates with integrity, transparency, and adherence to regulatory requirements, protecting both the platform and its clients from potential legal and reputational risks.



## 7. Execution Timeline

This section outlines a phased execution timeline, designed to prioritize rapid delivery of a Minimum Viable Product (MVP) and subsequent feature expansion. The timeline is structured into a 7-day sprint, a 30-day roadmap, and a 90-day roadmap, with clear milestones and role assignments for a small development and growth team.

### 7.1 7-Day Sprint Plan: MVP Policy Generator Live with Payments Enabled

**Objective:** Launch a functional AI-powered policy generator with basic user authentication and subscription capabilities within one week to validate core value proposition and begin monetization.

**Milestones:**

*   **Day 1-2: Infrastructure & Core API Setup [Dev, Ops]**
    *   **[Dev]** AWS Account setup, IAM roles, and basic AWS CLI configuration.
    *   **[Dev]** Deploy initial AWS API Gateway with `/policies/generate` endpoint.
    *   **[Dev]** Create `generatePolicyLambda` (Python) with placeholder logic.
    *   **[Dev]** Set up Amazon RDS PostgreSQL instance (`db.t3.micro`).
    *   **[Dev]** Create `organizations` and `policies` tables.
    *   **[Dev]** Create S3 bucket for policy storage (`policy-genesis-policies`).
    *   **[Ops]** Configure basic monitoring for Lambda and API Gateway.

*   **Day 3-4: AI Integration & Policy Generation [Dev]**
    *   **[Dev]** Enable Amazon Bedrock access and integrate `generatePolicyLambda` with a Foundation Model (e.g., Anthropic Claude).
    *   **[Dev]** Implement prompt construction logic within Lambda, using basic user input.
    *   **[Dev]** Store generated policy content in S3 and metadata in RDS.
    *   **[Dev]** Develop a simple frontend page for policy generation (input form, display generated text).

*   **Day 5-6: Authentication & Payments [Dev, Growth]**
    *   **[Dev]** Set up AWS Cognito User Pool for user authentication.
    *   **[Dev]** Integrate Cognito signup/login into the frontend.
    *   **[Dev]** Set up Stripe account, define Free and Paid tiers.
    *   **[Dev]** Implement Stripe Checkout on the frontend for Paid tier subscription.
    *   **[Dev]** Create `stripeWebhookHandler` Lambda to update RDS `organizations` table on subscription events.
    *   **[Dev]** Implement basic role-based access control (Free vs. Paid) in Lambda and frontend.
    *   **[Growth]** Prepare initial landing page copy and calls-to-action for free trial/paid subscription.

*   **Day 7: Testing & Deployment [Dev, Ops, Founder]**
    *   **[Dev]** End-to-end testing of policy generation, user signup, and payment flow.
    *   **[Dev]** Deploy frontend to Vercel/AWS Amplify.
    *   **[Ops]** Verify all services are running, logs are flowing, and basic security checks are passed.
    *   **[Founder]** Final review and go-live decision.

### 7.2 30-Day Roadmap: Tender-Writing Feature

**Objective:** Extend the platform with the Tender Auto-Writing feature, allowing users to upload tender documents and receive AI-generated draft responses.

**Milestones:**

*   **Week 2: Tender Document Ingestion & Analysis [Dev]**
    *   **[Dev]** Implement `/tenders/upload` API endpoint and `uploadTenderLambda`.
    *   **[Dev]** Integrate with S3 for raw tender document storage.
    *   **[Dev]** Implement text extraction from PDF/DOCX (e.g., AWS Textract or `python-docx`).
    *   **[Dev]** Develop `analyzeTenderLambda` to extract questions/requirements using Bedrock.
    *   **[Dev]** Update `tenders` table schema in RDS to store analysis summary.
    *   **[Dev]** Create frontend UI for tender upload and display of extracted questions.

*   **Week 3: AI Response Generation & Editing [Dev]**
    *   **[Dev]** Develop `generateTenderResponseLambda` to draft responses using Bedrock, leveraging client profile and existing policies.
    *   **[Dev]** Store draft responses in S3.
    *   **[Dev]** Create frontend UI for reviewing and editing AI-generated tender responses.
    *   **[Dev]** Implement saving user edits back to S3 (versioning).

*   **Week 4: Workflow Orchestration & Refinement [Dev, Ops]**
    *   **[Dev]** Implement n8n workflow for tender processing (trigger on upload, AI analysis, response generation, notifications).
    *   **[Dev]** Integrate n8n webhook with `uploadTenderLambda` or a dedicated API Gateway endpoint.
    *   **[Dev]** Implement export options for tender responses (DOCX, PDF).
    *   **[Dev]** Conduct internal testing and gather feedback.
    *   **[Ops]** Monitor n8n workflow performance and reliability.

### 7.3 90-Day Roadmap: Compliance Dashboard + Enterprise Pilot

**Objective:** Introduce the comprehensive Compliance Dashboard and onboard the first Enterprise pilot clients, validating the full SaaS offering.

**Milestones:**

*   **Month 2: Compliance Dashboard Data Model & UI [Dev]**
    *   **[Dev]** Finalize `compliance_frameworks`, `compliance_status`, and `compliance_evidence` table schemas in RDS.
    *   **[Dev]** Develop APIs for fetching compliance data (`/compliance/dashboard`, `/compliance/frameworks/{id}/controls`).
    *   **[Dev]** Build core UI components for the Compliance Dashboard (overview, framework-specific views, control lists, evidence management).
    *   **[Dev]** Implement evidence upload functionality (S3 integration).

*   **Month 3: Reporting, Alerts & Enterprise Onboarding [Dev, Growth, Ops]**
    *   **[Dev]** Implement basic reporting features (e.g., export compliance status to PDF).
    *   **[Dev]** Integrate n8n for compliance reminders and alerts (e.g., overdue tasks).
    *   **[Dev]** Enhance RBAC for multi-user Enterprise accounts.
    *   **[Growth]** Identify and engage 1-2 Enterprise pilot clients.
    *   **[Growth]** Develop onboarding materials and support processes for Enterprise clients.
    *   **[Ops]** Set up dedicated monitoring and support channels for pilot clients.
    *   **[Dev]** Gather feedback from pilot clients and prioritize enhancements.

### 7.4 Ongoing Activities (Post-90 Days)

*   **[Dev]** Continuous AI model refinement and prompt engineering.
*   **[Dev]** Addition of new compliance frameworks based on market demand.
*   **[Dev]** Development of advanced features (e.g., predictive analytics, automated remediation).
*   **[Growth]** Expansion of sales and marketing campaigns, A/B testing.
*   **[Ops]** Performance optimization, cost management, security audits.
*   **[Founder]** Strategic partnerships, market expansion, product roadmap planning.

This phased approach allows for agile development, continuous feedback integration, and a clear path to market leadership, ensuring that the Policy Genesis Suite evolves effectively to meet client needs and market demands.

## 8. Compile Final Operational Document

This final section consolidates all the technical and operational details into a comprehensive document, ensuring it is ready for immediate use by the development and growth teams. It includes structured sections, checklists, Standard Operating Procedures (SOPs), example code, and role tags to facilitate execution.

### 8.1 Output as Structured Sections with Checklists and SOPs

**Objective:** Present the entire document in a clear, actionable format that serves as a practical guide for the team.

**Instructions:**

1.  **[Founder/Ops] Review and Refine:**
    *   Review all sections for clarity, completeness, and accuracy.
    *   Ensure consistency in terminology and formatting.
    *   Verify that all instructions are step-by-step and actionable.

2.  **[Dev/Ops/Growth] Develop Checklists:**
    *   For each major task within the Development, Core Feature, Workflow, Membership, Sales, and Compliance sections, create a concise checklist of sub-tasks.
    *   **Example Checklist Item:**
        *   **Task:** Implement `/policies/generate` API endpoint
        *   **Checklist:**
            *   [ ] Create API Gateway resource and method.
            *   [ ] Integrate with `generatePolicyLambda`.
            *   [ ] Configure IAM permissions for Lambda.
            *   [ ] Enable CORS.
            *   [ ] Deploy API to `dev` stage.

3.  **[Ops] Create Standard Operating Procedures (SOPs):**
    *   For recurring operational tasks (e.g., deploying new Lambda versions, monitoring system health, handling customer support tickets, responding to security incidents), develop detailed SOPs.
    *   **Example SOP Title:** "SOP: Deploying a New Backend Lambda Function"
    *   **SOP Content:** Step-by-step instructions, required tools, verification steps, rollback procedures, and contact points for escalation.

### 8.2 Include Example API Routes, n8n JSON Skeletons, and DB Schema Outlines

**Objective:** Provide concrete technical examples to accelerate development and ensure consistency.

**Instructions:**

1.  **[Dev] Verify API Routes:**
    *   Ensure all example API routes provided in Section 1.1.1 and 2.x are accurate and reflect the planned implementation.
    *   Add any missing critical API endpoints.

2.  **[Dev] Validate n8n JSON Skeletons:**
    *   Confirm the n8n JSON skeleton provided in Section 3.3 is functional and can be directly imported into n8n.
    *   Add additional skeletons for other critical workflows (e.g., Tender Analysis, Compliance Reminders) as they are designed.

3.  **[Dev] Review DB Schema Outlines:**
    *   Ensure all database schema outlines (SQL `CREATE TABLE` statements) are complete, accurate, and include all necessary fields and relationships.
    *   Add comments to explain complex fields or design choices.

### 8.3 Role Tags for Each Step: [Dev], [Ops], [Growth], [Founder]

**Objective:** Clearly assign responsibility for each task to facilitate efficient execution and accountability within the small team.

**Instructions:**

1.  **[Founder] Assign Roles:**
    *   Review the entire document and ensure every actionable step, checklist item, and SOP has a clear role tag: `[Dev]` (Development), `[Ops]` (Operations/Infrastructure), `[Growth]` (Sales/Marketing/Product Growth), or `[Founder]` (Strategic/Executive decisions).
    *   For tasks requiring multiple roles, list all relevant tags (e.g., `[Dev, Ops]`).

This comprehensive operational document, with its structured content, actionable checklists, technical examples, and clear role assignments, will serve as the single source of truth for the Policy Genesis Suite team, guiding them from implementation to market success.

