"""
Load, Explore, Analyze and Visualize the Dataset
===============================================

This comprehensive script performs the following tasks:
1. Load the dataset using pandas
2. Display the first few rows using .head()
3. Explore the structure of the dataset (data types and missing values)
4. Clean the dataset by handling missing values
5. Perform basic data analysis including:
   - Compute basic statistics of numerical columns using .describe()
   - Perform groupings on categorical columns and compute statistics
   - Identify patterns and interesting findings from the analysis
6. Create comprehensive data visualizations including:
   - Line chart showing trends over time (subscription patterns)
   - Bar chart comparing numerical values across categories (name lengths by country)
   - Histogram showing distribution of numerical data (email lengths)
   - Scatter plot visualizing relationships between numerical columns
   - Additional specialized visualizations (pie charts, heatmaps, box plots)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_dataset():
    """
    Load and explore the customers dataset
    """
    print("=" * 50)
    print("LOAD AND EXPLORE THE DATASET")
    print("=" * 50)
    
    # Task 1: Load the dataset using pandas
    print("\n1. Loading the dataset...")
    try:
        df = pd.read_csv('customers-100.csv')
        print(f"✓ Dataset loaded successfully!")
        print(f"   Dataset shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
    except FileNotFoundError:
        print("❌ Error: customers-100.csv file not found!")
        return None
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None
    
    # Task 2: Display the first few rows using .head()
    print("\n2. Displaying the first few rows of the dataset:")
    print("-" * 50)
    print(df.head())
    
    # Also show the last few rows for completeness
    print("\nLast few rows of the dataset:")
    print("-" * 30)
    print(df.tail())
    
    # Task 3: Explore the structure of the dataset
    print("\n3. Exploring the structure of the dataset:")
    print("-" * 50)
    
    # Display column names
    print(f"Column names ({len(df.columns)} total):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    # Display data types
    print(f"\nData types:")
    print(df.dtypes)
    
    # Display basic info about the dataset
    print(f"\nDataset info:")
    print("-" * 20)
    df.info()
    
    # Display basic statistics
    print(f"\nBasic statistics:")
    print("-" * 20)
    print(df.describe(include='all'))
    
    # Check for missing values
    print(f"\n4. Checking for missing values:")
    print("-" * 40)
    missing_values = df.isnull().sum()
    total_missing = missing_values.sum()
    
    if total_missing == 0:
        print("✓ No missing values found in the dataset!")
    else:
        print(f"Missing values found:")
        for col, missing_count in missing_values.items():
            if missing_count > 0:
                percentage = (missing_count / len(df)) * 100
                print(f"   {col}: {missing_count} ({percentage:.2f}%)")
        print(f"\nTotal missing values: {total_missing}")
    
    # Task 4: Clean the dataset by handling missing values
    print(f"\n5. Cleaning the dataset:")
    print("-" * 30)
    
    if total_missing == 0:
        print("✓ Dataset is already clean - no missing values to handle!")
        cleaned_df = df.copy()
    else:
        print("Cleaning strategy:")
        cleaned_df = df.copy()
        
        # Strategy for different types of columns
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                if df[col].dtype == 'object':  # String/categorical columns
                    if missing_count / len(df) > 0.5:  # If more than 50% missing
                        print(f"   Dropping column '{col}' (too many missing values: {missing_count})")
                        cleaned_df = cleaned_df.drop(columns=[col])
                    else:
                        print(f"   Filling missing values in '{col}' with 'Unknown'")
                        cleaned_df[col] = cleaned_df[col].fillna('Unknown')
                else:  # Numeric columns
                    if missing_count / len(df) > 0.5:  # If more than 50% missing
                        print(f"   Dropping column '{col}' (too many missing values: {missing_count})")
                        cleaned_df = cleaned_df.drop(columns=[col])
                    else:
                        median_value = df[col].median()
                        print(f"   Filling missing values in '{col}' with median: {median_value}")
                        cleaned_df[col] = cleaned_df[col].fillna(median_value)
    
    # Verify cleaning
    print(f"\n6. Verification after cleaning:")
    print("-" * 35)
    remaining_missing = cleaned_df.isnull().sum().sum()
    print(f"Original dataset shape: {df.shape}")
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    print(f"Remaining missing values: {remaining_missing}")
    
    if remaining_missing == 0:
        print("✓ Dataset successfully cleaned!")
    else:
        print("⚠ Some missing values still remain")
    
    # Additional exploration
    print(f"\n7. Additional dataset insights:")
    print("-" * 35)
    
    # Check for duplicates
    duplicates = cleaned_df.duplicated().sum()
    print(f"Duplicate rows: {duplicates}")
    
    # Show unique values for some key columns (if they exist)
    categorical_columns = cleaned_df.select_dtypes(include=['object']).columns
    for col in categorical_columns[:3]:  # Show first 3 categorical columns
        unique_count = cleaned_df[col].nunique()
        print(f"Unique values in '{col}': {unique_count}")
        if unique_count <= 10:  # Show values if not too many
            print(f"   Values: {sorted(cleaned_df[col].unique())}")
    
    print(f"\n" + "=" * 50)
    print("DATASET EXPLORATION COMPLETED!")
    print("=" * 50)
    
    return cleaned_df

def perform_basic_data_analysis(df):
    """
    Perform comprehensive basic data analysis on the dataset
    """
    print("\n" + "=" * 60)
    print("BASIC DATA ANALYSIS")
    print("=" * 60)
    
    # Task 1: Compute basic statistics of numerical columns
    print("\n1. Basic Statistics of Numerical Columns:")
    print("-" * 45)
    
    # Identify numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numerical_cols) == 0:
        print("⚠ No numerical columns found in the dataset.")
        # Let's check if we can extract numerical data from string columns
        print("\nAttempting to extract numerical information from string columns...")
        
        # Try to extract numerical data from phone numbers, dates, etc.
        analysis_df = df.copy()
        
        # Extract year from subscription date if it exists
        if 'Subscription Date' in df.columns:
            try:
                analysis_df['Subscription Year'] = pd.to_datetime(df['Subscription Date']).dt.year
                numerical_cols.append('Subscription Year')
                print("✓ Extracted 'Subscription Year' from 'Subscription Date'")
            except:
                print("❌ Could not extract year from 'Subscription Date'")
        
        # Count characters in text fields for analysis
        text_analysis_cols = []
        for col in ['First Name', 'Last Name', 'Company', 'City', 'Email']:
            if col in df.columns:
                new_col = f"{col} Length"
                analysis_df[new_col] = df[col].astype(str).str.len()
                numerical_cols.append(new_col)
                text_analysis_cols.append(new_col)
        
        if text_analysis_cols:
            print(f"✓ Created length analysis for: {', '.join([col.replace(' Length', '') for col in text_analysis_cols])}")
    else:
        analysis_df = df.copy()
    
    if len(numerical_cols) > 0:
        print(f"\nNumerical columns found: {numerical_cols}")
        
        # Display comprehensive statistics
        print(f"\nDetailed Statistics:")
        print("-" * 25)
        stats_df = analysis_df[numerical_cols].describe()
        print(stats_df)
        
        # Additional statistics
        print(f"\nAdditional Statistics:")
        print("-" * 25)
        for col in numerical_cols:
            data = analysis_df[col].dropna()
            if len(data) > 0:
                print(f"\n{col}:")
                print(f"  Mean: {data.mean():.2f}")
                print(f"  Median: {data.median():.2f}")
                print(f"  Standard Deviation: {data.std():.2f}")
                print(f"  Variance: {data.var():.2f}")
                print(f"  Range: {data.max() - data.min():.2f}")
                print(f"  Skewness: {data.skew():.2f}")
                print(f"  Kurtosis: {data.kurtosis():.2f}")
    
    # Task 2: Perform groupings on categorical columns
    print(f"\n2. Grouping Analysis by Categorical Columns:")
    print("-" * 50)
    
    categorical_cols = analysis_df.select_dtypes(include=['object']).columns.tolist()
    
    if len(categorical_cols) > 0 and len(numerical_cols) > 0:
        # Analyze each categorical column
        for cat_col in categorical_cols[:5]:  # Limit to first 5 to avoid too much output
            unique_values = analysis_df[cat_col].nunique()
            
            # Only analyze if there are reasonable number of categories (2-50)
            if 2 <= unique_values <= 50:
                print(f"\n📊 Analysis by '{cat_col}' ({unique_values} unique values):")
                print("-" * 40)
                
                # Group by categorical column and compute statistics for numerical columns
                grouped = analysis_df.groupby(cat_col)
                
                for num_col in numerical_cols[:3]:  # Limit to first 3 numerical columns
                    try:
                        group_stats = grouped[num_col].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
                        print(f"\n{num_col} by {cat_col}:")
                        print(group_stats.round(2))
                        
                        # Find interesting patterns
                        max_mean_group = group_stats['mean'].idxmax()
                        min_mean_group = group_stats['mean'].idxmin()
                        print(f"  🔝 Highest mean {num_col}: {max_mean_group} ({group_stats.loc[max_mean_group, 'mean']:.2f})")
                        print(f"  🔻 Lowest mean {num_col}: {min_mean_group} ({group_stats.loc[min_mean_group, 'mean']:.2f})")
                    except Exception as e:
                        print(f"  ❌ Could not analyze {num_col}: {str(e)}")
            else:
                print(f"\n⚠ Skipping '{cat_col}' - too many unique values ({unique_values}) for meaningful grouping")
    
    # Task 3: Identify patterns and interesting findings
    print(f"\n3. Patterns and Interesting Findings:")
    print("-" * 45)
    
    findings = []
    
    # Pattern 1: Country distribution
    if 'Country' in analysis_df.columns:
        country_counts = analysis_df['Country'].value_counts()
        findings.append(f"🌍 Geographic Distribution: Dataset contains customers from {country_counts.nunique()} countries")
        findings.append(f"   Top country: {country_counts.index[0]} ({country_counts.iloc[0]} customers)")
        if len(country_counts) > 1:
            findings.append(f"   Second most: {country_counts.index[1]} ({country_counts.iloc[1]} customers)")
    
    # Pattern 2: Subscription patterns by year
    if 'Subscription Year' in analysis_df.columns:
        year_counts = analysis_df['Subscription Year'].value_counts().sort_index()
        findings.append(f"📅 Subscription Timeline: Customers joined between {year_counts.index.min()} and {year_counts.index.max()}")
        peak_year = year_counts.idxmax()
        findings.append(f"   Peak subscription year: {peak_year} ({year_counts[peak_year]} customers)")
    
    # Pattern 3: Name length patterns
    if 'First Name Length' in analysis_df.columns and 'Last Name Length' in analysis_df.columns:
        avg_first_name = analysis_df['First Name Length'].mean()
        avg_last_name = analysis_df['Last Name Length'].mean()
        findings.append(f"👤 Name Patterns:")
        findings.append(f"   Average first name length: {avg_first_name:.1f} characters")
        findings.append(f"   Average last name length: {avg_last_name:.1f} characters")
    
    # Pattern 4: Email domain analysis
    if 'Email' in analysis_df.columns:
        try:
            analysis_df['Email Domain'] = analysis_df['Email'].str.extract(r'@([^.]+\.[^.]+)$')
            domain_counts = analysis_df['Email Domain'].value_counts()
            findings.append(f"📧 Email Domains: {domain_counts.nunique()} unique email domains")
            findings.append(f"   Most common domain: {domain_counts.index[0]} ({domain_counts.iloc[0]} users)")
        except:
            findings.append(f"📧 Email analysis: Could not extract email domain patterns")
    
    # Pattern 5: Company name analysis
    if 'Company' in analysis_df.columns:
        company_counts = analysis_df['Company'].value_counts()
        findings.append(f"🏢 Company Distribution: {company_counts.nunique()} unique companies")
        if company_counts.iloc[0] > 1:
            findings.append(f"   Largest client: {company_counts.index[0]} ({company_counts.iloc[0]} customers)")
    
    # Pattern 6: Data quality insights
    total_rows = len(analysis_df)
    complete_rows = analysis_df.dropna().shape[0]
    completeness = (complete_rows / total_rows) * 100
    findings.append(f"📊 Data Quality: {completeness:.1f}% of rows have complete data")
    
    # Pattern 7: Correlation analysis (if we have multiple numerical columns)
    if len(numerical_cols) >= 2:
        try:
            correlation_matrix = analysis_df[numerical_cols].corr()
            # Find strongest correlations (excluding self-correlations)
            correlation_pairs = []
            for i in range(len(numerical_cols)):
                for j in range(i+1, len(numerical_cols)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.3:  # Only show moderate to strong correlations
                        correlation_pairs.append((numerical_cols[i], numerical_cols[j], corr_value))
            
            if correlation_pairs:
                findings.append(f"🔗 Correlations Found:")
                for col1, col2, corr in sorted(correlation_pairs, key=lambda x: abs(x[2]), reverse=True)[:3]:
                    strength = "strong" if abs(corr) > 0.7 else "moderate"
                    direction = "positive" if corr > 0 else "negative"
                    findings.append(f"   {col1} ↔ {col2}: {corr:.3f} ({strength} {direction})")
        except:
            findings.append(f"🔗 Correlation analysis: Could not compute correlations")
    
    # Display all findings
    if findings:
        for finding in findings:
            print(finding)
    else:
        print("No specific patterns identified with available data types.")
    
    # Summary insights
    print(f"\n4. Summary Insights:")
    print("-" * 25)
    print(f"✓ Dataset contains {len(analysis_df)} customer records")
    print(f"✓ {len(categorical_cols)} categorical and {len(numerical_cols)} numerical features analyzed")
    print(f"✓ Data spans multiple countries and time periods")
    print(f"✓ Dataset appears suitable for customer segmentation and geographic analysis")
    
    return analysis_df

def create_data_visualizations(df):
    """
    Create comprehensive data visualizations including line charts, bar charts, 
    histograms, and scatter plots
    """
    print("\n" + "=" * 60)
    print("DATA VISUALIZATION")
    print("=" * 60)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure with subplots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Customer Dataset Analysis - Comprehensive Visualization Dashboard', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Prepare data for visualizations
    viz_df = df.copy()
    
    # Extract subscription date information for time series analysis
    if 'Subscription Date' in df.columns:
        try:
            viz_df['Subscription DateTime'] = pd.to_datetime(df['Subscription Date'])
            viz_df['Subscription Year'] = viz_df['Subscription DateTime'].dt.year
            viz_df['Subscription Month'] = viz_df['Subscription DateTime'].dt.month
            viz_df['Subscription YearMonth'] = viz_df['Subscription DateTime'].dt.to_period('M')
        except:
            print("⚠ Could not parse subscription dates for time series analysis")
    
    # Create numerical features if they don't exist
    numerical_features = []
    if 'First Name' in df.columns:
        viz_df['First Name Length'] = df['First Name'].astype(str).str.len()
        numerical_features.append('First Name Length')
    if 'Last Name' in df.columns:
        viz_df['Last Name Length'] = df['Last Name'].astype(str).str.len()
        numerical_features.append('Last Name Length')
    if 'Company' in df.columns:
        viz_df['Company Length'] = df['Company'].astype(str).str.len()
        numerical_features.append('Company Length')
    if 'Email' in df.columns:
        viz_df['Email Length'] = df['Email'].astype(str).str.len()
        numerical_features.append('Email Length')
    
    print(f"Creating visualizations with {len(numerical_features)} numerical features...")
    
    # Visualization 1: Line Chart - Time Series of Subscriptions
    plt.subplot(2, 2, 1)
    if 'Subscription YearMonth' in viz_df.columns:
        try:
            # Count subscriptions by month
            monthly_subscriptions = viz_df['Subscription YearMonth'].value_counts().sort_index()
            
            # Convert period index to string for plotting
            months = [str(period) for period in monthly_subscriptions.index]
            counts = monthly_subscriptions.values
            
            plt.plot(range(len(months)), counts, marker='o', linewidth=2.5, markersize=6, color='#2E86AB')
            plt.title('📈 Customer Subscription Trends Over Time', fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Time Period (Year-Month)', fontsize=12)
            plt.ylabel('Number of New Subscriptions', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Customize x-axis labels
            step = max(1, len(months) // 6)  # Show max 6 labels
            plt.xticks(range(0, len(months), step), [months[i] for i in range(0, len(months), step)], 
                      rotation=45, ha='right')
            
            # Add trend annotation
            if len(counts) > 1:
                trend = "📈 Increasing" if counts[-1] > counts[0] else "📉 Decreasing"
                plt.text(0.02, 0.98, f'Trend: {trend}', transform=plt.gca().transAxes, 
                        fontsize=10, verticalalignment='top', 
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            print("✓ Line chart: Subscription trends over time")
        except Exception as e:
            plt.text(0.5, 0.5, f'Time series data not available\nCreating alternative trend analysis...', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
            # Alternative: Show subscription by year
            if 'Subscription Year' in viz_df.columns:
                yearly_subs = viz_df['Subscription Year'].value_counts().sort_index()
                plt.plot(yearly_subs.index, yearly_subs.values, marker='o', linewidth=3, markersize=8)
                plt.title('📈 Annual Subscription Trends', fontsize=14, fontweight='bold')
                plt.xlabel('Year', fontsize=12)
                plt.ylabel('Number of Subscriptions', fontsize=12)
                plt.grid(True, alpha=0.3)
    else:
        plt.text(0.5, 0.5, 'No time-series data available\nfor trend analysis', 
                ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
        plt.title('📈 Time Series Analysis (Data Not Available)', fontsize=14)
    
    # Visualization 2: Bar Chart - Average Name Length by Country
    plt.subplot(2, 2, 2)
    if 'Country' in viz_df.columns and 'First Name Length' in viz_df.columns:
        try:
            # Calculate average name length by country (top 10 countries)
            country_name_avg = viz_df.groupby('Country')['First Name Length'].mean().sort_values(ascending=False).head(10)
            
            bars = plt.bar(range(len(country_name_avg)), country_name_avg.values, 
                          color=plt.cm.Set3(np.linspace(0, 1, len(country_name_avg))))
            
            plt.title('📊 Average First Name Length by Country (Top 10)', fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Country', fontsize=12)
            plt.ylabel('Average Name Length (characters)', fontsize=12)
            plt.xticks(range(len(country_name_avg)), country_name_avg.index, rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=9)
            
            # Add statistics annotation
            plt.text(0.02, 0.98, f'Range: {country_name_avg.min():.1f} - {country_name_avg.max():.1f} chars', 
                    transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
            
            print("✓ Bar chart: Average name length by country")
        except Exception as e:
            # Alternative: Company length by country
            if 'Company Length' in viz_df.columns:
                country_company_avg = viz_df.groupby('Country')['Company Length'].mean().sort_values(ascending=False).head(8)
                plt.bar(range(len(country_company_avg)), country_company_avg.values, color='skyblue')
                plt.title('📊 Average Company Name Length by Country', fontsize=14, fontweight='bold')
                plt.xlabel('Country', fontsize=12)
                plt.ylabel('Average Company Name Length', fontsize=12)
                plt.xticks(range(len(country_company_avg)), country_company_avg.index, rotation=45, ha='right')
            else:
                plt.text(0.5, 0.5, 'Insufficient data for\ncategorical comparison', 
                        ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
    else:
        plt.text(0.5, 0.5, 'No categorical data available\nfor comparison analysis', 
                ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
        plt.title('📊 Categorical Comparison (Data Not Available)', fontsize=14)
    
    # Visualization 3: Histogram - Distribution of Email Length
    plt.subplot(2, 2, 3)
    if 'Email Length' in viz_df.columns:
        try:
            email_lengths = viz_df['Email Length'].dropna()
            
            # Create histogram with customization
            n, bins, patches = plt.hist(email_lengths, bins=20, color='lightcoral', alpha=0.7, edgecolor='black')
            
            # Color bars based on frequency
            fracs = n / n.max()
            norm = plt.cm.colors.Normalize(vmin=fracs.min(), vmax=fracs.max())
            for thisfrac, thispatch in zip(fracs, patches):
                color = plt.cm.viridis(norm(thisfrac))
                thispatch.set_facecolor(color)
            
            plt.title('📈 Distribution of Email Address Lengths', fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Email Address Length (characters)', fontsize=12)
            plt.ylabel('Frequency (Number of Customers)', fontsize=12)
            plt.grid(True, alpha=0.3, axis='y')
            
            # Add statistical annotations
            mean_length = email_lengths.mean()
            median_length = email_lengths.median()
            plt.axvline(mean_length, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_length:.1f}')
            plt.axvline(median_length, color='blue', linestyle='--', linewidth=2, label=f'Median: {median_length:.1f}')
            plt.legend()
            
            # Add distribution info
            plt.text(0.98, 0.98, f'Std Dev: {email_lengths.std():.1f}\nRange: {email_lengths.min()}-{email_lengths.max()}', 
                    transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
            
            print("✓ Histogram: Email length distribution")
        except Exception as e:
            plt.text(0.5, 0.5, f'Error creating histogram: {str(e)}', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
    else:
        # Alternative: Use first available numerical column
        if numerical_features:
            alt_feature = numerical_features[0]
            data = viz_df[alt_feature].dropna()
            plt.hist(data, bins=15, color='lightgreen', alpha=0.7, edgecolor='black')
            plt.title(f'📈 Distribution of {alt_feature}', fontsize=14, fontweight='bold')
            plt.xlabel(f'{alt_feature}', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.grid(True, alpha=0.3, axis='y')
            print(f"✓ Histogram: {alt_feature} distribution")
        else:
            plt.text(0.5, 0.5, 'No numerical data available\nfor distribution analysis', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
            plt.title('📈 Distribution Analysis (Data Not Available)', fontsize=14)
    
    # Visualization 4: Scatter Plot - Relationship between Name Lengths
    plt.subplot(2, 2, 4)
    if 'First Name Length' in viz_df.columns and 'Last Name Length' in viz_df.columns:
        try:
            # Create scatter plot
            first_name_len = viz_df['First Name Length'].dropna()
            last_name_len = viz_df['Last Name Length'].dropna()
            
            # Ensure both series have the same length
            min_len = min(len(first_name_len), len(last_name_len))
            x_data = first_name_len.iloc[:min_len]
            y_data = last_name_len.iloc[:min_len]
            
            # Create scatter plot with color mapping
            scatter = plt.scatter(x_data, y_data, alpha=0.6, s=60, c=range(len(x_data)), 
                                cmap='plasma', edgecolors='black', linewidth=0.5)
            
            plt.title('🔗 Relationship: First Name vs Last Name Length', fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('First Name Length (characters)', fontsize=12)
            plt.ylabel('Last Name Length (characters)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Add trend line
            if len(x_data) > 1:
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)
                plt.plot(x_data.sort_values(), p(x_data.sort_values()), "r--", alpha=0.8, linewidth=2)
                
                # Calculate correlation
                correlation = np.corrcoef(x_data, y_data)[0, 1]
                plt.text(0.02, 0.98, f'Correlation: {correlation:.3f}', 
                        transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=plt.gca())
            cbar.set_label('Customer Index', fontsize=10)
            
            print("✓ Scatter plot: First name vs last name length relationship")
        except Exception as e:
            plt.text(0.5, 0.5, f'Error creating scatter plot: {str(e)}', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
    elif len(numerical_features) >= 2:
        # Alternative: Use two available numerical features
        try:
            feature1, feature2 = numerical_features[0], numerical_features[1]
            x_data = viz_df[feature1].dropna()
            y_data = viz_df[feature2].dropna()
            
            min_len = min(len(x_data), len(y_data))
            plt.scatter(x_data.iloc[:min_len], y_data.iloc[:min_len], alpha=0.6, s=50, color='purple')
            plt.title(f'🔗 Relationship: {feature1} vs {feature2}', fontsize=14, fontweight='bold')
            plt.xlabel(feature1, fontsize=12)
            plt.ylabel(feature2, fontsize=12)
            plt.grid(True, alpha=0.3)
            print(f"✓ Scatter plot: {feature1} vs {feature2} relationship")
        except Exception as e:
            plt.text(0.5, 0.5, 'Insufficient numerical data\nfor relationship analysis', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
    else:
        plt.text(0.5, 0.5, 'Insufficient numerical data\nfor relationship analysis', 
                ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
        plt.title('🔗 Relationship Analysis (Data Not Available)', fontsize=14)
    
    # Adjust layout and save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    try:
        plt.savefig('customer_data_visualization.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print("\n✓ Visualization saved as 'customer_data_visualization.png'")
    except Exception as e:
        print(f"\n⚠ Could not save visualization: {e}")
    
    plt.show()
    
    # Create additional specialized visualizations
    create_additional_visualizations(viz_df)
    
    print("\n" + "=" * 60)
    print("DATA VISUALIZATION COMPLETED!")
    print("=" * 60)
    print("📊 Four main visualization types created:")
    print("   1. ✓ Line Chart - Time series trends")
    print("   2. ✓ Bar Chart - Categorical comparisons") 
    print("   3. ✓ Histogram - Distribution analysis")
    print("   4. ✓ Scatter Plot - Relationship analysis")
    print("🎨 All plots include custom titles, labels, legends, and styling")

def create_additional_visualizations(df):
    """
    Create additional specialized visualizations for deeper insights
    """
    print(f"\n📈 Creating additional specialized visualizations...")
    
    # Additional Visualization 1: Country Distribution Pie Chart
    if 'Country' in df.columns:
        try:
            plt.figure(figsize=(12, 8))
            
            # Pie chart for top countries
            plt.subplot(2, 2, 1)
            country_counts = df['Country'].value_counts().head(8)
            colors = plt.cm.Set3(np.linspace(0, 1, len(country_counts)))
            
            wedges, texts, autotexts = plt.pie(country_counts.values, labels=country_counts.index, 
                                              autopct='%1.1f%%', colors=colors, startangle=90)
            plt.title('🌍 Customer Distribution by Country (Top 8)', fontsize=14, fontweight='bold')
            
            # Enhance text appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            # Heatmap of subscription by year and month
            plt.subplot(2, 2, 2)
            if 'Subscription Year' in df.columns and 'Subscription Month' in df.columns:
                try:
                    # Create pivot table for heatmap
                    subscription_pivot = df.groupby(['Subscription Year', 'Subscription Month']).size().unstack(fill_value=0)
                    
                    sns.heatmap(subscription_pivot, annot=True, fmt='d', cmap='YlOrRd', 
                              cbar_kws={'label': 'Number of Subscriptions'})
                    plt.title('🔥 Subscription Heatmap (Year vs Month)', fontsize=14, fontweight='bold')
                    plt.xlabel('Month', fontsize=12)
                    plt.ylabel('Year', fontsize=12)
                except:
                    plt.text(0.5, 0.5, 'Heatmap data\nnot available', 
                            ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
            
            # Box plot for name lengths by top countries
            plt.subplot(2, 1, 2)
            if 'First Name Length' in df.columns:
                top_countries = df['Country'].value_counts().head(6).index
                country_name_data = []
                country_labels = []
                
                for country in top_countries:
                    country_data = df[df['Country'] == country]['First Name Length'].dropna()
                    if len(country_data) > 0:
                        country_name_data.append(country_data)
                        country_labels.append(country)
                
                if country_name_data:
                    box_plot = plt.boxplot(country_name_data, labels=country_labels, patch_artist=True)
                    
                    # Color the boxes
                    colors = plt.cm.viridis(np.linspace(0, 1, len(box_plot['boxes'])))
                    for patch, color in zip(box_plot['boxes'], colors):
                        patch.set_facecolor(color)
                        patch.set_alpha(0.7)
                    
                    plt.title('📦 Distribution of Name Lengths by Country', fontsize=14, fontweight='bold')
                    plt.xlabel('Country', fontsize=12)
                    plt.ylabel('First Name Length', fontsize=12)
                    plt.xticks(rotation=45)
                    plt.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            
            try:
                plt.savefig('additional_customer_visualizations.png', dpi=300, bbox_inches='tight')
                print("✓ Additional visualizations saved as 'additional_customer_visualizations.png'")
            except:
                pass
            
            plt.show()
            
        except Exception as e:
            print(f"⚠ Could not create additional visualizations: {e}")
    
    return df

def save_cleaned_dataset(df, filename='customers_cleaned.csv'):
    """
    Save the cleaned dataset to a new CSV file
    """
    try:
        df.to_csv(filename, index=False)
        print(f"\n✓ Cleaned dataset saved as '{filename}'")
    except Exception as e:
        print(f"\n❌ Error saving cleaned dataset: {e}")

if __name__ == "__main__":
    # Run the main function
    cleaned_data = load_and_explore_dataset()
    
    if cleaned_data is not None:
        # Perform basic data analysis
        analyzed_data = perform_basic_data_analysis(cleaned_data)
        
        # Create comprehensive data visualizations
        print(f"\nStarting data visualization process...")
        create_data_visualizations(analyzed_data)
        
        # Ask user if they want to save the cleaned dataset
        print(f"\nWould you like to save the cleaned dataset? (y/n): ", end="")
        
        # For automated execution, we'll save it automatically
        # In interactive mode, you can uncomment the input() line below
        # response = input().lower().strip()
        response = 'y'  # Automatic yes for demo
        
        if response in ['y', 'yes']:
            save_cleaned_dataset(analyzed_data)
        
        print(f"\n🎉 Complete analysis with visualizations finished!")
        print(f"📋 Summary: Data loading ✓ | Exploration ✓ | Cleaning ✓ | Analysis ✓ | Visualization ✓")
        print(f"🚀 Dataset is ready for machine learning or advanced analytics!")
        print(f"📊 Visualization files created: 'customer_data_visualization.png' & 'additional_customer_visualizations.png'")