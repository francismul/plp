"""
COVID-19 Research Data Analysis Pipeline

This comprehensive script provides a complete data analysis pipeline for the CORD-19 
COVID-19 research dataset from Kaggle. The pipeline includes:

1. Data Loading and Examination
2. Basic Data Exploration 
3. Missing Data Handling
4. Data Preparation for Analysis
5. Basic Statistical Analysis
6. Comprehensive Visualizations

Features:
- Handles large datasets (1M+ records)
- Intelligent missing data strategies
- Temporal analysis of publications
- Journal and author collaboration analysis
- Text analysis of paper titles and abstracts
- Publication quality visualizations

Dataset Source: 
- CORD-19 Research Challenge (Kaggle)
- URL: https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge
- Original size: 1,056,660 rows × 19 columns

Author: COVID-19 Research Analytics Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

def load_and_examine_dataset():
    """
    Load the COVID-19 research metadata and perform initial examination
    
    This function loads the metadata.csv file and provides comprehensive
    information about the dataset structure, including:
    - Dataset dimensions and memory usage
    - Column information and data types
    - Sample data preview
    - Missing values analysis
    - Basic statistics for numerical columns
    
    Returns:
        pandas.DataFrame: The loaded dataset, or None if loading fails
    """
    try:
        # Load the CSV file into a DataFrame
        print("Loading metadata.csv...")
        df = pd.read_csv('metadata.csv')
        
        print(f"Dataset loaded successfully!")
        print(f"Shape of the dataset: {df.shape}")
        print(f"Number of rows: {df.shape[0]:,}")
        print(f"Number of columns: {df.shape[1]}")
        print("\n" + "="*50)
        
        # Display basic information about the dataset
        print("DATASET INFO:")
        print("="*50)
        print(df.info())
        print("\n" + "="*50)
        
        # Display the first few rows
        print("FIRST 5 ROWS:")
        print("="*50)
        print(df.head())
        print("\n" + "="*50)
        
        # Display column names
        print("COLUMN NAMES:")
        print("="*50)
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
        print("\n" + "="*50)
        
        # Display data types
        print("DATA TYPES:")
        print("="*50)
        print(df.dtypes)
        print("\n" + "="*50)
        
        # Display basic statistics for numeric columns
        print("BASIC STATISTICS (Numeric columns):")
        print("="*50)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols].describe())
        else:
            print("No numeric columns found.")
        print("\n" + "="*50)
        
        # Check for missing values
        print("MISSING VALUES:")
        print("="*50)
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / len(df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing_values.index,
            'Missing Count': missing_values.values,
            'Missing Percentage': missing_percentage.values
        })
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        
        if len(missing_df) > 0:
            print(missing_df.to_string(index=False))
        else:
            print("No missing values found!")
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE!")
        
        return df
        
    except FileNotFoundError:
        print("Error: metadata.csv file not found in the current directory.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def basic_data_exploration(df):
    """
    Perform basic data exploration on the DataFrame
    """
    print("\n" + "="*60)
    print("BASIC DATA EXPLORATION")
    print("="*60)
    
    # 1. Check DataFrame dimensions
    print("1. DATAFRAME DIMENSIONS:")
    print("-" * 30)
    rows, cols = df.shape
    print(f"   • Total rows: {rows:,}")
    print(f"   • Total columns: {cols}")
    print(f"   • Total cells: {rows * cols:,}")
    print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 2. Identify data types
    print("\n2. DATA TYPES ANALYSIS:")
    print("-" * 30)
    dtype_counts = df.dtypes.value_counts()
    print("   Data type distribution:")
    for dtype, count in dtype_counts.items():
        print(f"   • {dtype}: {count} columns ({count/len(df.columns)*100:.1f}%)")
    
    print("\n   Detailed column types:")
    for i, (col, dtype) in enumerate(df.dtypes.items(), 1):
        print(f"   {i:2d}. {col:<20} → {dtype}")
    
    # 3. Check for missing values in important columns
    print("\n3. MISSING VALUES ANALYSIS:")
    print("-" * 30)
    
    # Define important columns (you can modify this based on your needs)
    important_columns = ['cord_uid', 'title', 'authors', 'abstract', 'publish_time', 
                        'journal', 'doi', 'url', 'source_x']
    
    # Check which important columns exist in the dataset
    existing_important_cols = [col for col in important_columns if col in df.columns]
    
    print(f"   Analyzing {len(existing_important_cols)} important columns:")
    
    missing_analysis = []
    for col in existing_important_cols:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_analysis.append({
            'Column': col,
            'Missing Count': missing_count,
            'Missing %': missing_pct,
            'Complete %': 100 - missing_pct
        })
    
    # Create DataFrame for better display
    missing_df = pd.DataFrame(missing_analysis)
    missing_df = missing_df.sort_values('Missing %', ascending=False)
    
    print("\n   Missing values in important columns:")
    for _, row in missing_df.iterrows():
        status = "⚠️  CRITICAL" if row['Missing %'] > 50 else "⚡ MODERATE" if row['Missing %'] > 10 else "✅ GOOD"
        print(f"   • {row['Column']:<15}: {row['Missing Count']:>8,} ({row['Missing %']:>5.1f}% missing) {status}")
    
    # Overall missing data summary
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    overall_missing_pct = (total_missing / total_cells) * 100
    
    print(f"\n   Overall missing data:")
    print(f"   • Total missing values: {total_missing:,}")
    print(f"   • Percentage of missing data: {overall_missing_pct:.2f}%")
    
    # 4. Generate basic statistics for numerical columns
    print("\n4. NUMERICAL COLUMNS STATISTICS:")
    print("-" * 30)
    
    # Identify numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 0:
        print(f"   Found {len(numeric_cols)} numerical column(s): {', '.join(numeric_cols)}")
        
        for col in numeric_cols:
            print(f"\n   📊 Statistics for '{col}':")
            
            # Check if column has any non-null values
            non_null_count = df[col].count()
            if non_null_count == 0:
                print(f"      ⚠️  Column is completely empty (no data)")
                continue
            
            # Basic statistics
            stats = df[col].describe()
            print(f"      • Count (non-null): {stats['count']:,.0f}")
            print(f"      • Mean: {stats['mean']:,.2f}")
            print(f"      • Median (50%): {stats['50%']:,.2f}")
            print(f"      • Standard Deviation: {stats['std']:,.2f}")
            print(f"      • Min: {stats['min']:,.2f}")
            print(f"      • Max: {stats['max']:,.2f}")
            print(f"      • Range: {stats['max'] - stats['min']:,.2f}")
            
            # Additional insights
            unique_count = df[col].nunique()
            print(f"      • Unique values: {unique_count:,}")
            
            if unique_count > 1:
                # Check for outliers using IQR method
                q1 = stats['25%']
                q3 = stats['75%']
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].count()
                print(f"      • Potential outliers: {outliers:,} ({outliers/non_null_count*100:.1f}%)")
    else:
        print("   ⚠️  No numerical columns found in the dataset")
        print("   💡 All columns appear to be categorical/text data")
    
    # 5. Additional insights
    print("\n5. ADDITIONAL INSIGHTS:")
    print("-" * 30)
    
    # Check for completely empty columns
    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    if empty_cols:
        print(f"   • Completely empty columns: {len(empty_cols)}")
        for col in empty_cols:
            print(f"     - {col}")
    else:
        print("   • No completely empty columns found ✅")
    
    # Check for duplicate rows
    duplicate_count = df.duplicated().sum()
    print(f"   • Duplicate rows: {duplicate_count:,} ({duplicate_count/len(df)*100:.2f}%)")
    
    # Check columns with all unique values (potential identifiers)
    unique_cols = [col for col in df.columns if df[col].nunique() == len(df) - df[col].isnull().sum()]
    if unique_cols:
        print(f"   • Columns with all unique values (potential IDs): {len(unique_cols)}")
        for col in unique_cols:
            print(f"     - {col}")
    
    print("\n" + "="*60)
    print("BASIC DATA EXPLORATION COMPLETE!")
    print("="*60)

def handle_missing_data(df, missing_threshold=50, strategy='auto'):
    """
    Handle missing data in the DataFrame
    
    Parameters:
    df: pandas DataFrame
    missing_threshold: percentage threshold for considering a column as having 'many' missing values
    strategy: 'auto', 'remove_columns', 'remove_rows', 'fill_forward', 'fill_backward', 'fill_mean', 'fill_mode', 'custom'
    """
    print("\n" + "="*60)
    print("MISSING DATA HANDLING")
    print("="*60)
    
    # Create a copy to avoid modifying original data
    df_cleaned = df.copy()
    original_shape = df.shape
    
    # 1. Identify columns with many missing values
    print("1. IDENTIFYING PROBLEMATIC COLUMNS:")
    print("-" * 40)
    
    missing_analysis = []
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_analysis.append({
            'Column': col,
            'Missing_Count': missing_count,
            'Missing_Percentage': missing_pct,
            'Data_Type': str(df[col].dtype),
            'Non_Null_Count': df[col].count()
        })
    
    # Create DataFrame for analysis
    missing_df = pd.DataFrame(missing_analysis)
    missing_df = missing_df.sort_values('Missing_Percentage', ascending=False)
    
    # Categorize columns by missing data severity
    high_missing = missing_df[missing_df['Missing_Percentage'] >= missing_threshold]
    moderate_missing = missing_df[(missing_df['Missing_Percentage'] >= 10) & 
                                 (missing_df['Missing_Percentage'] < missing_threshold)]
    low_missing = missing_df[missing_df['Missing_Percentage'] < 10]
    
    print(f"   📊 Missing Data Categories (threshold: {missing_threshold}%):")
    print(f"   • High missing (≥{missing_threshold}%): {len(high_missing)} columns")
    print(f"   • Moderate missing (10-{missing_threshold-1}%): {len(moderate_missing)} columns") 
    print(f"   • Low missing (<10%): {len(low_missing)} columns")
    
    print(f"\n   🚨 HIGH MISSING DATA COLUMNS (≥{missing_threshold}%):")
    if len(high_missing) > 0:
        for _, row in high_missing.iterrows():
            print(f"      • {row['Column']:<20}: {row['Missing_Percentage']:>6.1f}% missing ({row['Missing_Count']:,} values)")
    else:
        print("      ✅ No columns with high missing data!")
    
    print(f"\n   ⚡ MODERATE MISSING DATA COLUMNS (10-{missing_threshold-1}%):")
    if len(moderate_missing) > 0:
        for _, row in moderate_missing.iterrows():
            print(f"      • {row['Column']:<20}: {row['Missing_Percentage']:>6.1f}% missing ({row['Missing_Count']:,} values)")
    else:
        print("      ✅ No columns with moderate missing data!")
    
    # 2. Decision making and strategy application
    print(f"\n2. MISSING DATA HANDLING STRATEGY:")
    print("-" * 40)
    
    actions_taken = []
    
    if strategy == 'auto':
        print("   🤖 Using AUTOMATIC strategy:")
        print("      • Columns with >90% missing → DROP")
        print("      • Columns with 50-90% missing → KEEP but MARK")
        print("      • Columns with <50% missing → FILL or KEEP")
        
        # Drop columns with >90% missing data
        very_high_missing = missing_df[missing_df['Missing_Percentage'] > 90]['Column'].tolist()
        if very_high_missing:
            print(f"\n   🗑️  DROPPING {len(very_high_missing)} columns with >90% missing data:")
            for col in very_high_missing:
                pct = missing_df[missing_df['Column'] == col]['Missing_Percentage'].iloc[0]
                print(f"      • {col} ({pct:.1f}% missing)")
                df_cleaned = df_cleaned.drop(columns=[col])
                actions_taken.append(f"Dropped column '{col}' ({pct:.1f}% missing)")
        
        # Handle moderate missing data intelligently
        moderate_cols = missing_df[(missing_df['Missing_Percentage'] > 10) & 
                                  (missing_df['Missing_Percentage'] <= 90)]['Column'].tolist()
        
        print(f"\n   🔧 HANDLING {len(moderate_cols)} columns with moderate missing data:")
        for col in moderate_cols:
            if col not in df_cleaned.columns:
                continue
                
            missing_pct = missing_df[missing_df['Column'] == col]['Missing_Percentage'].iloc[0]
            col_dtype = df_cleaned[col].dtype
            
            if col_dtype == 'object':  # Text/categorical data
                # For text data, keep as is but could fill with 'Unknown' if needed
                print(f"      • {col:<20}: KEPT as-is ({missing_pct:.1f}% missing, text data)")
                actions_taken.append(f"Kept column '{col}' as-is (text data, {missing_pct:.1f}% missing)")
            else:  # Numerical data
                if missing_pct < 30:
                    # Fill with median for numerical data
                    median_val = df_cleaned[col].median()
                    df_cleaned[col].fillna(median_val, inplace=True)
                    print(f"      • {col:<20}: FILLED with median ({median_val:.2f})")
                    actions_taken.append(f"Filled column '{col}' with median value {median_val:.2f}")
                else:
                    print(f"      • {col:<20}: KEPT as-is ({missing_pct:.1f}% missing, high missing rate)")
                    actions_taken.append(f"Kept column '{col}' as-is (high missing rate)")
        
        # Handle low missing data
        low_missing_cols = missing_df[missing_df['Missing_Percentage'] <= 10]['Column'].tolist()
        low_missing_cols = [col for col in low_missing_cols if col in df_cleaned.columns]
        
        print(f"\n   ✨ HANDLING {len(low_missing_cols)} columns with low missing data:")
        for col in low_missing_cols:
            if df_cleaned[col].isnull().sum() == 0:
                continue
                
            missing_pct = missing_df[missing_df['Column'] == col]['Missing_Percentage'].iloc[0]
            col_dtype = df_cleaned[col].dtype
            
            if col_dtype == 'object':  # Text data
                mode_val = df_cleaned[col].mode()
                if len(mode_val) > 0:
                    df_cleaned[col].fillna(mode_val[0], inplace=True)
                    print(f"      • {col:<20}: FILLED with mode ('{mode_val[0]}')")
                    actions_taken.append(f"Filled column '{col}' with mode value")
                else:
                    df_cleaned[col].fillna('Unknown', inplace=True)
                    print(f"      • {col:<20}: FILLED with 'Unknown'")
                    actions_taken.append(f"Filled column '{col}' with 'Unknown'")
            else:  # Numerical data
                median_val = df_cleaned[col].median()
                df_cleaned[col].fillna(median_val, inplace=True)
                print(f"      • {col:<20}: FILLED with median ({median_val:.2f})")
                actions_taken.append(f"Filled column '{col}' with median value {median_val:.2f}")
    
    elif strategy == 'remove_columns':
        cols_to_drop = missing_df[missing_df['Missing_Percentage'] >= missing_threshold]['Column'].tolist()
        if cols_to_drop:
            df_cleaned = df_cleaned.drop(columns=cols_to_drop)
            print(f"   🗑️  DROPPED {len(cols_to_drop)} columns with ≥{missing_threshold}% missing data")
            actions_taken.extend([f"Dropped column '{col}'" for col in cols_to_drop])
        else:
            print(f"   ✅ No columns to drop (none have ≥{missing_threshold}% missing data)")
    
    elif strategy == 'remove_rows':
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.dropna()
        rows_dropped = initial_rows - len(df_cleaned)
        print(f"   🗑️  DROPPED {rows_dropped:,} rows with any missing values")
        actions_taken.append(f"Dropped {rows_dropped:,} rows with missing values")
    
    # Add other strategies as needed...
    
    # 3. Create cleaned dataset summary
    print(f"\n3. CLEANED DATASET SUMMARY:")
    print("-" * 40)
    
    cleaned_shape = df_cleaned.shape
    
    print(f"   📈 Dataset Transformation:")
    print(f"      • Original shape: {original_shape[0]:,} rows × {original_shape[1]} columns")
    print(f"      • Cleaned shape:  {cleaned_shape[0]:,} rows × {cleaned_shape[1]} columns")
    print(f"      • Rows change:    {cleaned_shape[0] - original_shape[0]:,} ({((cleaned_shape[0] - original_shape[0])/original_shape[0]*100):+.1f}%)")
    print(f"      • Columns change: {cleaned_shape[1] - original_shape[1]:+d} ({((cleaned_shape[1] - original_shape[1])/original_shape[1]*100):+.1f}%)")
    
    # Calculate remaining missing values
    remaining_missing = df_cleaned.isnull().sum().sum()
    total_cells_cleaned = df_cleaned.shape[0] * df_cleaned.shape[1]
    remaining_missing_pct = (remaining_missing / total_cells_cleaned) * 100
    
    print(f"\n   🎯 Missing Data Reduction:")
    original_missing = df.isnull().sum().sum()
    original_missing_pct = (original_missing / (original_shape[0] * original_shape[1])) * 100
    
    print(f"      • Original missing: {original_missing:,} values ({original_missing_pct:.2f}%)")
    print(f"      • Remaining missing: {remaining_missing:,} values ({remaining_missing_pct:.2f}%)")
    print(f"      • Reduction: {original_missing - remaining_missing:,} values ({original_missing_pct - remaining_missing_pct:+.2f}%)")
    
    # 4. Actions summary
    print(f"\n4. ACTIONS TAKEN:")
    print("-" * 40)
    if actions_taken:
        for i, action in enumerate(actions_taken, 1):
            print(f"   {i:2d}. {action}")
    else:
        print("   ℹ️  No actions were taken (data was already clean)")
    
    # 5. Data quality assessment
    print(f"\n5. DATA QUALITY ASSESSMENT:")
    print("-" * 40)
    
    if remaining_missing_pct < 1:
        quality_status = "🌟 EXCELLENT"
    elif remaining_missing_pct < 5:
        quality_status = "✅ GOOD"
    elif remaining_missing_pct < 15:
        quality_status = "⚡ MODERATE"
    else:
        quality_status = "⚠️  NEEDS ATTENTION"
    
    print(f"   Overall Data Quality: {quality_status}")
    print(f"   Completeness: {100 - remaining_missing_pct:.2f}%")
    
    # Recommendations
    print(f"\n   💡 RECOMMENDATIONS:")
    if remaining_missing_pct > 10:
        print("      • Consider additional data cleaning strategies")
        print("      • Review columns with high missing rates for domain-specific handling")
    if cleaned_shape[1] < original_shape[1] * 0.7:
        print("      • Many columns were dropped - verify this aligns with analysis goals")
    if cleaned_shape[0] < original_shape[0] * 0.8:
        print("      • Significant row reduction - consider imputation strategies")
    if remaining_missing_pct < 5:
        print("      ✅ Dataset is ready for analysis!")
    
    print("\n" + "="*60)
    print("MISSING DATA HANDLING COMPLETE!")
    print("="*60)
    
    return df_cleaned, actions_taken

def prepare_data_for_analysis(df):
    """
    Prepare the dataset for analysis by:
    - Converting date columns to datetime format
    - Extracting year from publication date
    - Creating new analytical columns
    """
    print("\n" + "="*60)
    print("DATA PREPARATION FOR ANALYSIS")
    print("="*60)
    
    # Create a copy to avoid modifying original data
    df_prepared = df.copy()
    preparation_actions = []
    
    # 1. Handle date columns
    print("1. PROCESSING DATE COLUMNS:")
    print("-" * 40)
    
    # Identify potential date columns
    date_columns = ['publish_time']  # Known date column
    other_potential_date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    date_columns.extend([col for col in other_potential_date_cols if col not in date_columns])
    
    for col in date_columns:
        if col in df_prepared.columns:
            print(f"\n   📅 Processing '{col}' column:")
            
            # Check current data type and sample values
            non_null_count = df_prepared[col].count()
            print(f"      • Current type: {df_prepared[col].dtype}")
            print(f"      • Non-null values: {non_null_count:,}")
            
            if non_null_count > 0:
                # Show sample values
                sample_values = df_prepared[col].dropna().head(3).tolist()
                print(f"      • Sample values: {sample_values}")
                
                try:
                    # Convert to datetime
                    df_prepared[col] = pd.to_datetime(df_prepared[col], errors='coerce')
                    successful_conversions = df_prepared[col].count()
                    failed_conversions = non_null_count - successful_conversions
                    
                    print(f"      ✅ Converted to datetime successfully!")
                    print(f"      • Successful conversions: {successful_conversions:,}")
                    if failed_conversions > 0:
                        print(f"      • Failed conversions: {failed_conversions:,}")
                    
                    preparation_actions.append(f"Converted '{col}' to datetime format")
                    
                    # Extract date components if conversion was successful
                    if successful_conversions > 0:
                        # Extract year
                        year_col = f"{col}_year"
                        df_prepared[year_col] = df_prepared[col].dt.year
                        print(f"      📈 Created '{year_col}' column")
                        preparation_actions.append(f"Extracted year to '{year_col}' column")
                        
                        # Extract month
                        month_col = f"{col}_month"
                        df_prepared[month_col] = df_prepared[col].dt.month
                        print(f"      📈 Created '{month_col}' column")
                        preparation_actions.append(f"Extracted month to '{month_col}' column")
                        
                        # Extract day of year for seasonal analysis
                        dayofyear_col = f"{col}_dayofyear"
                        df_prepared[dayofyear_col] = df_prepared[col].dt.dayofyear
                        print(f"      📈 Created '{dayofyear_col}' column for seasonal analysis")
                        preparation_actions.append(f"Extracted day of year to '{dayofyear_col}' column")
                        
                        # Show date range
                        min_date = df_prepared[col].min()
                        max_date = df_prepared[col].max()
                        if pd.notna(min_date) and pd.notna(max_date):
                            print(f"      📊 Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
                            print(f"      📊 Span: {(max_date - min_date).days:,} days")
                
                except Exception as e:
                    print(f"      ❌ Failed to convert to datetime: {e}")
            else:
                print(f"      ⚠️  Column is empty, skipping conversion")
    
    # 2. Create analytical columns
    print(f"\n2. CREATING ANALYTICAL COLUMNS:")
    print("-" * 40)
    
    # Abstract analysis
    if 'abstract' in df_prepared.columns:
        print(f"\n   📝 ABSTRACT ANALYSIS:")
        
        # Word count
        def safe_word_count(text):
            if pd.isna(text) or text == '':
                return 0
            return len(str(text).split())
        
        df_prepared['abstract_word_count'] = df_prepared['abstract'].apply(safe_word_count)
        non_zero_abstracts = (df_prepared['abstract_word_count'] > 0).sum()
        avg_word_count = df_prepared[df_prepared['abstract_word_count'] > 0]['abstract_word_count'].mean()
        
        print(f"      • Created 'abstract_word_count' column")
        print(f"      • Non-empty abstracts: {non_zero_abstracts:,}")
        print(f"      • Average word count: {avg_word_count:.1f} words")
        preparation_actions.append("Created 'abstract_word_count' column")
        
        # Character count
        def safe_char_count(text):
            if pd.isna(text):
                return 0
            return len(str(text))
        
        df_prepared['abstract_char_count'] = df_prepared['abstract'].apply(safe_char_count)
        print(f"      • Created 'abstract_char_count' column")
        preparation_actions.append("Created 'abstract_char_count' column")
        
        # Abstract length category
        def categorize_abstract_length(word_count):
            if word_count == 0:
                return 'No Abstract'
            elif word_count < 100:
                return 'Short'
            elif word_count < 250:
                return 'Medium'
            elif word_count < 400:
                return 'Long'
            else:
                return 'Very Long'
        
        df_prepared['abstract_length_category'] = df_prepared['abstract_word_count'].apply(categorize_abstract_length)
        print(f"      • Created 'abstract_length_category' column")
        
        # Show distribution
        length_dist = df_prepared['abstract_length_category'].value_counts()
        print(f"      📊 Abstract length distribution:")
        for category, count in length_dist.items():
            print(f"         - {category}: {count:,} ({count/len(df_prepared)*100:.1f}%)")
        preparation_actions.append("Created 'abstract_length_category' column")
    
    # Authors analysis
    if 'authors' in df_prepared.columns:
        print(f"\n   👥 AUTHORS ANALYSIS:")
        
        # Count number of authors
        def count_authors(authors_str):
            if pd.isna(authors_str) or authors_str == '':
                return 0
            # Count semicolons + 1 (common separator for authors)
            return len(str(authors_str).split(';'))
        
        df_prepared['author_count'] = df_prepared['authors'].apply(count_authors)
        non_zero_authors = (df_prepared['author_count'] > 0).sum()
        avg_author_count = df_prepared[df_prepared['author_count'] > 0]['author_count'].mean()
        
        print(f"      • Created 'author_count' column")
        print(f"      • Papers with authors: {non_zero_authors:,}")
        print(f"      • Average authors per paper: {avg_author_count:.1f}")
        preparation_actions.append("Created 'author_count' column")
        
        # Collaboration category
        def categorize_collaboration(author_count):
            if author_count == 0:
                return 'No Authors Listed'
            elif author_count == 1:
                return 'Single Author'
            elif author_count <= 3:
                return 'Small Team'
            elif author_count <= 6:
                return 'Medium Team'
            else:
                return 'Large Team'
        
        df_prepared['collaboration_type'] = df_prepared['author_count'].apply(categorize_collaboration)
        print(f"      • Created 'collaboration_type' column")
        
        # Show distribution
        collab_dist = df_prepared['collaboration_type'].value_counts()
        print(f"      📊 Collaboration type distribution:")
        for collab_type, count in collab_dist.items():
            print(f"         - {collab_type}: {count:,} ({count/len(df_prepared)*100:.1f}%)")
        preparation_actions.append("Created 'collaboration_type' column")
    
    # Title analysis
    if 'title' in df_prepared.columns:
        print(f"\n   📰 TITLE ANALYSIS:")
        
        # Title word count
        df_prepared['title_word_count'] = df_prepared['title'].apply(safe_word_count)
        non_empty_titles = (df_prepared['title_word_count'] > 0).sum()
        avg_title_length = df_prepared[df_prepared['title_word_count'] > 0]['title_word_count'].mean()
        
        print(f"      • Created 'title_word_count' column")
        print(f"      • Non-empty titles: {non_empty_titles:,}")
        print(f"      • Average title length: {avg_title_length:.1f} words")
        preparation_actions.append("Created 'title_word_count' column")
    
    # Journal analysis
    if 'journal' in df_prepared.columns:
        print(f"\n   📚 JOURNAL ANALYSIS:")
        
        # Count papers per journal
        journal_counts = df_prepared['journal'].value_counts()
        top_journals = journal_counts.head(5)
        
        print(f"      • Total unique journals: {df_prepared['journal'].nunique():,}")
        print(f"      📊 Top 5 journals by paper count:")
        for journal, count in top_journals.items():
            if pd.notna(journal):
                print(f"         - {journal[:50]}{'...' if len(str(journal)) > 50 else ''}: {count:,} papers")
        
        # Add journal productivity category
        journal_paper_counts = df_prepared['journal'].map(journal_counts)
        df_prepared['journal_productivity'] = pd.cut(
            journal_paper_counts, 
            bins=[0, 1, 10, 100, 1000, float('inf')], 
            labels=['Single Paper', 'Low (2-10)', 'Medium (11-100)', 'High (101-1000)', 'Very High (1000+)'],
            include_lowest=True
        )
        print(f"      • Created 'journal_productivity' category")
        preparation_actions.append("Created 'journal_productivity' category")
    
    # Source analysis
    if 'source_x' in df_prepared.columns:
        print(f"\n   🗂️  SOURCE ANALYSIS:")
        
        source_dist = df_prepared['source_x'].value_counts()
        print(f"      📊 Data sources distribution:")
        for source, count in source_dist.items():
            print(f"         - {source}: {count:,} ({count/len(df_prepared)*100:.1f}%)")
    
    # 3. Data quality indicators
    print(f"\n3. CREATING DATA QUALITY INDICATORS:")
    print("-" * 40)
    
    # Completeness score for each row
    total_important_cols = ['title', 'authors', 'abstract', 'publish_time', 'journal']
    existing_important_cols = [col for col in total_important_cols if col in df_prepared.columns]
    
    def calculate_completeness_score(row):
        non_null_count = sum(1 for col in existing_important_cols if pd.notna(row[col]) and row[col] != '')
        return (non_null_count / len(existing_important_cols)) * 100
    
    df_prepared['data_completeness_score'] = df_prepared.apply(calculate_completeness_score, axis=1)
    avg_completeness = df_prepared['data_completeness_score'].mean()
    
    print(f"   • Created 'data_completeness_score' column")
    print(f"   • Average completeness: {avg_completeness:.1f}%")
    preparation_actions.append("Created 'data_completeness_score' column")
    
    # Quality category
    def categorize_quality(score):
        if score >= 90:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 50:
            return 'Fair'
        else:
            return 'Poor'
    
    df_prepared['data_quality_category'] = df_prepared['data_completeness_score'].apply(categorize_quality)
    
    quality_dist = df_prepared['data_quality_category'].value_counts()
    print(f"   📊 Data quality distribution:")
    for quality, count in quality_dist.items():
        print(f"      - {quality}: {count:,} ({count/len(df_prepared)*100:.1f}%)")
    preparation_actions.append("Created 'data_quality_category' column")
    
    # 4. Summary of changes
    print(f"\n4. PREPARATION SUMMARY:")
    print("-" * 40)
    
    original_cols = df.shape[1]
    prepared_cols = df_prepared.shape[1]
    new_cols = prepared_cols - original_cols
    
    print(f"   📊 Column Changes:")
    print(f"      • Original columns: {original_cols}")
    print(f"      • Prepared columns: {prepared_cols}")
    print(f"      • New columns added: {new_cols}")
    
    print(f"\n   🆕 NEW COLUMNS CREATED:")
    new_column_names = [col for col in df_prepared.columns if col not in df.columns]
    for i, col in enumerate(new_column_names, 1):
        print(f"      {i:2d}. {col}")
    
    print(f"\n   ⚙️  ACTIONS PERFORMED:")
    for i, action in enumerate(preparation_actions, 1):
        print(f"      {i:2d}. {action}")
    
    print("\n" + "="*60)
    print("DATA PREPARATION COMPLETE!")
    print("="*60)
    
    return df_prepared, preparation_actions, new_column_names

def perform_basic_analysis(df):
    """
    Perform basic analysis on the dataset
    """
    print("\n" + "="*60)
    print("BASIC ANALYSIS")
    print("="*60)
    
    # 1. Count papers by publication year
    print("1. PAPERS BY PUBLICATION YEAR:")
    print("-" * 40)
    
    # First, let's check the publish_time column format
    if 'publish_time' in df.columns:
        # Get a sample of non-null publish_time values to understand the format
        sample_dates = df['publish_time'].dropna().head(10)
        print(f"   📅 Sample date formats:")
        for i, date in enumerate(sample_dates.iloc[:5], 1):
            print(f"      {i}. {date}")
        
        try:
            # Try to convert to datetime
            df_temp = df.copy()
            
            # Handle various date formats
            df_temp['publish_time_clean'] = pd.to_datetime(df_temp['publish_time'], errors='coerce')
            
            # Extract year
            df_temp['publication_year'] = df_temp['publish_time_clean'].dt.year
            
            # Count papers by year
            year_counts = df_temp['publication_year'].value_counts().sort_index()
            
            print(f"\n   📊 Papers by Year (showing top years):")
            
            # Show all years if reasonable number, otherwise show top 15
            if len(year_counts) <= 20:
                for year, count in year_counts.items():
                    if pd.notna(year):
                        print(f"      {int(year)}: {count:,} papers")
            else:
                print(f"      Showing top 15 years out of {len(year_counts)} total years:")
                for year, count in year_counts.head(15).items():
                    if pd.notna(year):
                        print(f"      {int(year)}: {count:,} papers")
            
            # Summary statistics
            valid_years = year_counts.dropna()
            if len(valid_years) > 0:
                print(f"\n   📈 Publication Timeline Summary:")
                print(f"      • Earliest paper: {int(valid_years.index.min())}")
                print(f"      • Latest paper: {int(valid_years.index.max())}")
                print(f"      • Most productive year: {int(valid_years.idxmax())} ({valid_years.max():,} papers)")
                print(f"      • Total years with publications: {len(valid_years)}")
                print(f"      • Papers with valid dates: {valid_years.sum():,}")
                
                # Check for recent COVID-19 surge (2020-2021)
                covid_years = valid_years[(valid_years.index >= 2020) & (valid_years.index <= 2021)]
                if len(covid_years) > 0:
                    covid_total = covid_years.sum()
                    covid_pct = (covid_total / valid_years.sum()) * 100
                    print(f"      • COVID-19 era papers (2020-2021): {covid_total:,} ({covid_pct:.1f}%)")
        
        except Exception as e:
            print(f"   ❌ Error processing publication dates: {e}")
            print("   💡 Dates may be in an unexpected format")
    else:
        print("   ❌ No 'publish_time' column found")
    
    # 2. Identify top journals
    print(f"\n2. TOP JOURNALS PUBLISHING COVID-19 RESEARCH:")
    print("-" * 40)
    
    if 'journal' in df.columns:
        # Clean and count journals
        journal_counts = df['journal'].value_counts()
        
        print(f"   📚 Journal Statistics:")
        print(f"      • Total unique journals: {len(journal_counts):,}")
        print(f"      • Papers with journal info: {journal_counts.sum():,}")
        print(f"      • Papers missing journal info: {df['journal'].isnull().sum():,}")
        
        print(f"\n   🏆 Top 15 Journals by Paper Count:")
        for i, (journal, count) in enumerate(journal_counts.head(15).items(), 1):
            percentage = (count / journal_counts.sum()) * 100
            print(f"      {i:2d}. {journal[:60]:<60} | {count:>6,} papers ({percentage:>4.1f}%)")
        
        # Additional journal insights
        single_paper_journals = (journal_counts == 1).sum()
        top_10_total = journal_counts.head(10).sum()
        top_10_pct = (top_10_total / journal_counts.sum()) * 100
        
        print(f"\n   📊 Journal Distribution Insights:")
        print(f"      • Journals with only 1 paper: {single_paper_journals:,} ({(single_paper_journals/len(journal_counts)*100):.1f}%)")
        print(f"      • Top 10 journals represent: {top_10_pct:.1f}% of all papers")
        print(f"      • Average papers per journal: {journal_counts.mean():.1f}")
        print(f"      • Median papers per journal: {journal_counts.median():.1f}")
        
    else:
        print("   ❌ No 'journal' column found")
    
    # 3. Most frequent words in titles
    print(f"\n3. MOST FREQUENT WORDS IN TITLES:")
    print("-" * 40)
    
    if 'title' in df.columns:
        # Get non-null titles
        titles = df['title'].dropna()
        
        print(f"   📝 Title Statistics:")
        print(f"      • Total papers with titles: {len(titles):,}")
        print(f"      • Papers missing titles: {df['title'].isnull().sum():,}")
        
        if len(titles) > 0:
            # Simple word frequency analysis
            import re
            from collections import Counter
            
            # Combine all titles and clean
            all_titles = ' '.join(titles.astype(str))
            
            # Basic text cleaning - convert to lowercase and extract words
            words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())
            
            # Common stop words to filter out
            stop_words = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
                'after', 'above', 'below', 'between', 'among', 'through', 'during',
                'within', 'without', 'upon', 'against', 'under', 'over', 'across',
                'this', 'that', 'these', 'those', 'are', 'was', 'were', 'been', 'being',
                'have', 'has', 'had', 'having', 'will', 'would', 'could', 'should',
                'may', 'might', 'must', 'can', 'shall', 'its', 'his', 'her', 'their',
                'our', 'your', 'than', 'then', 'now', 'here', 'there', 'when', 'where',
                'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                'other', 'some', 'such', 'only', 'own', 'same', 'so', 'very', 'just'
            }
            
            # Filter out stop words and count
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            word_counts = Counter(filtered_words)
            
            print(f"\n   🔤 Word Analysis:")
            print(f"      • Total words in titles: {len(words):,}")
            print(f"      • Unique words (after filtering): {len(word_counts):,}")
            print(f"      • Average words per title: {len(words)/len(titles):.1f}")
            
            print(f"\n   🏆 Top 20 Most Frequent Words in Titles:")
            for i, (word, count) in enumerate(word_counts.most_common(20), 1):
                percentage = (count / len(filtered_words)) * 100
                print(f"      {i:2d}. {word:<15} | {count:>6,} occurrences ({percentage:>4.1f}%)")
            
            # COVID-related terms analysis
            covid_terms = ['covid', 'coronavirus', 'sars', 'pandemic', 'virus', 'viral', 
                          'infection', 'disease', 'respiratory', 'pneumonia', 'outbreak']
            
            covid_word_counts = {term: word_counts.get(term, 0) for term in covid_terms}
            covid_total = sum(covid_word_counts.values())
            
            print(f"\n   🦠 COVID-19 Related Terms:")
            covid_found = False
            for term, count in sorted(covid_word_counts.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    covid_found = True
                    percentage = (count / len(filtered_words)) * 100
                    print(f"      • {term:<12}: {count:>6,} occurrences ({percentage:>4.1f}%)")
            
            if covid_found:
                print(f"      • Total COVID-related terms: {covid_total:,} ({(covid_total/len(filtered_words)*100):.1f}%)")
            else:
                print("      • No common COVID-related terms found in top frequency")
            
            # Medical/Scientific terms
            medical_terms = ['clinical', 'treatment', 'patient', 'patients', 'study', 'analysis', 
                           'research', 'hospital', 'health', 'care', 'medical', 'diagnosis']
            
            medical_counts = {term: word_counts.get(term, 0) for term in medical_terms}
            medical_found = False
            
            print(f"\n   🏥 Medical/Research Terms:")
            for term, count in sorted(medical_counts.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    medical_found = True
                    percentage = (count / len(filtered_words)) * 100
                    print(f"      • {term:<12}: {count:>6,} occurrences ({percentage:>4.1f}%)")
            
        else:
            print("   ❌ No titles available for analysis")
    else:
        print("   ❌ No 'title' column found")
    
    print("\n" + "="*60)
    print("BASIC ANALYSIS COMPLETE!")
    print("="*60)

def create_visualizations(df, save_plots=True):
    """
    Create comprehensive visualizations for the dataset
    """
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Set up matplotlib style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure directory if saving plots
    import os
    if save_plots:
        plots_dir = 'plots'
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
            print(f"📁 Created '{plots_dir}' directory for saving plots")
    
    visualizations_created = []
    
    # 1. Publications over time
    print("\n1. PLOTTING PUBLICATIONS OVER TIME:")
    print("-" * 40)
    
    if 'publish_time_year' in df.columns:
        try:
            # Get publication counts by year
            year_counts = df['publish_time_year'].value_counts().sort_index()
            
            # Filter to reasonable years (e.g., 1980 onwards)
            year_counts = year_counts[year_counts.index >= 1980]
            
            plt.figure(figsize=(12, 6))
            plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, markersize=4)
            plt.title('Number of Publications Over Time', fontsize=16, fontweight='bold')
            plt.xlabel('Publication Year', fontsize=12)
            plt.ylabel('Number of Papers', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Highlight COVID-19 period (2020 onwards)
            covid_years = year_counts[year_counts.index >= 2020]
            if len(covid_years) > 0:
                plt.fill_between(covid_years.index, covid_years.values, alpha=0.3, color='red', 
                               label='COVID-19 Period (2020+)')
                plt.legend()
            
            plt.tight_layout()
            
            if save_plots:
                plt.savefig(f'{plots_dir}/publications_over_time.png', dpi=300, bbox_inches='tight')
                print("   💾 Saved as 'plots/publications_over_time.png'")
            
            plt.show()
            
            # Show statistics
            total_papers = year_counts.sum()
            recent_papers = covid_years.sum() if len(covid_years) > 0 else 0
            peak_year = year_counts.idxmax()
            peak_count = year_counts.max()
            
            print(f"   📊 Timeline Statistics:")
            print(f"      • Total papers with dates: {total_papers:,}")
            print(f"      • Year range: {int(year_counts.index.min())}-{int(year_counts.index.max())}")
            print(f"      • Peak year: {int(peak_year)} ({peak_count:,} papers)")
            if recent_papers > 0:
                print(f"      • COVID-19 era papers (2020+): {recent_papers:,} ({recent_papers/total_papers*100:.1f}%)")
            
            visualizations_created.append("Publications over time line plot")
            
        except Exception as e:
            print(f"   ❌ Error creating timeline plot: {e}")
    else:
        print("   ⚠️  No 'publish_time_year' column found. Skipping timeline plot.")
    
    # 2. Top publishing journals
    print("\n2. CREATING BAR CHART OF TOP PUBLISHING JOURNALS:")
    print("-" * 40)
    
    if 'journal' in df.columns:
        try:
            # Get top journals
            journal_counts = df['journal'].value_counts().head(15)
            
            plt.figure(figsize=(12, 8))
            bars = plt.barh(range(len(journal_counts)), journal_counts.values)
            
            # Color bars with gradient
            colors = plt.cm.viridis(np.linspace(0, 1, len(journal_counts)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            plt.yticks(range(len(journal_counts)), 
                      [journal[:50] + '...' if len(str(journal)) > 50 else journal 
                       for journal in journal_counts.index])
            plt.xlabel('Number of Papers', fontsize=12)
            plt.title('Top 15 Journals by Number of Publications', fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3, axis='x')
            
            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, journal_counts.values)):
                plt.text(value + max(journal_counts.values) * 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{value:,}', va='center', fontsize=10)
            
            plt.tight_layout()
            
            if save_plots:
                plt.savefig(f'{plots_dir}/top_journals.png', dpi=300, bbox_inches='tight')
                print("   💾 Saved as 'plots/top_journals.png'")
            
            plt.show()
            
            # Show statistics
            total_journals = df['journal'].nunique()
            top_5_share = journal_counts.head(5).sum() / journal_counts.sum() * 100
            
            print(f"   📊 Journal Statistics:")
            print(f"      • Total unique journals: {total_journals:,}")
            print(f"      • Top 5 journals share: {top_5_share:.1f}% of all papers")
            print(f"      • Top journal: {journal_counts.index[0]} ({journal_counts.iloc[0]:,} papers)")
            
            visualizations_created.append("Top journals bar chart")
            
        except Exception as e:
            print(f"   ❌ Error creating journals chart: {e}")
    else:
        print("   ⚠️  No 'journal' column found. Skipping journals chart.")
    
    # 3. Word cloud of paper titles
    print("\n3. GENERATING WORD CLOUD OF PAPER TITLES:")
    print("-" * 40)
    
    if 'title' in df.columns:
        try:
            # Prepare text data
            titles = df['title'].dropna().astype(str)
            
            # Clean and prepare text
            def clean_text(text):
                # Remove special characters and numbers
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                # Convert to lowercase
                text = text.lower()
                # Remove common stop words
                stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                             'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
                             'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was', 
                             'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
                             'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
                             'a', 'an', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
                             'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                             'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
                             'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'}
                
                words = text.split()
                words = [word for word in words if word not in stop_words and len(word) > 2]
                return ' '.join(words)
            
            # Clean all titles
            cleaned_titles = titles.apply(clean_text)
            all_text = ' '.join(cleaned_titles)
            
            # Create word cloud
            plt.figure(figsize=(15, 8))
            
            wordcloud = WordCloud(
                width=1200, 
                height=600, 
                background_color='white',
                max_words=100,
                colormap='viridis',
                relative_scaling=0.5,
                random_state=42
            ).generate(all_text)
            
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Most Frequent Words in Paper Titles', fontsize=20, fontweight='bold', pad=20)
            plt.tight_layout()
            
            if save_plots:
                plt.savefig(f'{plots_dir}/title_wordcloud.png', dpi=300, bbox_inches='tight')
                print("   💾 Saved as 'plots/title_wordcloud.png'")
            
            plt.show()
            
            # Show top words statistics
            word_freq = Counter(all_text.split())
            top_words = word_freq.most_common(10)
            
            print(f"   📊 Title Word Statistics:")
            print(f"      • Total titles analyzed: {len(titles):,}")
            print(f"      • Unique words found: {len(word_freq):,}")
            print(f"      • Top 10 most frequent words:")
            for i, (word, count) in enumerate(top_words, 1):
                print(f"         {i:2d}. {word}: {count:,} occurrences")
            
            visualizations_created.append("Title word cloud")
            
        except Exception as e:
            print(f"   ❌ Error creating word cloud: {e}")
            print("   💡 Tip: Install wordcloud package with: pip install wordcloud")
    else:
        print("   ⚠️  No 'title' column found. Skipping word cloud.")
    
    # 4. Distribution of papers by source
    print("\n4. PLOTTING DISTRIBUTION OF PAPERS BY SOURCE:")
    print("-" * 40)
    
    if 'source_x' in df.columns:
        try:
            source_counts = df['source_x'].value_counts()
            
            # Create pie chart for sources
            plt.figure(figsize=(10, 8))
            
            # Use autopct to show percentages
            wedges, texts, autotexts = plt.pie(source_counts.values, 
                                              labels=source_counts.index,
                                              autopct='%1.1f%%',
                                              startangle=90,
                                              colors=plt.cm.Set3(np.linspace(0, 1, len(source_counts))))
            
            plt.title('Distribution of Papers by Data Source', fontsize=16, fontweight='bold')
            
            # Enhance text readability
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.axis('equal')
            
            if save_plots:
                plt.savefig(f'{plots_dir}/source_distribution.png', dpi=300, bbox_inches='tight')
                print("   💾 Saved as 'plots/source_distribution.png'")
            
            plt.show()
            
            # Also create a bar chart for better readability
            plt.figure(figsize=(10, 6))
            bars = plt.bar(range(len(source_counts)), source_counts.values)
            
            # Color bars
            colors = plt.cm.Set2(np.linspace(0, 1, len(source_counts)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            plt.xticks(range(len(source_counts)), source_counts.index, rotation=45)
            plt.ylabel('Number of Papers', fontsize=12)
            plt.title('Papers by Data Source (Bar Chart)', fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for bar, value in zip(bars, source_counts.values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(source_counts.values) * 0.01,
                        f'{value:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            plt.tight_layout()
            
            if save_plots:
                plt.savefig(f'{plots_dir}/source_distribution_bar.png', dpi=300, bbox_inches='tight')
                print("   💾 Saved as 'plots/source_distribution_bar.png'")
            
            plt.show()
            
            # Show statistics
            total_papers = source_counts.sum()
            largest_source = source_counts.index[0]
            largest_count = source_counts.iloc[0]
            
            print(f"   📊 Source Statistics:")
            print(f"      • Total data sources: {len(source_counts)}")
            print(f"      • Largest source: {largest_source} ({largest_count:,} papers, {largest_count/total_papers*100:.1f}%)")
            print(f"      • Source distribution:")
            for source, count in source_counts.items():
                print(f"         - {source}: {count:,} papers ({count/total_papers*100:.1f}%)")
            
            visualizations_created.append("Source distribution pie chart")
            visualizations_created.append("Source distribution bar chart")
            
        except Exception as e:
            print(f"   ❌ Error creating source distribution plots: {e}")
    else:
        print("   ⚠️  No 'source_x' column found. Skipping source distribution plots.")
    
    # 5. Summary
    print(f"\n5. VISUALIZATION SUMMARY:")
    print("-" * 40)
    
    print(f"   🎨 Visualizations Created: {len(visualizations_created)}")
    for i, viz in enumerate(visualizations_created, 1):
        print(f"      {i}. {viz}")
    
    if save_plots:
        print(f"\n   📁 All plots saved in '{plots_dir}/' directory")
        print("   💡 Tip: You can view these files in your file explorer or include them in reports")
    
    print("\n" + "="*60)
    print("VISUALIZATIONS COMPLETE!")
    print("="*60)
    
    return visualizations_created

if __name__ == "__main__":
    # Load and examine the dataset
    dataset = load_and_examine_dataset()
    
    if dataset is not None:
        print(f"\nDataset successfully loaded with {dataset.shape[0]:,} rows and {dataset.shape[1]} columns.")
        
        # Perform basic data exploration
        basic_data_exploration(dataset)
        
        # Handle missing data
        print("\n" + "🔄" * 30)
        print("PROCEEDING TO MISSING DATA HANDLING...")
        print("🔄" * 30)
        
        # Create cleaned dataset using automatic strategy
        cleaned_dataset, cleaning_actions = handle_missing_data(
            dataset, 
            missing_threshold=50,  # Columns with ≥50% missing data are considered problematic
            strategy='auto'        # Use intelligent automatic cleaning
        )
        
        # Save cleaned dataset
        try:
            cleaned_filename = 'metadata_cleaned.csv'
            cleaned_dataset.to_csv(cleaned_filename, index=False)
            print(f"\n💾 Cleaned dataset saved as '{cleaned_filename}'")
            print(f"   File size: {cleaned_dataset.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        except Exception as e:
            print(f"\n❌ Error saving cleaned dataset: {e}")
        
        # Prepare data for analysis
        print("\n" + "🚀" * 30)
        print("PROCEEDING TO DATA PREPARATION FOR ANALYSIS...")
        print("🚀" * 30)
        
        # Prepare the cleaned dataset for analysis
        prepared_dataset, prep_actions, new_columns = prepare_data_for_analysis(cleaned_dataset)
        
        # Save prepared dataset
        try:
            prepared_filename = 'metadata_prepared.csv'
            prepared_dataset.to_csv(prepared_filename, index=False)
            print(f"\n💾 Prepared dataset saved as '{prepared_filename}'")
            print(f"   File size: {prepared_dataset.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        except Exception as e:
            print(f"\n❌ Error saving prepared dataset: {e}")
        
        # Final comparison
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   Original dataset:  {dataset.shape[0]:,} rows × {dataset.shape[1]} columns")
        print(f"   Cleaned dataset:   {cleaned_dataset.shape[0]:,} rows × {cleaned_dataset.shape[1]} columns")
        print(f"   Prepared dataset:  {prepared_dataset.shape[0]:,} rows × {prepared_dataset.shape[1]} columns")
        print(f"   Data retention:    {(prepared_dataset.shape[0] * dataset.shape[1]) / (dataset.shape[0] * dataset.shape[1]) * 100:.1f}%")
        print(f"   Feature expansion: +{len(new_columns)} new analytical columns")
        
        # Show some interesting insights from the prepared data
        if 'publish_time_year' in prepared_dataset.columns:
            year_range = prepared_dataset['publish_time_year'].dropna()
            if len(year_range) > 0:
                print(f"\n📅 Publication Timeline: {int(year_range.min())}-{int(year_range.max())}")
                recent_papers = (year_range >= 2020).sum()
                print(f"   Recent papers (2020+): {recent_papers:,} ({recent_papers/len(year_range)*100:.1f}%)")
        
        if 'abstract_word_count' in prepared_dataset.columns:
            avg_abstract_length = prepared_dataset[prepared_dataset['abstract_word_count'] > 0]['abstract_word_count'].mean()
            print(f"\n📝 Average Abstract Length: {avg_abstract_length:.0f} words")
        
        if 'author_count' in prepared_dataset.columns:
            avg_authors = prepared_dataset[prepared_dataset['author_count'] > 0]['author_count'].mean()
            print(f"\n👥 Average Authors per Paper: {avg_authors:.1f}")
        
        print("\n✨ You now have three datasets to work with:")
        print("   • 'dataset' - Original raw data")
        print("   • 'cleaned_dataset' - Data with missing values handled")
        print("   • 'prepared_dataset' - Analysis-ready data with new features")
        print("\n📁 Saved files:")
        print("   • 'metadata_cleaned.csv' - Cleaned dataset")
        print("   • 'metadata_prepared.csv' - Analysis-ready dataset")
        
        print(f"\n🎯 Ready for analysis! The prepared dataset includes:")
        print(f"   • Date/time features for temporal analysis")
        print(f"   • Text analysis features (word counts, categories)")
        print(f"   • Collaboration metrics (author counts)")
        print(f"   • Data quality indicators")
        print(f"   • {len(new_columns)} new analytical columns total")
        
        # Perform basic analysis on the prepared dataset
        print("\n" + "🔍" * 30)
        print("PROCEEDING TO BASIC ANALYSIS...")
        print("🔍" * 30)
        
        perform_basic_analysis(prepared_dataset)
        
        # Create comprehensive visualizations
        print("\n" + "🎨" * 30)
        print("PROCEEDING TO CREATE VISUALIZATIONS...")
        print("🎨" * 30)
        
        visualizations = create_visualizations(prepared_dataset, save_plots=True)
        
        # Final summary
        print("\n" + "🎉" * 30)
        print("ANALYSIS PIPELINE COMPLETE!")
        print("🎉" * 30)
        
        print(f"\n📈 Complete Analysis Summary:")
        print(f"   • Original dataset processed: {dataset.shape[0]:,} rows")
        print(f"   • Final prepared dataset: {prepared_dataset.shape[0]:,} rows × {prepared_dataset.shape[1]} columns")
        print(f"   • New analytical features: {len(new_columns)}")
        print(f"   • Visualizations created: {len(visualizations)}")
        print(f"   • Missing data handled: ✅")
        print(f"   • Date processing: ✅")
        print(f"   • Text analysis: ✅")
        print(f"   • Statistical analysis: ✅")
        print(f"   • Visual analysis: ✅")
        
        print(f"\n📊 Available Resources:")
        print(f"   • Three datasets: original, cleaned, prepared")
        print(f"   • Saved CSV files for further use")
        print(f"   • Generated plots in 'plots/' directory")
        print(f"   • Comprehensive analysis results")
        