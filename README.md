# MMC Financial Dashboard

A comprehensive financial dashboard for **Mering Management Corporation Pty Ltd** built with Streamlit, providing insights into financial performance, cash flow analysis, and forecasting.

## Features

### 📊 Financial Overview
- **Key Metrics Display**: Current revenue, expenses, net income, and profit margin
- **Monthly Trends**: Visual charts showing revenue and expense trends over time
- **Profit Analysis**: Monthly profit margin and net income visualization

### 🔍 Detailed Analysis
- **Category Breakdown**: Pie chart showing distribution across Revenue, Expenses, Assets, Liabilities
- **Top Accounts**: List of largest accounts by total value
- **Monthly Trends by Category**: Line charts showing how each category performs over time

### ⚠️ Cash Flow Issues
- **Automated Issue Detection**: Identifies potential problems such as:
  - Negative net income months
  - Declining revenue trends
  - High expense ratios (>80% of revenue)
- **Monthly Cash Flow Summary**: Detailed table with highlighting for negative values

### 🔮 Financial Forecast
- **Predictive Analysis**: Simple linear trend forecasting for upcoming months
- **Actual vs Forecast Comparison**: Visual comparison of historical and projected data
- **Revenue and Expense Projections**: Separate forecasts for income and costs

### 📋 Raw Data Access
- **Complete Data Table**: View all financial data in tabular format
- **CSV Export**: Download functionality for further analysis

## Installation & Setup

### Prerequisites
- Python 3.12+
- UV package manager

### Installation
1. Clone or download the project files
2. Create a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Dashboard
1. Ensure the Excel file `MMC - Monthly Financial Data.xlsx` is in the project directory
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Launch the dashboard:
   ```bash
   streamlit run dashboard.py
   ```
4. Open your browser to the provided URL (typically http://localhost:8501)

## File Structure

```
Financial/
├── dashboard.py              # Main Streamlit application
├── financial_processor.py    # Data processing and analysis functions
├── examine_excel.py         # Excel file structure examination
├── test_dashboard.py        # Testing script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── MMC - Monthly Financial Data.xlsx  # Source data file
```

## Data Structure

The dashboard expects an Excel file with the following structure:
- **Sheet Name**: 'MMC'
- **Header Row**: Month names (July, August, September, etc.)
- **Data Rows**: Account names in column 2, monthly values in subsequent columns
- **Categories**: Accounts are automatically categorized based on keywords:
  - **Revenue**: Keywords like 'Revenue', 'Income', 'Sales', 'Fee'
  - **Expenses**: Keywords like 'Expense', 'Cost', 'Administrative'
  - **Assets**: Keywords like 'Cash', 'Receivable', 'Asset'
  - **Liabilities**: Keywords like 'Payable', 'Loan', 'Debt'

## Key Insights Provided

### Current Analysis (Based on your data):
- **Revenue Performance**: Monthly revenue ranging from $264,951 to $622,039
- **Expense Management**: Monthly expenses from $276,933 to $491,835
- **Profitability**: Net income varies from -$80,430 to $133,845
- **Risk Areas**: 10 potential issues identified including:
  - Negative net income in November, February, and May
  - High expense ratios (>80%) in multiple months

### Dashboard Navigation
- **Overview**: Quick snapshot of financial health
- **Detailed Analysis**: Deep dive into categories and trends
- **Cash Flow Issues**: Specific problems and warnings
- **Forecast**: Future projections based on trends
- **Raw Data**: Complete data access and export

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations
- **OpenPyXL**: Excel file reading

### Testing
Run the test suite to verify functionality:
```bash
python3 test_dashboard.py
```

### Performance Features
- **Data Caching**: Uses Streamlit's caching for faster load times
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Charts**: Hover, zoom, and pan capabilities

## Troubleshooting

### Common Issues
1. **Excel file not found**: Ensure `MMC - Monthly Financial Data.xlsx` is in the same directory
2. **Import errors**: Make sure all dependencies are installed with `uv pip install -r requirements.txt`
3. **Data loading failures**: Check Excel file format and sheet name

### Support
For issues or questions about the dashboard functionality, check the test script output for detailed error messages.

## Future Enhancements
- Multi-year analysis capability
- Custom forecast parameters
- Advanced financial ratios
- Export to PDF reports
- Email alert system for critical issues 