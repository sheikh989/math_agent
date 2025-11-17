# Task 4: Convert JSON input into formatted visual explanations

import json
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List
import textwrap

class VisualExplanationGenerator:
    
    def __init__(self, template_width=800, template_height=1000):
        self.width = template_width
        self.height = template_height
        self.bg_color = (255, 255, 255)
        self.primary_color = (41, 128, 185)
        self.secondary_color = (52, 73, 94)
        self.accent_color = (231, 76, 60)
        self.padding = 40
        
    def create_template(self) -> Image.Image:
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        return img
    
    def get_font(self, size=20, bold=False):
        try:
            if bold:
                return ImageFont.truetype("arialbd.ttf", size)
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()
    
    def draw_header(self, draw: ImageDraw, topic: str, q_number: int):
        draw.rectangle(
            [(self.padding, self.padding), (self.width - self.padding, self.padding + 60)],
            fill=self.primary_color
        )
        
        font_title = self.get_font(28, bold=True)
        draw.text(
            (self.width // 2, self.padding + 30),
            f"Q{q_number}. {topic}",
            fill=(255, 255, 255),
            font=font_title,
            anchor="mm"
        )
    
    def draw_question(self, draw: ImageDraw, question_text: str, y_start: int) -> int:
        font = self.get_font(18)
        
        draw.text(
            (self.padding, y_start),
            "Question:",
            fill=self.secondary_color,
            font=self.get_font(20, bold=True)
        )
        
        wrapped = textwrap.fill(question_text, width=70)
        lines = wrapped.split('\n')
        
        y = y_start + 35
        for line in lines:
            draw.text((self.padding, y), line, fill=self.secondary_color, font=font)
            y += 28
        
        return y + 20
    
    def draw_solution_steps(self, draw: ImageDraw, steps: List[str], y_start: int) -> int:
        draw.rectangle(
            [(self.padding, y_start), (self.width - self.padding, y_start + 40)],
            fill=(236, 240, 241)
        )
        draw.text(
            (self.padding + 10, y_start + 20),
            "Solution:",
            fill=self.primary_color,
            font=self.get_font(22, bold=True),
            anchor="lm"
        )
        
        y = y_start + 60
        font = self.get_font(16)
        
        for i, step in enumerate(steps, 1):
            circle_x = self.padding + 15
            circle_y = y + 10
            draw.ellipse(
                [(circle_x - 12, circle_y - 12), (circle_x + 12, circle_y + 12)],
                fill=self.primary_color
            )
            draw.text(
                (circle_x, circle_y),
                str(i),
                fill=(255, 255, 255),
                font=self.get_font(14, bold=True),
                anchor="mm"
            )
            
            wrapped = textwrap.fill(step, width=65)
            step_lines = wrapped.split('\n')
            
            for line in step_lines:
                draw.text((self.padding + 40, y), line, fill=self.secondary_color, font=font)
                y += 24
            
            y += 10
        
        return y + 10
    
    def draw_answer(self, draw: ImageDraw, answer: str, y_start: int):
        box_height = 60
        draw.rectangle(
            [(self.padding, y_start), (self.width - self.padding, y_start + box_height)],
            fill=self.accent_color,
            outline=self.accent_color,
            width=3
        )
        
        draw.text(
            (self.width // 2, y_start + box_height // 2),
            f"Answer: {answer}",
            fill=(255, 255, 255),
            font=self.get_font(24, bold=True),
            anchor="mm"
        )
    
    def generate_visual(self, question_data: Dict, q_number: int = 1) -> Image.Image:
        img = self.create_template()
        draw = ImageDraw.Draw(img)
        
        topic = question_data.get('topic', 'General')
        question_text = question_data.get('raw_text', '')
        solution_steps = question_data.get('solution_steps', [])
        answer = question_data.get('answer', 'N/A')
        
        y_pos = self.padding + 80
        self.draw_header(draw, topic, q_number)
        
        y_pos = self.draw_question(draw, question_text, y_pos)
        y_pos = self.draw_solution_steps(draw, solution_steps, y_pos)
        
        answer_y = min(y_pos, self.height - 100)
        self.draw_answer(draw, answer, answer_y)
        
        return img
    
    def process_json_dataset(self, json_file: str, output_dir: str = "output_visuals"):
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        
        for i, q_data in enumerate(questions, 1):
            img = self.generate_visual(q_data, i)
            output_path = os.path.join(output_dir, f"question_{i}.png")
            img.save(output_path)
            print(f"Generated: {output_path}")
        
        print(f"\nTotal visuals generated: {len(questions)}")

if __name__ == "__main__":
    generator = VisualExplanationGenerator()
    
    sample_data = {
        "topic": "Profit & Loss",
        "raw_text": "A trader marks an article 40% above its cost price. He allows a 10% discount and earns ₹36 profit.",
        "solution_steps": [
            "Let Cost Price = ₹x",
            "Marked Price = 1.40x",
            "After 10% discount → SP = 1.40x × 0.90 = 1.26x",
            "Profit = SP - CP = 1.26x - x = 0.26x",
            "Given: 0.26x = 36",
            "x = 36/0.26 ≈ 138.46"
        ],
        "answer": "₹138.46"
    }
    
    img = generator.generate_visual(sample_data)
    img.save("sample_visual.png")
    print("Sample visual created: sample_visual.png")
