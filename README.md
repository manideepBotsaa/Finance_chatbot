# Personal Finance Assistant 💰

A comprehensive Streamlit-based financial chatbot that provides personalized financial guidance using AI. The assistant adapts its communication style and recommendations based on user demographics (student vs professional) and provides interactive budget analysis with visualizations.

## Features

### 🎯 Core Functionality
- **Personalized Chat Interface**: Natural language financial conversations
- **User Profile Management**: Age, income, goals, and demographic tracking
- **Budget Analysis**: Comprehensive income/expense tracking with visual charts
- **Spending Insights**: Automated detection of overspending patterns
- **Demographic-Aware Responses**: Tailored advice for students vs professionals

### 📊 Budget & Analytics
- Interactive expense tracking forms
- Real-time budget calculations
- Visual charts (pie charts, bar graphs) using Plotly
- Spending pattern analysis with recommendations
- Savings rate calculations and benchmarking

### 🤖 AI-Powered Guidance
- Context-aware financial advice
- Rule-based response system with AI integration
- Personalized investment recommendations
- Savings strategy suggestions
- Tax optimization tips

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

### Setting Up Your Profile
1. Use the sidebar "Your Profile" section
2. Enter your age, monthly income, demographic (student/professional), and financial goals
3. Click "Update Profile" to save

### Budget Analysis
1. Fill out the "Budget Analyzer" form in the sidebar
2. Enter your monthly expenses across different categories
3. Click "Analyze Budget" to generate insights
4. View detailed charts and recommendations in the main area

### Chat Interface
- Ask natural language questions about finances
- Examples:
  - "How do I save for a laptop?"
  - "What investments should I consider?"
  - "Help me create a budget"
  - "How much should I spend on entertainment?"

## Sample Test Profiles

### Student Profile
- **Age**: 20
- **Income**: ₹10,000/month
- **Goals**: Save for laptop and emergency fund
- **Sample Budget**:
  - Housing: ₹4,000
  - Food: ₹2,500
  - Transport: ₹1,000
  - Others: ₹2,500

### Professional Profile
- **Age**: 28
- **Income**: ₹1,00,000/month
- **Goals**: House down payment, retirement planning
- **Sample Budget**:
  - Housing: ₹25,000
  - Food: ₹8,000
  - Transport: ₹5,000
  - Others: ₹33,000

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
- **Transformers**: AI model integration (Granite/DialoGPT)
- **Matplotlib**: Additional charting capabilities

### Financial Guidelines
- Savings rate benchmarks (10%, 20%, 30%)
- Expense ratio guidelines by category
- Demographic-specific advice templates

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

## Future Enhancements

- [ ] Integration with real Granite model API
- [ ] Export budget data to Excel/PDF
- [ ] Investment portfolio tracking
- [ ] Goal-based savings tracking
- [ ] Multi-language support
- [ ] Mobile-responsive design improvements

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
