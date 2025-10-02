# Week 7 Python Assignment: Complete Data Analysis and Visualization

## Task Overview
This comprehensive assignment focuses on loading, exploring, analyzing, and visualizing a customer dataset using pandas, matplotlib, and seaborn. The main objectives are to:

1. **Load the dataset** using pandas
2. **Display the first few rows** using `.head()` to inspect the data
3. **Explore the structure** of the dataset by checking data types and missing values
4. **Clean the dataset** by handling any missing values
5. **Perform basic data analysis** including:
   - Compute basic statistics of numerical columns using `.describe()`
   - Perform groupings on categorical columns and compute statistics
   - Identify patterns and interesting findings from the analysis
6. **Create comprehensive data visualizations** including:
   - Line chart showing trends over time (subscription patterns)
   - Bar chart comparing numerical values across categories
   - Histogram showing distribution of numerical data
   - Scatter plot visualizing relationships between variables
   - Additional specialized visualizations

## Dataset
- **File**: `customers-100.csv`
- **Description**: A dataset containing customer information including names, companies, contact details, and subscription dates
- **Size**: 100+ rows with multiple columns

## Files
- `customers-100.csv` - The original dataset
- `load_and_explore_dataset.py` - Main Python script for the assignment
- `README.md` - This documentation file

## Requirements
Make sure you have the following Python packages installed:
```bash
pip install pandas numpy matplotlib seaborn
```

**Required Libraries:**
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Basic plotting and visualization
- `seaborn` - Statistical data visualization
- `datetime` - Date and time handling (built-in)

## How to Run
1. Open a terminal/command prompt
2. Navigate to the `week7-python-assignment` directory
3. Run the script:
   ```bash
   python load_and_explore_dataset.py
   ```

## What the Script Does

### 1. Load Dataset
- Uses `pandas.read_csv()` to load the customer data
- Displays basic information about the dataset dimensions

### 2. Display Data
- Shows the first 5 rows using `.head()`
- Also displays the last 5 rows using `.tail()` for completeness

### 3. Explore Structure
- Lists all column names
- Shows data types for each column
- Provides dataset info using `.info()`
- Generates basic statistics using `.describe()`

### 4. Check Missing Values
- Identifies any missing values in the dataset
- Calculates percentages of missing data per column

### 5. Clean Dataset
- Implements a smart cleaning strategy:
  - For string/categorical columns: fills missing values with 'Unknown'
  - For numeric columns: fills missing values with the median
  - Drops columns with more than 50% missing values
- Removes any duplicate rows if found

### 6. Additional Insights
- Checks for duplicate rows
- Shows unique value counts for categorical columns
- Provides summary of the cleaning process

### 7. Basic Data Analysis
- **Statistical Analysis**: Computes comprehensive statistics for numerical columns
  - Mean, median, standard deviation, variance, range
  - Skewness and kurtosis for distribution analysis
  - Creates numerical features from text data (e.g., name lengths, subscription years)
- **Grouping Analysis**: Groups data by categorical columns and analyzes:
  - Country-based customer distribution
  - Company-based customer segmentation
  - Time-based subscription patterns
- **Pattern Recognition**: Identifies interesting findings such as:
  - Geographic distribution patterns
  - Subscription timeline trends
  - Email domain analysis
  - Name length patterns
  - Data quality insights
  - Correlation analysis between numerical variables

### 8. Data Visualization
- **Line Chart**: Time series analysis of customer subscriptions over time
  - Shows subscription trends by month/year
  - Includes trend annotations and statistical overlays
  - Custom styling with markers and grid lines
- **Bar Chart**: Comparative analysis across categories
  - Average name lengths by country (top 10 countries)
  - Color-coded bars with value labels
  - Statistical annotations and ranges
- **Histogram**: Distribution analysis of numerical data
  - Email address length distribution
  - Color-coded frequency bars
  - Mean and median lines with statistical info
- **Scatter Plot**: Relationship analysis between variables
  - First name vs last name length correlation
  - Color-mapped points with trend lines
  - Correlation coefficient display
- **Additional Visualizations**:
  - Pie chart for country distribution
  - Heatmap for subscription patterns by year/month
  - Box plots for name length distributions by country

## Output
The script will:
- Display comprehensive analysis results in the terminal
- **Generate visualization files**:
  - `customer_data_visualization.png` - Main dashboard with 4 core visualizations
  - `additional_customer_visualizations.png` - Specialized charts and plots
- Optionally save a cleaned version as `customers_cleaned.csv`
- Provide detailed feedback on each step of the process

## Expected Learning Outcomes
After completing this assignment, you should understand:
- How to load CSV files using pandas
- Basic data exploration techniques
- How to identify and handle missing values
- Data cleaning best practices
- How to verify data quality after cleaning
- **Statistical analysis of numerical data**
- **Grouping and aggregation techniques**
- **Pattern recognition in datasets**
- **Creating derived features from existing data**
- **Correlation analysis between variables**
- **Data visualization principles and best practices**
- **Creating line charts for time series analysis**
- **Building bar charts for categorical comparisons**
- **Generating histograms for distribution analysis**
- **Developing scatter plots for relationship analysis**
- **Customizing plots with titles, labels, legends, and styling**
- **Saving and exporting visualizations for reports**

## Sample Output Structure
```
==================================================
LOAD AND EXPLORE THE DATASET
==================================================

1. Loading the dataset...
✓ Dataset loaded successfully!
   Dataset shape: (100, 12) (rows: 100, columns: 12)

2. Displaying the first few rows of the dataset:
[DataFrame display]

3. Exploring the structure of the dataset:
[Column info, data types, statistics]

4. Checking for missing values:
[Missing value analysis]

5. Cleaning the dataset:
[Cleaning process and results]

6. Verification after cleaning:
[Final verification]

============================================================
BASIC DATA ANALYSIS
============================================================

1. Basic Statistics of Numerical Columns:
[Detailed statistics with mean, median, std, etc.]

2. Grouping Analysis by Categorical Columns:
[Country-based analysis, company groupings, etc.]

3. Patterns and Interesting Findings:
🌍 Geographic Distribution: Dataset contains customers from X countries
📅 Subscription Timeline: Customers joined between YYYY and YYYY
👤 Name Patterns: Average lengths and characteristics
📧 Email Domains: Domain distribution analysis
🏢 Company Distribution: Business customer patterns
📊 Data Quality: Completeness metrics
🔗 Correlations Found: Relationships between variables

4. Summary Insights:
[Overall analysis summary]

============================================================
DATA VISUALIZATION
============================================================

Creating visualizations with X numerical features...
✓ Line chart: Subscription trends over time
✓ Bar chart: Average name length by country  
✓ Histogram: Email length distribution
✓ Scatter plot: First name vs last name length relationship
✓ Visualization saved as 'customer_data_visualization.png'

📈 Creating additional specialized visualizations...
✓ Additional visualizations saved as 'additional_customer_visualizations.png'

============================================================
DATA VISUALIZATION COMPLETED!
============================================================
📊 Four main visualization types created:
   1. ✓ Line Chart - Time series trends
   2. ✓ Bar Chart - Categorical comparisons
   3. ✓ Histogram - Distribution analysis  
   4. ✓ Scatter Plot - Relationship analysis
🎨 All plots include custom titles, labels, legends, and styling
```

---
*This assignment is part of the Python Learning Path (PLP) curriculum.*