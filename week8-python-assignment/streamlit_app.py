"""
COVID-19 Research Analytics Dashboard

A comprehensive Streamlit application for analyzing COVID-19 research publications.
This dashboard provides interactive visualizations and statistical insights on:
- Publication trends over time
- Journal distribution analysis  
- Word frequency analysis of paper titles
- Data quality assessment
- Research collaboration patterns

Author: COVID-19 Research Analytics Team
Dataset: CORD-19 Research Challenge (Kaggle)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page settings for optimal user experience
st.set_page_config(
    page_title="COVID-19 Research Analytics Dashboard",
    page_icon="🔬",
    layout="wide",  # Use full width of the screen
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# Custom CSS styling for enhanced visual appeal and user experience
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    /* Sub-section headers */
    .sub-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin: 1rem 0;
    }
    /* Metric cards for displaying key statistics */
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    /* Information boxes for important notifications */
    .info-box {
        background-color: #222222;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """
    Load and cache the COVID-19 research dataset
    
    This function attempts to load datasets in priority order:
    1. metadata_prepared.csv (fully processed with additional features)
    2. metadata_cleaned.csv (cleaned data with missing values handled)
    3. metadata.csv (original raw dataset)
    4. metadata_sample.csv (sample dataset for testing)
    
    Returns:
        tuple: (DataFrame, str) - The loaded dataset and its type
    """
    try:
        # Priority 1: Try to load the prepared dataset (best option)
        if st.session_state.get('use_prepared', True):
            try:
                df = pd.read_csv('metadata_prepared.csv')
                return df, "prepared"
            except FileNotFoundError:
                pass
        
        # Priority 2: Try to load the cleaned dataset
        try:
            df = pd.read_csv('metadata_cleaned.csv')
            return df, "cleaned"
        except FileNotFoundError:
            pass
        
        # Priority 3: Try to load the original dataset
        try:
            df = pd.read_csv('metadata.csv')
            return df, "original"
        except FileNotFoundError:
            pass
            
        # Priority 4: Try to load the sample dataset (for GitHub testing)
        try:
            df = pd.read_csv('metadata_sample.csv')
            return df, "sample"
        except FileNotFoundError:
            pass
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def clean_text_for_wordcloud(text_series):
    """
    Clean and preprocess text data for word cloud generation
    
    This function performs several text cleaning operations:
    - Removes special characters and numbers
    - Converts to lowercase
    - Removes common stop words
    - Filters out COVID-19 related terms to focus on research topics
    
    Args:
        text_series (pd.Series): Series containing text data (paper titles)
        
    Returns:
        str: Cleaned text ready for word cloud generation
    """
    # Combine all text into a single string
    all_text = ' '.join(text_series.dropna().astype(str))
    
    # Remove special characters and numbers, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', all_text)
    text = text.lower()
    
    # Define comprehensive stop words list
    # Including common English words and COVID-19 specific terms
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
                 'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was', 
                 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
                 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
                 'a', 'an', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
                 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
                 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                 # COVID-19 specific terms to exclude for better topic diversity
                 'covid', 'coronavirus', 'pandemic', 'virus', 'disease', 'infection'}
    
    # Filter words: remove stop words and keep only words longer than 2 characters
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word) > 2]
    return ' '.join(words)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🔬 COVID-19 Research Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h4>📊 Interactive Analysis Platform</h4>
    <p>Explore and analyze COVID-19 research publications with interactive visualizations and statistical insights. 
    This dashboard provides comprehensive analytics on publication trends, journal distributions, research patterns, and more.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading dataset... This may take a moment for large files."):
        df, data_type = load_data()
    
    if df is None:
        st.error("❌ Could not load any dataset. Please ensure metadata.csv exists in the project directory.")
        return
    
    # Data info sidebar
    st.sidebar.markdown("## 📋 Dataset Information")
    st.sidebar.info(f"**Dataset Type:** {data_type.title()}")
    st.sidebar.metric("Total Records", f"{len(df):,}")
    st.sidebar.metric("Total Columns", f"{len(df.columns)}")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2
    st.sidebar.metric("Memory Usage", f"{memory_usage:.1f} MB")
    
    # Data quality indicator
    if 'data_completeness_score' in df.columns:
        avg_completeness = df['data_completeness_score'].mean()
        st.sidebar.metric("Avg Data Quality", f"{avg_completeness:.1f}%")
    
    # Sidebar controls
    st.sidebar.markdown("## ⚙️ Control Panel")
    
    # Date range filter
    if 'publish_time_year' in df.columns:
        year_col = df['publish_time_year'].dropna()
        if len(year_col) > 0:
            min_year, max_year = int(year_col.min()), int(year_col.max())
            year_range = st.sidebar.slider(
                "📅 Publication Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(max(min_year, 2000), max_year),
                step=1
            )
            
            # Filter data by year
            df_filtered = df[
                (df['publish_time_year'].isna()) | 
                ((df['publish_time_year'] >= year_range[0]) & (df['publish_time_year'] <= year_range[1]))
            ]
        else:
            df_filtered = df
            year_range = None
    else:
        df_filtered = df
        year_range = None
    
    # Journal filter
    if 'journal' in df.columns:
        top_journals = df['journal'].value_counts().head(20).index.tolist()
        selected_journals = st.sidebar.multiselect(
            "📚 Filter by Top Journals",
            options=["All Journals"] + top_journals,
            default=["All Journals"]
        )
        
        if "All Journals" not in selected_journals and selected_journals:
            df_filtered = df_filtered[df_filtered['journal'].isin(selected_journals)]
    
    # Source filter
    if 'source_x' in df.columns:
        sources = df['source_x'].unique().tolist()
        selected_sources = st.sidebar.multiselect(
            "🗂️ Filter by Data Source",
            options=["All Sources"] + sources,
            default=["All Sources"]
        )
        
        if "All Sources" not in selected_sources and selected_sources:
            df_filtered = df_filtered[df_filtered['source_x'].isin(selected_sources)]
    
    # Analysis options
    st.sidebar.markdown("## 🎛️ Analysis Options")
    show_top_n = st.sidebar.slider("📊 Top N items to display", 5, 20, 10)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Publications Over Time", "📚 Journal Analysis", "☁️ Word Cloud", "📄 Data Sample"])
    
    # Tab 1: Overview
    with tab1:
        st.markdown('<h2 class="sub-header">📊 Dataset Overview</h2>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📄 Total Papers",
                value=f"{len(df_filtered):,}",
                delta=f"{len(df_filtered) - len(df):,}" if len(df_filtered) != len(df) else None
            )
        
        with col2:
            if 'journal' in df_filtered.columns:
                unique_journals = df_filtered['journal'].nunique()
                st.metric("📚 Unique Journals", f"{unique_journals:,}")
            else:
                st.metric("📚 Unique Journals", "N/A")
        
        with col3:
            if 'abstract_word_count' in df_filtered.columns:
                avg_abstract_length = df_filtered[df_filtered['abstract_word_count'] > 0]['abstract_word_count'].mean()
                st.metric("📝 Avg Abstract Length", f"{avg_abstract_length:.0f} words" if not pd.isna(avg_abstract_length) else "N/A")
            else:
                st.metric("📝 Avg Abstract Length", "N/A")
        
        with col4:
            if 'author_count' in df_filtered.columns:
                avg_authors = df_filtered[df_filtered['author_count'] > 0]['author_count'].mean()
                st.metric("👥 Avg Authors/Paper", f"{avg_authors:.1f}" if not pd.isna(avg_authors) else "N/A")
            else:
                st.metric("👥 Avg Authors/Paper", "N/A")
        
        # Missing data overview
        if len(df_filtered) > 0:
            st.markdown("### 🔍 Data Completeness Analysis")
            
            # Calculate missing percentages
            missing_data = []
            important_cols = ['title', 'authors', 'abstract', 'journal', 'publish_time']
            existing_cols = [col for col in important_cols if col in df_filtered.columns]
            
            for col in existing_cols:
                missing_count = df_filtered[col].isnull().sum()
                missing_pct = (missing_count / len(df_filtered)) * 100
                missing_data.append({
                    'Column': col.title(),
                    'Missing Count': missing_count,
                    'Missing %': missing_pct,
                    'Complete %': 100 - missing_pct
                })
            
            if missing_data:
                missing_df = pd.DataFrame(missing_data)
                
                # Create completeness chart
                fig = px.bar(
                    missing_df, 
                    x='Column', 
                    y='Complete %',
                    title="Data Completeness by Column",
                    color='Complete %',
                    color_continuous_scale='RdYlGn',
                    text='Complete %'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Source distribution
        if 'source_x' in df_filtered.columns:
            st.markdown("### 🗂️ Data Source Distribution")
            source_counts = df_filtered['source_x'].value_counts()
            
            fig = px.pie(
                values=source_counts.values,
                names=source_counts.index,
                title="Distribution of Papers by Data Source"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Publications Over Time
    with tab2:
        st.markdown('<h2 class="sub-header">📈 Publication Trends Over Time</h2>', unsafe_allow_html=True)
        
        if 'publish_time_year' in df_filtered.columns:
            year_counts = df_filtered['publish_time_year'].value_counts().sort_index()
            year_counts = year_counts[year_counts.index >= 1980]  # Filter reasonable years
            
            if len(year_counts) > 0:
                # Time series plot
                fig = px.line(
                    x=year_counts.index,
                    y=year_counts.values,
                    title="Publications by Year",
                    labels={'x': 'Year', 'y': 'Number of Publications'}
                )
                fig.add_scatter(
                    x=year_counts.index,
                    y=year_counts.values,
                    mode='markers',
                    marker=dict(size=6, color='red'),
                    name='Data Points'
                )
                
                # Highlight COVID-19 period
                covid_years = year_counts[year_counts.index >= 2020]
                if len(covid_years) > 0:
                    fig.add_vrect(
                        x0=2019.5, x1=year_counts.index.max() + 0.5,
                        fillcolor="rgba(255,0,0,0.1)",
                        layer="below", line_width=0,
                        annotation_text="COVID-19 Period",
                        annotation_position="top left"
                    )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Peak Year", f"{int(year_counts.idxmax())}")
                with col2:
                    st.metric("Peak Publications", f"{year_counts.max():,}")
                with col3:
                    if len(covid_years) > 0:
                        covid_total = covid_years.sum()
                        st.metric("COVID-19 Era Papers", f"{covid_total:,}")
                
                # Monthly distribution if data available
                if 'publish_time_month' in df_filtered.columns:
                    st.markdown("### 📅 Publication Distribution by Month")
                    month_counts = df_filtered['publish_time_month'].value_counts().sort_index()
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    # Filter out NaN values and ensure integers
                    valid_months = []
                    valid_counts = []
                    valid_month_names = []
                    
                    for month_num in month_counts.index:
                        if pd.notna(month_num) and isinstance(month_num, (int, float)) and 1 <= month_num <= 12:
                            month_int = int(month_num)
                            valid_months.append(month_int)
                            valid_counts.append(month_counts[month_num])
                            valid_month_names.append(month_names[month_int - 1])
                    
                    if valid_months:
                        fig = px.bar(
                            x=valid_month_names,
                            y=valid_counts,
                            title="Publications by Month",
                            labels={'x': 'Month', 'y': 'Number of Publications'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No valid monthly data available for visualization.")
            else:
                st.warning("No valid publication years found in the filtered data.")
        else:
            st.warning("No publication date information available.")
    
    # Tab 3: Journal Analysis
    with tab3:
        st.markdown('<h2 class="sub-header">📚 Journal Publication Analysis</h2>', unsafe_allow_html=True)
        
        if 'journal' in df_filtered.columns:
            journal_counts = df_filtered['journal'].value_counts().head(show_top_n)
            
            if len(journal_counts) > 0:
                # Top journals bar chart
                fig = px.bar(
                    x=journal_counts.values,
                    y=[j[:50] + '...' if len(str(j)) > 50 else j for j in journal_counts.index],
                    orientation='h',
                    title=f"Top {show_top_n} Journals by Publication Count",
                    labels={'x': 'Number of Publications', 'y': 'Journal'}
                )
                fig.update_layout(height=max(400, show_top_n * 30))
                st.plotly_chart(fig, use_container_width=True)
                
                # Journal statistics
                total_journals = df_filtered['journal'].nunique()
                top_5_share = journal_counts.head(5).sum() / journal_counts.sum() * 100 if len(journal_counts) >= 5 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Journals", f"{total_journals:,}")
                with col2:
                    st.metric("Top Journal", journal_counts.iloc[0] if len(journal_counts) > 0 else 0)
                with col3:
                    st.metric("Top 5 Share", f"{top_5_share:.1f}%")
                
                # Journal productivity distribution
                if 'journal_productivity' in df_filtered.columns:
                    st.markdown("### 📊 Journal Productivity Categories")
                    productivity_counts = df_filtered['journal_productivity'].value_counts()
                    
                    fig = px.pie(
                        values=productivity_counts.values,
                        names=productivity_counts.index,
                        title="Journal Productivity Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No journal data found in the filtered dataset.")
        else:
            st.warning("No journal information available in the dataset.")
    
    # Tab 4: Word Cloud
    with tab4:
        st.markdown('<h2 class="sub-header">☁️ Title Word Analysis</h2>', unsafe_allow_html=True)
        
        if 'title' in df_filtered.columns:
            # Word cloud options
            max_words = st.slider("Maximum Words in Cloud", 50, 200, 100)
            
            try:
                # Clean text for word cloud
                cleaned_text = clean_text_for_wordcloud(df_filtered['title'])
                
                if cleaned_text:
                    # Generate word cloud
                    wordcloud = WordCloud(
                        width=800, 
                        height=400, 
                        background_color='white',
                        max_words=max_words,
                        colormap='viridis',
                        relative_scaling=0.5,
                        random_state=42
                    ).generate(cleaned_text)
                    
                    # Display word cloud
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title('Most Frequent Words in Paper Titles', fontsize=16, fontweight='bold')
                    st.pyplot(fig)
                    
                    # Word frequency analysis
                    st.markdown("### 📝 Top Words Analysis")
                    word_freq = Counter(cleaned_text.split())
                    top_words = word_freq.most_common(20)
                    
                    if top_words:
                        words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                        
                        fig = px.bar(
                            words_df.head(15),
                            x='Frequency',
                            y='Word',
                            orientation='h',
                            title="Top 15 Most Frequent Words",
                            color='Frequency',
                            color_continuous_scale='Blues'
                        )
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show top words table
                        st.markdown("#### 📊 Word Frequency Table")
                        st.dataframe(words_df.head(10), use_container_width=True)
                else:
                    st.warning("No text data available for word cloud generation.")
                    
            except Exception as e:
                st.error(f"Error generating word cloud: {e}")
                st.info("💡 Tip: Make sure the wordcloud package is installed: pip install wordcloud")
        else:
            st.warning("No title information available for word cloud analysis.")
    
    # Tab 5: Data Sample
    with tab5:
        st.markdown('<h2 class="sub-header">📄 Data Sample & Exploration</h2>', unsafe_allow_html=True)
        
        # Sample size selector
        sample_size = st.selectbox(
            "Select sample size to display:",
            [10, 25, 50, 100, 200]
        )
        
        # Column selector
        all_columns = df_filtered.columns.tolist()
        important_columns = ['cord_uid', 'title', 'authors', 'journal', 'abstract', 'publish_time']
        default_columns = [col for col in important_columns if col in all_columns]
        
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=all_columns,
            default=default_columns[:6] if len(default_columns) >= 6 else default_columns
        )
        
        if selected_columns:
            # Display sample
            st.markdown(f"### 📋 Sample of {sample_size} Records")
            sample_df = df_filtered[selected_columns].head(sample_size)
            st.dataframe(sample_df, use_container_width=True)
            
            # Download option
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Sample as CSV",
                data=csv,
                file_name=f"covid_research_sample_{sample_size}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Please select at least one column to display.")
        
        # Data summary
        st.markdown("### 📊 Column Information")
        
        # Create summary table
        summary_data = []
        for col in df_filtered.columns:
            dtype = str(df_filtered[col].dtype)
            non_null = df_filtered[col].count()
            null_count = df_filtered[col].isnull().sum()
            unique_count = df_filtered[col].nunique()
            
            summary_data.append({
                'Column': col,
                'Data Type': dtype,
                'Non-Null Count': f"{non_null:,}",
                'Null Count': f"{null_count:,}",
                'Unique Values': f"{unique_count:,}",
                'Sample Value': str(df_filtered[col].dropna().iloc[0]) if non_null > 0 else "N/A"
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>🔬 COVID-19 Research Analytics Dashboard | Built with Streamlit</p>
    <p>📊 Interactive data exploration and visualization platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()