#!/usr/bin/env python3
"""
Test script for the dashboard functionality
"""
from financial_processor import (
    load_financial_data, 
    categorize_accounts, 
    calculate_financial_metrics,
    identify_cash_flow_issues,
    generate_forecast
)

def test_dashboard_data():
    """Test that all dashboard data functions work correctly"""
    try:
        print("Testing dashboard data loading...")
        
        # Load data
        filename = "MMC - Monthly Financial Data.xlsx"
        df = load_financial_data(filename)
        
        if df is None:
            print("❌ Failed to load data")
            return False
        
        print(f"✅ Data loaded successfully: {df.shape}")
        
        # Categorize accounts
        df = categorize_accounts(df)
        print(f"✅ Accounts categorized: {df['Category'].value_counts().to_dict()}")
        
        # Calculate metrics
        metrics = calculate_financial_metrics(df)
        print(f"✅ Metrics calculated for {len(metrics)} periods")
        
        # Identify issues
        issues = identify_cash_flow_issues(df, metrics)
        print(f"✅ Issues identified: {len(issues)} issues found")
        
        # Generate forecast
        forecast = generate_forecast(df, metrics)
        print(f"✅ Forecast generated for {len(forecast)} periods")
        
        # Test chart data preparation
        months = [month for month in metrics.keys() if month != 'Total']
        revenues = [metrics[month]['revenue'] for month in months]
        expenses = [metrics[month]['expenses'] for month in months]
        net_incomes = [metrics[month]['net_income'] for month in months]
        
        print(f"✅ Chart data prepared: {len(months)} months")
        print(f"   Revenue range: ${min(revenues):,.0f} - ${max(revenues):,.0f}")
        print(f"   Expense range: ${min(expenses):,.0f} - ${max(expenses):,.0f}")
        print(f"   Net income range: ${min(net_incomes):,.0f} - ${max(net_incomes):,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    if test_dashboard_data():
        print("\n🎉 All tests passed! Dashboard should work correctly.")
        print("\nTo run the dashboard, use:")
        print("streamlit run dashboard.py")
    else:
        print("\n❌ Tests failed. Please check the errors above.") 