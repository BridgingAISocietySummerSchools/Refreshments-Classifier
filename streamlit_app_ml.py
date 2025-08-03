import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import json

# API Configuration
API_BASE_URL = "http://localhost:8000"

def get_feature_info():
    """Get feature information from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/feature-info")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to get feature information from API")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Please make sure the API server is running.")
        return None

def predict_quality(features):
    """Make prediction using the API"""
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=features)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Prediction failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Please make sure the API server is running.")
        return None

def get_database_stats():
    """Get statistics from the database"""
    try:
        conn = sqlite3.connect('beverage_data.db')
        
        # Get total beverages
        total_beverages = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM beverages", conn
        ).iloc[0]['count']
        
        # Get total predictions
        total_predictions = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM predictions", conn
        ).iloc[0]['count']
        
        # Get quality distribution
        quality_dist = pd.read_sql_query(
            "SELECT quality_label, COUNT(*) as count FROM beverages GROUP BY quality_label", 
            conn
        )
        
        conn.close()
        return total_beverages, total_predictions, quality_dist
    except Exception as e:
        st.error(f"Database error: {e}")
        return 0, 0, pd.DataFrame()

def create_quality_distribution_chart(quality_dist):
    """Create a pie chart for quality distribution"""
    if not quality_dist.empty:
        fig = px.pie(
            quality_dist, 
            values='count', 
            names='quality_label',
            title="Beverage Quality Distribution in Database"
        )
        return fig
    return None

def create_feature_radar_chart(features):
    """Create a radar chart for feature visualization"""
    feature_names = list(features.keys())
    feature_values = list(features.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=feature_values,
        theta=feature_names,
        fill='toself',
        name='Beverage Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Beverage Feature Profile"
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Beverage Quality Classifier",
        page_icon="🥤",
        layout="wide"
    )
    
    st.title("🥤 Beverage Quality Classifier")
    st.markdown("*Classify the quality of beverages based on their characteristics*")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Classifier", "Database Stats", "About"])
    
    if page == "Classifier":
        classifier_page()
    elif page == "Database Stats":
        database_stats_page()
    else:
        about_page()

def classifier_page():
    st.header("🔬 Beverage Quality Classifier")
    
    # Get feature information
    feature_info = get_feature_info()
    if feature_info is None:
        st.stop()
    
    features = feature_info['features']
    
    st.markdown("### Enter Beverage Characteristics")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    input_features = {}
    
    with col1:
        st.subheader("Taste Profile")
        input_features['sweetness'] = st.slider(
            "Sweetness", 
            min_value=0.0, 
            max_value=10.0, 
            value=5.0, 
            step=0.1,
            help="How sweet is the beverage? (0 = not sweet, 10 = very sweet)"
        )
        
        input_features['acidity'] = st.slider(
            "Acidity", 
            min_value=0.0, 
            max_value=10.0, 
            value=5.0, 
            step=0.1,
            help="How acidic is the beverage? (0 = not acidic, 10 = very acidic)"
        )
        
        input_features['bitterness'] = st.slider(
            "Bitterness", 
            min_value=0.0, 
            max_value=10.0, 
            value=5.0, 
            step=0.1,
            help="How bitter is the beverage? (0 = not bitter, 10 = very bitter)"
        )
        
        input_features['carbonation'] = st.slider(
            "Carbonation", 
            min_value=0.0, 
            max_value=10.0, 
            value=5.0, 
            step=0.1,
            help="How carbonated is the beverage? (0 = flat, 10 = very fizzy)"
        )
    
    with col2:
        st.subheader("Physical Properties")
        input_features['alcohol_content'] = st.slider(
            "Alcohol Content (%)", 
            min_value=0.0, 
            max_value=15.0, 
            value=0.0, 
            step=0.1,
            help="Alcohol percentage by volume"
        )
        
        input_features['temperature'] = st.slider(
            "Temperature (°C)", 
            min_value=0.0, 
            max_value=25.0, 
            value=4.0, 
            step=0.1,
            help="Serving temperature in Celsius"
        )
        
        input_features['clarity'] = st.slider(
            "Clarity", 
            min_value=0.0, 
            max_value=10.0, 
            value=8.0, 
            step=0.1,
            help="How clear is the beverage? (0 = very cloudy, 10 = crystal clear)"
        )
        
        input_features['aroma_intensity'] = st.slider(
            "Aroma Intensity", 
            min_value=0.0, 
            max_value=10.0, 
            value=5.0, 
            step=0.1,
            help="How strong is the aroma? (0 = no aroma, 10 = very strong)"
        )
    
    # Feature visualization
    st.markdown("### Feature Profile Visualization")
    radar_chart = create_feature_radar_chart(input_features)
    st.plotly_chart(radar_chart, use_container_width=True)
    
    # Prediction button
    if st.button("🔮 Predict Quality", type="primary", use_container_width=True):
        with st.spinner("Analyzing beverage characteristics..."):
            prediction = predict_quality(input_features)
            
            if prediction:
                st.markdown("### 🎯 Prediction Results")
                
                # Create three columns for results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Quality", prediction['quality'])
                
                with col2:
                    confidence = prediction['confidence'] * 100
                    st.metric("Confidence", f"{confidence:.1f}%")
                
                with col3:
                    quality_score = prediction['quality_index'] + 1
                    st.metric("Quality Score", f"{quality_score}/4")
                
                # Probability distribution
                st.markdown("### 📊 Probability Distribution")
                prob_df = pd.DataFrame.from_dict(
                    prediction['probabilities'], 
                    orient='index', 
                    columns=['Probability']
                ).reset_index()
                prob_df.columns = ['Quality', 'Probability']
                
                fig = px.bar(
                    prob_df, 
                    x='Quality', 
                    y='Probability',
                    title="Probability of Each Quality Level",
                    color='Probability',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Quality interpretation
                quality = prediction['quality']
                if quality == "Excellent":
                    st.success("🌟 This beverage has excellent quality! It has a great balance of flavors and characteristics.")
                elif quality == "Good":
                    st.success("👍 This beverage has good quality! It's quite enjoyable with nice characteristics.")
                elif quality == "Fair":
                    st.warning("⚠️ This beverage has fair quality. It's acceptable but could be improved.")
                else:
                    st.error("❌ This beverage has poor quality. Consider adjusting the formulation.")

def database_stats_page():
    st.header("📊 Database Statistics")
    
    total_beverages, total_predictions, quality_dist = get_database_stats()
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Beverages in Database", total_beverages)
    
    with col2:
        st.metric("Total Predictions Made", total_predictions)
    
    with col3:
        if total_beverages > 0:
            st.metric("Database Status", "✅ Active")
        else:
            st.metric("Database Status", "❌ Empty")
    
    # Quality distribution chart
    if not quality_dist.empty:
        st.markdown("### Quality Distribution")
        quality_chart = create_quality_distribution_chart(quality_dist)
        st.plotly_chart(quality_chart, use_container_width=True)
        
        # Show detailed table
        st.markdown("### Detailed Statistics")
        st.dataframe(quality_dist, use_container_width=True)
    else:
        st.info("No data available in the database. Run the ML classifier training first.")

def about_page():
    st.header("ℹ️ About the Beverage Quality Classifier")
    
    st.markdown("""
    ## 🎯 Purpose
    This application uses machine learning to classify the quality of beverages based on their characteristics.
    
    ## 🔬 Features Analyzed
    - **Sweetness**: The sweetness level of the beverage
    - **Acidity**: The acidity level 
    - **Bitterness**: The bitterness level
    - **Carbonation**: The carbonation level
    - **Alcohol Content**: Percentage of alcohol by volume
    - **Temperature**: Serving temperature in Celsius
    - **Clarity**: How clear/transparent the beverage is
    - **Aroma Intensity**: Strength of the beverage's aroma
    
    ## 🏆 Quality Classifications
    - **Poor**: Below average quality, needs improvement
    - **Fair**: Acceptable quality, some room for improvement
    - **Good**: Above average quality, quite enjoyable
    - **Excellent**: Outstanding quality, exceptional characteristics
    
    ## 🤖 Machine Learning Model
    The classifier uses a Random Forest algorithm trained on synthetic data that models realistic relationships 
    between beverage characteristics and quality ratings.
    
    ## 💾 Database
    All predictions and training data are stored in a SQLite database for analysis and continuous improvement.
    
    ## 🚀 How to Use
    1. Navigate to the "Classifier" page
    2. Adjust the sliders to match your beverage's characteristics
    3. Click "Predict Quality" to get the classification
    4. View the results including confidence levels and probability distribution
    
    ## 🔧 Technical Stack
    - **Frontend**: Streamlit
    - **Backend**: FastAPI
    - **ML Framework**: Scikit-learn
    - **Database**: SQLite
    - **Visualization**: Plotly
    """)

if __name__ == "__main__":
    main()
