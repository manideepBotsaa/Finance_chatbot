"""
Configuration settings for the Financial Assistant
"""

# Model Configuration
MODEL_CONFIG = {
    "primary_model": "ibm/granite-3b-code-instruct",  # Granite model when available
    "fallback_model": "microsoft/DialoGPT-medium",    # Fallback model
    "max_length": 512,
    "temperature": 0.7,
    "do_sample": True,
    "pad_token_id": 50256
}

# Financial Guidelines
FINANCIAL_GUIDELINES = {
    "savings_rate": {
        "excellent": 30,
        "good": 20,
        "acceptable": 10,
        "poor": 0
    },
    "expense_ratios": {
        "housing": 30,
        "food": 15,
        "transport": 15,
        "entertainment": 10,
        "utilities": 10,
        "shopping": 10,
        "others": 10
    }
}

# Response Templates
RESPONSE_TEMPLATES = {
    "student": {
        "tone": "friendly, simple, and example-based",
        "focus": "small savings strategies, budgeting tips, and affordable options",
        "greeting": "Hey there! I'm here to help you with your finances as a student. 🎓",
        "savings_advice": "Start small and be consistent - even ₹500/month adds up!",
        "investment_advice": "Begin with SIPs in index funds - they're simple and effective for beginners."
    },
    "professional": {
        "tone": "professional, structured, and detailed",
        "focus": "investment strategies, tax optimization, and wealth building",
        "greeting": "Welcome! I'll help you optimize your financial strategy. 💼",
        "savings_advice": "Follow the 50-30-20 rule and maximize tax-advantaged accounts.",
        "investment_advice": "Consider diversified portfolio allocation based on your risk tolerance."
    }
}

# Sample Profiles for Testing
SAMPLE_PROFILES = {
    "student": {
        "age": 20,
        "income": 10000,
        "demographic": "student",
        "goals": "Save for laptop and emergency fund",
        "sample_expenses": {
            "Rent/Housing": 4000,
            "Food & Groceries": 2500,
            "Transport": 1000,
            "Utilities": 500,
            "Entertainment": 1500,
            "Shopping": 500,
            "Others": 0
        }
    },
    "professional": {
        "age": 28,
        "income": 100000,
        "demographic": "professional",
        "goals": "House down payment, retirement planning, tax optimization",
        "sample_expenses": {
            "Rent/Housing": 25000,
            "Food & Groceries": 8000,
            "Transport": 5000,
            "Utilities": 3000,
            "Entertainment": 10000,
            "Shopping": 15000,
            "Others": 5000
        }
    }
}

# Error Messages
ERROR_MESSAGES = {
    "model_error": "I'm having trouble processing your request. Please try again in a moment.",
    "invalid_input": "Please provide valid numerical values for your financial data.",
    "no_profile": "Please set up your profile first using the sidebar form.",
    "calculation_error": "There was an error calculating your budget. Please check your inputs."
}

# UI Configuration
UI_CONFIG = {
    "primary_color": "#1f77b4",
    "success_color": "#4caf50",
    "warning_color": "#ff9800",
    "error_color": "#f44336",
    "chart_colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
}
