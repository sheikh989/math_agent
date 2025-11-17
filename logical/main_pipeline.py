# Main Pipeline: Integrates all tasks for complete automation

import json
import os
from typing import List, Dict
from question_automation import QuestionAnalyzer
from json_converter import DatasetToJSON
from ai_solver import MathSolver
from visual_generator import VisualExplanationGenerator
from bonus_validator import AutoSaveManager

class QuestionToVisualPipeline:
    
    def __init__(self, output_dir="outputs"):
        self.analyzer = QuestionAnalyzer()
        self.converter = DatasetToJSON()
        self.solver = MathSolver()
        self.visual_gen = VisualExplanationGenerator()
        self.save_manager = AutoSaveManager(output_dir)
        self.output_dir = output_dir
    
    def process_raw_dataset(self, raw_text: str) -> List[Dict]:
        print("Step 1: Analyzing questions...")
        structured_data = self.converter.parse_raw_dataset(raw_text)
        print(f"Analyzed {len(structured_data)} questions")
        return structured_data
    
    def enhance_with_ai_solutions(self, questions: List[Dict]) -> List[Dict]:
        print("\nStep 2: Generating AI solutions...")
        enhanced = []
        
        for i, q in enumerate(questions, 1):
            if not q.get('solution_steps') or len(q.get('solution_steps', [])) < 2:
                ai_solution = self.solver.solve_question(q)
                q['solution_steps'] = ai_solution['steps']
                q['answer'] = ai_solution.get('answer', q.get('answer', 'N/A'))
                q['formula_used'] = ai_solution.get('formula_used', [])
            
            enhanced.append(q)
            print(f"  Q{i}: {q.get('question_type', 'unknown')} - Solution generated")
        
        print(f"Enhanced {len(enhanced)} questions with AI solutions")
        return enhanced
    
    def generate_visuals(self, questions: List[Dict]) -> List[str]:
        print("\nStep 3: Generating visual explanations...")
        visual_dir = os.path.join(self.output_dir, "visuals")
        os.makedirs(visual_dir, exist_ok=True)
        
        visual_paths = []
        
        for i, q in enumerate(questions, 1):
            try:
                img = self.visual_gen.generate_visual(q, i)
                img_path = os.path.join(visual_dir, f"question_{i}.png")
                img.save(img_path)
                visual_paths.append(img_path)
                print(f"  Q{i}: Visual created")
            except Exception as e:
                print(f"  Q{i}: Error - {str(e)}")
                visual_paths.append(None)
        
        print(f"Generated {len([p for p in visual_paths if p])} visuals")
        return visual_paths
    
    def validate_and_save(self, questions: List[Dict]) -> Dict:
        print("\nStep 4: Validating and saving...")
        
        validated_questions = []
        stats = {"valid": 0, "invalid": 0}
        
        for i, q in enumerate(questions, 1):
            is_valid, json_path = self.save_manager.save_question(q, i)
            validated_questions.append(q)
            
            if is_valid:
                stats["valid"] += 1
                print(f"  Q{i}: Valid")
            else:
                stats["invalid"] += 1
                errors = q.get('validation', {}).get('errors', [])
                print(f"  Q{i}: Invalid - {', '.join(errors)}")
        
        report = self.save_manager.generate_validation_report(validated_questions)
        report_path = self.save_manager.save_report(report)
        
        print(f"\nValidation complete: {stats['valid']} valid, {stats['invalid']} invalid")
        print(f"Report saved: {report_path}")
        
        return stats
    
    def run_complete_pipeline(self, raw_dataset: str):
        
        print("QUESTION TO VISUAL AUTOMATION PIPELINE\n")
        
        
        questions = self.process_raw_dataset(raw_dataset)
        
        json_path = os.path.join(self.output_dir, "json", "raw_dataset.json")
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({"questions": questions}, f, indent=2, ensure_ascii=False)
        print(f"Raw JSON saved: {json_path}")
        
        questions = self.enhance_with_ai_solutions(questions)
        
        visual_paths = self.generate_visuals(questions)
        
        stats = self.validate_and_save(questions)
        
       
        print("PIPELINE COMPLETE")
       
        print(f"\nTotal Questions Processed: {len(questions)}")
        print(f"Valid Questions: {stats['valid']}")
        print(f"Invalid Questions: {stats['invalid']}")
        print(f"Visuals Generated: {len([p for p in visual_paths if p])}")
        print(f"Output Directory: {self.output_dir}")
       

if __name__ == "__main__":
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
    
    pipeline = QuestionToVisualPipeline()
    pipeline.run_complete_pipeline(raw_dataset)
