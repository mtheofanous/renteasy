import streamlit as st
import json
import os
import uuid

# Initialize session state for navigation and user data
if "role" not in st.session_state:
    st.session_state.role = None
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "homepage"
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Database file path
DB_FILE = "database.json"

# Function to load database
def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save database
def save_database(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Initialize database
db = load_database()

# Function to reset session state (clear all data)
def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.current_page = "homepage"

# Function for navigation
def navigate_to(page):
    st.session_state.current_page = page

# Homepage
def homepage():
    st.title("Welcome to the Rental App")
    st.write("Please login or sign up to continue.")
    if st.button("Login"):
        navigate_to("dashboard")
    if st.button("Sign Up"):
        navigate_to("sign_up")

# Sign-Up Page
def sign_up():
    st.title("Sign Up")
    role = st.radio("Choose Your Role", ["Renter", "Landlord", "Agent"])
    if st.button("Confirm"):
        # Generate a new user ID for each new sign-up
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.role = role
        st.session_state.profile = {}  # Start with a fresh profile
        st.success(f"Signed up as {role}! Redirecting to dashboard...")
        navigate_to("dashboard")
    if st.button("Back"):
        navigate_to("homepage")

# Dashboard
def dashboard():
    st.title("Dashboard")
    st.sidebar.title("Navigation")
    st.sidebar.button("Log Out", on_click=reset_session)  # Reset session on log out
    st.sidebar.button("Profile Settings", on_click=lambda: navigate_to("profile_settings"))
    st.sidebar.button("Switch Role", on_click=lambda: navigate_to("choose_role"))
    
    # Role-specific dashboard
    role = st.session_state.role
    if role == "Renter":
        renter_dashboard()
    elif role == "Landlord":
        landlord_dashboard()
    elif role == "Agent":
        agent_dashboard()
    else:
        choose_role()

# Role Selection
def choose_role():
    st.header("Choose Your Profile Role")
    role = st.radio("Select Role", ["Renter", "Landlord", "Agent"])
    if st.button("Confirm"):
        st.session_state.role = role
        navigate_to("dashboard")
    if st.button("Back"):
        navigate_to("dashboard")

# Renter Dashboard
def renter_dashboard():
    st.header("Renter Dashboard")
    user_id = st.session_state.get("user_id", "default_user")
    if user_id in db and "renter_profile" in db[user_id]:
        st.subheader("Your Profile")
        st.write(db[user_id]["renter_profile"])
        if st.button("Edit Profile"):
            create_full_profile()
    else:
        st.write("You have not created a profile yet.")
        if st.button("Create Profile"):
            navigate_to("create_renter_profile")
    if st.button("Back"):
        navigate_to("dashboard")

def create_renter_profile():
    st.header("Create/Edit Renter Profile")
    user_id = st.session_state.get("user_id", "default_user")
    current_profile = db.get(user_id, {}).get("renter_profile", {})
    username = st.text_input("Username", value=current_profile.get("username", ""))
    email = st.text_input("Email", value=current_profile.get("email", ""))
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if password != confirm_password:
        st.warning("Passwords do not match!")
    
    if st.button("Save Profile"):
        # Update the database
        db[user_id] = db.get(user_id, {})
        db[user_id]["renter_profile"] = {"username": username, "email": email,"password": password}
        save_database(db)
        
        st.success("Profile saved!")
        navigate_to("renter_dashboard")
    if st.button("Back"):
        navigate_to("renter_dashboard")
        
def create_full_profile():
    st.header("Create/Edit Full Renter Profile")
    user_id = st.session_state.get("user_id", "default_user")
    current_profile = db.get(user_id, {}).get("renter_profile", {})
    
    # Profile Header
    name = st.text_input("Full Name", value=current_profile.get("name", ""), placeholder="John Doe")
    tagline = st.text_input("Tagline", value=current_profile.get("tagline", ""), placeholder="Looking for a cozy apartment in downtown LA")

    # Personal Details
    with st.expander("Personal Details"):
        email = st.text_input("Email", value=current_profile.get("email", ""))
        phone = st.text_input("Phone Number", value=current_profile.get("phone", ""))
        nationality = st.text_input("Nationality", value=current_profile.get("nationality", ""), placeholder="e.g., American, Indian")
        marital_status = st.radio("Marital Status", ["Single", "Married", "Divorced", "Widowed"], index=["Single", "Married", "Divorced", "Widowed"].index(current_profile.get("marital_status", "Single")))
        pets = st.radio("Do you have pets?", ["No", "Yes"], index=["No", "Yes"].index(current_profile.get("pets", "No")))
        occupation = st.text_input("Current Job", value=current_profile.get("occupation", ""), placeholder="e.g., Software Engineer")
        contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"], index=["Permanent", "Contract", "Freelancer", "Unemployed"].index(current_profile.get("contract_type", "Permanent")))
        social_media = st.text_input("Social Media Link (Optional)", value=current_profile.get("social_media", ""))

    # Rental Preferences
    with st.expander("Rental Preferences"):
        city = st.selectbox("Preferred City", ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"], index=["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"].index(current_profile.get("city", "Athens")))
        areas = {
            "Athens": ["Plaka", "Kolonaki", "Glyfada", "Marousi", "Kifisia"],
            "Thessaloniki": ["Ladadika", "Toumba", "Panorama", "Pylaia", "Thermi"],
            "Patras": ["Psila Alonia", "Rio", "Agios Andreas", "Vrachneika"],
            "Heraklion": ["Knossos", "Ammoudara", "Poros", "Agios Nikolaos"],
            "Other": ["Specify Other"]
        }
        area = current_profile.get("area", "")
        if city in areas:
            area = st.selectbox("Preferred Area", areas[city], index=areas[city].index(area) if area in areas[city] else 0)
            if area == "Specify Other":
                area = st.text_input("Specify your area", value=current_profile.get("area", ""), placeholder="Enter area name")
        budget = st.slider("Budget Range ($)", 500, 5000, current_profile.get("budget", (1000, 3000)))
        property_type = st.selectbox("Type of Property", ["Apartment", "House", "Shared Accommodation"], index=["Apartment", "House", "Shared Accommodation"].index(current_profile.get("property_type", "Apartment")))
        move_in_date = st.date_input("Move-in Date", value=current_profile.get("move_in_date", None))
        lease_duration = st.selectbox("Lease Duration", ["Short-term", "Long-term", "Flexible"], index=["Short-term", "Long-term", "Flexible"].index(current_profile.get("lease_duration", "Long-term")))

    # Save Profile Button
    if st.button("Save Profile"):
        profile = {
            "name": name,
            "tagline": tagline,
            "email": email,
            "phone": phone,
            "nationality": nationality,
            "marital_status": marital_status,
            "pets": pets,
            "occupation": occupation,
            "contract_type": contract_type,
            "social_media": social_media,
            "city": city,
            "area": area,
            "budget": budget,
            "property_type": property_type,
            "move_in_date": str(move_in_date),
            "lease_duration": lease_duration,
        }
        # Save profile to the database
        db[user_id] = {"renter_profile": profile}
        save_database(db)
        st.success("Profile saved successfully! You can continue editing or return to the dashboard.")

    # Back Button
    if st.button("Back to Dashboard"):
        navigate_to("renter_dashboard")


    
    
    
        

# Landlord Dashboard
def landlord_dashboard():
    st.header("Landlord Dashboard")
    st.subheader("Search for Renters")
    filters = {}
    filters["age"] = st.slider("Age Range", 18, 70, (25, 35))
    filters["budget"] = st.slider("Budget Range", 500, 5000, (1000, 3000))
    filters["location"] = st.text_input("Location Filter")
    if st.button("Search"):
        st.write("Search Results (TBD)")
    if st.button("Back"):
        navigate_to("dashboard")
    
    st.subheader("Manage Recommendation Forms")
    if st.button("View Forms"):
        st.write("Form management (TBD)")

# Agent Dashboard
def agent_dashboard():
    st.header("Agent Dashboard")
    st.subheader("Renter Profiles")
    st.write("Access all renter profiles (TBD)")
    st.subheader("Landlord Profiles")
    st.write("Access all landlord profiles (TBD)")
    st.subheader("Property Listings")
    st.write("Access all rental properties (TBD)")
    st.subheader("Analytics")
    st.write("Aggregate insights (TBD)")
    if st.button("Back"):
        navigate_to("dashboard")

# Profile Settings
def profile_settings():
    st.header("Profile Settings")
    st.write("Edit your personal settings here (TBD).")
    if st.button("Back"):
        navigate_to("dashboard")

# App flow
pages = {
    "homepage": homepage,
    "sign_up": sign_up,
    "dashboard": dashboard,
    "choose_role": choose_role,
    "renter_dashboard": renter_dashboard,
    "create_renter_profile": create_renter_profile,
    "profile_settings": profile_settings,
}

# Display the current page
if st.session_state.current_page in pages:
    pages[st.session_state.current_page]()
else:
    homepage()
