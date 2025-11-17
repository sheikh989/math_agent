# Script to test your own custom questions

from main_pipeline import QuestionToVisualPipeline

YOUR_QUESTIONS = """
Q. Your first question here...
Sol: Your solution here...

Q. Your second question here...
Sol: Your solution here...
"""

def test_from_file(filename="my_questions.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = f.read()
        
        pipeline = QuestionToVisualPipeline(output_dir="my_outputs")
        pipeline.run_complete_pipeline(questions)
        
        print(f"\nSuccessfully processed questions from {filename}")
        print("Check 'my_outputs' folder for results!")
        
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        print("Create the file and add your questions in this format:")
        print("\nQ. Your question here...")
        print("Sol: Your solution here...")

def test_from_string():
    if YOUR_QUESTIONS.strip():
        pipeline = QuestionToVisualPipeline(output_dir="my_outputs")
        pipeline.run_complete_pipeline(YOUR_QUESTIONS)
        print("\nSuccessfully processed your questions!")
        print("Check 'my_outputs' folder for results!")
    else:
        print("No questions found! Add your questions to YOUR_QUESTIONS variable.")

if __name__ == "__main__":
    print("="*70)
    print("CUSTOM QUESTION TESTER")
    print("="*70)
    print("\nChoose your method:")
    print("1. Edit YOUR_QUESTIONS variable in this file and run")
    print("2. Create 'my_questions.txt' file with your questions")
    print("\n" + "="*70 + "\n")
    
    if YOUR_QUESTIONS.strip() and "Your first question" not in YOUR_QUESTIONS:
        print("Using questions from YOUR_QUESTIONS variable...\n")
        test_from_string()
    elif input("Do you have 'my_questions.txt' file? (y/n): ").lower() == 'y':
        test_from_file()
    else:
        print("\nInstructions:")
        print("1. Create a file called 'my_questions.txt'")
        print("2. Add your questions in this format:")
        print("\n   Q. Your question here...")
        print("   Sol: Your solution here...")
        print("\n   Q. Another question...")
        print("   Sol: Another solution...")
        print("\n3. Run this script again!")
