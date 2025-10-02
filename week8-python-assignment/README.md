# COVID-19 Research Analytics Dashboard 🔬

A comprehensive data analysis and visualization platform for exploring COVID-19 research publications from the CORD-19 dataset. This project provides both a command-line analysis pipeline and an interactive Streamlit web dashboard.

## 📊 Project Overview

This project analyzes the CORD-19 Research Challenge dataset from Kaggle, which contains over 1 million COVID-19 research papers. The analysis includes publication trends, journal distributions, research collaboration patterns, and text analysis of paper titles and abstracts.

### 🎯 Key Features

- **Complete Data Pipeline**: From raw data loading to publication-ready visualizations
- **Missing Data Handling**: Intelligent strategies for dealing with incomplete data
- **Temporal Analysis**: Publication trends over time with COVID-19 period highlighting
- **Journal Analytics**: Top publishers and publication patterns
- **Text Analysis**: Word clouds and frequency analysis of research titles
- **Interactive Dashboard**: Streamlit-based web interface with filters and controls
- **Data Quality Assessment**: Comprehensive data completeness scoring

## 📁 Repository Structure

```
├── index.py                 # Main analysis pipeline script
├── streamlit_app.py         # Interactive Streamlit dashboard
├── create_sample.py         # Script to create sample dataset
├── metadata_sample.csv      # Sample dataset (200 records) for testing
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📈 Dataset Information

### Original Dataset
- **Source**: [CORD-19 Research Challenge (Kaggle)](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge?resource=download&select=metadata.csv)
- **Size**: 1,056,660 rows × 19 columns
- **File Size**: ~1.6 GB
- **Content**: COVID-19 research paper metadata including titles, authors, abstracts, publication dates, and journal information

### Sample Dataset (Included)
- **File**: `metadata_sample.csv`
- **Size**: 200 rows × 19 columns  
- **Purpose**: Testing and demonstration without downloading the full dataset
- **Note**: This sample contains the first 200 records from the original dataset

### Data Columns
- `cord_uid`: Unique paper identifier
- `title`: Paper title
- `authors`: Author names (semicolon-separated)
- `abstract`: Paper abstract
- `publish_time`: Publication date
- `journal`: Journal name
- `doi`: Digital Object Identifier
- `source_x`: Data source
- And 11 additional metadata columns

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation


1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the dataset** (Choose one option)

   **Option A: Use the sample dataset (Recommended for testing)**
   - The repository includes `metadata_sample.csv` with 200 records
   - Perfect for testing functionality without large downloads

   **Option B: Download the full dataset**
   - Download `metadata.csv` from [Kaggle](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge?resource=download&select=metadata.csv)
   - Place it in the project root directory
   - Note: File is ~1.6 GB

### Usage

#### Command Line Analysis
Run the complete analysis pipeline:
```bash
python index.py
```

This will:
- Load and examine the dataset
- Perform data exploration and quality assessment
- Handle missing values intelligently
- Create analytical features (publication years, word counts, etc.)
- Generate statistical insights
- Create and save visualizations

#### Interactive Dashboard
Launch the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

Then open your browser to the displayed URL (typically `http://localhost:8501`)

## 📊 Analysis Pipeline

### 1. Data Loading and Examination
- Loads metadata and displays basic information
- Shows dataset dimensions, data types, and memory usage
- Provides sample data preview

### 2. Basic Data Exploration  
- Analyzes data completeness for important columns
- Identifies numerical vs categorical features
- Calculates missing data percentages
- Generates data quality indicators

### 3. Missing Data Handling
- **Automatic Strategy**: Intelligently handles missing values based on data types and missing percentages
- **Column Removal**: Drops columns with >90% missing data
- **Smart Imputation**: Fills missing values with appropriate strategies (median for numbers, mode for text)
- **Data Quality Scoring**: Creates completeness scores for each record

### 4. Data Preparation for Analysis
- **Date Processing**: Converts publication dates to datetime format
- **Feature Engineering**: Extracts years, months, and day-of-year for temporal analysis
- **Text Analysis**: Creates word counts and length categories for abstracts and titles
- **Collaboration Metrics**: Analyzes author counts and team sizes
- **Quality Indicators**: Adds data completeness and quality categories

