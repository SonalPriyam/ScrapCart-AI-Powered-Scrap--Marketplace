import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium
from data_store import scrap_listings, offers, chats
from ml_modules.image_classifier import predict_scrap_type
from ml_modules.price_predictor import predict_price
from ml_modules.image_quality import is_image_blurry
from ml_modules.image_captioning import generate_image_caption
from ml_modules.map_insights import compute_clusters, extract_lat_lon

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

def show_map_insights():
    st.subheader("Geographical Scrap Hotspots")
    locs = extract_lat_lon(scrap_listings)
    labels, centers = compute_clusters(scrap_listings, n_clusters=5)
    m = folium.Map(location=[22.5937, 78.9629], zoom_start=5)

    # Plot listing locations
    for idx, (lat, lon) in enumerate(locs):
        folium.CircleMarker([lat, lon], radius=3, color='blue').add_to(m)

    # Plot cluster centers as red "Hotspots"
    for idx, (clat, clon) in enumerate(centers):
        folium.Marker([clat, clon], icon=folium.Icon(color='red', icon='star'),
                      popup=f"Hotspot #{idx+1}").add_to(m)
    # Optional: Draw Heatmap
    try:
        from folium.plugins import HeatMap
        HeatMap(locs, radius=15).add_to(m)
    except Exception:
        pass

    st_folium(m, width=900, height=500)
    st.info("Red stars = cluster centers (hotspots). Blue dots = listings.")

def seller_dashboard(username):
    st.header(f"Dashboard for Seller: {username}")
    user_listings = [l for l in scrap_listings if l['seller'] == username]
    for listing in user_listings:
        render_listing_card(listing)
    user_offers = [o for o in offers if o['seller'] == username]
    st.write(f"Total Listings: {len(user_listings)}")
    st.write(f"Total Offers Received: {len(user_offers)}")

    # --- Fixed: Correct use of st.columns context managers ---
    if "show_map" not in st.session_state:
        st.session_state["show_map"] = False

    cols = st.columns([1, 1])
    # Use individual columns as context managers -- FIXED
    with cols[0]:
        if st.button("Show Map Insights"):
            st.session_state["show_map"] = True
    with cols[1]:
        if st.session_state["show_map"]:
            if st.button("Hide Map Insights"):
                st.session_state["show_map"] = False

    if st.session_state["show_map"]:
        show_map_insights()

