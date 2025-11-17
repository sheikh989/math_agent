# Task 5 (Bonus): Auto-save outputs and detect invalid/meaningless questions
import json
import os
from typing import Dict, List, Tuple
import re
from datetime import datetime

class QuestionValidator:
    
    def __init__(self):
        self.min_question_length = 20
        self.min_numbers_required = 1
        self.required_elements = ['?', 'find', 'calculate', 'what', 'how']
    
    def is_valid_question(self, question_text: str) -> Tuple[bool, str]:
        text = question_text.lower().strip()
        
        if len(text) < self.min_question_length:
            return False, "Question too short"
        
        numbers = re.findall(r'\d+', text)
        if len(numbers) < self.min_numbers_required:
            return False, "No numerical data found"
        
        has_question_indicator = any(elem in text for elem in self.required_elements)
        if not has_question_indicator:
            return False, "No question indicator found"
        
        common_words = ['the', 'a', 'an', 'is', 'of', 'to', 'in', 'and', 'or']
        has_common_words = any(word in text.split() for word in common_words)
        if not has_common_words:
            return False, "Appears to be gibberish"
        
        alpha_ratio = sum(c.isalpha() for c in text) / len(text)
        if alpha_ratio < 0.5:
            return False, "Too many special characters"
        
        return True, "Valid"
    
    def validate_solution(self, solution_steps: List[str]) -> Tuple[bool, str]:
        if not solution_steps:
            return False, "No solution steps provided"
        
        if len(solution_steps) < 2:
            return False, "Solution too brief"
        
        math_indicators = ['=', '+', '-', '×', '÷', '%', '/', '*']
        has_math = any(
            any(indicator in step for indicator in math_indicators)
            for step in solution_steps
        )
        
        if not has_math:
            return False, "No mathematical operations in solution"
        
        return True, "Valid"
    
    def validate_answer(self, answer: str) -> Tuple[bool, str]:
        if not answer or answer.lower() in ['n/a', 'not found', 'none', '']:
            return False, "No answer provided"
        
        if not re.search(r'\d+', answer):
            return False, "Answer doesn't contain numerical value"
        
        return True, "Valid"

class AutoSaveManager:
    
    def __init__(self, output_base_dir="outputs"):
        self.output_base_dir = output_base_dir
        self.validator = QuestionValidator()
        self.create_directory_structure()
    
    def create_directory_structure(self):
        dirs = [
            os.path.join(self.output_base_dir, "valid"),
            os.path.join(self.output_base_dir, "invalid"),
            os.path.join(self.output_base_dir, "json"),
            os.path.join(self.output_base_dir, "visuals"),
            os.path.join(self.output_base_dir, "logs")
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def validate_and_categorize(self, question_data: Dict) -> Dict:
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        q_valid, q_msg = self.validator.is_valid_question(
            question_data.get('raw_text', '')
        )
        if not q_valid:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Question: {q_msg}")
        
        sol_valid, sol_msg = self.validator.validate_solution(
            question_data.get('solution_steps', [])
        )
        if not sol_valid:
            validation_result["warnings"].append(f"Solution: {sol_msg}")
        
        ans_valid, ans_msg = self.validator.validate_answer(
            question_data.get('answer', '')
        )
        if not ans_valid:
            validation_result["warnings"].append(f"Answer: {ans_msg}")
        
        question_data['validation'] = validation_result
        return question_data
    
    def save_question(self, question_data: Dict, q_number: int):
        validated_data = self.validate_and_categorize(question_data)
        
        is_valid = validated_data['validation']['is_valid']
        category = "valid" if is_valid else "invalid"
        
        json_path = os.path.join(
            self.output_base_dir, 
            "json", 
            category,
            f"question_{q_number}.json"
        )
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(validated_data, f, indent=2, ensure_ascii=False)
        
        return is_valid, json_path
    
    def generate_validation_report(self, all_questions: List[Dict]) -> str:
        total = len(all_questions)
        valid_count = sum(1 for q in all_questions if q.get('validation', {}).get('is_valid', False))
        invalid_count = total - valid_count
        
        report = f"""
=== Validation Report ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Questions: {total}
Valid Questions: {valid_count} ({valid_count/total*100:.1f}%)
Invalid Questions: {invalid_count} ({invalid_count/total*100:.1f}%)

Invalid Questions Details:
"""
        
        for i, q in enumerate(all_questions, 1):
            if not q.get('validation', {}).get('is_valid', True):
                errors = q['validation'].get('errors', [])
                report += f"\nQ{i}: {', '.join(errors)}"
        
        return report
    
    def save_report(self, report: str):
        report_path = os.path.join(
            self.output_base_dir,
            "logs",
            f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Validation report saved: {report_path}")
        return report_path

if __name__ == "__main__":
    manager = AutoSaveManager()
    
    sample_questions = [
        {
            "raw_text": "A trader marks an article 40% above cost price and gives 10% discount. Find CP if profit is ₹36.",
            "solution_steps": ["Let CP = x", "MP = 1.4x", "SP = 1.26x", "Profit = 0.26x = 36", "x = 138.46"],
            "answer": "₹138.46"
        },
        {
            "raw_text": "Invalid",
            "solution_steps": [],
            "answer": ""
        }
    ]
    
    validated = []
    for i, q in enumerate(sample_questions, 1):
        is_valid, path = manager.save_question(q, i)
        validated.append(q)
        print(f"Q{i}: {'Valid' if is_valid else 'Invalid'} - Saved to {path}")
    
    report = manager.generate_validation_report(validated)
    print(report)
    manager.save_report(report)
