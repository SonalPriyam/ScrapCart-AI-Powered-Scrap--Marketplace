# ScrapCart: AI-Powered Scrap Marketplace



## Overview

ScrapCart is a modern, AI-powered platform connecting sellers and merchants to turn waste materials into cash — all with smart automation, instant price prediction, and seamless pickup/payments.  
This project goes beyond traditional marketplace apps by integrating deep learning, NLP, computer vision, and interactive geospatial analytics for a truly next-gen experience.


## Features

- **AI Scrap Type Prediction**: Instantly classify scrap images using deep learning.
- **Image Quality & Captioning**: Automated blur detection and smart captions (BLIP Vision+NLP).
- **ML Price Prediction**: Data-driven price recommendations.
- **Personalized Buyer Recommendations**: Content-based matching based on user behavior.
- **Smart Map Insights**: Hotspot heatmaps and route planning for efficient scrap pickup.
- **Clean, Responsive UI/UX**: Modern landing page, styled listing cards, interactive forms.
- **Seller/Buyer Dashboards**: Manage listings, offers, and chat in real time.
- **Performance Optimized**: Streamlit caching for fast execution.

---

## Folder Structure

│
├── app.py # Main entry point
├── style.css # Custom themes
├── data_store.py # Global marketplace data
├── buyer.py # Buyer dashboard/logic
├── seller.py # Seller dashboard/logic
├── auth.py # Authentication/login
│
├── requirements.txt
│
├── ml_modules/ # All ML/DL/NLP modules
│ ├── image_classifier.py
│ ├── train_image_classifier.py
│ ├── image_quality.py
│ ├── image_captioning.py
│ ├── price_predictor.py
│ ├── map_insights.py
│ ├── generate_scrap_price_dataset.py
│ ├── price_model.pkl
│ ├── price_encoder.pkl
│ └── scrap_price_dataset.csv
│
├── saved_model/ # Additional trained models (if any)
├── dataset/ # Custom scrap images/data
└── venv/ # Python environment

## Technical Stack

- **Streamlit** (UI & dashboard)
- **scikit-learn** (Price prediction)
- **OpenCV, PIL** (Image processing)
- **Transformers (Hugging Face BLIP/BERT)** (Image captioning, NLP)
- **folium, streamlit-folium** (Mapping & clustering)
- **Joblib, Pandas, NumPy** (Data management)