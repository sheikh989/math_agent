from .crew import MathCrew

def run():
    print("\n=== Math Solver ===\n")
    question = '''A shopkeeper sells a book at a profit of 10%. Later, he reduces the cost price by 4%
                  and increases the selling price by ₹6. As a result, his profit percentage becomes
                  18.75% (or 3/16). Find the original cost price of the book.'''

    crew = MathCrew()
    result = crew.kickoff(question)

    print("\n\n=== FINAL OUTPUT ===\n")
    print(result)

if __name__ == "__main__":
    run()
