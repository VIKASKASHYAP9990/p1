"""
Sales Data Analysis Dashboard
Project 1: Complete Implementation
Author: Data Analysis Project
"""

# ============================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set visual style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================
# 2. LOAD AND EXPLORE DATASET
# ============================================

# Load the dataset (you'll need to download this from Kaggle)
# For this example, I'll create sample data, but you should load the actual Superstore dataset
def load_data():
    """
    Load the Superstore dataset
    """
    try:
        # Option 1: Load from file
        df = pd.read_csv('superstore.csv')
        print("✅ Dataset loaded successfully from file!")
        return df
    except FileNotFoundError:
        # Option 2: Generate sample data if file not found
        print("⚠️ File not found. Generating sample dataset for demonstration...")
        return generate_sample_data()

def generate_sample_data():
    """
    Generate sample sales data for demonstration
    """
    np.random.seed(42)
    n_records = 1000
    
    # Categories and sub-categories
    categories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Labels', 'Envelopes', 'Storage'],
        'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines']
    }
    
    regions = ['West', 'East', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    states = ['California', 'Texas', 'New York', 'Florida', 'Illinois', 'Ohio', 'Pennsylvania']
    
    data = []
    for i in range(n_records):
        category = np.random.choice(list(categories.keys()))
        sub_category = np.random.choice(categories[category])
        region = np.random.choice(regions)
        segment = np.random.choice(segments)
        state = np.random.choice(states)
        
        # Sales price depends on category
        if category == 'Technology':
            sales = np.random.uniform(100, 1000)
        elif category == 'Furniture':
            sales = np.random.uniform(50, 800)
        else:
            sales = np.random.uniform(10, 500)
        
        quantity = np.random.randint(1, 5)
        discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3])
        profit = sales * np.random.uniform(0.05, 0.4) - (sales * discount * 0.8)
        
        # Generate dates (2023)
        date = pd.date_range('2023-01-01', '2023-12-31')[np.random.randint(0, 365)]
        
        data.append({
            'Order ID': f'ORD-{i+1:04d}',
            'Order Date': date,
            'Ship Date': date + pd.Timedelta(days=np.random.randint(1, 7)),
            'Ship Mode': np.random.choice(['Standard', 'Second Class', 'First Class']),
            'Customer ID': f'CUST-{np.random.randint(100, 999)}',
            'Customer Name': f'Customer {np.random.randint(1, 100)}',
            'Segment': segment,
            'Country': 'United States',
            'City': f'City_{np.random.randint(1, 50)}',
            'State': state,
            'Postal Code': np.random.randint(10000, 99999),
            'Region': region,
            'Product ID': f'PROD-{np.random.randint(1000, 9999)}',
            'Category': category,
            'Sub-Category': sub_category,
            'Product Name': f'Product {sub_category} {np.random.randint(1, 100)}',
            'Sales': round(sales, 2),
            'Quantity': quantity,
            'Discount': discount,
            'Profit': round(profit, 2)
        })
    
    df = pd.DataFrame(data)
    print("✅ Sample dataset generated successfully!")
    return df

# Load the data
df = load_data()

# ============================================
# 3. DATA EXPLORATION
# ============================================

def explore_data(df):
    """
    Explore the dataset structure and content
    """
    print("\n" + "="*60)
    print("📊 DATA EXPLORATION")
    print("="*60)
    
    print(f"\n📌 Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\n📌 Columns: {list(df.columns)}")
    
    print(f"\n📌 Data Types:")
    print(df.dtypes)
    
    print(f"\n📌 First 5 rows:")
    print(df.head())
    
    print(f"\n📌 Summary Statistics:")
    print(df[['Sales', 'Quantity', 'Discount', 'Profit']].describe())
    
    print(f"\n📌 Missing Values:")
    print(df.isnull().sum())
    
    return df

df = explore_data(df)

# ============================================
# 4. DATA CLEANING
# ============================================

