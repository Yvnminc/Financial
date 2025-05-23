#!/usr/bin/env python3
"""
Financial data processor for MMC dashboard
"""
import pandas as pd
import numpy as np

def load_financial_data(filename):
    """Load and clean the financial data from Excel"""
    try:
        # Read the raw data
        df_raw = pd.read_excel(filename, sheet_name='MMC', header=None)
        
        # Find the header row (row with months)
        header_row = None
        data_start_row = None
        
        for i, row in df_raw.iterrows():
            row_values = [str(val).strip() if pd.notna(val) else '' for val in row]
            if 'July' in row_values:
                header_row = i
                data_start_row = i + 1
                break
        
        if header_row is not None:
            # Extract column names (months)
            columns = ['Account']
            for val in df_raw.iloc[header_row, 2:]:  # Skip first two columns
                if pd.notna(val):
                    columns.append(str(val).strip())
            
            # Extract data starting from data_start_row
            data_df = df_raw.iloc[data_start_row:].copy()
            
            # Create a clean dataframe
            clean_data = []
            for _, row in data_df.iterrows():
                account_name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ''
                if account_name and account_name != 'nan' and account_name.strip():
                    row_data = {'Account': account_name.strip()}
                    
                    # Add monthly data
                    for j, col_name in enumerate(columns[1:], start=2):
                        if j < len(row):
                            try:
                                value = row.iloc[j]
                                if pd.notna(value) and str(value).strip() != '':
                                    # Try to convert to numeric
                                    try:
                                        clean_value = str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', '')
                                        row_data[col_name] = float(clean_value)
                                    except ValueError:
                                        row_data[col_name] = 0.0
                                else:
                                    row_data[col_name] = 0.0
                            except (IndexError, AttributeError):
                                row_data[col_name] = 0.0
                    
                    if len(row_data) > 1:  # Only add if we have more than just the account name
                        clean_data.append(row_data)
            
            # Convert to DataFrame
            df_clean = pd.DataFrame(clean_data)
            
            # Skip the first row (Financial Status row)
            if len(df_clean) > 0 and 'Financial Status' in df_clean.iloc[0]['Account']:
                df_clean = df_clean.iloc[1:].reset_index(drop=True)
            
            return df_clean
        
        return None
        
    except Exception as e:
        print(f"Error loading financial data: {e}")
        return None

def categorize_accounts(df):
    """Categorize accounts into Revenue, Expenses, Assets, Liabilities"""
    revenue_keywords = ['Revenue', 'Income', 'Sales', 'Fee']
    expense_keywords = ['Expense', 'Cost', 'Administrative', 'Operating', 'Interest', 'Tax', 'Depreciation']
    asset_keywords = ['Cash', 'Account Receivable', 'Inventory', 'Asset', 'Equipment', 'Property']
    liability_keywords = ['Account Payable', 'Loan', 'Liability', 'Debt', 'Payable']
    
    categories = []
    for account in df['Account']:
        account_lower = account.lower()
        if any(keyword.lower() in account_lower for keyword in revenue_keywords):
            categories.append('Revenue')
        elif any(keyword.lower() in account_lower for keyword in expense_keywords):
            categories.append('Expenses')
        elif any(keyword.lower() in account_lower for keyword in asset_keywords):
            categories.append('Assets')
        elif any(keyword.lower() in account_lower for keyword in liability_keywords):
            categories.append('Liabilities')
        else:
            categories.append('Other')
    
    df['Category'] = categories
    return df

def calculate_financial_metrics(df):
    """Calculate key financial metrics"""
    months = [col for col in df.columns if col not in ['Account', 'Category', 'Total']]
    
    # Separate revenue and expenses
    revenue_df = df[df['Category'] == 'Revenue']
    expense_df = df[df['Category'] == 'Expenses']
    
    metrics = {}
    
    for month in months:
        total_revenue = revenue_df[month].sum() if len(revenue_df) > 0 else 0
        total_expenses = expense_df[month].sum() if len(expense_df) > 0 else 0
        net_income = total_revenue - total_expenses
        
        metrics[month] = {
            'revenue': total_revenue,
            'expenses': total_expenses,
            'net_income': net_income,
            'profit_margin': (net_income / total_revenue * 100) if total_revenue != 0 else 0
        }
    
    return metrics

