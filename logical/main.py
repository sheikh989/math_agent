# Demo script to test the complete automation system

from main_pipeline import QuestionToVisualPipeline

SAMPLE_DATASET = """
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

def main():
    print(" AI AUTOMATION FOR CREATIVE CONTENT DEVELOPMENT - DEMO")
    
    print("\nThis demo will:")
    print("  1. Analyze and categorize questions")
    print("  2. Convert to structured JSON format")
    print("  3. Generate AI-powered solutions")
    print("  4. Create visual explanations")
    print("  5. Validate and auto-save outputs")
    print("\n" + "="*70 + "\n")
    
    pipeline = QuestionToVisualPipeline(output_dir="demo_outputs")
    
    pipeline.run_complete_pipeline(SAMPLE_DATASET)
    
 
    print(" DEMO COMPLETE!")
    
    print("\nCheck the 'demo_outputs' folder for:")
    print("  - JSON files with structured data")
    print("  - Visual explanations (PNG images)")
    print("  - Validation reports")
    

if __name__ == "__main__":
    main()