def clean_data(df):
    """
    Clean the dataset: handle missing values, duplicates, and fix data types
    """
    print("\n" + "="*60)
    print("🧹 DATA CLEANING")
    print("="*60)
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # 1. Handle missing values
    print("\n1️⃣ Checking for missing values...")
    missing_before = df_clean.isnull().sum().sum()
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if col in ['Postal Code', 'Ship Mode']:
                df_clean[col] = df_clean[col].fillna('Unknown')
            elif col in ['Sales', 'Profit', 'Quantity']:
                df_clean[col] = df_clean[col].fillna(0)
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
    
    print(f"   ✅ Missing values handled: {missing_before} → {df_clean.isnull().sum().sum()}")
    
    # 2. Remove duplicates
    print("\n2️⃣ Removing duplicates...")
    duplicates_before = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"   ✅ {duplicates_before} duplicates removed")
    
    # 3. Fix date formats
    print("\n3️⃣ Fixing date formats...")
    df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'])
    df_clean['Ship Date'] = pd.to_datetime(df_clean['Ship Date'])
    
    # 4. Create additional columns for analysis
    print("\n4️⃣ Creating analysis columns...")
    df_clean['Year'] = df_clean['Order Date'].dt.year
    df_clean['Month'] = df_clean['Order Date'].dt.month
    df_clean['Month Name'] = df_clean['Order Date'].dt.month_name()
    df_clean['Quarter'] = df_clean['Order Date'].dt.quarter
    df_clean['Year-Month'] = df_clean['Order Date'].dt.strftime('%Y-%m')
    df_clean['Profit Margin'] = (df_clean['Profit'] / df_clean['Sales']) * 100
    df_clean['Profit Margin'] = df_clean['Profit Margin'].replace([np.inf, -np.inf], 0)
    df_clean['Profit Margin'] = df_clean['Profit Margin'].fillna(0)
    
    print("\n📌 Cleaned dataset info:")
    print(f"   Shape: {df_clean.shape}")
    print(f"   Date range: {df_clean['Order Date'].min()} to {df_clean['Order Date'].max()}")
    
    return df_clean

df_clean = clean_data(df)

# ============================================
# 5. KEY METRICS ANALYSIS
# ============================================

def calculate_metrics(df):
    """
    Calculate key business metrics
    """
    print("\n" + "="*60)
    print("📈 KEY METRICS ANALYSIS")
    print("="*60)
    
    metrics = {
        'Total Sales': df['Sales'].sum(),
        'Total Profit': df['Profit'].sum(),
        'Total Orders': df['Order ID'].nunique(),
        'Total Quantity': df['Quantity'].sum(),
        'Average Order Value': df['Sales'].sum() / df['Order ID'].nunique(),
        'Average Profit per Order': df['Profit'].sum() / df['Order ID'].nunique(),
        'Overall Profit Margin (%)': (df['Profit'].sum() / df['Sales'].sum()) * 100,
        'Unique Customers': df['Customer ID'].nunique(),
        'Unique Products': df['Product ID'].nunique()
    }
    
    metrics_df = pd.DataFrame(metrics.items(), columns=['Metric', 'Value'])
    metrics_df['Value'] = metrics_df['Value'].round(2)
    
    print("\n" + metrics_df.to_string(index=False))
    return metrics

metrics = calculate_metrics(df_clean)

# ============================================
# 6. TOP PERFORMING PRODUCTS
# ============================================

def top_products(df):
    """
    Analyze top performing products
    """
    print("\n" + "="*60)
    print("🏆 TOP PERFORMING PRODUCTS")
    print("="*60)
    
    # Top 10 products by sales
    top_sales = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    print("\n📌 Top 10 Products by Sales:")
    print(top_sales)
    
    # Top 10 products by profit
    top_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
    print("\n📌 Top 10 Products by Profit:")
    print(top_profit)
    
    # Category performance
    category_perf = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).round(2)
    category_perf['Profit Margin'] = (category_perf['Profit'] / category_perf['Sales']) * 100
    print("\n📌 Category Performance:")
    print(category_perf)
    
    # Sub-category performance
    subcategory_perf = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).sort_values('Sales', ascending=False).head(10).round(2)
    subcategory_perf['Profit Margin'] = (subcategory_perf['Profit'] / subcategory_perf['Sales']) * 100
    print("\n📌 Top 10 Sub-Categories by Sales:")
    print(subcategory_perf)
    
    return top_sales, top_profit

top_sales, top_profit = top_products(df_clean)

# ============================================
# 7. REGIONAL ANALYSIS
# ============================================

