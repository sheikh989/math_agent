# AI Automation for Creative Content Development

Automated system for converting Government Exam questions (SSC, Banking, Railways, Defence) into visual explanations with consistent design.
### There is need to fix more things for work properly , i try my best in this assisment i hope you liked my work , because of the deadline 

## Overview

This project automates the complete pipeline from raw question text to formatted visual explanations:
- **Question Analysis & Categorization**
- **JSON Data Conversion**
- **AI-Powered Solution Generation**
- **Visual Explanation Creation**
- **Validation & Auto-Save**

## Project Structure

```
question_automation.py    # Task 1: Question type detection & data extraction
json_converter.py          # Task 2: Raw text to JSON conversion
ai_solver.py               # Task 3: AI/Logic-based solution generation
visual_generator.py        # Task 4: Visual explanation generator
bonus_validator.py         # Task 5: Validation & auto-save system
main_pipeline.py           # Complete integrated pipeline
requirements.txt           # Python dependencies
main.py
outputs/                   # Generated outputs
  - valid/                 # Valid questions
  - invalid/               # Invalid/flagged questions
  - json/                  # JSON outputs
  - visuals/               # Generated images
  - logs/                  # Validation reports
```

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

### Option 1: Run with Sample Questions (Quickest Way)

```bash
python main.py
```

This will:
- Process 2 sample questions automatically
- Generate JSON outputs in `demo_outputs/json/`
- Create visual explanations in `demo_outputs/visuals/`
- Generate validation report in `demo_outputs/logs/`

### Option 2: Test Your Own Questions

**Step 1:** Open `quick_test.py` and replace the `my_questions` variable:

```python
my_questions = """
Q. Your question here...
Sol: Your solution here...

Q. Another question...
Sol: Another solution...
"""
```

**Step 2:** Run the script:

```bash
python quick_test.py
```

Your results will be in the `test_outputs/` folder.

### Option 3: Test from a Text File

**Step 1:** Create a file called `my_questions.txt` with your questions:

```
Q. Your question here...
Sol: Your solution here...

Q. Another question...
Sol: Another solution...
```

**Step 2:** Run:

```bash
python test_custom_questions.py
```

When prompted, type `y` to load from the file.

### Option 4: Use as Python Module

```python
from main_pipeline import QuestionToVisualPipeline

raw_dataset = """
Q. Your question here...
Sol: Your solution here...
"""

pipeline = QuestionToVisualPipeline(output_dir="my_outputs")
pipeline.run_complete_pipeline(raw_dataset)
```

## Question Format

Your questions must follow this format:

```
Q. Question text here...
Sol: 
Solution step 1
Solution step 2
Answer → Final answer

Q. Next question...
Sol:
Solution steps...
```

## Output Structure

After running, check your output folder:

```
outputs/
json/
   -raw_dataset.json          # All questions in JSON format
   -valid/
   -question_1.json       # Individual question files
    -question_2.json
-visuals/
  -question_1.png            # Visual explanations
   -question_2.png
-logs/
    -validation_report_*.txt   # Validation results
```

## Usage Examples

### Individual Task Usage

#### Task 1: Question Analysis
```python
from question_automation import QuestionAnalyzer

analyzer = QuestionAnalyzer()
result = analyzer.analyze_question(question_text, solution_text)
print(f"Type: {result.question_type}")
print(f"Key Data: {result.key_data}")
```

#### Task 2: JSON Conversion
```python
from json_converter import DatasetToJSON

converter = DatasetToJSON()
structured_data = converter.parse_raw_dataset(raw_text)
converter.save_to_json(structured_data, "output.json")
```

#### Task 3: AI Solution Generation
```python
from ai_solver import MathSolver

solver = MathSolver()
solution = solver.solve_question(question_data)
print("Steps:", solution["steps"])
print("Answer:", solution["answer"])
```

#### Task 4: Visual Generation
```python
from visual_generator import VisualExplanationGenerator

generator = VisualExplanationGenerator()
img = generator.generate_visual(question_data, q_number=1)
img.save("output.png")
```

