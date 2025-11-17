# Task 3: AI/Logic Integration - Auto-solve questions step by step

import re
from typing import List, Dict, Tuple
import json

class MathSolver:
    
    def solve_profit_loss_problem(self, question_data: Dict) -> Dict:
        text = question_data.get('raw_text', '')
        
        profit_match = re.search(r'profit of (\d+(?:\.\d+)?)%', text, re.I)
        discount_match = re.search(r'discount.*?(\d+(?:\.\d+)?)%', text, re.I)
        markup_match = re.search(r'marks?.*?(\d+(?:\.\d+)?)%\s*above', text, re.I)
        
        solution = {
            "steps": [],
            "formula_used": [],
            "answer": None
        }
        
        if markup_match and discount_match:
            markup = float(markup_match.group(1))
            discount = float(discount_match.group(1))
            
            solution["steps"].append(f"Let Cost Price = ₹x")
            solution["steps"].append(f"Marked Price = x + {markup}% of x = {1 + markup/100}x")
            solution["steps"].append(f"After {discount}% discount:")
            solution["steps"].append(f"Selling Price = {1 + markup/100}x × {1 - discount/100} = {(1 + markup/100) * (1 - discount/100)}x")
            
            profit_amt_match = re.search(r'profit of ₹(\d+(?:\.\d+)?)', text)
            if profit_amt_match:
                profit_amt = float(profit_amt_match.group(1))
                sp_multiplier = (1 + markup/100) * (1 - discount/100)
                profit_multiplier = sp_multiplier - 1
                
                solution["steps"].append(f"Profit = SP - CP = {sp_multiplier}x - x = {profit_multiplier}x")
                solution["steps"].append(f"Given: {profit_multiplier}x = ₹{profit_amt}")
                
                cp = profit_amt / profit_multiplier
                solution["steps"].append(f"x = ₹{profit_amt}/{profit_multiplier} = ₹{cp:.2f}")
                solution["answer"] = f"₹{cp:.2f}"
            
            solution["formula_used"].append("SP = MP × (1 - Discount%/100)")
            solution["formula_used"].append("Profit = SP - CP")
        
        elif text.count('profit') >= 2 or 'reduces' in text.lower():
            solution["steps"].append("Scenario 1: Original transaction")
            solution["steps"].append("Let original CP = ₹x")
            
            if profit_match:
                profit1 = float(profit_match.group(1))
                solution["steps"].append(f"Original SP = x + {profit1}% of x = {1 + profit1/100}x")
            
            solution["steps"].append("\nScenario 2: Modified transaction")
            
            cp_reduce = re.search(r'reduces.*?cost price by (\d+(?:\.\d+)?)%', text, re.I)
            if cp_reduce:
                reduce_pct = float(cp_reduce.group(1))
                solution["steps"].append(f"New CP = x - {reduce_pct}% of x = {1 - reduce_pct/100}x")
            
            sp_increase = re.search(r'increases.*?selling price by ₹(\d+(?:\.\d+)?)', text, re.I)
            if sp_increase and profit_match:
                increase_amt = float(sp_increase.group(1))
                profit1 = float(profit_match.group(1))
                solution["steps"].append(f"New SP = {1 + profit1/100}x + ₹{increase_amt}")
            
            new_profit = re.search(r'profit percentage becomes (\d+(?:\.\d+)?)%', text, re.I)
            if new_profit and cp_reduce and sp_increase:
                new_profit_pct = float(new_profit.group(1))
                reduce_pct = float(cp_reduce.group(1))
                increase_amt = float(sp_increase.group(1))
                profit1 = float(profit_match.group(1))
                
                solution["steps"].append(f"\nNew Profit% = {new_profit_pct}%")
                solution["steps"].append(f"New Profit = New SP - New CP")
                solution["steps"].append(f"({1 + profit1/100}x + {increase_amt}) - {1 - reduce_pct/100}x = {new_profit_pct/100} × {1 - reduce_pct/100}x")
                
                left_coef = (1 + profit1/100) - (1 - reduce_pct/100)
                right_coef = (new_profit_pct/100) * (1 - reduce_pct/100)
                
                if abs(left_coef - right_coef) > 0.001:
                    x = increase_amt / (right_coef - left_coef)
                    solution["steps"].append(f"Solving: x = ₹{x:.2f}")
                    solution["answer"] = f"₹{x:.2f}"
            
            solution["formula_used"].append("Profit% = (Profit/CP) × 100")
        
        return solution
    
    def solve_question(self, question_data: Dict) -> Dict:
        q_type = question_data.get('question_type', 'general')
        
        if q_type == 'profit_loss':
            return self.solve_profit_loss_problem(question_data)
        
        return {
            "steps": ["Solution method not implemented for this question type"],
            "formula_used": [],
            "answer": "N/A"
        }

if __name__ == "__main__":
    solver = MathSolver()
    
    q_data = {
        "raw_text": """A trader marks an article 40% above its cost price.
He allows a 10% discount on the marked price and still earns a profit of ₹36.
Find the cost price of the article.""",
        "question_type": "profit_loss"
    }
    
    solution = solver.solve_question(q_data)
    print("Solution Steps:")
    for i, step in enumerate(solution["steps"], 1):
        print(f"{i}. {step}")
    print(f"\nAnswer: {solution['answer']}")
