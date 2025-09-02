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
if 'savings_goals' not in st.session_state:
    st.session_state.savings_goals = []
if 'risk_tolerance' not in st.session_state:
    st.session_state.risk_tolerance = 'moderate'
if 'expense_history' not in st.session_state:
    st.session_state.expense_history = []

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
            risk_tolerance = st.session_state.risk_tolerance
            
            if demographic == 'student':
                if risk_tolerance == 'conservative':
                    return """As a student with conservative risk preference:

🛡️ **Safe Start**:
- Begin with ₹500/month in debt funds
- Fixed deposits for emergency fund
- PPF for long-term tax savings

📚 **Learn & Grow**: 
- Start with 80% debt, 20% equity
- Use SIP to average out market volatility
- Focus on large-cap funds initially"""
                elif risk_tolerance == 'aggressive':
                    return """As a student ready for higher risk:

🚀 **Growth Focus**:
- Start with ₹1000/month in equity funds
- 70% equity, 30% debt allocation
- Consider small-cap funds for higher returns

⚡ **High Growth Strategy**:
- Index funds + sectoral funds
- Start early for compound growth advantage
- Review and increase SIP annually"""
                else:
                    return """As a student with moderate risk appetite:

⚖️ **Balanced Approach**:
- Start with ₹500-1000/month SIP
- 50% equity, 50% debt allocation
- Mix of large-cap and mid-cap funds

📈 **Steady Growth**: 
- Use apps like Groww or Zerodha Coin
- Increase investment as income grows
- Focus on consistency over amount"""
            else:
                # Professional investment advice based on risk tolerance
                if risk_tolerance == 'conservative':
                    return f"""Conservative investment strategy for ₹{income:,} income:

🛡️ **Low-Risk Portfolio**:
- Debt funds (60%): ₹{income*0.12:,.0f}/month
- Large-cap equity (30%): ₹{income*0.06:,.0f}/month  
- Gold ETF (10%): ₹{income*0.02:,.0f}/month

🏛️ **Tax-Efficient Options**:
- PPF: ₹12,500/month for 15-year lock-in
- ELSS: Tax-saving with 3-year lock-in
- NSC/FD: For stable returns"""
                elif risk_tolerance == 'aggressive':
                    return f"""Aggressive growth strategy for ₹{income:,} income:

🚀 **High-Growth Portfolio**:
- Equity funds (70%): ₹{income*0.14:,.0f}/month
- Mid/Small cap (20%): ₹{income*0.04:,.0f}/month
- International funds (10%): ₹{income*0.02:,.0f}/month

📈 **Growth Focus**:
- Sectoral funds for higher returns
- Direct equity for experienced investors
- Regular portfolio rebalancing"""
                else:
                    return f"""Balanced investment strategy for ₹{income:,} income:

⚖️ **Moderate Portfolio**:
- Equity funds (60%): ₹{income*0.12:,.0f}/month
- Debt funds (30%): ₹{income*0.06:,.0f}/month
- Gold/International (10%): ₹{income*0.02:,.0f}/month

🎯 **Tax-Saving Options**:
- ELSS funds: Up to ₹1.5L under 80C
- PPF: 15-year lock-in, tax-free returns
- NPS: Additional ₹50K deduction under 80CCD"""
        
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
        demographic = st.selectbox("I am a:", ["student", "professional", "freelancer", "entrepreneur", "retiree"])
        goals = st.text_area("Financial Goals", 
                           placeholder="e.g., Save for laptop, buy a house, retirement planning")
        
        # Risk tolerance assessment
        st.markdown("### Risk Tolerance")
        risk_tolerance = st.radio(
            "Investment Risk Preference:",
            ["conservative", "moderate", "aggressive"],
            index=1,
            help="Conservative: Safe investments, Moderate: Balanced approach, Aggressive: Higher risk/reward"
        )
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            st.session_state.user_profile = {
                'age': age,
                'income': income,
                'demographic': demographic,
                'goals': goals
            }
            st.session_state.risk_tolerance = risk_tolerance
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
        <strong>Risk:</strong> {st.session_state.risk_tolerance.title()}<br>
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