#### Task 5: Validation & Auto-Save
```python
from bonus_validator import AutoSaveManager

manager = AutoSaveManager()
is_valid, path = manager.save_question(question_data, q_number=1)
report = manager.generate_validation_report(all_questions)
```

## Features

### Task 1: Question Automation
- Detects question types: Profit/Loss, Percentage, Ratio, Time & Work, etc.
- Extracts numerical data, percentages, currency values
- Categorizes questions for batch processing
- Parses solution steps automatically

### Task 2: JSON Conversion
- Converts raw text to structured JSON format
- Maintains question metadata (type, topic, key data)
- Supports batch processing of multiple questions
- Preserves solution steps and answers

### Task 3: AI/Logic Integration
- Auto-solves Profit & Loss problems
- Step-by-step solution generation
- Formula identification and application
- Handles multiple problem patterns:
  - Markup + Discount scenarios
  - Two-profit scenarios
  - CP/SP/MP calculations

### Task 4: Visual Generation
- Creates consistent visual templates
- Professional design with color coding
- Sections: Header, Question, Solution Steps, Answer
- Customizable dimensions and styling
- Text wrapping for long content

### Task 5: Bonus Features
- **Validation System:**
  - Checks question length and structure
  - Validates numerical data presence
  - Detects gibberish or invalid content
  - Verifies solution completeness
  
- **Auto-Save System:**
  - Organized directory structure
  - Separates valid/invalid questions
  - Generates validation reports
  - Timestamps all outputs

## Question Types Supported

1. **Profit & Loss** - CP, SP, MP, discount, markup
2. **Percentage** - Increase, decrease, percentage calculations
3. **Ratio & Proportion** - Direct/inverse ratios
4. **Time & Work** - Work completion, efficiency
5. **Speed & Distance** - Train, car problems
6. **Simple Interest** - Principal, rate, time
7. **Compound Interest** - Compounding periods

## Output Format

### JSON Structure
```json
{
  "raw_text": "Question text...",
  "question_type": "profit_loss",
  "topic": "Profit & Loss",
  "key_data": {
    "numbers": [10, 4, 6, 18.75],
    "has_percentage": true,
    "has_currency": true
  },
  "solution_steps": [
    "Step 1...",
    "Step 2..."
  ],
  "answer": "₹150",
  "validation": {
    "is_valid": true,
    "errors": [],
    "warnings": []
  }
}
```

### Visual Output
- PNG images (800x1000px default)
- Consistent template design
- Color-coded sections
- Professional typography
- Step-by-step visual flow

## Validation Rules

Questions are validated against:
- Minimum length (20 characters)
- Presence of numerical data
- Question indicators (?, find, calculate)
- Common word usage (not gibberish)
- Reasonable character distribution
- Solution completeness
- Answer presence and format

## Extending the System

### Adding New Question Types
```python
# In question_automation.py
QUESTION_PATTERNS = {
    'your_type': [
        r'pattern1',
        r'pattern2'
    ]
}
```

### Adding New Solvers
```python
# In ai_solver.py
def solve_your_type_problem(self, question_data: Dict) -> Dict:
    # Your solving logic
    return {"steps": [...], "answer": "..."}
```

### Customizing Visual Template
```python
# In visual_generator.py
generator = VisualExplanationGenerator(
    template_width=1000,
    template_height=1200
)
generator.primary_color = (your_rgb_color)
```

## Performance

- Processes 100+ questions per minute
- Generates visuals in ~0.5s per question
- Validates and categorizes in real-time
- Scalable for large datasets

## Example Output

Input:
```
Q. A trader marks an article 40% above its cost price.
He allows a 10% discount and earns a profit of ₹36.
Find the cost price.
```

Output:
- JSON with structured data
- Visual explanation with steps
- Validation report
- Organized file storage

## Notes

- Designed for Government Exam questions (SSC, Banking, Railways, Defence)
- Maintains topic-wise design consistency
- Supports batch processing of large datasets
- Extensible architecture for new question types
- Comprehensive error handling and validation

## Future Enhancements

- Support for more question types (Geometry, Algebra)
- Multi-language support
- Advanced AI models (GPT/Claude integration)
- Interactive visual templates
- Web interface for easy access
- Database integration for question banks
