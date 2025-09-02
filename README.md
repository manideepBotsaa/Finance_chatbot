# Personal Finance Assistant 💰

A comprehensive Streamlit-based financial chatbot that provides personalized financial guidance using AI. The assistant features a modern dark theme with attractive Poppins font, adapts its communication style based on user demographics and risk tolerance, and provides advanced financial tools including savings goal tracking, spending alerts, and investment calculators.

## Features
## Technical Architecture

### Core Components
- **app.py**: Main Streamlit application
- **config.py**: Configuration settings and templates
- **utils.py**: Utility functions for calculations and analysis
- **requirements.txt**: Python dependencies

### Key Technologies
- **Streamlit**: Web interface framework
- **Pandas**: Data analysis and calculations
- **Plotly**: Interactive visualizations
- **Transformers**: AI model integration (IBM Granite-Hugging Face model)
- **Matplotlib**: Additional charting capabilities
### 🎯 Core Functionality
- **Personalized Chat Interface**: Natural language financial conversations with AI
- **Enhanced User Profiling**: Age, income, goals, demographic, and risk tolerance assessment
- **Multi-Tab Interface**: Organized sections for chat, budget analysis, monthly tracking, savings goals, and tools
- **Dark Theme UI**: Clean, modern interface with attractive Poppins font
- **Demographic-Aware Responses**: Tailored advice for students, professionals, freelancers, entrepreneurs, and retirees

### 📊 Advanced Budget & Analytics
- **Budget Analysis**: Comprehensive income/expense tracking with visual charts
- **Monthly Analysis**: Custom expense categories with flexible tracking
- **CSV Upload**: Import and analyze expense data from bank statements
- **Spending Alerts**: Automated detection of overspending patterns and anomalies
- **What-If Scenarios**: Simulate income changes and expense reductions

### 🎯 Savings & Goals Management
- **Savings Goal Tracker**: Set multiple goals with progress visualization
- **Priority-Based Planning**: High/Medium/Low priority goal management
- **Progress Updates**: Track monthly savings progress with visual indicators
- **Goal Timeline Calculation**: Automatic calculation of months needed to reach targets

### 📈 Investment Tools
- **Risk-Based Investment Calculator**: Returns based on conservative/moderate/aggressive profiles
- **Portfolio Allocation**: Customized asset allocation recommendations
- **SIP Calculator**: Compound interest calculations for systematic investments
- **Tax-Saving Options**: ELSS, PPF, and NPS recommendations

### 🤖 Enhanced AI Guidance
- **Risk-Aware Advice**: Investment recommendations based on risk tolerance
- **Multi-Demographic Support**: Specialized advice for different user types
- **Context-Aware Responses**: Considers user profile, budget data, and goals
- **Spending Pattern Analysis**: Intelligent insights and recommendations

## Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## Usage Guide

### 1. Setting Up Your Profile
1. Use the sidebar "Your Profile" section
2. Enter your age, monthly income, demographic (student/professional/freelancer/entrepreneur/retiree)
3. Set your risk tolerance (conservative/moderate/aggressive)
4. Add your financial goals
5. Click "Update Profile" to save

### 2. Budget Analysis
1. Fill out the "Budget Analyzer" form in the sidebar
2. Enter your monthly expenses across different categories
3. Click "Analyze Budget" to generate insights
4. View detailed charts and recommendations in the "Budget Analysis" tab

### 3. Monthly Analysis (Custom Expenses)
1. Add custom expense categories in the "Monthly Analysis" section
2. Input your monthly expenses for each category
3. Select the month you're analyzing
4. View personalized insights and visualizations

### 4. Savings Goals
1. Set multiple savings goals with target amounts
2. Define monthly savings for each goal
3. Set priorities (High/Medium/Low)
4. Track progress with visual progress bars
5. Update progress monthly