def monthly_analysis_section():
    """Monthly analysis with custom expense categories"""
    st.sidebar.header("📅 Monthly Analysis")
    
    # Add custom category
    with st.sidebar.form("add_category_form"):
        st.markdown("### Add Custom Category")
        new_category = st.text_input("Category Name", placeholder="e.g., Gym Membership, Pet Care")
        add_category = st.form_submit_button("Add Category")
        
        if add_category and new_category:
            if new_category not in st.session_state.custom_categories:
                st.session_state.custom_categories.append(new_category)
                st.success(f"Added '{new_category}' category!")
            else:
                st.warning("Category already exists!")
    
    # Monthly expense input
    if st.session_state.custom_categories:
        with st.sidebar.form("monthly_expenses_form"):
            st.markdown("### Monthly Expenses")
            
            # Default categories
            default_categories = {
                "Food & Dining": 0,
                "Transportation": 0,
                "Shopping": 0,
                "Entertainment": 0,
                "Bills & Utilities": 0,
                "Healthcare": 0
            }
            
            # Collect expenses for default categories
            monthly_expenses = {}
            for category in default_categories:
                amount = st.number_input(f"{category} (₹)", min_value=0, value=0, step=100, key=f"default_{category}")
                monthly_expenses[category] = amount
            
            # Collect expenses for custom categories
            for category in st.session_state.custom_categories:
                amount = st.number_input(f"{category} (₹)", min_value=0, value=0, step=100, key=f"custom_{category}")
                monthly_expenses[category] = amount
            
            # Month selection
            selected_month = st.selectbox("Month", 
                ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"])
            
            analyze_month = st.form_submit_button("Analyze This Month")
            
            if analyze_month:
                # Filter out zero expenses
                filtered_expenses = {k: v for k, v in monthly_expenses.items() if v > 0}
                
                if filtered_expenses:
                    st.session_state.monthly_analysis = {
                        'month': selected_month,
                        'expenses': filtered_expenses,
                        'total': sum(filtered_expenses.values()),
                        'timestamp': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.success(f"Analyzed expenses for {selected_month}!")
                else:
                    st.warning("Please add at least one expense amount!")
    
    # Remove category option
    if st.session_state.custom_categories:
        st.sidebar.markdown("### Manage Categories")
        category_to_remove = st.sidebar.selectbox("Remove Category", 
            ["Select category to remove..."] + st.session_state.custom_categories)
        
        if st.sidebar.button("Remove Selected Category"):
            if category_to_remove != "Select category to remove...":
                st.session_state.custom_categories.remove(category_to_remove)
                st.success(f"Removed '{category_to_remove}' category!")

def savings_goal_tracker():
    """Savings goal tracker with progress visualization"""
    st.sidebar.header("🎯 Savings Goals")
    
    # Add new goal
    with st.sidebar.form("add_goal_form"):
        st.markdown("### Add Savings Goal")
        goal_name = st.text_input("Goal Name", placeholder="e.g., New Laptop, Vacation")
        target_amount = st.number_input("Target Amount (₹)", min_value=0, value=20000, step=1000)
        monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0, value=2000, step=100)
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        add_goal = st.form_submit_button("Add Goal")
        
        if add_goal and goal_name and target_amount > 0:
            months_needed = target_amount / monthly_savings if monthly_savings > 0 else float('inf')
            
            new_goal = {
                'name': goal_name,
                'target': target_amount,
                'monthly_savings': monthly_savings,
                'current_saved': 0,
                'priority': priority,
                'months_needed': months_needed,
                'created_date': pd.Timestamp.now().strftime("%Y-%m-%d")
            }
            
            st.session_state.savings_goals.append(new_goal)
            st.success(f"Added goal: {goal_name}!")
    
    # Update progress
    if st.session_state.savings_goals:
        with st.sidebar.form("update_progress_form"):
            st.markdown("### Update Progress")
            goal_names = [goal['name'] for goal in st.session_state.savings_goals]
            selected_goal = st.selectbox("Select Goal", goal_names)
            amount_saved = st.number_input("Amount Saved This Month (₹)", min_value=0, value=0, step=100)
            
            update_progress = st.form_submit_button("Update Progress")
            
            if update_progress and amount_saved > 0:
                for goal in st.session_state.savings_goals:
                    if goal['name'] == selected_goal:
                        goal['current_saved'] += amount_saved
                        st.success(f"Updated {selected_goal} progress!")
                        break

def display_savings_goals():
    """Display savings goals with progress bars"""
    if not st.session_state.savings_goals:
        st.info("💡 Use the Savings Goals section in the sidebar to set your financial targets!")
        return
    
    st.header("🎯 Your Savings Goals")
    
    for i, goal in enumerate(st.session_state.savings_goals):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                progress = min(goal['current_saved'] / goal['target'], 1.0)
                st.markdown(f"### {goal['name']}")
                st.progress(progress)
                
                remaining = max(goal['target'] - goal['current_saved'], 0)
                months_remaining = remaining / goal['monthly_savings'] if goal['monthly_savings'] > 0 else float('inf')
                
                st.markdown(f"""
                **Target:** ₹{goal['target']:,} | **Saved:** ₹{goal['current_saved']:,} | **Remaining:** ₹{remaining:,}
                
                **Progress:** {progress*100:.1f}% | **Months to go:** {months_remaining:.1f}
                """)
            
            with col2:
                st.metric("Priority", goal['priority'])
            
            with col3:
                if st.button(f"Remove", key=f"remove_goal_{i}"):
                    st.session_state.savings_goals.pop(i)
                    st.rerun()
        
        st.divider()

def csv_expense_uploader():
    """CSV expense upload and analysis"""
    st.header("📁 Upload Expense Data")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            # Display sample data
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Column mapping
            st.subheader("🔗 Map Columns")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                amount_col = st.selectbox("Amount Column", df.columns)
            with col2:
                category_col = st.selectbox("Category Column", df.columns)
            with col3:
                date_col = st.selectbox("Date Column", df.columns)
            
            if st.button("Analyze Uploaded Data"):
                # Process the data
                df_clean = df[[amount_col, category_col, date_col]].copy()
                df_clean.columns = ['Amount', 'Category', 'Date']
                df_clean['Amount'] = pd.to_numeric(df_clean['Amount'], errors='coerce')
                df_clean = df_clean.dropna()
                
                # Store in session state
                st.session_state.expense_history = df_clean.to_dict('records')
                
                # Display analysis
                st.subheader("📊 Expense Analysis")
                
                total_expenses = df_clean['Amount'].sum()
                avg_expense = df_clean['Amount'].mean()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Expenses", f"₹{total_expenses:,.0f}")
                with col2:
                    st.metric("Average Expense", f"₹{avg_expense:,.0f}")
                with col3:
                    st.metric("Number of Transactions", len(df_clean))
                
                # Category breakdown
                category_summary = df_clean.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                
                fig_category = px.bar(
                    x=category_summary.index,
                    y=category_summary.values,
                    title="Expenses by Category",
                    color=category_summary.values,
                    color_continuous_scale="Viridis"
                )
                fig_category.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_category, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def what_if_simulator():
    """What-if scenario simulation"""
    st.header("🔮 What-If Scenarios")
    
    if not st.session_state.user_profile:
        st.warning("Please set up your profile first!")
        return
    
    current_income = st.session_state.user_profile.get('income', 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Income Change Simulation")
        income_change = st.slider("Income Change (%)", -50, 100, 0)
        new_income = current_income * (1 + income_change/100)
        
        st.metric("New Monthly Income", f"₹{new_income:,.0f}", f"{income_change:+.0f}%")
        
        if st.session_state.budget_data:
            current_expenses = st.session_state.budget_data.get('total_expenses', 0)
            new_savings = new_income - current_expenses
            savings_change = new_savings - st.session_state.budget_data.get('savings', 0)
            
            st.metric("New Monthly Savings", f"₹{new_savings:,.0f}", f"₹{savings_change:+,.0f}")
    
    with col2:
        st.subheader("💸 Expense Reduction Simulation")
        expense_reduction = st.slider("Expense Reduction (%)", 0, 50, 0)
        
        if st.session_state.budget_data:
            current_expenses = st.session_state.budget_data.get('total_expenses', 0)
            new_expenses = current_expenses * (1 - expense_reduction/100)
            expense_savings = current_expenses - new_expenses
            
            st.metric("New Monthly Expenses", f"₹{new_expenses:,.0f}", f"-₹{expense_savings:,.0f}")
            
            new_total_savings = current_income - new_expenses
            additional_savings = new_total_savings - st.session_state.budget_data.get('savings', 0)
            
            st.metric("Additional Savings", f"₹{additional_savings:,.0f}")

def spending_alerts():
    """Generate spending alerts and anomaly detection"""
    if not st.session_state.budget_data and not st.session_state.monthly_analysis:
        st.info("💡 Set up your budget or monthly analysis first to get spending alerts!")
        return
    
    st.header("🚨 Spending Alerts")
    
    alerts = []
    
    # Budget-based alerts
    if st.session_state.budget_data:
        data = st.session_state.budget_data
        income = data.get('income', 0)
        
        for category, amount in data.get('expenses', {}).items():
            percentage = (amount / income * 100) if income > 0 else 0
            
            if category == 'Rent/Housing' and percentage > 30:
                alerts.append(f"🏠 **Housing Alert**: {percentage:.1f}% of income (recommended: <30%)")
            elif category == 'Food & Groceries' and percentage > 15:
                alerts.append(f"🍽️ **Food Alert**: {percentage:.1f}% of income (recommended: <15%)")
            elif category == 'Entertainment' and percentage > 10:
                alerts.append(f"🎬 **Entertainment Alert**: {percentage:.1f}% of income (recommended: <10%)")
    
    # Monthly analysis alerts
    if st.session_state.monthly_analysis:
        data = st.session_state.monthly_analysis
        expenses = data.get('expenses', {})
        
        if expenses:
            total = sum(expenses.values())
            max_expense = max(expenses.values())
            max_category = max(expenses, key=expenses.get)
            
            if max_expense / total > 0.5:
                alerts.append(f"⚠️ **Concentration Alert**: {max_category} represents {(max_expense/total*100):.1f}% of total expenses")
    
    # Display alerts
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("✅ No spending alerts - your budget looks healthy!")

def investment_calculator():
    """Investment calculator with risk-based recommendations"""
    st.header("📈 Investment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Investment Details")
        monthly_investment = st.number_input("Monthly Investment (₹)", min_value=0, value=5000, step=500)
        investment_period = st.number_input("Investment Period (Years)", min_value=1, value=10, step=1)
        
        # Risk-based returns
        risk_tolerance = st.session_state.risk_tolerance
        if risk_tolerance == 'conservative':
            expected_return = 7
            st.info("Conservative: 7% expected annual return")
        elif risk_tolerance == 'moderate':
            expected_return = 10
            st.info("Moderate: 10% expected annual return")
        else:
            expected_return = 13
            st.info("Aggressive: 13% expected annual return")
    
    with col2:
        st.subheader("📊 Investment Projections")
        
        # Calculate compound interest
        total_invested = monthly_investment * 12 * investment_period
        monthly_rate = expected_return / 100 / 12
        total_months = investment_period * 12
        
        # SIP future value formula
        if monthly_rate > 0:
            future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
        else:
            future_value = total_invested
        
        returns = future_value - total_invested
        
        st.metric("Total Invested", f"₹{total_invested:,.0f}")
        st.metric("Expected Returns", f"₹{returns:,.0f}")
        st.metric("Final Amount", f"₹{future_value:,.0f}")
        
        # Investment allocation based on risk tolerance
        st.subheader("🎯 Recommended Allocation")
        if risk_tolerance == 'conservative':
            st.markdown("""
            - **60%** Debt Funds/FDs
            - **30%** Large Cap Equity
            - **10%** Gold ETF
            """)
        elif risk_tolerance == 'moderate':
            st.markdown("""
            - **50%** Equity Funds
            - **30%** Debt Funds
            - **20%** International/Gold
            """)
        else:
            st.markdown("""
            - **70%** Equity Funds
            - **20%** Mid/Small Cap
            - **10%** Debt Funds
            """)

def display_monthly_analysis():
    """Display monthly analysis with visualizations"""
    if not st.session_state.monthly_analysis:
        st.info("💡 Use the Monthly Analysis section in the sidebar to track your custom expenses!")
        return
    
    data = st.session_state.monthly_analysis
    
    st.header(f"📅 Monthly Analysis - {data['month']}")
    st.caption(f"Last updated: {data['timestamp']}")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Expenses", f"₹{data['total']:,}")
    
    with col2:
        avg_per_category = data['total'] / len(data['expenses']) if data['expenses'] else 0
        st.metric("Avg per Category", f"₹{avg_per_category:,.0f}")
    
    with col3:
        highest_expense = max(data['expenses'].values()) if data['expenses'] else 0
        highest_category = max(data['expenses'], key=data['expenses'].get) if data['expenses'] else "None"
        st.metric("Highest Expense", f"₹{highest_expense:,}", f"{highest_category}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        if data['expenses']:
            fig_pie = px.pie(
                values=list(data['expenses'].values()),
                names=list(data['expenses'].keys()),
                title=f"Expense Distribution - {data['month']}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        if data['expenses']:
            categories = list(data['expenses'].keys())
            amounts = list(data['expenses'].values())
            
            fig_bar = px.bar(
                x=categories,
                y=amounts,
                title=f"Expense Breakdown - {data['month']}",
                color=amounts,
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Expense breakdown table
    st.subheader("💰 Detailed Breakdown")
    if data['expenses']:
        expense_df = pd.DataFrame([
            {"Category": cat, "Amount": f"₹{amt:,}", "Percentage": f"{(amt/data['total']*100):.1f}%"}
            for cat, amt in sorted(data['expenses'].items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(expense_df, use_container_width=True, hide_index=True)
    
    # Insights
    generate_monthly_insights(data)

def generate_monthly_insights(data):
    """Generate insights for monthly analysis"""
    st.subheader("💡 Monthly Insights")
    
    if not data['expenses']:
        return
    
    total = data['total']
    expenses = data['expenses']
    
    # Find top spending categories
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_expenses[0] if sorted_expenses else None
    
    insights = []
    
    if top_category:
        percentage = (top_category[1] / total * 100)
        insights.append(f"🔝 **{top_category[0]}** is your highest expense at ₹{top_category[1]:,} ({percentage:.1f}% of total)")
    
    # Check for balanced spending
    if len(expenses) > 1:
        amounts = list(expenses.values())
        avg_amount = sum(amounts) / len(amounts)
        high_variance = any(amt > avg_amount * 2 for amt in amounts)
        
        if high_variance:
            insights.append("⚖️ **Unbalanced spending** detected - some categories are significantly higher than others")
        else:
            insights.append("✅ **Balanced spending** across categories")
    
    # Spending pattern analysis
    if total > 0:
        if len(expenses) <= 3:
            insights.append("📊 **Focused spending** - You track expenses in few categories")
        elif len(expenses) > 6:
            insights.append("📈 **Diverse spending** - You have expenses across many categories")
    
    # Display insights
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Recommendations
    st.subheader("🎯 Recommendations")
    recommendations = []
    
    if top_category and (top_category[1] / total) > 0.4:
        recommendations.append(f"Consider reducing spending in **{top_category[0]}** as it takes up a large portion of your budget")
    
    if len(expenses) > 8:
        recommendations.append("Try consolidating similar expense categories for better tracking")
    
    recommendations.append("Set monthly limits for each category to stay within budget")
    recommendations.append("Review and update your categories monthly to reflect changing spending patterns")
    
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
    monthly_analysis_section()
    savings_goal_tracker()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat Assistant", "📊 Budget Analysis", "📅 Monthly Analysis", "🎯 Savings Goals", "🔮 Tools & Analysis"])
    
    with tab1:
        st.header("💬 Chat with Your Financial Assistant")
        
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
    
    with tab2:
        # Display budget analysis if available
        if st.session_state.budget_data:
            display_budget_analysis()
        else:
            st.info("💡 Use the Budget Analyzer in the sidebar to get started with budget analysis!")
    
    with tab3:
        display_monthly_analysis()
    
    with tab4:
        display_savings_goals()
    
    with tab5:
        # Tools and Analysis section
        tool_option = st.selectbox("Select Tool", 
            ["Spending Alerts", "What-If Scenarios", "CSV Upload", "Investment Calculator"])
        
        if tool_option == "Spending Alerts":
            spending_alerts()
        elif tool_option == "What-If Scenarios":
            what_if_simulator()
        elif tool_option == "CSV Upload":
            csv_expense_uploader()
        elif tool_option == "Investment Calculator":
            investment_calculator()

if __name__ == "__main__":
    main()
