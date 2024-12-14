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

# File to store profiles
PROFILE_FILE = "profiles.json"

# Helper function to load profiles
def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as file:
            return json.load(file)
    return []

# Helper function to save profiles
def save_profile_to_file(profile):
    profiles = load_profiles()
    profiles.append(profile)
    with open(PROFILE_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

# Helper function to reset the profile saved state
def reset_profile_saved_state():
    st.session_state["profile_saved"] = False
    st.session_state["saved_profile"] = {}

# Landing Page
def landing_page():
    st.title("Welcome to RentEasy!")
    st.subheader("A platform to connect renters with landlords and real estate agents.")

    st.write("""
    ### Choose your role:
    - Are you looking to rent a property? Select **Renter**.
    - Are you a landlord or real estate agent? Select **Landlord/Agent**.
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("I am a Renter"):
            st.session_state["user_type"] = "renter"

    with col2:
        if st.button("I am a Landlord/Real Estate Agent"):
            st.session_state["user_type"] = "landlord_agent"

# Renter's Profile Setup
def renter_profile():
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
        st.write(f"**Landlord Name:** {landlord_name}")
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
        if not name or not email:
            st.error("Please fill out all required fields.")
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
        st.markdown("## 🎉 Profile Preview")
        st.json(st.session_state["saved_profile"])

# Landlord/Agent Placeholder Page
def landlord_agent_page():
    st.title("Landlord/Agent Page")
    st.write("This section is under construction. Stay tuned!")

# Navigation Logic
if st.session_state["user_type"] is None:
    landing_page()
elif st.session_state["user_type"] == "renter":
    renter_profile()
elif st.session_state["user_type"] == "landlord_agent":
    landlord_agent_page()

# Sidebar Reset
st.sidebar.title("Navigation")
if st.sidebar.button("Go Back to Home"):
    st.session_state["user_type"] = None
    reset_profile_saved_state()