### 5. Advanced Tools
- **Spending Alerts**: Get warnings for overspending in categories
- **What-If Scenarios**: Simulate income/expense changes
- **CSV Upload**: Import bank statements for automatic analysis
- **Investment Calculator**: Calculate returns based on your risk profile

### 6. Chat Interface
- Ask natural language questions about finances
- Get risk-aware investment advice
- Examples:
  - "How do I save for a laptop and bike together?"
  - "What investments suit my aggressive risk profile?"
  - "Help me create a budget for a freelancer"
  - "Show me what-if scenarios for 20% income increase"

## Features in Detail

### 💬 Chat Interface
- Real-time conversational AI
- Context-aware responses
- Session memory for continuous conversations
- Personalized advice based on user profile

### 📈 Budget Analysis
- Comprehensive expense tracking
- Visual breakdown with pie and bar charts
- Savings rate calculation
- Expense ratio analysis
- Overspending detection

### 🎯 Personalized Recommendations
- **Students**: Focus on small savings, budgeting basics, affordable options
- **Professionals**: Investment strategies, tax optimization, wealth building
- Dynamic response generation based on user context

### 📊 Visual Analytics
- Interactive Plotly charts
- Expense category breakdowns
- Income vs expenses comparison
- Savings trend visualization

## Security & Privacy

- **No Data Storage**: All data is session-based only
- **Privacy First**: No personal information is permanently stored
- **Disclaimer**: Clear messaging that this is not licensed financial advice
- **Input Validation**: Robust error handling for user inputs

## Customization

### Adding New Response Templates
Edit `config.py` to add new demographic categories or response patterns:

```python
RESPONSE_TEMPLATES = {
    "new_demographic": {
        "tone": "your_preferred_tone",
        "focus": "specific_focus_areas",
        "greeting": "custom_greeting"
    }
}
```

### Modifying Financial Guidelines
Update expense ratios and savings benchmarks in `config.py`:

```python
FINANCIAL_GUIDELINES = {
    "expense_ratios": {
        "category_name": percentage_limit
    }
}
```

## Troubleshooting

### Common Issues
1. **Model Loading Errors**: Check internet connection and model availability
2. **Chart Display Issues**: Ensure Plotly is properly installed
3. **Calculation Errors**: Verify all numeric inputs are valid

### Performance Optimization
- Model responses are cached using Streamlit's caching
- Large datasets are processed efficiently with Pandas
- Charts are rendered client-side for better performance

## Application Structure

### Main Tabs
1. **Chat Assistant**: AI-powered financial conversations with risk-aware advice
2. **Budget Analysis**: Comprehensive expense tracking and visualization
3. **Monthly Analysis**: Custom expense categories and monthly insights
4. **Savings Goals**: Multi-goal tracking with progress visualization
5. **Tools & Analysis**: Advanced features including:
   - Spending Alerts & Anomaly Detection
   - What-If Scenario Simulator
   - CSV Expense Upload & Analysis
   - Investment Calculator with Risk Profiles

### Sidebar Features
- **User Profile**: Demographics, income, goals, and risk tolerance
- **Budget Analyzer**: Quick expense input and analysis
- **Monthly Analysis**: Custom category management
- **Savings Goal Tracker**: Goal creation and progress updates

## Future Enhancements

- [ ] Integration with real banking APIs for automatic transaction import
- [ ] Export budget data to Excel/PDF reports
- [ ] Advanced portfolio tracking with real-time market data
- [ ] Recurring vs one-time expense categorization
- [ ] Tax estimation and inflation adjustment tools
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Voice input/output capabilities
- [ ] Mobile app version
- [ ] Gamification features (badges, achievements)
- [ ] Educational resources and financial literacy modules

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and personal use. Please consult with qualified financial professionals for personalized financial advice.

## Disclaimer

⚠️ **Important**: This chatbot provides general financial guidance and is not a licensed financial advisor. Always consult with qualified professionals for personalized financial advice tailored to your specific situation.

---

**Built with ❤️ using Streamlit, AI, and modern data visualization tools.**