def regional_analysis(df):
    """
    Analyze performance by region
    """
    print("\n" + "="*60)
    print("🌍 REGIONAL ANALYSIS")
    print("="*60)
    
    regional_perf = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count',
        'Quantity': 'sum'
    }).round(2)
    regional_perf.columns = ['Total Sales', 'Total Profit', 'Order Count', 'Total Quantity']
    regional_perf['Profit Margin (%)'] = (regional_perf['Total Profit'] / regional_perf['Total Sales']) * 100
    regional_perf['Avg Order Value'] = regional_perf['Total Sales'] / regional_perf['Order Count']
    
    print("\n📌 Regional Performance:")
    print(regional_perf.sort_values('Total Sales', ascending=False))
    
    # Top states by sales
    top_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
    print("\n📌 Top 10 States by Sales:")
    print(top_states)
    
    return regional_perf

regional_perf = regional_analysis(df_clean)

# ============================================
# 8. TIME TRENDS ANALYSIS
# ============================================

def time_trends(df):
    """
    Analyze trends over time
    """
    print("\n" + "="*60)
    print("📅 TIME TRENDS ANALYSIS")
    print("="*60)
    
    # Monthly trends
    monthly_trends = df.groupby('Year-Month').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).round(2)
    monthly_trends.index = pd.to_datetime(monthly_trends.index)
    monthly_trends = monthly_trends.sort_index()
    
    print("\n📌 Monthly Trends (Last 12 months):")
    print(monthly_trends.tail(12))
    
    # Quarterly trends
    quarterly_trends = df.groupby('Quarter').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).round(2)
    print("\n📌 Quarterly Trends:")
    print(quarterly_trends)
    
    # Calculate growth rates
    monthly_sales = df.groupby('Year-Month')['Sales'].sum()
    monthly_sales.index = pd.to_datetime(monthly_sales.index)
    monthly_sales = monthly_sales.sort_index()
    
    if len(monthly_sales) > 1:
        growth_rate = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
        print(f"\n📌 Month-over-Month Growth: {growth_rate:.2f}%")
    
    return monthly_trends

monthly_trends = time_trends(df_clean)

# ============================================
# 9. STATIC VISUALIZATIONS (Matplotlib/Seaborn)
# ============================================

