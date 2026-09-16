import streamlit as st
import requests

st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Solar PV Designer Pro Africa")
st.markdown("Professional solar system design for Africa")
st.markdown("---")

# Use localhost for local testing
API_URL = "http://localhost:8000/api"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Sidebar
with st.sidebar:
    st.title("☀️ Menu")
    
    if st.session_state.authenticated:
        st.success(f"Logged in as: {st.session_state.user_email}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user_email = None
            st.rerun()
    else:
        st.info("Please login or register")

# Main app
if not st.session_state.authenticated:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={"email": login_email, "password": login_password},
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    st.session_state.user_email = login_email
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is it running on http://localhost:8000?")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("Create new account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_country = st.text_input("Country", key="reg_country", value="Uganda")
        
        if st.button("Register", type="primary"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "email": reg_email,
                        "password": reg_password,
                        "full_name": reg_name,
                        "country": reg_country
                    },
                    timeout=10
                )
                
                if response.status_code == 201:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is it running on http://localhost:8000?")
            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    # Logged in - show main app
    st.markdown("### Welcome to your Solar Design Dashboard")
    
    nav = st.radio("Navigate", ["New Design", "Quick Calculator"], horizontal=True)
    
    if nav == "New Design":
        st.header("Create New Solar System Design")
        
        with st.form("design_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name", "Home Solar System")
                location_name = st.text_input("Location", "Kampala, Uganda")
                daily_consumption = st.number_input("Daily Consumption (kWh)", min_value=1.0, value=10.0, step=1.0)
                system_type = st.selectbox("System Type", ["hybrid", "standalone", "grid"])
            
            with col2:
                peak_sun_hours = st.number_input("Peak Sun Hours", min_value=1.0, value=5.4, step=0.1)
                autonomy_days = st.number_input("Battery Autonomy (days)", min_value=1.0, value=2.0, step=0.5)
            
            submitted = st.form_submit_button("Calculate Design", type="primary")
            
            if submitted:
                try:
                    calc_response = requests.post(
                        f"{API_URL}/calculations/design",
                        params={
                            "daily_consumption_kwh": daily_consumption,
                            "peak_sun_hours": peak_sun_hours,
                            "peak_load_kw": daily_consumption / 4,
                            "system_type": system_type,
                            "autonomy_days": autonomy_days,
                        },
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        timeout=10
                    )
                    
                    if calc_response.status_code == 200:
                        design = calc_response.json()
                        
                        st.success("✅ Design calculated successfully!")
                        
                        # PV System
                        st.subheader("🔆 PV System")
                        pv = design["pv_system"]
                        col1, col2, col3 = st.columns(3)
                        col1.metric("PV Capacity", f"{pv['pv_capacity_kw']} kW")
                        col2.metric("Number of Panels", f"{pv['num_pv_panels']} units")
                        col3.metric("Daily Production", f"{pv['daily_production_kwh']} kWh")
                        
                        # Battery System
                        st.subheader("🔋 Battery Storage")
                        batt = design["battery_system"]
                        col1, col2 = st.columns(2)
                        col1.metric("Battery Capacity", f"{batt['battery_capacity_kwh']} kWh")
                        col2.metric("Battery Voltage", f"{batt['battery_voltage']} V")
                        
                        # Financial Analysis
                        st.subheader("💰 Financial Analysis")
                        fin = design["financial_analysis"]
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Cost", f"${fin['total_system_cost']:,.2f}")
                        col2.metric("Monthly Savings", f"${fin['monthly_savings']:,.2f}")
                        col3.metric("Payback Period", f"{fin['payback_period_years']} years")
                        
                    else:
                        st.error(f"Calculation failed: {calc_response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Is it running?")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif nav == "Quick Calculator":
        st.header("Quick Solar Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            daily_kwh = st.number_input("Daily Energy (kWh)", 1.0, 100.0, 10.0)
            sun_hours = st.number_input("Peak Sun Hours", 3.0, 7.0, 5.5, 0.1)
        
        with col2:
            peak_kw = st.number_input("Peak Load (kW)", 0.5, 20.0, 2.5)
            system_type = st.selectbox("System Type", ["hybrid", "standalone",