### 5. Statistical Analysis
- **Publication Trends**: Papers published by year with COVID-19 period analysis
- **Journal Analysis**: Top publishers and publication patterns
- **Text Mining**: Word frequency analysis of paper titles
- **Source Distribution**: Analysis of data sources and their contributions

### 6. Visualizations
- **Timeline Plots**: Publication trends over time
- **Bar Charts**: Top journals and publishers
- **Word Clouds**: Most frequent terms in paper titles
- **Distribution Charts**: Source and categorical data analysis

## 🎛️ Dashboard Features

The Streamlit dashboard provides:

### Interactive Controls
- **Year Range Slider**: Filter papers by publication year
- **Journal Filter**: Select specific journals to analyze
- **Source Filter**: Filter by data source
- **Top N Selector**: Adjust number of items displayed in charts

### Visualization Tabs
1. **📊 Overview**: Key metrics and data completeness analysis
2. **📈 Publications Over Time**: Temporal trends with COVID-19 highlighting
3. **📚 Journal Analysis**: Top publishers and productivity categories
4. **☁️ Word Cloud**: Interactive text analysis of paper titles
5. **📄 Data Sample**: Explore raw data with column selection

### Real-time Filtering
All visualizations update automatically based on selected filters, allowing for dynamic exploration of different data subsets.

## 📈 Key Findings and Insights

### Publication Trends
- **Massive Growth**: Significant increase in COVID-19 research publications from 2020 onwards
- **Peak Years**: 2020-2021 saw unprecedented research output
- **Research Acceleration**: The pandemic accelerated scientific publication timelines

### Journal Landscape
- **Top Publishers**: Identified leading journals in COVID-19 research
- **Publication Concentration**: Top 5 journals account for a significant portion of publications
- **Journal Diversity**: Research spans across multiple disciplines and specialized journals

### Research Characteristics
- **Collaboration Patterns**: Average of 4-6 authors per paper, indicating high collaboration
- **Abstract Length**: Papers average 150-200 words in abstracts
- **Research Topics**: Analysis reveals focus areas beyond just COVID-19 (immunology, public health, etc.)

### Data Quality Insights
- **Completeness**: ~35% of all data cells contain missing values
- **Critical Fields**: Title and publication time have excellent completeness (>99%)
- **Challenge Areas**: Some fields like DOI and PMC ID have significant missing data

## 🛠️ Technical Details

### Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Static visualizations
- **plotly**: Interactive visualizations
- **streamlit**: Web dashboard framework
- **wordcloud**: Text visualization
- **re**: Regular expressions for text processing

### Performance Considerations
- **Caching**: Streamlit dashboard uses `@st.cache_data` for efficient data loading
- **Memory Management**: Large datasets are processed efficiently with pandas optimization
- **Incremental Processing**: Analysis pipeline processes data in logical stages

### File Outputs
The analysis pipeline generates several output files:
- `metadata_cleaned.csv`: Dataset with missing values handled
- `metadata_prepared.csv`: Analysis-ready dataset with new features
- `plots/`: Directory containing saved visualizations

## 🔧 Customization

### Adding New Analysis
1. Create new functions in `index.py` following the existing pattern
2. Add corresponding dashboard sections in `streamlit_app.py`
3. Update the main execution pipeline

### Modifying Visualizations
- Edit the `create_visualizations()` function in `index.py`
- Customize Plotly charts in `streamlit_app.py`
- Adjust styling in the CSS section of the Streamlit app

### Changing Data Sources
- Modify the `load_data()` function to handle different file formats
- Update column mappings if using different datasets
- Adjust analysis functions for new data structures

## 🙏 Acknowledgments

- **CORD-19 Dataset**: Allen Institute for AI and collaborators
- **Kaggle**: For hosting and providing access to the dataset
- **Open Source Community**: For the excellent Python libraries used in this project

---

**Note**: This project is designed for educational and research purposes. The analysis and insights should be validated against the latest scientific literature for any research applications.