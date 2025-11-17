# Quick test script - Just paste your questions and run!

from main_pipeline import QuestionToVisualPipeline

my_questions = """
A sells an item to B at 20 % profit.
B sells it to C at 10 % loss.
C pays ₹ 594.
Find A’s cost price.

Sol: A’s SP = 1.20 x
B’s SP = 1.20 x × 0.90 = 1.08 x
Given 1.08 x = 594 → x = 594 ÷ 1.08 = 550
Answer → A’s Cost Price = ₹ 550
"""

if __name__ == "__main__":
    print("Testing your custom questions...\n")
    
    pipeline = QuestionToVisualPipeline(output_dir="test_outputs")
    pipeline.run_complete_pipeline(my_questions)
    
    print("\nDone! Check 'test_outputs' folder for results.")