def create_static_visualizations(df):
    """
    Create static visualizations using Matplotlib and Seaborn
    """
    print("\n" + "="*60)
    print("📊 CREATING STATIC VISUALIZATIONS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Sales by Category
    category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    axes[0, 0].bar(category_sales.index, category_sales.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[0, 0].set_title('Sales by Category', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Category')
    axes[0, 0].set_ylabel('Total Sales ($)')
    for i, v in enumerate(category_sales.values):
        axes[0, 0].text(i, v + 500, f'${v:,.0f}', ha='center', va='bottom', fontsize=10)
    
    # 2. Sales by Region
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    colors = ['#FF9F43', '#EE5A24', '#0ABDE3', '#10AC84']
    axes[0, 1].bar(region_sales.index, region_sales.values, color=colors)
    axes[0, 1].set_title('Sales by Region', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Region')
    axes[0, 1].set_ylabel('Total Sales ($)')
    for i, v in enumerate(region_sales.values):
        axes[0, 1].text(i, v + 500, f'${v:,.0f}', ha='center', va='bottom', fontsize=10)
    
    # 3. Monthly Sales Trend (Line Chart)
    monthly_sales = df.groupby('Month Name')['Sales'].sum()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_sales = monthly_sales.reindex(month_order)
    axes[1, 0].plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, 
                    color='#FF6B6B', markersize=8)
    axes[1, 0].fill_between(monthly_sales.index, monthly_sales.values, alpha=0.3, color='#FF6B6B')
    axes[1, 0].set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Sales ($)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Profit Margin by Category (Pie Chart)
    profit_by_category = df.groupby('Category')['Profit'].sum()
    wedges, texts, autotexts = axes[1, 1].pie(profit_by_category.values, 
                                               labels=profit_by_category.index,
                                               autopct='%1.1f%%', 
                                               colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                                               explode=(0.05, 0.05, 0.05))
    axes[1, 1].set_title('Profit Distribution by Category', fontsize=14, fontweight='bold')
    
    plt.suptitle('Superstore Sales Dashboard - Key Visualizations', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('superstore_dashboard_static.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Static visualization saved as 'superstore_dashboard_static.png'")
    
    # Additional visualization: Scatter plot - Discount vs Profit
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Discount'], df['Profit'], alpha=0.5, c=df['Sales'], cmap='viridis')
    plt.colorbar(label='Sales ($)')
    plt.xlabel('Discount')
    plt.ylabel('Profit ($)')
    plt.title('Discount vs Profit Relationship')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    plt.savefig('discount_vs_profit.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Discount vs Profit visualization saved as 'discount_vs_profit.png'")

create_static_visualizations(df_clean)

# ============================================
# 10. INTERACTIVE DASHBOARD (Plotly)
# ============================================

def create_interactive_dashboard(df):
    """
    Create an interactive dashboard using Plotly
    """
    print("\n" + "="*60)
    print("🎨 CREATING INTERACTIVE DASHBOARD")
    print("="*60)
    
    # Create subplots with different chart types
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=('Sales by Category', 'Sales by Region', 
                        'Monthly Sales Trend', 'Profit by Category',
                        'Top 10 Products', 'Sales vs Profit Scatter',
                        'Regional Profit Margins', 'Category Distribution',
                        'Top States by Sales'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'pie'}, {'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'bar'}, {'type': 'pie'}, {'type': 'bar'}]]
    )
    
    # 1. Sales by Category
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=cat_sales.index, y=cat_sales.values, 
                         name='Sales by Category',
                         marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                         text=[f'${x:,.0f}' for x in cat_sales.values],
                         textposition='outside'), row=1, col=1)
    
    # 2. Sales by Region
    reg_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=reg_sales.index, y=reg_sales.values, 
                         name='Sales by Region',
                         marker_color=['#FF9F43', '#EE5A24', '#0ABDE3', '#10AC84'],
                         text=[f'${x:,.0f}' for x in reg_sales.values],
                         textposition='outside'), row=1, col=2)
    
    # 3. Monthly Sales Trend
    monthly = df.groupby('Month Name')['Sales'].sum()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly = monthly.reindex(month_order)
    fig.add_trace(go.Scatter(x=monthly.index, y=monthly.values, 
                            mode='lines+markers', name='Sales Trend',
                            line=dict(color='#FF6B6B', width=3),
                            marker=dict(size=10)),
                  row=1, col=3)
    
    # 4. Profit by Category (Pie)
    cat_profit = df.groupby('Category')['Profit'].sum()
    fig.add_trace(go.Pie(labels=cat_profit.index, values=cat_profit.values,
                         name='Profit by Category',
                         textinfo='label+percent',
                         marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])),
                  row=2, col=1)
    
    # 5. Top 10 Products
    top10 = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    fig.add_trace(go.Bar(x=top10.values, y=top10.index, 
                         name='Top Products', orientation='h',
                         marker_color='#4ECDC4',
                         text=[f'${x:,.0f}' for x in top10.values],
                         textposition='outside'),
                  row=2, col=2)
    
    # 6. Sales vs Profit Scatter
    fig.add_trace(go.Scatter(x=df['Sales'], y=df['Profit'], 
                            mode='markers', name='Sales vs Profit',
                            marker=dict(size=8, opacity=0.6,
                                       color=df['Category'].astype('category').cat.codes,
                                       colorscale='Viridis'),
                            text=df['Category']),
                  row=2, col=3)
    
    # 7. Regional Profit Margins
    reg_profit = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    })
    reg_profit['Margin'] = (reg_profit['Profit'] / reg_profit['Sales']) * 100
    reg_profit = reg_profit.sort_values('Margin', ascending=False)
    fig.add_trace(go.Bar(x=reg_profit.index, y=reg_profit['Margin'],
                         name='Profit Margins',
                         marker_color=['#10AC84' if x > 0 else '#FF6B6B' for x in reg_profit['Margin']],
                         text=[f'{x:.1f}%' for x in reg_profit['Margin']],
                         textposition='outside'),
                  row=3, col=1)
    
    # 8. Segment Distribution (Pie)
    segment_sales = df.groupby('Segment')['Sales'].sum()
    fig.add_trace(go.Pie(labels=segment_sales.index, values=segment_sales.values,
                         name='Segment Sales',
                         textinfo='label+percent',
                         marker=dict(colors=['#FF9F43', '#EE5A24', '#0ABDE3'])),
                  row=3, col=2)
    
    # 9. Top States
    top_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
    fig.add_trace(go.Bar(x=top_states.values, y=top_states.index,
                         name='Top States', orientation='h',
                         marker_color='#45B7D1',
                         text=[f'${x:,.0f}' for x in top_states.values],
                         textposition='outside'),
                  row=3, col=3)
    
    # Update layout
    fig.update_layout(height=1200, width=1600, showlegend=False,
                     title_text='📊 Superstore Sales Analysis Dashboard',
                     title_font_size=20,
                     template='plotly_white')
    
    # Update axes
    fig.update_xaxes(title_text='Category', row=1, col=1)
    fig.update_xaxes(title_text='Region', row=1, col=2)
    fig.update_xaxes(title_text='Month', row=1, col=3)
    fig.update_yaxes(title_text='Sales ($)', row=1, col=1)
    fig.update_yaxes(title_text='Sales ($)', row=1, col=2)
    fig.update_yaxes(title_text='Sales ($)', row=1, col=3)
    fig.update_yaxes(title_text='Profit ($)', row=2, col=3)
    fig.update_xaxes(title_text='Sales ($)', row=2, col=3)
    fig.update_xaxes(title_text='State', row=3, col=3)
    
    # Show the dashboard
    fig.show()
    
    # Save as HTML
    fig.write_html('superstore_dashboard_interactive.html')
    print("✅ Interactive dashboard saved as 'superstore_dashboard_interactive.html'")
    
    return fig

