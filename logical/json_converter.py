# Task 2: Convert raw dataset into JSON format input

import json
import re
from typing import List, Dict
from question_automation import QuestionAnalyzer, Question
from dataclasses import asdict

class DatasetToJSON:
    
    def __init__(self):
        self.analyzer = QuestionAnalyzer()
    
    def parse_raw_dataset(self, raw_text: str) -> List[Dict]:
        qa_pairs = re.split(r'\n\s*Q\.\s*', raw_text)
        qa_pairs = [q.strip() for q in qa_pairs if q.strip()]
        
        structured_data = []
        
        for qa in qa_pairs:
            parts = re.split(r'\n\s*Sol:\s*', qa, maxsplit=1)
            
            if len(parts) == 2:
                question_text = parts[0].strip()
                solution_text = parts[1].strip()
                
                analyzed = self.analyzer.analyze_question(question_text, solution_text)
                structured_data.append(asdict(analyzed))
        
        return structured_data
    
    def create_json_input(self, questions: List[Question]) -> str:
        json_data = {
            "dataset_info": {
                "total_questions": len(questions),
                "exam_types": ["SSC", "Banking", "Railways", "Defence"],
                "format_version": "1.0"
            },
            "questions": [asdict(q) for q in questions]
        }
        
        return json.dumps(json_data, indent=2, ensure_ascii=False)
    
    def save_to_json(self, questions: List[Question], filename: str = "questions_dataset.json"):
        json_str = self.create_json_input(questions)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"Saved {len(questions)} questions to {filename}")

if __name__ == "__main__":
    import re
    
    raw_dataset = """
    Q. A shopkeeper sells a book at a profit of 10%. Later, he reduces the cost price by 4%
and increases the selling price by ₹6. As a result, his profit percentage becomes
18.75% (or 3/16). Find the original cost price of the book.
Sol:
Given:
• Original profit = 10% → SP1 = 1.10x
• New CP = 0.96x
• New SP = 1.10x + 6
• New Profit% = 18.75% = 3/16
Solving gives: (1.10x + 6) - 0.96x = 30.96x 16
x = ₹150

Q. A trader marks an article 40% above its cost price.
He allows a 10% discount on the marked price and still earns a profit of ₹36.
Find the cost price of the article.
Sol: Let the cost price = ₹ x
1. Marked Price = 1.40 x
2. After 10 % discount → Selling Price = 1.40x X 0.90 = 1.26x
3. Profit = SP − CP = 1.26x − x = 0.26x
Given profit = ₹ 36
0.26x = 36
=> x = 36/0.26 ≈ 138.46
Answer → Cost Price ≈ ₹ 138.46
    """
    
    converter = DatasetToJSON()
    structured = converter.parse_raw_dataset(raw_dataset)
    
    with open("questions_dataset.json", 'w', encoding='utf-8') as f:
        json.dump({"questions": structured}, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {len(structured)} questions to JSON")
    print("\nSample output:")
    print(json.dumps(structured[0], indent=2, ensure_ascii=False))
