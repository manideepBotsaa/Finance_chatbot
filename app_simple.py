import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for vibrant and attractive UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main > div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 2rem;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chat-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: inherit;
        filter: blur(20px);
        z-index: -1;
    }
    
    .chat-message:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 6px solid #4f46e5;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-left: 6px solid #ec4899;
    }
    
    .profile-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        border: 2px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .profile-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .disclaimer {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border: 3px solid #f59e0b;
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin: 2rem 0;
        font-size: 1rem;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        position: relative;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 2rem;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stSelectbox > div > div {
        border-radius: 1.5rem;
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 1.5rem;
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
        font-weight: 600;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 1.5rem;
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
    }
    
    .stMetric > div {
        color: white !important;
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .stExpander {
        border: 3px solid #667eea;
        border-radius: 1.5rem;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 0 2rem 2rem 0;
    }
    
    .stChatInput > div {
        border-radius: 2rem;
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
    }
    
    .insight-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(132, 250, 176, 0.3);
        border-left: 6px solid #10b981;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1.5rem;
        border-radius: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 234, 167, 0.3);
        border-left: 6px solid #f59e0b;
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

class FinancialAssistant:
    """Simple rule-based financial assistant"""
    
    def generate_response(self, user_input, user_profile, context=""):
        """Generate personalized financial advice using rule-based logic"""
        demographic = user_profile.get('demographic', 'general')
        income = user_profile.get('income', 0)
        age = user_profile.get('age', 25)
        
        user_input_lower = user_input.lower()
        
        # Savings-related queries
        if any(word in user_input_lower for word in ['save', 'saving', 'savings', 'laptop', 'phone']):
            if demographic == 'student':
                return f"""Great question! As a student, here are some practical saving tips:

💡 **Start Small**: Try saving ₹500-1000 monthly by:
- Cooking at home instead of ordering food (save ₹2000+/month)
- Using student discounts everywhere
- Sharing subscriptions with friends
- Walking/cycling instead of taking auto/cab

📱 **For specific goals**:
- Laptop (₹40,000): Save ₹3,500/month for 12 months
- Phone (₹15,000): Save ₹2,500/month for 6 months
- Emergency fund: Start with ₹500/month

🎯 **Pro tip**: Use the 50-30-20 rule adapted for students:
- 50% for essentials (₹{income*0.5:,.0f})
- 30% for fun/wants (₹{income*0.3:,.0f})
- 20% for savings (₹{income*0.2:,.0f})

Would you like me to create a personalized budget plan for you?"""
            else:
                return f"""Based on your professional profile, here's a structured savings approach:

💼 **The 50-30-20 Rule**:
- 50% for needs (₹{income*0.5:,.0f})
- 30% for wants (₹{income*0.3:,.0f})  
- 20% for savings (₹{income*0.2:,.0f})

🎯 **Investment Options**:
- Emergency fund: 6 months expenses in high-yield savings
- SIP in index funds: ₹{min(income*0.1, 15000):,.0f}/month
- PPF for tax savings: Up to ₹1.5 lakh/year
- ELSS funds: Tax-saving mutual funds

📈 **Advanced strategies**:
- Diversify across large-cap, mid-cap, and international funds
- Consider debt funds for stability
- Use systematic transfer plans (STP) for better timing

Would you like a detailed investment breakdown based on your ₹{income:,} income?"""
        
        # Investment queries
        elif any(word in user_input_lower for word in ['invest', 'investment', 'sip', 'mutual fund', 'portfolio']):
            if demographic == 'student':
                return """As a student, start with these simple investment steps:

🌱 **Begin Small**:
- Start with ₹500-1000/month SIP
- Choose index funds (low cost, diversified)
- Use apps like Groww, Zerodha Coin, or Paytm Money

📚 **Learn First**: 
- Understand risk vs returns
- Start with large-cap funds (safer for beginners)
- Avoid individual stock picking initially
- Read about compound interest - it's magical! ✨

🎯 **Sample portfolio for students**:
- 70% Large-cap index funds
- 20% Mid-cap funds
- 10% International funds

Remember: Time in market > timing the market!"""
            else:
                return f"""Here's a professional investment strategy for your ₹{income:,} monthly income:

📊 **Asset Allocation by Age ({age} years)**:
- Equity: {100-age}% (₹{income*(100-age)/100*0.2:,.0f}/month)
- Debt: {age}% (₹{income*age/100*0.2:,.0f}/month)

🏛️ **Tax-Saving Options**:
- ELSS funds: Up to ₹1.5L under Section 80C
- PPF: 15-year lock-in, tax-free returns
- NPS: Additional ₹50K deduction under 80CCD(1B)
- ULIP: Insurance + investment (consider carefully)

💰 **Monthly Investment Plan**:
- Large-cap funds: ₹{income*0.08:,.0f}
- Mid-cap funds: ₹{income*0.05:,.0f}
- International funds: ₹{income*0.03:,.0f}
- Debt funds: ₹{income*0.04:,.0f}

Want me to create a detailed portfolio allocation?"""
        
        # Budget queries
        elif any(word in user_input_lower for word in ['budget', 'expense', 'spending', 'money']):
            return """I'd love to help you create a comprehensive budget! 📊

📝 **Let's gather your financial info**:
- Monthly income (already have: ₹{:,})
- Fixed expenses (rent, utilities, EMIs)
- Variable expenses (food, transport, entertainment)
- Savings goals

You can either:
1. Tell me your numbers in this chat
2. Use the "Budget Analyzer" form in the sidebar

Once I have your data, I'll create:
- 📊 Visual budget breakdown (pie charts, bar graphs)
- 📈 Spending analysis with recommendations
- 💡 Personalized tips to optimize your finances
- 🎯 Goal-based savings plan

Try the budget form now and I'll give you instant insights!"""
        
        # Emergency fund queries
        elif any(word in user_input_lower for word in ['emergency', 'fund', 'crisis']):
            months_expense = income * 0.7  # Assuming 70% of income goes to expenses
            emergency_target = months_expense * 6
            
            if demographic == 'student':
                return f"""Emergency funds are super important, even for students! 🚨

🎯 **Your target**: ₹{emergency_target:,.0f} (6 months of expenses)
💰 **Monthly saving needed**: ₹{emergency_target/12:,.0f} to build it in 1 year

📍 **Where to keep it**:
- High-yield savings account (4-6% interest)
- Liquid funds (slightly better returns)
- Fixed deposits (if you won't need it soon)

🚀 **Quick start**: Begin with ₹1000/month and increase gradually!"""
            else:
                return f"""Emergency fund is crucial for financial stability! 🛡️

🎯 **Your target**: ₹{emergency_target:,.0f} (6 months of expenses)
💰 **Monthly allocation**: ₹{emergency_target/12:,.0f} to build in 1 year

📍 **Best places to keep emergency funds**:
- High-yield savings accounts (SBI, HDFC, ICICI)
- Liquid mutual funds (instant redemption)
- Ultra-short duration funds
- Sweep-in fixed deposits

⚡ **Pro tip**: Keep 3 months in savings account, 3 months in liquid funds for better returns!"""
        
        # Tax queries
        elif any(word in user_input_lower for word in ['tax', 'saving', '80c', 'deduction']):
            if demographic == 'professional':
                return f"""Tax optimization is key for professionals! 💼

🏛️ **Section 80C (₹1.5L limit)**:
- PPF: ₹12,500/month (15-year lock, tax-free returns)
- ELSS: ₹12,500/month (3-year lock, market returns)
- Life insurance: Term + health insurance premiums
- Home loan principal repayment

💰 **Additional deductions**:
- 80D: Health insurance (₹25K-₹50K)
- 80CCD(1B): NPS (additional ₹50K)
- 80G: Donations to eligible charities

📊 **Your potential savings** (assuming 30% tax bracket):
- Section 80C: Save ₹45,000 in taxes
- Total deductions: Up to ₹2L+ possible

Want me to calculate your exact tax savings?"""
            else:
                return """Tax planning for students is simpler but still important! 🎓

📚 **Key points**:
- Income up to ₹2.5L is tax-free
- Keep receipts for tuition fees (80C deduction)
- Health insurance premiums count (80D)

💡 **Future planning**:
- Start learning about tax-saving investments
- Consider opening PPF account early
- Understand basics of income tax

You're in a great position to learn and plan ahead! 🚀"""
        
        # General greeting or unclear query
        else:
            greeting = "Hello! I'm your personal finance assistant. 👋"
            
            if demographic == 'student':
                greeting += f"""

As a student with ₹{income:,} monthly income, I can help you with:
- 💰 Smart saving strategies for students
- 📱 Saving for gadgets (laptops, phones)
- 📊 Simple budgeting techniques
- 🎯 Building good financial habits early

**Quick tips for you**:
- Start saving even ₹500/month - it builds discipline!
- Use student discounts everywhere
- Learn about SIPs and compound interest
- Build an emergency fund gradually"""
            else:
                greeting += f"""

As a professional with ₹{income:,} monthly income, I can help you with:
- 📈 Investment portfolio optimization
- 🏛️ Tax-saving strategies
- 🏠 Home buying and loan planning
- 💼 Retirement and wealth building

**Key focus areas**:
- Maximize your 80C deductions (₹1.5L)
- Build diversified investment portfolio
- Plan for major life goals
- Optimize your tax efficiency"""
            
            greeting += """

**What would you like to explore?**
- "How do I save for [specific goal]?"
- "What investments should I consider?"
- "Help me create a budget"
- "How can I save on taxes?"

Feel free to use the sidebar to set up your profile and analyze your budget! 📊"""
            
            return greeting

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
            if income == 0:
                st.error("Please set up your profile first!")
                return
                
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
        color = "normal"
        if data['savings'] < 0:
            color = "inverse"
        st.metric("Savings", f"₹{data['savings']:,}", f"{savings_rate:.1f}%", delta_color=color)
    
    with col4:
        expense_ratio = (data['total_expenses'] / data['income'] * 100) if data['income'] > 0 else 0
        st.metric("Expense Ratio", f"{expense_ratio:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced pie chart of expenses
        fig_pie = px.pie(
            values=list(data['expenses'].values()),
            names=list(data['expenses'].keys()),
            title="💸 Expense Breakdown",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#a8edea', '#fed6e3']
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Percentage: %{percent}<extra></extra>',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=3))
        )
        fig_pie.update_layout(
            title_font_size=20,
            title_font_color='#667eea',
            title_font_family='Poppins',
            font=dict(family='Poppins', size=14),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=60, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Enhanced bar chart comparison
        categories = ['💰 Income', '💸 Expenses', '💎 Savings']
        values = [data['income'], data['total_expenses'], data['savings']]
        colors = ['#84fab0', '#ff7675', '#74b9ff']
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=categories, 
                y=values, 
                marker_color=colors,
                marker_line_color='white',
                marker_line_width=2,
                text=[f"₹{v:,.0f}" for v in values],
                textposition='auto',
                textfont=dict(size=14, color='white', family='Poppins')
            )
        ])
        fig_bar.update_layout(
            title="💰 Income vs Expenses vs Savings",
            title_font_size=20,
            title_font_color='#667eea',
            title_font_family='Poppins',
            yaxis_title="Amount (₹)",
            font=dict(family='Poppins', size=14),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='rgba(102, 126, 234, 0.2)'),
            margin=dict(t=60, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Generate insights
    generate_budget_insights(data)

def generate_budget_insights(data):
    """Generate spending insights and recommendations"""
    st.header("💡 Spending Insights & Recommendations")
    
    income = data['income']
    expenses = data['expenses']
    savings = data['savings']
    savings_rate = (savings / income * 100) if income > 0 else 0
    
    # Savings rate analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Savings Analysis")
        if savings_rate < 0:
            st.markdown("""
            <div class="error-card">
                <h4>⚠️ Critical: You're Overspending!</h4>
                <p>Your expenses exceed your income by ₹{:,}</p>
                <strong>Immediate Actions:</strong>
                <ul>
                    <li>🔍 Review and cut non-essential expenses</li>
                    <li>💼 Look for additional income sources</li>
                    <li>⚖️ Consider lifestyle adjustments</li>
                </ul>
            </div>
            """.format(abs(savings)), unsafe_allow_html=True)
        elif savings_rate < 10:
            st.markdown("""
            <div class="warning-card">
                <h4>⚠️ Low Savings Rate</h4>
                <p>Current: {:.1f}% | Target: 20%+</p>
                <strong>Recommendations:</strong>
                <ul>
                    <li>📊 Track expenses more carefully</li>
                    <li>✂️ Identify areas to cut spending</li>
                    <li>🤖 Automate savings to pay yourself first</li>
                </ul>
            </div>
            """.format(savings_rate), unsafe_allow_html=True)
        elif savings_rate < 20:
            st.markdown("""
            <div class="insight-card">
                <h4>📈 Good Progress!</h4>
                <p>Savings Rate: {:.1f}% - Room for improvement</p>
                <strong>Next Steps:</strong>
                <ul>
                    <li>🎯 Aim for 20-30% savings rate</li>
                    <li>📈 Consider investing surplus funds</li>
                    <li>🔧 Review and optimize major expenses</li>
                </ul>
            </div>
            """.format(savings_rate), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <h4>✅ Excellent Savings Rate!</h4>
                <p>Outstanding: {:.1f}% savings rate</p>
                <strong>Advanced Strategies:</strong>
                <ul>
                    <li>📊 Diversified investment portfolio</li>
                    <li>🏛️ Tax-saving optimization</li>
                    <li>🎯 Long-term wealth building goals</li>
                </ul>
            </div>
            """.format(savings_rate), unsafe_allow_html=True)
    
    with col2:
        st.subheader("🔍 Category Analysis")
        
        # Category-wise analysis
        issues_found = False
        for category, amount in expenses.items():
            percentage = (amount / income * 100) if income > 0 else 0
            
            # Define thresholds
            thresholds = {
                'Rent/Housing': 30,
                'Food & Groceries': 15,
                'Transport': 15,
                'Entertainment': 10,
                'Shopping': 15,
                'Utilities': 10,
                'Others': 10
            }
            
            threshold = thresholds.get(category, 10)
            
            if percentage > threshold:
                issues_found = True
                st.markdown(f"""
                <div class="warning-card">
                    <h5>🚨 {category}: {percentage:.1f}%</h5>
                    <p>Recommended: <{threshold}% | Overspend: {percentage-threshold:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Specific recommendations
                if 'Housing' in category:
                    st.markdown("💡 **Consider**: roommates, cheaper area, or house-sharing")
                elif 'Food' in category:
                    st.markdown("💡 **Try**: meal planning, cooking at home, bulk buying")
                elif 'Entertainment' in category:
                    st.markdown("💡 **Look for**: free events, streaming instead of movies, group activities")
                elif 'Shopping' in category:
                    st.markdown("💡 **Practice**: 24-hour rule, compare prices, buy only necessities")
            else:
                st.markdown(f"""
                <div class="insight-card">
                    <h5>✅ {category}: {percentage:.1f}%</h5>
                    <p>Within {threshold}% recommended limit - Great job! 🎉</p>
                </div>
                """, unsafe_allow_html=True)
        
        if not issues_found:
            st.success("🎉 All categories are within recommended limits!")

def main():
    """Main application"""
    # Initialize assistant
    assistant = FinancialAssistant()
    
    # Header with enhanced styling
    st.markdown('''
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="main-header">💰 Personal Finance Assistant</h1>
        <p style="font-size: 1.2rem; color: #667eea; font-weight: 500;">
            Your AI-powered financial companion for smart money decisions ✨
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
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
    
    # Sample profile buttons
    if not st.session_state.user_profile:
        st.info("👆 Set up your profile in the sidebar to get personalized advice!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Load Student Sample"):
                st.session_state.user_profile = {
                    'age': 20,
                    'income': 10000,
                    'demographic': 'student',
                    'goals': 'Save for laptop and emergency fund'
                }
                st.rerun()
        
        with col2:
            if st.button("💼 Load Professional Sample"):
                st.session_state.user_profile = {
                    'age': 28,
                    'income': 100000,
                    'demographic': 'professional',
                    'goals': 'House down payment, retirement planning'
                }
                st.rerun()
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about personal finance..."):
        # Check if profile exists
        if not st.session_state.user_profile:
            st.error("Please set up your profile first using the sidebar or sample buttons above!")
            return
        
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
