"""
Utility functions for the Financial Assistant
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from config import FINANCIAL_GUIDELINES, ERROR_MESSAGES

class BudgetAnalyzer:
    """Class for budget analysis and financial calculations"""
    
    @staticmethod
    def calculate_budget_metrics(income, expenses_dict):
        """Calculate comprehensive budget metrics"""
        try:
            total_expenses = sum(expenses_dict.values())
            savings = income - total_expenses
            savings_rate = (savings / income * 100) if income > 0 else 0
            
            # Calculate expense ratios
            expense_ratios = {}
            for category, amount in expenses_dict.items():
                expense_ratios[category] = (amount / income * 100) if income > 0 else 0
            
            return {
                'total_expenses': total_expenses,
                'savings': savings,
                'savings_rate': savings_rate,
                'expense_ratios': expense_ratios,
                'is_overspending': savings < 0
            }
        except Exception as e:
            raise ValueError(ERROR_MESSAGES['calculation_error'])
    
    @staticmethod
    def analyze_spending_patterns(expense_ratios):
        """Analyze spending patterns and identify issues"""
        guidelines = FINANCIAL_GUIDELINES['expense_ratios']
        issues = []
        recommendations = []
        
        for category, ratio in expense_ratios.items():
            category_key = category.lower().replace('/', '_').replace(' & ', '_').replace(' ', '_')
            
            # Map categories to guidelines
            if 'rent' in category_key or 'housing' in category_key:
                guideline_key = 'housing'
            elif 'food' in category_key or 'groceries' in category_key:
                guideline_key = 'food'
            elif 'transport' in category_key:
                guideline_key = 'transport'
            elif 'entertainment' in category_key:
                guideline_key = 'entertainment'
            elif 'utilities' in category_key:
                guideline_key = 'utilities'
            elif 'shopping' in category_key:
                guideline_key = 'shopping'
            else:
                guideline_key = 'others'
            
            recommended_ratio = guidelines.get(guideline_key, 10)
            
            if ratio > recommended_ratio:
                issues.append({
                    'category': category,
                    'current_ratio': ratio,
                    'recommended_ratio': recommended_ratio,
                    'excess': ratio - recommended_ratio
                })
        
        return issues
    
    @staticmethod
    def generate_savings_recommendations(profile, budget_metrics):
        """Generate personalized savings recommendations"""
        demographic = profile.get('demographic', 'general')
        income = profile.get('income', 0)
        savings_rate = budget_metrics['savings_rate']
        
        recommendations = []
        
        if savings_rate < 10:
            if demographic == 'student':
                recommendations.extend([
                    "🎯 Start with micro-savings: Save ₹50-100 daily",
                    "🍕 Cook meals instead of ordering food - save ₹2000+/month",
                    "📚 Use library/free resources instead of buying books",
                    "🚌 Use public transport or walk when possible"
                ])
            else:
                recommendations.extend([
                    "⚡ Automate savings: Set up automatic transfer to savings account",
                    "🏠 Consider reducing housing costs if possible",
                    "📱 Review and cancel unused subscriptions",
                    "🛒 Create a monthly budget and stick to it"
                ])
        
        elif savings_rate < 20:
            recommendations.extend([
                "📈 Increase savings rate to 20% for better financial security",
                "💰 Consider investing surplus in SIPs or mutual funds",
                "🎯 Set specific savings goals to stay motivated"
            ])
        
        return recommendations

class ResponseGenerator:
    """Class for generating personalized responses"""
    
    @staticmethod
    def format_currency(amount):
        """Format currency in Indian format"""
        if amount >= 10000000:  # 1 crore
            return f"₹{amount/10000000:.1f} crore"
        elif amount >= 100000:  # 1 lakh
            return f"₹{amount/100000:.1f} lakh"
        else:
            return f"₹{amount:,.0f}"
    
    @staticmethod
    def get_demographic_greeting(demographic):
        """Get personalized greeting based on demographic"""
        greetings = {
            'student': "Hey there! 🎓 I'm here to help you manage your finances as a student.",
            'professional': "Hello! 💼 I'm your personal finance assistant, ready to help optimize your financial strategy."
        }
        return greetings.get(demographic, "Hello! I'm here to help with your financial questions.")
    
    @staticmethod
    def generate_budget_summary(income, expenses, savings, demographic):
        """Generate a natural language budget summary"""
        total_expenses = sum(expenses.values())
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        if demographic == 'student':
            if savings_rate >= 20:
                tone = "Amazing job! 🌟"
            elif savings_rate >= 10:
                tone = "Good work! 👍"
            else:
                tone = "Let's work on this together! 💪"
        else:
            if savings_rate >= 30:
                tone = "Excellent financial discipline! 🎯"
            elif savings_rate >= 20:
                tone = "You're on the right track! 📈"
            else:
                tone = "There's room for improvement. 🔧"
        
        summary = f"""{tone}
        
**Your Financial Snapshot:**
- Monthly Income: {ResponseGenerator.format_currency(income)}
- Total Expenses: {ResponseGenerator.format_currency(total_expenses)}
- Monthly Savings: {ResponseGenerator.format_currency(savings)} ({savings_rate:.1f}%)

**Top Expense Categories:**"""
        
        # Sort expenses by amount
        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        for category, amount in sorted_expenses[:3]:
            percentage = (amount / income * 100) if income > 0 else 0
            summary += f"\n- {category}: {ResponseGenerator.format_currency(amount)} ({percentage:.1f}%)"
        
        return summary

def validate_financial_input(value, field_name, min_value=0, max_value=None):
    """Validate financial input values"""
    try:
        value = float(value)
        if value < min_value:
            raise ValueError(f"{field_name} cannot be less than {min_value}")
        if max_value and value > max_value:
            raise ValueError(f"{field_name} cannot be more than {max_value}")
        return value
    except (ValueError, TypeError):
        raise ValueError(f"Please enter a valid number for {field_name}")

def load_sample_data(demographic):
    """Load sample data for testing"""
    from config import SAMPLE_PROFILES
    return SAMPLE_PROFILES.get(demographic, SAMPLE_PROFILES['student'])

def export_budget_data(budget_data, filename=None):
    """Export budget data to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"budget_export_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(budget_data, f, indent=2, default=str)
        return filename
    except Exception as e:
        raise ValueError(f"Error exporting data: {str(e)}")

def calculate_investment_projection(monthly_amount, annual_return_rate, years):
    """Calculate investment projection using compound interest"""
    try:
        monthly_rate = annual_return_rate / 12 / 100
        total_months = years * 12
        
        if monthly_rate == 0:
            future_value = monthly_amount * total_months
        else:
            future_value = monthly_amount * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
        
        total_invested = monthly_amount * total_months
        returns = future_value - total_invested
        
        return {
            'future_value': future_value,
            'total_invested': total_invested,
            'returns': returns,
            'return_percentage': (returns / total_invested * 100) if total_invested > 0 else 0
        }
    except Exception as e:
        raise ValueError("Error calculating investment projection")
