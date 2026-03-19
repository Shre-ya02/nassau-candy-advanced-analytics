import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Nassau Candy Advanced Analytics",
    page_icon="candy_icon.png",
    layout="wide",
)

# Custom Styling (Vanilla CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# State mapping for Choropleth
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC", "American Samoa": "AS", "Guam": "GU", "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR", "United States Minor Outlying Islands": "UM", "U.S. Virgin Islands": "VI",
}

# Helper function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("processed_nassau_candy.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['State Code'] = df['State/Province'].map(us_state_to_abbrev)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.image("candy_icon.png", width=100)
st.sidebar.header("Global Filters")

# Date range selector
min_date = df['Order Date'].min().to_pydatetime()
max_date = df['Order Date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# Division Filter
divisions = ['All'] + sorted(df['Division'].unique().tolist())
selected_division = st.sidebar.selectbox("Select Division", divisions)

# Region Filter
regions = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Margin Threshold Slider
margin_threshold = st.sidebar.slider("Minimum Gross Margin %", 0, 100, 0)

# Product Search
product_search = st.sidebar.text_input("Search Product", "")

# Apply Filters
filtered_df = df.copy()
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_date) & (filtered_df['Order Date'].dt.date <= end_date)]

if selected_division != 'All':
    filtered_df = filtered_df[filtered_df['Division'] == selected_division]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

filtered_df = filtered_df[filtered_df['Gross Margin (%)'] >= margin_threshold]

if product_search:
    filtered_df = filtered_df[filtered_df['Product Name'].str.contains(product_search, case=False)]

# Main Dashboard Layout
# col_logo, col_text = st.columns([1, 5]) --- Moved to standard layout for better look
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

col_logo, col_text = st.columns([1, 6])
with col_logo:
    st.image("candy_icon.png", width=100)
with col_text:
    st.title("Nassau Candy Advanced Analytics")
    st.write("Strategic Profitability & Operational Intelligence Dashboard")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Gross Profit'].sum()
avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_units = filtered_df['Units'].sum()

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Total Gross Profit", f"${total_profit:,.2f}")
with col3:
    st.metric("Avg. Gross Margin", f"{avg_margin:.2f}%")
with col4:
    st.metric("Total Units Sold", f"{total_units:,.0f}")

# Dashboard Tabs
tabs = st.tabs([
    "Geographic Intelligence",
    "Product Performance", 
    "Regional & Division", 
    "Customer Segments", 
    "Margin Trends", 
    "Operational Diagnostics",
    "Concentration (Pareto)"
])

with tabs[0]:
    st.subheader("US Profitability Heatmap")
    state_stats = filtered_df.groupby('State Code').agg({
        'Gross Profit': 'sum',
        'Sales': 'sum',
        'Units': 'sum'
    }).reset_index()
    state_stats['Margin %'] = (state_stats['Gross Profit'] / state_stats['Sales']) * 100

    fig_map = px.choropleth(
        state_stats,
        locations='State Code',
        locationmode="USA-states",
        color='Gross Profit',
        scope="usa",
        hover_data=['Sales', 'Margin %'],
        color_continuous_scale="Viridis",
        title="Gross Profit by State"
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.info("💡 **Tip**: Hover over states to see specific Sales and Margin % details.")

with tabs[1]:
    st.subheader("Leaderboard: Top Profitable Products")
    product_stats = filtered_df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Gross Profit': 'sum',
        'Gross Margin (%)': 'mean',
        'Units': 'sum',
        'Cost': 'sum'
    }).sort_values(by='Gross Profit', ascending=False)
    
    st.dataframe(product_stats.head(15).style.format({
        'Sales': '${:,.2f}',
        'Gross Profit': '${:,.2f}',
        'Gross Margin (%)': '{:.2f}%',
        'Units': '{:,.0f}',
        'Cost': '${:,.2f}'
    }), use_container_width=True)

    fig_prod = px.bar(product_stats.head(10).reset_index(), x='Gross Profit', y='Product Name', 
                      orientation='h', title="Top 10 Products by Gross Profit",
                      color='Gross Profit', color_continuous_scale='Portland')
    st.plotly_chart(fig_prod, use_container_width=True)