def identify_cash_flow_issues(df, metrics):
    """Identify potential cash flow issues"""
    issues = []
    months = [col for col in df.columns if col not in ['Account', 'Category', 'Total']]
    
    # Check for negative net income
    negative_months = [month for month in months if metrics[month]['net_income'] < 0]
    if negative_months:
        issues.append({
            'type': 'Negative Net Income',
            'description': f"Negative net income in: {', '.join(negative_months)}",
            'severity': 'High'
        })
    
    # Check for declining revenue
    revenues = [metrics[month]['revenue'] for month in months if month != 'Total']
    if len(revenues) >= 3:
        recent_trend = revenues[-3:]
        if all(recent_trend[i] > recent_trend[i+1] for i in range(len(recent_trend)-1)):
            issues.append({
                'type': 'Declining Revenue',
                'description': "Revenue has been declining for the last 3 months",
                'severity': 'Medium'
            })
    
    # Check for high expense ratios
    for month in months:
        if month != 'Total' and metrics[month]['revenue'] != 0:
            expense_ratio = metrics[month]['expenses'] / metrics[month]['revenue']
            if expense_ratio > 0.8:
                issues.append({
                    'type': 'High Expense Ratio',
                    'description': f"Expenses are {expense_ratio:.1%} of revenue in {month}",
                    'severity': 'Medium'
                })
    
    return issues

def generate_forecast(df, metrics):
    """Generate simple forecast for remaining months"""
    months = [col for col in df.columns if col not in ['Account', 'Category', 'Total']]
    actual_months = months[:10]  # Assuming first 10 months are actual
    forecast_months = months[10:]  # Last 2 months are forecast
    
    if len(actual_months) < 3:
        return {}
    
    # Calculate trends from actual data
    actual_revenues = [metrics[month]['revenue'] for month in actual_months]
    actual_expenses = [metrics[month]['expenses'] for month in actual_months]
    
    # Simple linear trend
    revenue_trend = np.polyfit(range(len(actual_revenues)), actual_revenues, 1)[0]
    expense_trend = np.polyfit(range(len(actual_expenses)), actual_expenses, 1)[0]
    
    forecast = {}
    for i, month in enumerate(forecast_months):
        forecast_revenue = actual_revenues[-1] + revenue_trend * (i + 1)
        forecast_expense = actual_expenses[-1] + expense_trend * (i + 1)
        
        forecast[month] = {
            'revenue': max(0, forecast_revenue),  # Ensure non-negative
            'expenses': max(0, forecast_expense),
            'net_income': forecast_revenue - forecast_expense
        }
    
    return forecast

def test_financial_processor():
    """Test the financial processor functions"""
    filename = "MMC - Monthly Financial Data.xlsx"
    df = load_financial_data(filename)
    
    if df is not None:
        print("Data loaded successfully")
        print(f"Shape: {df.shape}")
        
        # Categorize accounts
        df = categorize_accounts(df)
        print(f"\nAccount categories:")
        print(df['Category'].value_counts())
        
        # Calculate metrics
        metrics = calculate_financial_metrics(df)
        print(f"\nSample metrics for July:")
        print(metrics['July'])
        
        # Identify issues
        issues = identify_cash_flow_issues(df, metrics)
        print(f"\nIdentified {len(issues)} potential issues")
        for issue in issues:
            print(f"- {issue['type']}: {issue['description']}")
        
        # Generate forecast
        forecast = generate_forecast(df, metrics)
        print(f"\nForecast generated for {len(forecast)} months")
        
    else:
        print("Failed to load data")

if __name__ == "__main__":
    test_financial_processor() 