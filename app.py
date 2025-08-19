import streamlit as st

# set_page_config must be the very first Streamlit command in your script
st.set_page_config(
    page_title="Scrap Cart",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from auth import seller_registration, seller_login, buyer_registration, buyer_login
from seller import seller_page
from buyer import buyer_page

# Load external CSS styles
def local_css(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS immediately after page config, before any widgets
local_css("style.css")  # Make sure style.css is in the same folder

def show_login_page():
    st.markdown('<div class="main-login">', unsafe_allow_html=True)

    st.markdown('<div class="login-title">♻️ Scrap Cart</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">From Trash to Cash </div>', unsafe_allow_html=True)

    role = st.selectbox("Role:", ["Seller", "Buyer"])
    tab = st.radio("Authentication:", ["Login", "Register"])

    st.markdown("<hr>", unsafe_allow_html=True)

    if role == "Seller":
        if tab == "Login":
            st.subheader("👨‍🔧 Seller Login")
            username = st.text_input("Seller Username", help="Your unique seller username.")
            password = st.text_input("Seller Password", type="password", help="Enter a secure password.")
            login_btn = st.button("Log In", key="seller_login_btn")
            if login_btn:
                user = seller_login(username, password, caller_app=True)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_role = 'seller'
                    st.session_state.username = user
                    st.success("Welcome Seller! Redirecting...", icon="✅")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please check your information.", icon="❌")
        else:
            st.subheader("👨‍🔧 Seller Registration")
            username = st.text_input("Choose Seller Username")
            password = st.text_input("Choose Seller Password", type="password")
            email = st.text_input("Seller Email (optional)")
            reg_btn = st.button("Register", key="seller_reg_btn")
            if reg_btn:
                success = seller_registration(username, password, email, caller_app=True)
                if success:
                    st.success("Registration successful! Please login.", icon="✅")
                else:
                    st.error("Registration failed. Try a different username.", icon="❌")
    else:
        if tab == "Login":
            st.subheader("🧑‍💼 Buyer Login")
            username = st.text_input("Buyer Username", help="Your unique buyer username.")
            password = st.text_input("Buyer Password", type="password", help="Enter your buyer password.")
            login_btn = st.button("Log In", key="buyer_login_btn")
            if login_btn:
                user = buyer_login(username, password, caller_app=True)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_role = 'buyer'
                    st.session_state.username = user
                    st.success("Welcome Buyer! Redirecting...", icon="✅")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.", icon="❌")
        else:
            st.subheader("🧑‍💼 Buyer Registration")
            username = st.text_input("Choose Buyer Username")
            password = st.text_input("Choose Buyer Password", type="password")
            email = st.text_input("Buyer Email (optional)")
            reg_btn = st.button("Register", key="buyer_reg_btn")
            if reg_btn:
                success = buyer_registration(username, password, email, caller_app=True)
                if success:
                    st.success("Registration successful! Please login.", icon="✅")
                else:
                    st.error("Registration failed. Try a different username.", icon="❌")

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        show_login_page()
    else:
        st.sidebar.image(
            "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
            width=120,
        )
        st.sidebar.markdown('<div class="sidebar-title">Scrap Marketplace</div>', unsafe_allow_html=True)
        st.sidebar.markdown("---")
        if st.session_state.user_role == 'seller':
            st.sidebar.subheader(f"👋 Hello, {st.session_state.username}")
            menu = st.sidebar.radio(
                "Seller Menu",
                [
                    "🏠 Dashboard",
                    "➕ Add Listing",
                    "💸 View Offers",
                    "💬 Chat",
                    "🚪 Logout"
                ],
            )
            if menu == "🚪 Logout":
                if st.sidebar.button("Confirm Logout", key="seller_logout"):
                    st.session_state.logged_in = False
                    st.session_state.user_role = None
                    st.session_state.username = ""
                    st.rerun()
            else:
                seller_page(
                    st.session_state.username,
                    menu.replace("🏠 ", "").replace("➕ ", "").replace("💸 ", "").replace("💬 ", "")
                )
        elif st.session_state.user_role == 'buyer':
            st.sidebar.subheader(f"👋 Welcome, {st.session_state.username}")
            menu = st.sidebar.radio(
                "Buyer Menu",
                [
                    "🔎 Browse Listings",
                    "⭐ Favorites",
                    "💸 Offers Made",
                    "💬 Chat",
                    "🚪 Logout"
                ],
            )
            if menu == "🚪 Logout":
                if st.sidebar.button("Confirm Logout", key="buyer_logout"):
                    st.session_state.logged_in = False
                    st.session_state.user_role = None
                    st.session_state.username = ""
                    st.rerun()
            else:
                buyer_page(st.session_state.username)
        st.markdown(
            f"<div class='main-dashboard'><h2 class='dashboard-title'>{st.session_state.user_role.capitalize()} Dashboard</h2><hr></div>",
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()

