import streamlit as st
from streamlit_folium import st_folium
import folium
from data_store import scrap_listings
from ml_modules.image_classifier import predict_scrap_type

def render_listing_card(listing):
    color_map = {
        "metal": "#d35400",
        "plastic": "#2980b9",
        "paper": "#27ae60",
        "glass": "#16a085",
        "clothes": "#5e6a92",
        "e waste": "#6610f2",
        "others": "#34495e"
    }
    type_color = color_map.get(listing.get("scrap_type", "").lower(), "#9b59b6")
    whatsapp_link = f"https://wa.me/{listing['contact']}?text=I'm%20interested%20in%20your%20scrap%20listing"
    st.markdown(
        f"""
        <div style='background:rgba(255,255,255,0.97); border-radius:15px; box-shadow:0 2px 14px #bcd0e6;
        padding:1.5rem 1.1rem; margin-bottom:1.2rem; border:1px solid #eee; position:relative;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div style='font-size:1.25rem;font-weight:700;color:{type_color};'>
                    <span style='margin-right:8px;'>🗂️</span>{listing['scrap_type']}
                </div>
                <div style='font-size:1rem;font-weight:500;padding:2px 11px;border-radius:6px;background-color:#f8f5fc;
                color:#344164;border:1px solid #e8dbf8;'>{listing['condition']}</div>
            </div>
            <div style='margin:10px 0;'>
                <img src='{listing['image_url']}' width='100%' style='border-radius:11px;border:1px solid #eaf3fc;
                box-shadow:0 1px 4px #dbe8f6;'/>
            </div>
            <div style='margin:0.4rem 0 0.8rem 0;color:#344164;'>{listing['description']}</div>
            <div style='margin-bottom:7px;'><b>Quantity:</b> {listing['quantity']} kg &nbsp; <b>Expected Price:</b> ₹{listing['expected_price']} /kg</div>
            <div style='margin-bottom:7px;'><b>Contact:</b> <a href='tel:{listing['contact']}' style='color:#4267b2;text-decoration:none;'>{listing['contact']}</a> | 
            <a href='{whatsapp_link}' target='_blank' style='color:#43d854;font-weight:500;margin-left:4px;text-decoration:none;'>WhatsApp</a></div>
        """,
        unsafe_allow_html=True
    )
    location = listing.get('location')
    if location and ',' in location:
        try:
            lat, lon = map(float, location.split(','))
            m = folium.Map(location=[lat, lon], zoom_start=13)
            folium.Marker([lat, lon], popup="Listing Location").add_to(m)
            st_folium(m, width=230, height=180)
        except Exception:
            st.info("Location info not available.")
    elif location:
        st.write(f"Location: {location}")
    st.markdown("</div>", unsafe_allow_html=True)

# -------- Recommendation System --------

def get_buyer_preferences(username):
    prefs = {
        "scrap_type": st.session_state.get("preferred_scrap_type"),
        "condition": st.session_state.get("preferred_condition"),
        "city": st.session_state.get("preferred_city")
    }
    return prefs

def score_listing_for_buyer(listing, prefs):
    score = 0
    if prefs.get("scrap_type") and listing.get("scrap_type") == prefs["scrap_type"]:
        score += 2
    if prefs.get("condition") and listing.get("condition") == prefs["condition"]:
        score += 1
    if prefs.get("city") and listing.get("location") == prefs["city"]:
        score += 2
    return score

def recommended_listings(username):
    prefs = get_buyer_preferences(username)
    scored = []
    for l in scrap_listings:
        s = score_listing_for_buyer(l, prefs)
        scored.append((s, l))
    recommended = [l for s, l in sorted(scored, reverse=True, key=lambda x: x[0])]
    return recommended

def browse_listings(username):
    st.header("Recommended Scrap Listings For You")

    # Buyer preference form
    with st.form("Set Buyer Preferences"):
        scrap_types = ["Metal", "Plastic", "Paper", "Glass", "Clothes", "E waste", "Others"]
        conditions = ["New", "Used", "Recyclable", "Damaged", "Other"]
        cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Ahmedabad", "Lucknow", "Jaipur"]
        preferred_scrap_type = st.selectbox("Preferred Type", scrap_types)
        preferred_condition = st.selectbox("Preferred Condition", conditions)
        preferred_city = st.selectbox("Preferred City", cities)
        if st.form_submit_button("Save Preferences"):
            st.session_state["preferred_scrap_type"] = preferred_scrap_type
            st.session_state["preferred_condition"] = preferred_condition
            st.session_state["preferred_city"] = preferred_city

    recs = recommended_listings(username)
    if not recs:
        st.info("No listings available right now.")
        return
    for listing in recs:
        render_listing_card(listing)

def buyer_page(username):
    browse_listings(username)
    # Future: add favorites, offers made, chat features


