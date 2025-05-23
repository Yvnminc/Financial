#!/usr/bin/env python3
"""
MMC Financial Dashboard - Streamlit Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from financial_processor import (
    load_financial_data, 
    categorize_accounts, 
    calculate_financial_metrics,
    identify_cash_flow_issues,
    generate_forecast
)

# Page configuration
st.set_page_config(
    page_title="MMC Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_and_process_data():
    """Load and process financial data with caching"""
    filename = "MMC - Monthly Financial Data.xlsx"
    df = load_financial_data(filename)
    
    if df is not None:
        df = categorize_accounts(df)
        metrics = calculate_financial_metrics(df)
        issues = identify_cash_flow_issues(df, metrics)
        forecast = generate_forecast(df, metrics)
        return df, metrics, issues, forecast
    return None, None, None, None

def create_revenue_chart(metrics):
    """Create revenue trend chart"""
    months = [month for month in metrics.keys() if month != 'Total']
    revenues = [metrics[month]['revenue'] for month in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=revenues,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    
    return fig

def create_expense_chart(metrics):
    """Create expense trend chart"""
    months = [month for month in metrics.keys() if month != 'Total']
    expenses = [metrics[month]['expenses'] for month in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=expenses,
        mode='lines+markers',
        name='Expenses',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Monthly Expense Trend",
        xaxis_title="Month",
        yaxis_title="Expenses ($)",
        hovermode='x unified'
    )
    
    return fig

def create_profit_margin_chart(metrics):
    """Create profit margin chart"""
    months = [month for month in metrics.keys() if month != 'Total']
    margins = [metrics[month]['profit_margin'] for month in months]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=margins,
        name='Profit Margin',
        marker_color=['green' if m >= 0 else 'red' for m in margins]
    ))
    
    fig.update_layout(
        title="Monthly Profit Margin (%)",
        xaxis_title="Month",
        yaxis_title="Profit Margin (%)",
        hovermode='x unified'
    )
    
    return fig

def create_net_income_chart(metrics):
    """Create net income chart"""
    months = [month for month in metrics.keys() if month != 'Total']
    net_incomes = [metrics[month]['net_income'] for month in months]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=net_incomes,
        name='Net Income',
        marker_color=['green' if ni >= 0 else 'red' for ni in net_incomes]
    ))
    
    fig.update_layout(
        title="Monthly Net Income",
        xaxis_title="Month",
        yaxis_title="Net Income ($)",
        hovermode='x unified'
    )
    
    return fig

def create_category_breakdown(df):
    """Create category breakdown pie chart"""
    months = [col for col in df.columns if col not in ['Account', 'Category', 'Total']]
    
    # Calculate total by category (using 'Total' column or sum of months)
    if 'Total' in df.columns:
        category_totals = df.groupby('Category')['Total'].sum()
    else:
        category_totals = df.groupby('Category')[months].sum().sum(axis=1)
    
    fig = px.pie(
        values=category_totals.abs(),  # Use absolute values for pie chart
        names=category_totals.index,
        title="Financial Categories Breakdown"
    )
    
    return fig

def display_key_metrics(metrics):
    """Display key financial metrics"""
    months = [month for month in metrics.keys() if month != 'Total']
    current_month = months[-3] if len(months) >= 3 else months[-1]  # Latest actual month
    
    current_metrics = metrics[current_month]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Revenue",
            value=f"${current_metrics['revenue']:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Current Expenses", 
            value=f"${current_metrics['expenses']:,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Net Income",
            value=f"${current_metrics['net_income']:,.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Profit Margin",
            value=f"{current_metrics['profit_margin']:.1f}%",
            delta=None
        )

def display_issues(issues):
    """Display identified issues"""
    if not issues:
        st.success("🎉 No major financial issues identified!")
        return
    
    st.warning(f"⚠️ {len(issues)} potential issues identified:")
    
    for issue in issues:
        severity_color = {
            'High': '🔴',
            'Medium': '🟡', 
            'Low': '🟢'
        }
        
        st.write(f"{severity_color.get(issue['severity'], '⚪')} **{issue['type']}** ({issue['severity']} Priority)")
        st.write(f"   {issue['description']}")

def main():
    """Main dashboard function"""
    # Header
    st.title("💰 MMC Financial Dashboard")
    st.markdown("**Mering Management Corporation Pty Ltd** - Financial Year 2025")
    
    # Load data
    with st.spinner("Loading financial data..."):
        df, metrics, issues, forecast = load_and_process_data()
    
    if df is None:
        st.error("Failed to load financial data. Please check the Excel file.")
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a view:",
        ["Overview", "Detailed Analysis", "Cash Flow Issues", "Forecast", "Raw Data"]
    )
    
    if page == "Overview":
        st.header("📊 Financial Overview")
        
        # Key metrics
        st.subheader("Key Metrics")
        display_key_metrics(metrics)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_revenue_chart(metrics), use_container_width=True)
            st.plotly_chart(create_profit_margin_chart(metrics), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_expense_chart(metrics), use_container_width=True)
            st.plotly_chart(create_net_income_chart(metrics), use_container_width=True)
    
    elif page == "Detailed Analysis":
        st.header("🔍 Detailed Financial Analysis")
        
        # Category breakdown
        st.subheader("Category Breakdown")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.plotly_chart(create_category_breakdown(df), use_container_width=True)
        
        with col2:
            # Top accounts by total
            if 'Total' in df.columns:
                top_accounts = df.nlargest(10, 'Total')[['Account', 'Total']].copy()
                top_accounts['Total'] = top_accounts['Total'].round(0)
                st.subheader("Top 10 Accounts by Total")
                st.dataframe(top_accounts, use_container_width=True)
        
        # Monthly trends by category
        st.subheader("Monthly Trends by Category")
        months = [col for col in df.columns if col not in ['Account', 'Category', 'Total']]
        
        category_monthly = df.groupby('Category')[months].sum()
        
        fig = go.Figure()
        for category in category_monthly.index:
            fig.add_trace(go.Scatter(
                x=months,
                y=category_monthly.loc[category],
                mode='lines+markers',
                name=category
            ))
        
        fig.update_layout(
            title="Monthly Trends by Category",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Cash Flow Issues":
        st.header("⚠️ Cash Flow Analysis")
        
        # Display issues
        st.subheader("Identified Issues")
        display_issues(issues)
        
        # Monthly cash flow summary
        st.subheader("Monthly Cash Flow Summary")
        
        months = [month for month in metrics.keys() if month != 'Total']
        cash_flow_data = []
        
        for month in months:
            cash_flow_data.append({
                'Month': month,
                'Revenue': metrics[month]['revenue'],
                'Expenses': metrics[month]['expenses'],
                'Net Income': metrics[month]['net_income'],
                'Profit Margin (%)': metrics[month]['profit_margin']
            })
        
        cash_flow_df = pd.DataFrame(cash_flow_data)
        
        # Color negative values red
        def highlight_negative(val):
            if isinstance(val, (int, float)) and val < 0:
                return 'background-color: #ffcccc'
            return ''
        
        st.dataframe(
            cash_flow_df.style.applymap(highlight_negative, subset=['Net Income', 'Profit Margin (%)']),
            use_container_width=True
        )
    
    elif page == "Forecast":
        st.header("🔮 Financial Forecast")
        
        if forecast:
            st.subheader("Forecast Summary")
            
            forecast_data = []
            for month, data in forecast.items():
                forecast_data.append({
                    'Month': month,
                    'Forecasted Revenue': data['revenue'],
                    'Forecasted Expenses': data['expenses'],
                    'Forecasted Net Income': data['net_income']
                })
            
            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, use_container_width=True)
            
            # Combined actual vs forecast chart
            months = [month for month in metrics.keys() if month != 'Total']
            actual_revenues = [metrics[month]['revenue'] for month in months if month not in forecast]
            actual_expenses = [metrics[month]['expenses'] for month in months if month not in forecast]
            
            forecast_months = list(forecast.keys())
            forecast_revenues = [forecast[month]['revenue'] for month in forecast_months]
            forecast_expenses = [forecast[month]['expenses'] for month in forecast_months]
            
            fig = go.Figure()
            
            # Actual data
            fig.add_trace(go.Scatter(
                x=months[:len(actual_revenues)],
                y=actual_revenues,
                mode='lines+markers',
                name='Actual Revenue',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=months[:len(actual_expenses)],
                y=actual_expenses,
                mode='lines+markers',
                name='Actual Expenses',
                line=dict(color='red')
            ))
            
            # Forecast data
            fig.add_trace(go.Scatter(
                x=forecast_months,
                y=forecast_revenues,
                mode='lines+markers',
                name='Forecasted Revenue',
                line=dict(color='lightblue', dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_months,
                y=forecast_expenses,
                mode='lines+markers',
                name='Forecasted Expenses',
                line=dict(color='lightcoral', dash='dash')
            ))
            
            fig.update_layout(
                title="Actual vs Forecasted Financial Performance",
                xaxis_title="Month",
                yaxis_title="Amount ($)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data to generate forecast.")
    
    elif page == "Raw Data":
        st.header("📋 Raw Data")
        
        st.subheader("Financial Data Table")
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="mmc_financial_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 