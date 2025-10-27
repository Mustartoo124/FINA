import datetime 

def generate_budget_plan(summary: dict, goals: dict = None) -> dict:
    """
    Generate a personalized monthly budget plan based on financial summary and goals.

    Args:
        summary (dict): User's financial summary with fields like 'total_income', 'total_expenses', 'debts', etc.
        goals (dict, optional): Financial goals (e.g., saving target).

    Returns:
        dict: Recommended budget breakdown.
    """
    income = summary.get("total_income", 0)
    expenses = summary.get("total_expenses", 0)
    available = max(income - expenses, 0)

    # Basic 50/30/20 rule allocation
    essentials = income * 0.5
    wants = income * 0.3
    savings = income * 0.2

    # Adjust based on user goals
    if goals and "saving_target" in goals:
        target = goals["saving_target"]
        if target > savings:
            diff = target - savings
            wants -= diff / 2
            essentials -= diff / 2
            savings = target

    plan = {
        "total_income": income,
        "suggested_allocation": {
            "essentials": round(essentials, 2),
            "wants": round(wants, 2),
            "savings": round(savings, 2)
        },
        "expected_remaining": round(available, 2),
        "notes": "Plan based on 50/30/20 rule, adjusted for goals if provided."
    }
    return plan

def set_financial_goal(goal_type: str, target_amount: float, period: str) -> dict:
    """
    Set a financial goal (saving, investment, or debt reduction).

    Args:
        goal_type (str): Type of goal, e.g., 'saving', 'investment', 'debt_reduction'.
        target_amount (float): The target amount for the goal.
        period (str): The time period for achieving the goal (e.g., '1 month', '6 months').

    Returns:
        dict: Confirmation and goal summary.
    """
    goal = {
        "goal_type": goal_type,
        "target_amount": target_amount,
        "period": period,
        "start_date": datetime.date.today().isoformat(),
        "status": "active"
    }
    return {
        "message": f"Goal set successfully: {goal_type} of {target_amount} within {period}.",
        "goal_details": goal
    }

def evaluate_plan_progress(summary: dict, goal_data: dict) -> dict:
    """
    Evaluate how well the user is progressing toward their financial goals.

    Args:
        summary (dict): Financial summary containing current income, savings, or expenses.
        goal_data (dict): The user's defined financial goal.

    Returns:
        dict: Progress report with completion percentage and advice.
    """
    goal_type = goal_data.get("goal_type", "saving")
    target = goal_data.get("target_amount", 0)
    current_savings = summary.get("total_savings", 0)

    progress = 0
    if target > 0:
        progress = min((current_savings / target) * 100, 100)

    evaluation = {
        "goal_type": goal_type,
        "target_amount": target,
        "current_savings": current_savings,
        "progress_percent": round(progress, 2),
        "status": "on track" if progress >= 70 else "behind schedule" if progress < 40 else "moderate",
        "advice": "Increase savings rate to meet target faster." if progress < 50 else "Great progress, keep it up!"
    }
    return evaluation