with tabs[2]:
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.subheader("Regional Profitability")
        reg_stats = filtered_df.groupby('Region').agg({'Gross Profit': 'sum', 'Sales': 'sum'}).reset_index()
        fig_reg = px.bar(reg_stats, x='Region', y='Gross Profit', color='Region', title="Profit by Region")
        st.plotly_chart(fig_reg, use_container_width=True)
    with col_r2:
        st.subheader("Division Metrics")
        div_stats = filtered_df.groupby('Division').agg({'Sales': 'sum', 'Gross Profit': 'sum'}).reset_index()
        fig_div_pie = px.pie(div_stats, values='Sales', names='Division', title="Revenue Share by Division", hole=0.4)
        st.plotly_chart(fig_div_pie, use_container_width=True)

with tabs[3]:
    st.subheader("Customer Profitability Analysis")
    cust_stats = filtered_df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Gross Profit': 'sum',
        'Gross Margin (%)': 'mean'
    }).sort_values(by='Gross Profit', ascending=False).reset_index()
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.write("Top 20 Customers by Profit Contribution")
        st.dataframe(cust_stats.head(20).style.format({
            'Sales': '${:,.2f}',
            'Gross Profit': '${:,.2f}',
            'Gross Margin (%)': '{:.2f}%'
        }), use_container_width=True)
    with col_c2:
        fig_cust_scatter = px.scatter(cust_stats, x='Sales', y='Gross Margin (%)', 
                                      title="Customer Value Matrix",
                                      labels={'Sales': 'Total Spend ($)', 'Gross Margin (%)': 'Average Margin %'})
        st.plotly_chart(fig_cust_scatter, use_container_width=True)

with tabs[4]:
    st.subheader("Margin Volatility & Trends")
    df_trend = filtered_df.copy()
    df_trend['Month'] = df_trend['Order Date'].dt.to_period('M').astype(str)
    trend_stats = df_trend.groupby('Month').agg({
        'Gross Profit': 'sum',
        'Sales': 'sum'
    }).reset_index()
    trend_stats['Margin %'] = (trend_stats['Gross Profit'] / trend_stats['Sales']) * 100
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend_stats['Month'], y=trend_stats['Margin %'], name="Avg Margin %", line=dict(color='firebrick', width=4)))
    fig_trend.update_layout(title="Monthly Gross Margin Trend", yaxis_title="Margin %", xaxis_title="Month")
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.info("💡 **Insight**: Seasonal fluctuations in margin highlight the impact of promotions or supply chain shifts.")

with tabs[5]:
    st.subheader("Operational & Factory Diagnostics")
    fact_stats = filtered_df.groupby('Factory').agg({
        'Sales': 'sum',
        'Gross Profit': 'sum',
        'Gross Margin (%)': 'mean',
        'Cost': 'sum'
    }).reset_index()
    
    fig_fact = px.scatter(fact_stats, x='Cost', y='Gross Profit', size='Sales', color='Factory',
                          hover_name='Factory', title="Factory Performance Matrix (Efficiency)")
    st.plotly_chart(fig_fact, use_container_width=True)
    
    st.subheader("Cost vs Sales (Product Level Risk)")
    fig_scatter = px.scatter(filtered_df, x='Sales', y='Cost', color='Division', 
                             hover_name='Product Name', size='Units',
                             title="Identifying Margin Risk (Cost vs Sales)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with tabs[6]:
    st.subheader("Pareto Analysis (80/20 Rule)")
    pareto_df = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).reset_index()
    pareto_df['Cumulative Profit %'] = 100 * (pareto_df['Gross Profit'].cumsum() / pareto_df['Gross Profit'].sum())

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=pareto_df['Product Name'][:20], y=pareto_df['Gross Profit'][:20], name="Individual Profit"))
    fig_pareto.add_trace(go.Scatter(x=pareto_df['Product Name'][:20], y=pareto_df['Cumulative Profit %'][:20], 
                                   name="Cumulative Profit %", yaxis="y2", line=dict(color='red')))
    
    fig_pareto.update_layout(
        title="Profit Concentration (Top 20 Products)",
        yaxis=dict(title="Gross Profit ($)"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig_pareto, use_container_width=True)
    
    high_impact_products = pareto_df[pareto_df['Cumulative Profit %'] <= 80]
    st.success(f"**Strategic Insight**: {len(high_impact_products)} products account for 80% of total gross profit.")

# Footer
st.markdown("---")
st.markdown("Developed for Nassau Candy Distributor | Strategic Profitability Analytics")
