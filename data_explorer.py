import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(
        page_title="Beverage Data Explorer",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Beverage Data Explorer")
    st.markdown("*Explore the training data and predictions*")
    
    try:
        conn = sqlite3.connect('beverage_data.db')
        
        # Sidebar for table selection
        st.sidebar.title("Data Selection")
        table = st.sidebar.selectbox("Select Table", ["Training Data", "Predictions"])
        
        if table == "Training Data":
            explore_training_data(conn)
        else:
            explore_predictions(conn)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Database error: {e}")
        st.info("Make sure to run the setup script first to create the database.")

def explore_training_data(conn):
    st.header("🎯 Training Data")
    
    # Load training data
    df = pd.read_sql_query("SELECT * FROM beverages", conn)
    
    if df.empty:
        st.warning("No training data found. Please run ml_classifier.py first.")
        return
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Samples", len(df))
    
    with col2:
        st.metric("Features", 8)
    
    with col3:
        st.metric("Quality Classes", df['quality_label'].nunique())
    
    with col4:
        avg_quality = df['quality'].mean()
        st.metric("Avg Quality Score", f"{avg_quality:.2f}")
    
    # Quality distribution
    st.subheader("📈 Quality Distribution")
    quality_counts = df['quality_label'].value_counts()
    fig = px.pie(values=quality_counts.values, names=quality_counts.index,
                 title="Distribution of Quality Labels")
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature distributions
    st.subheader("📊 Feature Distributions")
    
    feature_cols = ['sweetness', 'acidity', 'bitterness', 'carbonation',
                   'alcohol_content', 'temperature', 'clarity', 'aroma_intensity']
    
    selected_features = st.multiselect("Select features to visualize", 
                                     feature_cols, 
                                     default=['sweetness', 'acidity', 'bitterness', 'carbonation'])
    
    if selected_features:
        fig = go.Figure()
        
        for feature in selected_features:
            fig.add_trace(go.Histogram(x=df[feature], name=feature, alpha=0.7))
        
        fig.update_layout(title="Feature Distributions", 
                         xaxis_title="Value", 
                         yaxis_title="Frequency",
                         barmode='overlay')
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation matrix
    st.subheader("🔗 Feature Correlations")
    corr_matrix = df[feature_cols + ['quality']].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                   title="Feature Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)
    
    # Quality vs Features
    st.subheader("🎯 Quality vs Features")
    
    feature_to_plot = st.selectbox("Select feature to plot against quality", feature_cols)
    
    fig = px.box(df, x='quality_label', y=feature_to_plot,
                title=f"{feature_to_plot.title()} by Quality Level")
    st.plotly_chart(fig, use_container_width=True)
    
    # Raw data
    if st.checkbox("Show Raw Data"):
        st.subheader("📋 Raw Training Data")
        st.dataframe(df.drop(['id', 'created_at'], axis=1, errors='ignore'), use_container_width=True)

def explore_predictions(conn):
    st.header("🔮 Prediction History")
    
    # Load predictions
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    
    if df.empty:
        st.warning("No predictions found. Make some predictions using the main app first.")
        return
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(df))
    
    with col2:
        avg_confidence = df['confidence'].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.2%}")
    
    with col3:
        most_common = df['predicted_quality_label'].mode()[0]
        st.metric("Most Common", most_common)
    
    with col4:
        recent_predictions = len(df[df['created_at'] >= pd.Timestamp.now().date()])
        st.metric("Today's Predictions", recent_predictions)
    
    # Prediction distribution
    st.subheader("📈 Prediction Distribution")
    pred_counts = df['predicted_quality_label'].value_counts()
    fig = px.bar(x=pred_counts.index, y=pred_counts.values,
                title="Distribution of Predicted Quality Labels")
    fig.update_xaxis(title="Quality")
    fig.update_yaxis(title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    # Confidence distribution
    st.subheader("📊 Confidence Distribution")
    fig = px.histogram(df, x='confidence', bins=20,
                      title="Distribution of Prediction Confidence")
    fig.update_xaxis(title="Confidence")
    fig.update_yaxis(title="Frequency")
    st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("📅 Predictions Over Time")
    df['created_at'] = pd.to_datetime(df['created_at'])
    daily_predictions = df.groupby(df['created_at'].dt.date).size().reset_index()
    daily_predictions.columns = ['Date', 'Count']
    
    fig = px.line(daily_predictions, x='Date', y='Count',
                 title="Predictions Per Day")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent predictions
    st.subheader("🕒 Recent Predictions")
    recent_df = df.sort_values('created_at', ascending=False).head(10)
    
    # Format for display
    display_df = recent_df[['sweetness', 'acidity', 'bitterness', 'carbonation',
                           'predicted_quality_label', 'confidence', 'created_at']].copy()
    display_df['confidence'] = display_df['confidence'].apply(lambda x: f"{x:.2%}")
    display_df.columns = ['Sweetness', 'Acidity', 'Bitterness', 'Carbonation',
                         'Predicted Quality', 'Confidence', 'Timestamp']
    
    st.dataframe(display_df, use_container_width=True)

if __name__ == "__main__":
    main()
