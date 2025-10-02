"""
Setup script for COVID-19 Research Analytics Dashboard

This script helps users set up the project environment and verify functionality.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_simple.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please install manually:")
        print("   pip install pandas numpy matplotlib seaborn plotly streamlit wordcloud")

def check_dataset():
    """Check if dataset files are available"""
    print("\n📁 Checking dataset availability...")
    
    datasets = {
        "metadata_sample.csv": "Sample dataset (200 records) - ✅ Available for testing",
        "metadata.csv": "Full dataset (1M+ records) - Download from Kaggle if needed",
        "metadata_cleaned.csv": "Cleaned dataset - Generated after running index.py",
        "metadata_prepared.csv": "Analysis-ready dataset - Generated after running index.py"
    }
    
    for filename, description in datasets.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024 / 1024  # MB
            print(f"   ✅ {filename} - {size:.1f} MB - {description}")
        else:
            print(f"   ❌ {filename} - Not found - {description}")

def run_quick_test():
    """Run a quick test with the sample dataset"""
    print("\n🧪 Running quick functionality test...")
    try:
        import pandas as pd
        
        # Try to load sample dataset
        if os.path.exists("metadata_sample.csv"):
            df = pd.read_csv("metadata_sample.csv")
            print(f"   ✅ Sample dataset loaded: {len(df)} rows × {len(df.columns)} columns")
            
            # Basic analysis
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            print(f"   📊 Missing data: {missing_pct:.1f}%")
            
            if 'title' in df.columns:
                titles_with_data = df['title'].notna().sum()
                print(f"   📄 Papers with titles: {titles_with_data}")
            
            if 'journal' in df.columns:
                unique_journals = df['journal'].nunique()
                print(f"   📚 Unique journals: {unique_journals}")
                
            print("   ✅ Basic functionality test passed!")
        else:
            print("   ⚠️  No sample dataset found. Please ensure metadata_sample.csv is available.")
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Please install required packages first.")
    except Exception as e:
        print(f"   ❌ Test error: {e}")

def main():
    """Main setup function"""
    print("🔬 COVID-19 Research Analytics Dashboard Setup")
    print("=" * 50)
    
    # Install requirements
    install_requirements()
    
    # Check datasets
    check_dataset()
    
    # Run test
    run_quick_test()
    
    # Final instructions
    print("\n🚀 Setup Complete! Next Steps:")
    print("   1. For command-line analysis: python index.py")
    print("   2. For interactive dashboard: streamlit run streamlit_app.py")
    print("   3. For full dataset: Download metadata.csv from Kaggle")
    print("      URL: https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge")
    
    print("\n📖 Documentation:")
    print("   • README.md - Complete project documentation")
    print("   • CHANGELOG.md - Project development history")
    print("   • Code comments - Detailed implementation explanations")

if __name__ == "__main__":
    main()