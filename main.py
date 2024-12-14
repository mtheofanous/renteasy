import streamlit as st
import json
import os

# Initialize session state
if "user_type" not in st.session_state:
    st.session_state["user_type"] = None
if "show_landlord_form" not in st.session_state:
    st.session_state["show_landlord_form"] = False
if "error_message" not in st.session_state:
    st.session_state["error_message"] = ""
if "recommendation_verified" not in st.session_state:
    st.session_state["recommendation_verified"] = False
if "profile_saved" not in st.session_state:
    st.session_state["profile_saved"] = False
if "saved_profile" not in st.session_state:
    st.session_state["saved_profile"] = {}
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"



# File to store profiles
PROFILE_FILE = "fake_profiles.json"

# Add Back to Home Button
def back_to_home():
    if st.button("🏠 Homepage", key="back_to_home"):
        st.session_state["current_page"] = "landing"
        st.session_state["user_type"] = None
        reset_profile_saved_state()
        
def back_to_dashboard():
    if st.button("🏠 Dashboard", key="back_to_dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.session_state["user_type"] = None
        reset_profile_saved_state()
        
# Sign Up Page
def signup_page():
    back_to_home()
    st.title("Sign Up")
    st.write("Create an account to get started.")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            st.success("Account created successfully!")
            st.session_state["current_page"] = "dashboard"  # Redirect to dashboard after login
    
# Log In Page
def login_page():
    
    back_to_home()
    st.title("Log In")
    st.write("Enter your credentials to log in.")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        st.success("Logged in successfully!")
        st.session_state["current_page"] = "dashboard"  # Redirect to dashboard after signup
        
def logout():
    if st.button("Log Out"):
        st.session_state["current_page"] = "landing"
        st.session_state["user_type"] = None
        reset_profile_saved_state()

# Helper function to load profiles
# def load_profiles():
#     """Load profiles from the JSON file."""
#     if os.path.exists(PROFILE_FILE):
#         with open(PROFILE_FILE, "r") as file:
#             try:
#                 profiles = json.load(file)
#                 return profiles
#             except json.JSONDecodeError:
#                 st.warning("Profile file is corrupted or empty. Resetting profiles.")
#                 return {}
#     return {}


def load_profiles():
    """Load profiles from the JSON file."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as file:
            try:
                profiles = json.load(file)
                return profiles
            except json.JSONDecodeError:
                st.warning("Profile file is corrupted or empty. Resetting profiles.")
                return []
    return []

# Helper function to save profiles
def save_profile_to_file(profile):
    profiles = load_profiles()
    profiles.append(profile)
    with open(PROFILE_FILE, "w") as file:
        json.dump(profiles, file, indent=4)
        
# Load profiles into session state on startup
if "all_profiles" not in st.session_state:
    st.session_state["all_profiles"] = load_profiles()
        
def update_profile_to_file(profiles):
    with open(PROFILE_FILE, "w") as file:
        json.dump(profiles, file, indent=4)
        
def profile_settings():
    st.title("Edit Profile")
    profile = st.session_state["profile_data"]
    profile["name"] = st.text_input("Name", profile.get("name", ""))
    profile["email"] = st.text_input("Email", profile.get("email", ""))
    if st.button("Save"):
        st.success("Profile updated successfully!")
        update_profile_to_file(profile)

# Helper function to reset the profile saved state
def reset_profile_saved_state():
    st.session_state["profile_saved"] = False
    st.session_state["saved_profile"] = {}


#     st.divider()
def render_profile_preview(profile):
    st.markdown("## 🎉 Profile Preview")
    st.divider()

    # Header Section
    st.markdown(f"""
    <div style="text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 20px;">
        {profile.get('name', 'No Name Provided')}
    </div>
    <div style="text-align: center; font-size: 18px; color: grey; margin-bottom: 30px;">
        {profile.get('tagline', 'No Tagline Provided')}
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Personal Details
    st.markdown("### 🧍 Personal Details")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- **Email:** {profile.get('email', 'Not Provided')}")
        st.markdown(f"- **Phone:** {profile.get('phone', 'Not Provided')}")
        st.markdown(f"- **Nationality:** {profile.get('nationality', 'Not Provided')}")
    with col2:
        st.markdown(f"- **Marital Status:** {profile.get('marital_status', 'Not Provided')}")
        st.markdown(f"- **Pets:** {profile.get('pets', 'Not Provided')}")
        st.markdown(f"- **Occupation:** {profile.get('occupation', 'Not Provided')} ({profile.get('contract_type', 'Not Provided')})")

    st.divider()

    # Rental Preferences
    st.markdown("### 🏡 Rental Preferences")
    st.markdown(f"""
    - **City:** {profile.get('city', 'Not Provided')}
    - **Area:** {profile.get('area', 'Not Provided')}
    - **Budget Range:** ${profile.get('budget', [0, 0])[0]} - ${profile.get('budget', [0, 0])[1]}
    - **Property Type:** {profile.get('property_type', 'Not Provided')}
    - **Move-in Date:** {profile.get('move_in_date', 'Not Provided')}
    - **Lease Duration:** {profile.get('lease_duration', 'Not Provided')}
    """)
    st.divider()

    # About Me
    st.markdown("### 📝 About Me")
    st.markdown(f"""
    - **Bio:** {profile.get('bio', 'No Bio Provided')}
    - **Hobbies:** {profile.get('hobbies', 'Not Provided')}
    """)
    st.divider()

    # Income and Credit Score
    st.markdown("### 💳 Income and Credit Score")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- **Monthly Income:** ${profile.get('income', 'Not Provided')}")
    with col2:
        if profile.get('credit_score_verified', False):
            st.markdown("✅ **Credit Score Verified**")
        else:
            st.markdown("⚠️ **Credit Score Not Verified**")

    st.divider()

    # Landlord Recommendation (Handles Nested Key)
    st.markdown("### 🏠 Landlord Recommendation")
    landlord_recommendation = profile.get('landlord_recommendation', {})
    if landlord_recommendation:
        st.markdown(f"""
        - **Landlord Name:** {landlord_recommendation.get('landlord_name', 'Not Provided')}
        - **Recommendation:** {landlord_recommendation.get('recommendation', 'No Recommendation Provided')}
        """)
    else:
        st.markdown("- No landlord recommendation provided.")
    
    st.divider()





# Landing Page
def landing_page():
    # Back to Home Button
    left_column, right_column = st.columns([2.5, 1])
    with left_column:
        back_to_home()
    
    with right_column:
        # Login/Sign-in Section
        login_col, signup_col = st.columns([1,1],gap='small')
        with login_col:
            if st.button("Log In", key="login_button"):
                st.session_state["current_page"] = "login"
                
            
        with signup_col:
            if st.button("Sign Up", key="signup_button"):
                st.session_state["current_page"] = "signup"
    

    # Page Title
    st.title("Welcome to RentEasy!")
    st.subheader("Connecting renters with landlords and real estate agents seamlessly.")
    
    # Platform Information
    st.write("""
    ### About RentEasy:
    - **For Renters**: Easily find and rent properties matching your preferences.
    - **For Landlords/Agents**: Manage tenant profiles, verify recommendations, and more.
    - Safe, secure, and user-friendly.
    """)
# Dashboard Page
def dashboard_page():
    left_column, right_column = st.columns([6, 1])
    with left_column:
        back_to_home()
    with right_column:
        logout()
    st.title("Dashboard")
    st.write("Choose your profile to proceed:")
    
    
    # Role Selection
    role_col1, role_col2 = st.columns(2)
    with role_col1:
        if st.button("I am a Renter"):
            st.session_state["user_type"] = "renter"
            st.session_state["current_page"] = "home"
            
            
    with role_col2:
        if st.button("I am a Landlord/Real Estate Agent"):
            st.session_state["user_type"] = "landlord_agent"
            st.session_state["current_page"] = "home"


# Renter's Profile Setup
def renter_profile():
    left_column, right_column = st.columns([6,1])
    with left_column:
        back_to_dashboard()
    with right_column:
        logout()
    st.title("Renter Profile Setup")
    st.write("Please fill out your profile to get started!")

    # Profile Header
    name = st.text_input("Full Name", placeholder="John Doe")
    tagline = st.text_input("Tagline", placeholder="Looking for a cozy apartment in downtown LA")

    # Personal Details
    with st.expander("Personal Details"):
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        nationality = st.text_input("Nationality", placeholder="e.g., American, Indian")
        marital_status = st.radio("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        pets = st.radio("Do you have pets?", ["No", "Yes"])
        occupation = st.text_input("Current Job", placeholder="e.g., Software Engineer")
        contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"])
        social_media = st.text_input("Social Media Link (Optional)")

    # Rental Preferences
    with st.expander("Rental Preferences"):
        city = st.selectbox("Preferred City", ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"])
        areas = {
            "Athens": ["Plaka", "Kolonaki", "Glyfada", "Marousi", "Kifisia"],
            "Thessaloniki": ["Ladadika", "Toumba", "Panorama", "Pylaia", "Thermi"],
            "Patras": ["Psila Alonia", "Rio", "Agios Andreas", "Vrachneika"],
            "Heraklion": ["Knossos", "Ammoudara", "Poros", "Agios Nikolaos"],
            "Other": ["Specify Other"]
        }
        if city in areas:
            area = st.selectbox("Preferred Area", areas[city])
            if area == "Specify Other":
                area = st.text_input("Specify your area", placeholder="Enter area name")
        budget = st.slider("Budget Range ($)", 500, 5000, (1000, 3000))
        property_type = st.selectbox("Type of Property", ["Apartment", "House", "Shared Accommodation"])
        move_in_date = st.date_input("Move-in Date")
        lease_duration = st.selectbox("Lease Duration", ["Short-term", "Long-term", "Flexible"])

    # About Me Section
    with st.expander("About Me"):
        bio = st.text_area("Bio")
        hobbies = st.text_input("Hobbies & Interests (Comma separated)")

    # Income and Credit Score
    with st.expander("Income and Credit Score"):
        income = st.number_input("Monthly Income ($)", min_value=0, step=100)
        authorization = st.checkbox("I authorize contacting Teiresias.gr for my credit score verification.")
        uploaded_file = None
        credit_score_verified = False
        if authorization:
            st.info("Please upload the credit score result from Teiresias.gr.")
            uploaded_file = st.file_uploader("Upload your credit score result (PDF or Image)", type=["pdf", "jpg", "png"])
            if uploaded_file:
                credit_score_verified = True
                st.success("Credit score uploaded successfully!")

    # Previous Landlord Recommendation
    with st.expander("Previous Landlord Recommendation"):
        landlord_name = st.text_input("Landlord's Full Name", placeholder="e.g., Jane Doe")
        landlord_email = st.text_input("Landlord's Email", placeholder="e.g., landlord@example.com")
        landlord_phone = st.text_input("Landlord's Phone Number", placeholder="e.g., +123456789")
        if st.session_state["recommendation_verified"]:
            st.markdown("### ✅ Recommendation Verified")

        if st.button("Send Recommendation Request"):
            if not landlord_name or not landlord_email or not landlord_phone:
                st.error("Please fill in all landlord details before sending the request.")
            else:
                st.session_state["show_landlord_form"] = True
                st.success("Recommendation request sent!")

    # Show Landlord Recommendation Form
    if st.session_state["show_landlord_form"]:
        st.markdown("### Landlord Recommendation Form")
        st.write(f"**Recommendation Request Sent to:** {landlord_name} by {name}")
        st.write(f"**Landlord Email:** {landlord_email}")
        st.write(f"**Landlord Phone:** {landlord_phone}")
        
        # Recommendation form fields
        on_time_payment = st.radio("Did the tenant pay rent on time?", ["Yes", "No"])
        utilities_payment = st.radio("Did the tenant pay utility bills on time?", ["Yes", "No"])
        property_condition = st.radio("Did the tenant maintain the property well?", ["Yes", "No"])
        noise_complaints = st.radio("Were there noise or behavioral complaints?", ["No", "Yes"])
        would_recommend = st.radio("Would you recommend this tenant to other landlords?", ["Yes", "No"])
        additional_comments = st.text_area("Additional Comments (Optional)")
        
        if st.button("Submit Recommendation"):
            st.session_state["recommendation_verified"] = True
            st.session_state["show_landlord_form"] = False
            st.success("Recommendation submitted successfully!")

    # Save Profile Button
    if st.button("Save Profile"):
        # Check for missing required fields
        missing_fields = []
        if not name:
            missing_fields.append("Full Name")
        if not email:
            missing_fields.append("Email")
        if not phone:
            missing_fields.append("Phone Number")
        if not nationality:
            missing_fields.append("Nationality")
        if not occupation:
            missing_fields.append("Current Job")
        if not city:
            missing_fields.append("Preferred City")
        if not area:
            missing_fields.append("Preferred Area")

        # Display error with missing fields
        if missing_fields:
            st.error(f"Please fill out all required fields: {', '.join(missing_fields)}")
        else:
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
                "bio": bio,
                "hobbies": hobbies,
                "income": income,
                "credit_score_verified": credit_score_verified,
                "landlord_recommendation": {
                    "landlord_name": landlord_name,
                    "landlord_email": landlord_email,
                    "landlord_phone": landlord_phone,
                    "recommendation_verified": st.session_state["recommendation_verified"],
                }
            }
            save_profile_to_file(profile)
            st.session_state["profile_saved"] = True
            st.session_state["saved_profile"] = profile
            st.success("Profile saved successfully!")


    # Profile Preview
    if st.session_state["profile_saved"]:
        render_profile_preview(st.session_state["saved_profile"])

# Landlord/Agent Placeholder Page
def landlord_agent_page():
    
    left_column, right_column = st.columns([6,1])
    with left_column:
        back_to_dashboard()
    with right_column:
        logout()
    
    st.title("Landlord / Real Estate Agent Dashboard")
    st.subheader("Manage renter profiles and recommendations.")

    # Navigation Options
    option = st.radio("What would you like to do?", ["View Renter Profiles", "Verify Recommendations"])

    if option == "View Renter Profiles":
        view_renter_profiles()
    elif option == "Verify Recommendations":
        verify_recommendations()

# View Renter Profiles
# def view_renter_profiles():
#     st.subheader("🏘️ View Renter Profiles")
#     profiles = load_profiles()

#     if not profiles:
#         st.warning("No renter profiles available.")
#         return

#     # Filter Options
#     with st.expander("Filter Profiles"):
#         city_filter = st.selectbox("City", ["All"] + list({p["city"] for p in profiles}))

#         # Dynamically populate area filter based on selected city
#         if city_filter == "All":
#             area_options = {p["area"] for p in profiles}
#         else:
#             area_options = {p["area"] for p in profiles if p["city"] == city_filter}
#         area_filter = st.selectbox("Area", ["All"] + list(area_options))

#         budget_min, budget_max = st.slider("Budget Range ($)", 500, 5000, (500, 5000))
#         credit_filter = st.radio("Credit Score Verified", ["All", "Yes", "No"])
#         recommendation_filter = st.radio("Recommendation Verified", ["All", "Yes", "No"])


def view_renter_profiles():
    st.subheader("🏘️ View Renter Profiles")
    profiles = load_profiles()  # Assuming this function loads the profiles as a list of dictionaries

    if not profiles:
        st.warning("No renter profiles available.")
        return

    # Filter Options
    with st.expander("Filter Profiles"):
        city_filter = st.selectbox("City", ["All"] + sorted({p.get("city", "Unknown") for p in profiles}))

        # Dynamically populate area filter based on selected city
        if city_filter == "All":
            area_options = {p.get("area", "Unknown") for p in profiles}
        else:
            area_options = {p.get("area", "Unknown") for p in profiles if p.get("city") == city_filter}
        area_filter = st.selectbox("Area", ["All"] + sorted(area_options))

        budget_min, budget_max = st.slider("Budget Range ($)", 500, 5000, (500, 5000))
        credit_filter = st.radio("Credit Score Verified", ["All", "Yes", "No"])
        recommendation_filter = st.radio("Recommendation Verified", ["All", "Yes", "No"])

    # Filter Profiles
    filtered_profiles = []
    for profile in profiles:
        try:
            # Handle budget as a range [min, max] or single value
            budget = profile.get("budget", [0, 0])
            if isinstance(budget, list) and len(budget) == 2:
                in_budget_range = not (budget_max < budget[0] or budget_min > budget[1])
            elif isinstance(budget, (int, float)):
                in_budget_range = budget_min <= budget <= budget_max
            else:
                continue

            # Apply all filters
            if (city_filter == "All" or profile.get("city") == city_filter) and \
               (area_filter == "All" or profile.get("area") == area_filter) and \
               in_budget_range and \
               (credit_filter == "All" or (credit_filter == "Yes" and profile.get("credit_score_verified")) or
                (credit_filter == "No" and not profile.get("credit_score_verified"))) and \
               (recommendation_filter == "All" or
                (recommendation_filter == "Yes" and profile.get("landlord_recommendation", {}).get("recommendation_verified")) or
                (recommendation_filter == "No" and not profile.get("landlord_recommendation", {}).get("recommendation_verified"))):
                filtered_profiles.append(profile)
        except KeyError as e:
            st.error(f"Profile missing field: {e}")

    # Display Filtered Profiles
    if not filtered_profiles:
        st.warning("No profiles match the selected filters.")
        return

    st.markdown(
        """
        <style>
        .profile-box {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    for i, profile in enumerate(filtered_profiles):
        with (col1 if i % 2 == 0 else col2):
            profile_key = f"profile_{i}"  # Unique key for each profile's state

            # Initialize session state for profile visibility
            if profile_key not in st.session_state:
                st.session_state[profile_key] = False

            st.markdown(
                f"""
                <div class="profile-box">
                    <strong>Name:</strong> {profile.get('name', 'N/A')}<br>
                    <strong>City:</strong> {profile.get('city', 'N/A')}<br>
                    <strong>Area:</strong> {profile.get('area', 'N/A')}<br>
                    <strong>Budget:</strong> ${profile.get('budget', [0, 0])[0]} - ${profile.get('budget', [0, 0])[1]}<br>
                    <strong>Credit Score Verified:</strong> {"✅" if profile.get('credit_score_verified') else "❌"}<br>
                    <strong>Recommendation Verified:</strong> {"✅" if profile.get('landlord_recommendation', {}).get('recommendation_verified') else "❌"}<br>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Toggle View Profile
            if st.button(f"View Profile: {profile['name']}", key=f"view_profile_{i}"):
                st.session_state[profile_key] = not st.session_state[profile_key]

            # Display full profile if toggled on
            if st.session_state[profile_key]:
                render_profile_preview(profile)



# Verify Recommendations
def verify_recommendations():
    st.subheader("📄 Verify Recommendations")
    profiles = load_profiles()

    pending_recommendations = [p for p in profiles if not p["landlord_recommendation"]["recommendation_verified"]]

    if not pending_recommendations:
        st.success("All recommendations have been verified!")
        return

    for i, profile in enumerate(pending_recommendations):
        st.markdown(f"### {profile['name']}")
        st.markdown(f"- **Landlord Name:** {profile['landlord_recommendation']['landlord_name']}")
        st.markdown(f"- **Landlord Email:** {profile['landlord_recommendation']['landlord_email']}")
        st.markdown(f"- **Landlord Phone:** {profile['landlord_recommendation']['landlord_phone']}")

        if st.button(f"Open Recommendation Form: {profile['name']}", key=f"open_form_{i}"):
            with st.form(f"landlord_form_{i}"):
                on_time_payment = st.radio("Did the tenant pay rent on time?", ["Yes", "No"], key=f"on_time_{i}")
                utilities_payment = st.radio("Did the tenant pay utility bills on time?", ["Yes", "No"], key=f"utilities_{i}")
                property_condition = st.radio("Did the tenant maintain the property well?", ["Yes", "No"], key=f"property_{i}")
                noise_complaints = st.radio("Were there noise or behavioral complaints?", ["No", "Yes"], key=f"noise_{i}")
                would_recommend = st.radio("Would you recommend this tenant to other landlords?", ["Yes", "No"], key=f"recommend_{i}")
                additional_comments = st.text_area("Additional Comments (Optional)", key=f"comments_{i}")

                submitted = st.form_submit_button("Save Form")
                if submitted:
                    st.success("Form saved successfully!")
                    profile["landlord_recommendation"]["recommendation_verified"] = True
                    save_profile_to_file(profile)


# Navigation Logic
# Navigation Logic
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"

if st.session_state["current_page"] == "landing":
    landing_page()
elif st.session_state["current_page"] == "signup":
    signup_page()
elif st.session_state["current_page"] == "login":
    login_page()
elif st.session_state["current_page"] == "dashboard":
    dashboard_page()
elif st.session_state["current_page"] == "home":
    if st.session_state["user_type"] == "renter":
        renter_profile()
    elif st.session_state["user_type"] == "landlord_agent":
        landlord_agent_page()




