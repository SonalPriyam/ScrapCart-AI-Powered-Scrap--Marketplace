# data_store.py

# ---- Scrap Listings ----
# For demo, listings use placeholder images from picsum.photos.
# In production, replace image_url with paths to uploaded images, or URLs to images hosted on cloud storage.

scrap_listings = []

# ---- Offers ----
offers = [
    # Example offer dictionary:
    # {
    #     'buyer': 'buyer1',
    #     'seller': 'eco_seller',
    #     'listing_idx': 1,
    #     'offer_price': 14,
    #     'status': 'Pending'
    # }
]

# ---- Chats ----
# Key is (listing_idx, buyer, seller), value is list of messages
chats = {
    # Example:
    # (1, 'buyer1', 'eco_seller'): [{'sender': 'buyer1', 'text': 'Hi, is the plastic still available?'}]
}
