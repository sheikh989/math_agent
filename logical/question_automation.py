# Task 1: Question Automation - Detect question type and extract key data

import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Question:
    raw_text: str
    question_type: str
    topic: str
    key_data: Dict
    solution_steps: List[str]
    answer: str

class QuestionAnalyzer:
    
    QUESTION_PATTERNS = {
        'profit_loss': [
            r'profit|loss|selling price|cost price|marked price',
            r'SP|CP|MP|discount'
        ],
        'percentage': [
            r'percentage|percent|%',
            r'increase|decrease by \d+%'
        ],
        'ratio_proportion': [
            r'ratio|proportion',
            r':\s*\d+'
        ],
        'time_work': [
            r'days|hours|work|complete',
            r'together|alone'
        ],
        'speed_distance': [
            r'speed|distance|time|km|m/s',
            r'train|car|bus'
        ],
        'simple_interest': [
            r'simple interest|SI|principal|rate|time',
            r'interest'
        ],
        'compound_interest': [
            r'compound interest|CI|compounded',
            r'annually|half-yearly'
        ]
    }
    
    def detect_question_type(self, text: str) -> str:
        text_lower = text.lower()
        
        for q_type, patterns in self.QUESTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return q_type
        
        return 'general'
    
    def extract_numbers(self, text: str) -> List[float]:
        pattern = r'₹?\s*(\d+(?:\.\d+)?)\s*%?'
        matches = re.findall(pattern, text)
        return [float(m) for m in matches]
    
    def extract_key_data(self, text: str, q_type: str) -> Dict:
        data = {
            'numbers': self.extract_numbers(text),
            'has_percentage': '%' in text,
            'has_currency': '₹' in text
        }
        
        if q_type == 'profit_loss':
            data['profit_mentioned'] = bool(re.search(r'profit', text, re.I))
            data['loss_mentioned'] = bool(re.search(r'loss', text, re.I))
            data['discount_mentioned'] = bool(re.search(r'discount', text, re.I))
        
        return data
    
    def parse_solution(self, solution_text: str) -> List[str]:
        steps = re.split(r'\n\s*[\d•→]+\.?\s*', solution_text)
        return [step.strip() for step in steps if step.strip()]
    
    def extract_answer(self, text: str) -> str:
        answer_patterns = [
            r'Answer\s*[→:=]\s*(.+?)(?:\n|$)',
            r'(?:CP|SP|MP)\s*=\s*₹?\s*(\d+(?:\.\d+)?)',
            r'x\s*=\s*₹?\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        
        return "Not found"
    
    def analyze_question(self, question_text: str, solution_text: str = "") -> Question:
        q_type = self.detect_question_type(question_text)
        topic = q_type.replace('_', ' ').title()
        key_data = self.extract_key_data(question_text + " " + solution_text, q_type)
        solution_steps = self.parse_solution(solution_text) if solution_text else []
        answer = self.extract_answer(solution_text) if solution_text else ""
        
        return Question(
            raw_text=question_text,
            question_type=q_type,
            topic=topic,
            key_data=key_data,
            solution_steps=solution_steps,
            answer=answer
        )

if __name__ == "__main__":
    analyzer = QuestionAnalyzer()
    
    q1 = """A shopkeeper sells a book at a profit of 10%. Later, he reduces the cost price by 4%
and increases the selling price by ₹6. As a result, his profit percentage becomes
18.75% (or 3/16). Find the original cost price of the book."""
    
    sol1 = """Given:
• Original profit = 10% → SP1 = 1.10x
• New CP = 0.96x
• New SP = 1.10x + 6
• New Profit% = 18.75% = 3/16
Solving gives: (1.10x + 6) - 0.96x = 30.96x 16
x = ₹150"""
    
    result = analyzer.analyze_question(q1, sol1)
    print(f"Question Type: {result.question_type}")
    print(f"Topic: {result.topic}")
    print(f"Key Data: {result.key_data}")
    print(f"Answer: {result.answer}")