interactive_dashboard = create_interactive_dashboard(df_clean)

# ============================================
# 11. EXPORT CLEANED DATA
# ============================================

def export_data(df):
    """
    Export cleaned data for use in Power BI/Tableau
    """
    print("\n" + "="*60)
    print("💾 EXPORTING CLEANED DATA")
    print("="*60)
    
    # Export to CSV
    df.to_csv('superstore_cleaned.csv', index=False)
    print("✅ Cleaned data exported to 'superstore_cleaned.csv'")
    
    # Export summary statistics
    summary = df.describe()
    summary.to_csv('superstore_summary_stats.csv')
    print("✅ Summary statistics exported to 'superstore_summary_stats.csv'")

export_data(df_clean)

# ============================================
# 12. GENERATE REPORT
# ============================================

def generate_report(df):
    """
    Generate a comprehensive analysis report
    """
    print("\n" + "="*60)
    print("📝 GENERATING ANALYSIS REPORT")
    print("="*60)
    
    report = f"""
    ========================================================================
                     SUPERSTORE SALES ANALYSIS REPORT
    ========================================================================
    
    EXECUTIVE SUMMARY
    ------------------------------------------------------------------------
    Total Sales: ${df['Sales'].sum():,.2f}
    Total Profit: ${df['Profit'].sum():,.2f}
    Total Orders: {df['Order ID'].nunique():,}
    Overall Profit Margin: {(df['Profit'].sum() / df['Sales'].sum() * 100):.2f}%
    Average Order Value: ${(df['Sales'].sum() / df['Order ID'].nunique()):.2f}
    Number of Customers: {df['Customer ID'].nunique():,}
    Number of Products: {df['Product ID'].nunique():,}
    
    KEY INSIGHTS
    ------------------------------------------------------------------------
    1. TOP PERFORMING CATEGORIES:
    {df.groupby('Category')['Sales'].sum().sort_values(ascending=False).to_string()}
    
    2. REGIONAL PERFORMANCE:
    {df.groupby('Region')['Sales'].sum().sort_values(ascending=False).to_string()}
    
    3. TOP 5 PRODUCTS BY SALES:
    {df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).to_string()}
    
    4. CUSTOMER SEGMENT BREAKDOWN:
    {df.groupby('Segment')['Sales'].sum().sort_values(ascending=False).to_string()}
    
    RECOMMENDATIONS
    ------------------------------------------------------------------------
    1. Focus on high-performing categories and regions for growth
    2. Address underperforming products and categories
    3. Optimize discount strategy to maximize profit margins
    4. Expand successful strategies to underperforming regions
    5. Increase customer retention in high-value segments
    
    ========================================================================
    Report Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
    ========================================================================
    """
    
    # Save report
    with open('sales_analysis_report.txt', 'w') as f:
        f.write(report)
    
    print(report)
    print("✅ Report saved as 'sales_analysis_report.txt'")
    
    return report

generate_report(df_clean)

print("\n" + "="*60)
print("🎉 PROJECT COMPLETED SUCCESSFULLY!")
print("="*60)
print("\n📁 Generated Files:")
print("   1. superstore_dashboard_static.png - Static visualization")
print("   2. superstore_dashboard_interactive.html - Interactive dashboard")
print("   3. superstore_cleaned.csv - Cleaned dataset")
print("   4. superstore_summary_stats.csv - Summary statistics")
print("   5. sales_analysis_report.txt - Analysis report")
print("   6. discount_vs_profit.png - Additional visualization")
print("\n📊 Open the HTML file in your browser to explore the interactive dashboard!")
print("="*60)
