## 3. Membership & SaaS Service Layer Implementation

This section provides operational steps for implementing the membership and SaaS service layer, covering user authentication, subscription management, and role-based access control. The goal is to enable a tiered service offering (Free vs. Premium) with appropriate data access limits.

**Who does this:** [Dev], [Founder]

### 3.1. Operational Steps to Implement Login/Signup on Replit

**Goal:** Provide secure user registration and authentication for the SaaS application.

**Steps:**
1.  **Backend API Endpoints:**
    *   **`/register` (POST):** Create an endpoint to handle new user registrations. This endpoint will receive `username`, `email`, and `password`.
        *   Hash the password using a strong hashing algorithm (e.g., `bcrypt` in Python) before storing it in the database.
        *   Store user details (username, hashed password, email, default role, subscription status) in the database (PostgreSQL recommended for scale).
        *   Return a success message or a JWT upon successful registration.
    *   **`/login` (POST):** Create an endpoint to handle user logins. This endpoint will receive `email` and `password`.
        *   Verify the provided password against the hashed password in the database.
        *   If credentials are valid, generate a JWT containing user ID, role, and subscription status, and return it to the client.
    *   **`/refresh-token` (POST, optional):** Implement a mechanism to refresh JWTs to maintain user sessions without requiring re-login.
2.  **Frontend Integration:**
    *   **Registration Form:** Create a React component for user registration, sending data to the `/register` endpoint.
    *   **Login Form:** Create a React component for user login, sending data to the `/login` endpoint.
    *   **JWT Handling:** Store the received JWT securely on the client-side (e.g., in `localStorage` or `httpOnly` cookies). Include the JWT in the `Authorization` header of all subsequent authenticated API requests.
    *   **Protected Routes:** Implement client-side routing protection to restrict access to certain pages based on the presence and validity of the JWT.

**Sample Backend (Flask) Code Snippet for Authentication:**

```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# Placeholder for a user database (replace with actual DB integration)
users = {}

@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if email in users:
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    users[email] = {"password": hashed_password, "role": "free", "subscription_status": "inactive"}
    return jsonify({"msg": "User created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = users.get(email)
    if user and check_password_hash(user["password"], password):
        access_token = create_access_token(identity=email, additional_claims={"role": user["role"], "subscription_status": user["subscription_status"]})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_email = get_jwt_identity()
    claims = get_jwt()
    return jsonify(logged_in_as=current_user_email, role=claims["role"], subscription=claims["subscription_status"]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 3.2. Stripe/PayPal Integration for Subscriptions

**Goal:** Enable users to subscribe to premium tiers and manage their subscriptions.

**Steps:**
1.  **Choose Payment Gateway:** Select either [Stripe](https://stripe.com/) or [PayPal](https://www.paypal.com/us/business/platforms-and-marketplaces) for subscription management. Stripe is generally preferred for its developer-friendly APIs and extensive documentation.
2.  **Set up Products and Pricing Plans:**
    *   In your chosen payment gateway dashboard, define your subscription products (e.g., "Premium Access") and pricing plans (e.g., monthly, yearly).
3.  **Backend Integration:**
    *   **Webhook Endpoint:** Create a backend endpoint (e.g., `/stripe-webhook`) to listen for events from the payment gateway (e.g., `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`).
    *   **Customer Creation:** When a user initiates a subscription, create a customer record in the payment gateway and link it to your internal user ID.
    *   **Subscription Management:** Update the user's `subscription_status` and `role` in your database based on webhook events. This ensures your application always reflects the current subscription status.
    *   **API Keys:** Store payment gateway API keys securely as environment variables in Replit.
4.  **Frontend Integration:**
    *   **Subscription Page:** Create a dedicated page where users can view available plans and initiate a subscription.
    *   **Checkout Flow:** Use the payment gateway's client-side libraries (e.g., Stripe.js) to handle the checkout process securely, redirecting users to a hosted checkout page or embedding a payment form.
    *   **Success/Failure Pages:** Redirect users to appropriate pages after checkout (e.g., `/subscription-success`, `/subscription-failed`).

### 3.3. Role-Based Access: Free vs Premium Tiers

**Goal:** Differentiate user access and features based on their subscription status.

**Steps:**
1.  **Define Roles:** Establish clear roles (e.g., `free`, `premium`) in your user database.
2.  **Backend Authorization:**
    *   Modify API endpoints to check the user's role (extracted from the JWT claims) before granting access to premium features or data.
    *   Example: A premium endpoint might return more detailed data or allow more frequent requests.
3.  **Frontend UI/UX:**
    *   Dynamically adjust the user interface based on the user's role. For example, hide premium features for free users or display upgrade prompts.
    *   Show current subscription status and options to upgrade/manage subscription.

### 3.4. Data Access Limits per User Type

**Goal:** Enforce usage quotas for different subscription tiers.

**Steps:**
1.  **Database Fields:** Add fields to your user database to track usage (e.g., `daily_lead_count`, `max_daily_leads`, `export_credits`).
2.  **Backend Middleware/Decorators:**
    *   Implement middleware or decorators on your API endpoints that serve property leads.
    *   Before returning data, check the user's `role` and `daily_lead_count` against their `max_daily_leads`.
    *   If a free user exceeds their quota, return an error (e.g., 403 Forbidden) and suggest upgrading.
    *   Increment `daily_lead_count` for each lead accessed.
3.  **Reset Mechanism:** Implement a scheduled task (e.g., an n8n workflow or a cron job on the backend server) to reset `daily_lead_count` for all users at the beginning of each day.
4.  **Frontend Feedback:** Display the user's current usage and remaining quota in the dashboard to provide transparency and encourage upgrades.