def add_listing(username):
    st.header(f"Add Listing - Seller: {username}")
    uploaded_file = st.file_uploader("Upload Scrap Photo", type=["png", "jpg", "jpeg"])

    auto_description = ""
    # --- Image Quality Check ---
    if uploaded_file is not None:
        try:
            blurry, sharpness = is_image_blurry(uploaded_file, threshold=100.0)
            if blurry:
                st.warning(f"⚠️ The uploaded image seems blurry (sharpness score {sharpness:.2f}). Consider using a clearer photo!")
            else:
                st.success(f"✅ Image looks clear (sharpness score {sharpness:.2f}).")
        except Exception as e:
            st.error(f"Error checking image quality: {e}")

        # --- Automated Scrap Type Prediction ---
        try:
            predicted_type = predict_scrap_type(uploaded_file)
            st.info(f"AI Suggests Scrap Type: {predicted_type}")
        except Exception as e:
            predicted_type = None
            st.error(f"Prediction error: {e}")

        # --- Automated Description (Image Captioning) ---
        try:
            auto_description = generate_image_caption(uploaded_file)
            st.info(f"AI-generated description: {auto_description}")
        except Exception as e:
            st.error(f"Image captioning error: {e}")
    else:
        predicted_type = None

    scrap_type_options = ["Clothes", "e waste", "Glass", "metal", "others", "paper", "plastic"]
    scrap_type = st.selectbox(
        "Scrap Type", scrap_type_options,
        index=scrap_type_options.index(predicted_type)
        if predicted_type in scrap_type_options else 0
    )
    description = st.text_area("Description", value=auto_description)
    quantity = st.number_input("Quantity (kg)", min_value=1)
    condition = st.selectbox("Condition", ["New", "Used", "Recyclable", "Damaged", "Other"])
    contact = st.text_input("Mobile Number for Contact")
    date_posted = st.date_input("Date of Posting", value=datetime.date.today())
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Ahmedabad", "Lucknow", "Jaipur"]
    city = st.selectbox("City (location for recommended price)", cities)

    st.subheader("Optional: Select Location on Map")
    m = folium.Map(location=[22.5937, 78.9629], zoom_start=6)
    map_data = st_folium(m, width=700, height=400)

    location = None
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        location = f"{lat},{lon}"
        st.success(f"Selected Location: Latitude {lat:.5f}, Longitude {lon:.5f}")
    else:
        location = city

    # ---- Smart Price Recommendation ----
    if scrap_type and quantity and city and condition:
        recommended_price = predict_price(scrap_type, quantity, city, condition)
        st.info(f"💡 Recommended Price: ₹{recommended_price} per kg (AI market estimate)")
    expected_price = st.number_input("Expected Price (per kg)", min_value=0.0, format="%.2f")

    if st.button("Submit Listing"):
        if not contact.strip():
            st.error("Please enter your contact mobile number.")
        elif not uploaded_file:
            st.error("Please upload a scrap photo.")
        elif not description.strip():
            st.error("Please provide a description.")
        elif quantity <= 0:
            st.error("Quantity must be greater than zero.")
        elif not location:
            st.error("Please select or enter a location.")
        elif not scrap_type:
            st.error("Please select a scrap type.")
        else:
            image_url = f"https://picsum.photos/seed/{contact}{quantity}/300/210"
            scrap_listings.append({
                "seller": username,
                "image_url": image_url,
                "scrap_type": scrap_type,
                "description": description,
                "quantity": quantity,
                "location": location,
                "condition": condition,
                "expected_price": expected_price,
                "contact": contact,
                "date_posted": date_posted
            })
            st.success("Scrap listing submitted!")

def view_offers(username):
    st.header(f"View Offers - Seller: {username}")
    seller_offers = [o for o in offers if o['seller'] == username]
    if not seller_offers:
        st.info("No offers yet.")
    else:
        for i, offer in enumerate(seller_offers):
            st.write(
                f"Offer #{i+1}: Buyer `{offer['buyer']}` offered **{offer['offer_price']}** on listing #{offer['listing_idx']} | Status: {offer.get('status','Pending')}"
            )

def seller_chat(username):
    st.header(f"Chat - Seller: {username}")
    seller_chat_keys = [key for key in chats.keys() if key[2] == username]
    if not seller_chat_keys:
        st.info("No chat threads.")
    else:
        for chat_key in seller_chat_keys:
            listing_idx, buyer, _ = chat_key
            st.subheader(f"Chat with Buyer {buyer} for listing #{listing_idx}")
            chat_history = chats[chat_key]
            for msg in chat_history:
                st.write(f"{msg['sender']}: {msg['text']}")
            reply_key = f"reply_{listing_idx}_{buyer}"
            seller_reply = st.text_input("Your reply", key=reply_key)
            if st.button(
                f"Send Reply to {buyer} (listing {listing_idx})",
                key=f"send_reply_{listing_idx}_{buyer}"
            ):
                if seller_reply.strip():
                    chat_history.append({"sender": username, "text": seller_reply.strip()})
                    st.success("Reply sent!")
                    st.experimental_rerun()

def seller_page(username, page):
    if page == "Dashboard":
        seller_dashboard(username)
    elif page == "Add Listing":
        add_listing(username)
    elif page == "View Offers":
        view_offers(username)
    elif page == "Chat":
        seller_chat(username)
    else:
        st.write("Invalid option")

