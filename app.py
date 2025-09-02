import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from transformers import pipeline
import json
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple dark theme with attractive font
st.markdown("""
<style>
    /* Import attractive font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Main container */
    .main .block-container {
        background-color: #2d2d2d;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid #404040;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #252525;
        border-radius: 12px;
        border: 1px solid #404040;
    }
    
    /* Sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff;
        font-weight: 500;
        border-bottom: 1px solid #404040;
        padding-bottom: 0.5rem;
    }
    
    /* Profile card */
    .profile-card {
        background-color: #3a3a3a;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #505050;
        margin: 1rem 0;
    }
    
    /* Disclaimer */
    .disclaimer {
        background-color: #2a2a2a;
        border: 1px solid #505050;
        border-radius: 8px;
        padding: 1rem;
        color: #d0d0d0;
        margin: 1rem 0;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #3a3a3a;
        border-radius: 12px;
        border: 1px solid #505050;
        margin: 0.5rem 0;
    }
    
    /* User messages */
    .stChatMessage[data-testid="user-message"] {
        background-color: #4a4a4a;
        border-left: 3px solid #6c63ff;
    }
    
    /* Assistant messages */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #353535;
        border-left: 3px solid #00d4aa;
    }
    
    /* Metrics */
    .css-1xarl3l {
        background-color: #3a3a3a;
        border-radius: 8px;
        border: 1px solid #505050;
        transition: transform 0.2s ease;
    }
    
    .css-1xarl3l:hover {
        transform: translateY(-2px);
        border-color: #6c63ff;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #6c63ff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #5a52d5;
        transform: translateY(-1px);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: #404040;
        color: #e0e0e0;
        border: 1px solid #606060;
        border-radius: 6px;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6c63ff;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #505050;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background-color: #2d2d2d;
        border: 1px solid #505050;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Success/Error/Warning messages */
    .stSuccess {
        background-color: #1a4d3a;
        border: 1px solid #28a745;
        color: #90ee90;
    }
    
    .stError {
        background-color: #4d1a1a;
        border: 1px solid #dc3545;
        color: #ffb3b3;
    }
    
    .stWarning {
        background-color: #4d4d1a;
        border: 1px solid #ffc107;
        color: #ffeb99;
    }
    
    .stInfo {
        background-color: #1a3a4d;
        border: 1px solid #17a2b8;
        color: #99d6e6;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #2d2d2d;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #6c63ff;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a52d5;
    }
    
    /* Form styling */
    .stForm {
        background-color: #353535;
        border-radius: 12px;
        border: 1px solid #505050;
        padding: 1.5rem;
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    
    p, div, span {
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {}
if 'monthly_analysis' not in st.session_state:
    st.session_state.monthly_analysis = {}
if 'custom_categories' not in st.session_state:
    st.session_state.custom_categories = []

class FinancialAssistant:
    def __init__(self):
        self.load_model()
    
    @st.cache_resource
    def load_model(_self):
        """Load Granite model for text generation"""
        try:
            # Using a lighter model for demo purposes - replace with Granite when available
            generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                tokenizer="microsoft/DialoGPT-medium",
                device=-1  # CPU
            )
            return generator
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None
    
    def generate_response(self, user_input, user_profile, context=""):
        """Generate personalized financial advice"""
        if not self.load_model():
            return "I'm having trouble connecting to my AI model. Please try again later."
        
        # Create demographic-aware prompt
        demographic = user_profile.get('demographic', 'general')
        age = user_profile.get('age', 'unknown')
        income = user_profile.get('income', 'unknown')
        goals = user_profile.get('goals', 'general financial wellness')
        
        if demographic == 'student':
            tone = "friendly, simple, and example-based"
            focus = "small savings strategies, budgeting tips, and affordable options"
        else:
            tone = "professional, structured, and detailed"
            focus = "investment strategies, tax optimization, and wealth building"
        
        prompt = f"""
        You are a helpful financial advisor. Respond in a {tone} manner.
        User profile: {demographic}, age {age}, income ₹{income}, goals: {goals}
        Focus on: {focus}
        
        User question: {user_input}
        Context: {context}
        
        Provide practical, personalized financial advice:
        """
        
        try:
            # Simulate Granite response with rule-based logic for demo
            return self.generate_rule_based_response(user_input, user_profile)
        except Exception as e:
            return f"I encountered an error while processing your request. Please try rephrasing your question."
    
    def generate_rule_based_response(self, user_input, user_profile):
        """Rule-based response generation as fallback"""
        demographic = user_profile.get('demographic', 'general')
        income = user_profile.get('income', 0)
        
        user_input_lower = user_input.lower()
        
        # Savings-related queries
        if any(word in user_input_lower for word in ['save', 'saving', 'savings']):
            if demographic == 'student':
                return f"""Great question! As a student, here are some practical saving tips:

💡 **Start Small**: Try saving ₹500-1000 monthly by:
- Cooking at home instead of ordering food
- Using student discounts
- Sharing subscriptions with friends
- Walking/cycling instead of taking auto/cab

📱 **For your goals**: If you're saving for something specific like a phone or laptop, break it down:
- Phone (₹15,000): Save ₹2,500/month for 6 months
- Laptop (₹40,000): Save ₹3,500/month for 12 months

Would you like me to create a personalized budget plan for you?"""
            else:
                return f"""Based on your professional profile, here's a structured savings approach:

💼 **The 50-30-20 Rule**:
- 50% for needs (₹{income*0.5:,.0f})
- 30% for wants (₹{income*0.3:,.0f})  
- 20% for savings (₹{income*0.2:,.0f})

🎯 **Investment Options**:
- Emergency fund: 6 months expenses in savings account
- SIP in index funds: ₹{min(income*0.1, 10000):,.0f}/month
- PPF for tax savings: Up to ₹1.5 lakh/year

Would you like a detailed investment breakdown?"""
        
        # Investment queries
        elif any(word in user_input_lower for word in ['invest', 'investment', 'sip', 'mutual fund']):
            if demographic == 'student':
                return """As a student, start with these simple investment steps:

🌱 **Begin Small**:
- Start with ₹500-1000/month SIP
- Choose index funds (low cost, diversified)
- Use apps like Groww or Zerodha Coin

📚 **Learn First**: 
- Understand risk vs returns
- Start with large-cap funds (safer)
- Avoid stock picking initially

Remember: Consistency matters more than amount!"""
            else:
                return f"""Here's a professional investment strategy for your ₹{income:,} monthly income:

📊 **Asset Allocation**:
- Equity (60%): ₹{income*0.12:,.0f}/month in diversified funds
- Debt (30%): ₹{income*0.06:,.0f}/month in debt funds/FDs
- Gold (10%): ₹{income*0.02:,.0f}/month in gold ETFs

🏛️ **Tax-Saving Options**:
- ELSS funds: Up to ₹1.5L under 80C
- PPF: 15-year lock-in, tax-free returns
- NPS: Additional ₹50K deduction under 80CCD

Want me to create a detailed investment portfolio?"""
        
        # Budget queries
        elif any(word in user_input_lower for word in ['budget', 'expense', 'spending']):
            return """I'd love to help you create a budget! 

📝 **Let's gather your financial info**:
- Monthly income
- Fixed expenses (rent, utilities, EMIs)
- Variable expenses (food, transport, entertainment)
- Savings goals

You can either:
1. Tell me your numbers in chat
2. Use the budget form in the sidebar

Once I have your data, I'll create:
- Visual budget breakdown
- Spending analysis
- Personalized recommendations"""
        
        # General greeting or unclear query
        else:
            return f"""Hello! I'm your personal finance assistant. 

Based on your profile ({demographic}), I can help you with:
- 💰 Savings strategies
- 📈 Investment advice  
- 📊 Budget planning
- 💡 Spending insights

What would you like to know about? Feel free to ask questions like:
- "How do I save for a laptop?"
- "What investments should I consider?"
- "Help me create a budget"
- "How much should I spend on entertainment?"

I'm here to provide personalized advice based on your situation!"""

def collect_user_profile():
    """Collect user profile information"""
    st.sidebar.header("👤 Your Profile")
    
    with st.sidebar.form("profile_form"):
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        income = st.number_input("Monthly Income (₹)", min_value=0, value=30000, step=1000)
        demographic = st.selectbox("I am a:", ["student", "professional"])
        goals = st.text_area("Financial Goals", 
                           placeholder="e.g., Save for laptop, buy a house, retirement planning")
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            st.session_state.user_profile = {
                'age': age,
                'income': income,
                'demographic': demographic,
                'goals': goals
            }
            st.success("Profile updated!")
    
    # Display current profile
    if st.session_state.user_profile:
        st.sidebar.markdown("### Current Profile")
        profile = st.session_state.user_profile
        st.sidebar.markdown(f"""
        <div class="profile-card">
        <strong>Age:</strong> {profile.get('age', 'Not set')}<br>
        <strong>Income:</strong> ₹{profile.get('income', 0):,}/month<br>
        <strong>Type:</strong> {profile.get('demographic', 'Not set').title()}<br>
        <strong>Goals:</strong> {profile.get('goals', 'Not set')}
        </div>
        """, unsafe_allow_html=True)

def budget_analyzer():
    """Budget analysis interface"""
    st.sidebar.header("📊 Budget Analyzer")
    
    with st.sidebar.form("budget_form"):
        st.markdown("### Monthly Expenses")
        rent = st.number_input("Rent/Housing (₹)", min_value=0, value=10000)
        food = st.number_input("Food & Groceries (₹)", min_value=0, value=5000)
        transport = st.number_input("Transport (₹)", min_value=0, value=3000)
        utilities = st.number_input("Utilities (₹)", min_value=0, value=2000)
        entertainment = st.number_input("Entertainment (₹)", min_value=0, value=3000)
        shopping = st.number_input("Shopping (₹)", min_value=0, value=2000)
        others = st.number_input("Others (₹)", min_value=0, value=1000)
        
        analyze_budget = st.form_submit_button("Analyze Budget")
        
        if analyze_budget:
            income = st.session_state.user_profile.get('income', 0)
            expenses = {
                'Rent/Housing': rent,
                'Food & Groceries': food,
                'Transport': transport,
                'Utilities': utilities,
                'Entertainment': entertainment,
                'Shopping': shopping,
                'Others': others
            }
            
            total_expenses = sum(expenses.values())
            savings = income - total_expenses
            
            st.session_state.budget_data = {
                'income': income,
                'expenses': expenses,
                'total_expenses': total_expenses,
                'savings': savings
            }
            
            st.success("Budget analyzed! Check the main area for insights.")

def display_budget_analysis():
    """Display budget analysis with charts"""
    if not st.session_state.budget_data:
        return
    
    data = st.session_state.budget_data
    
    st.header("📊 Your Budget Analysis")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Income", f"₹{data['income']:,}")
    
    with col2:
        st.metric("Total Expenses", f"₹{data['total_expenses']:,}")
    
    with col3:
        savings_rate = (data['savings'] / data['income'] * 100) if data['income'] > 0 else 0
        st.metric("Savings", f"₹{data['savings']:,}", f"{savings_rate:.1f}%")
    
    with col4:
        expense_ratio = (data['total_expenses'] / data['income'] * 100) if data['income'] > 0 else 0
        st.metric("Expense Ratio", f"{expense_ratio:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart of expenses
        fig_pie = px.pie(
            values=list(data['expenses'].values()),
            names=list(data['expenses'].keys()),
            title="Expense Breakdown"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart comparison
        categories = ['Income', 'Expenses', 'Savings']
        values = [data['income'], data['total_expenses'], data['savings']]
        colors = ['green', 'red', 'blue']
        
        fig_bar = go.Figure(data=[
            go.Bar(x=categories, y=values, marker_color=colors)
        ])
        fig_bar.update_layout(title="Income vs Expenses vs Savings")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Generate insights
    generate_budget_insights(data)

def generate_budget_insights(data):
    """Generate spending insights and recommendations"""
    st.header("💡 Spending Insights")
    
    income = data['income']
    expenses = data['expenses']
    savings_rate = (data['savings'] / income * 100) if income > 0 else 0
    
    insights = []
    recommendations = []
    
    # Savings rate analysis
    if savings_rate < 10:
        insights.append("⚠️ Your savings rate is below 10% - this is concerning for long-term financial health.")
        recommendations.append("Try to increase your savings to at least 20% of income.")
    elif savings_rate < 20:
        insights.append("📈 Your savings rate is decent but could be improved.")
        recommendations.append("Aim for 20-30% savings rate for better financial security.")
    else:
        insights.append("✅ Excellent savings rate! You're on track for good financial health.")
    
    # Category-wise analysis
    for category, amount in expenses.items():
        percentage = (amount / income * 100) if income > 0 else 0
        
        if category == 'Rent/Housing' and percentage > 30:
            insights.append(f"🏠 Housing costs ({percentage:.1f}%) are high - ideally should be under 30%.")
            recommendations.append("Consider finding more affordable housing or getting roommates.")
        
        elif category == 'Food & Groceries' and percentage > 15:
            insights.append(f"🍽️ Food expenses ({percentage:.1f}%) are above recommended 10-15%.")
            recommendations.append("Try meal planning and cooking at home more often.")
        
        elif category == 'Entertainment' and percentage > 10:
            insights.append(f"🎬 Entertainment spending ({percentage:.1f}%) is quite high.")
            recommendations.append("Look for free or low-cost entertainment options.")
    
    # Display insights
    for insight in insights:
        st.markdown(f"- {insight}")
    
    if recommendations:
        st.subheader("🎯 Recommendations")
        for rec in recommendations:
            st.markdown(f"- {rec}")

def main():
    """Main application"""
    # Initialize assistant
    assistant = FinancialAssistant()
    
    # Header
    st.markdown('<h1 class="main-header">💰 Personal Finance Assistant</h1>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
    <strong>⚠️ Disclaimer:</strong> This chatbot provides general financial guidance and is not a licensed financial advisor. 
    Please consult with qualified professionals for personalized financial advice.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    collect_user_profile()
    budget_analyzer()
    
    # Main chat interface
    st.header("💬 Chat with Your Financial Assistant")
    
    # Display budget analysis if available
    if st.session_state.budget_data:
        with st.expander("📊 View Budget Analysis", expanded=False):
            display_budget_analysis()
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about personal finance..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context = ""
                if st.session_state.budget_data:
                    context = f"User's budget data: Income ₹{st.session_state.budget_data['income']:,}, Expenses ₹{st.session_state.budget_data['total_expenses']:,}, Savings ₹{st.session_state.budget_data['savings']:,}"
                
                response = assistant.generate_response(
                    prompt, 
                    st.session_state.user_profile,
                    context
                )
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
