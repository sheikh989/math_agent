# Math Agent - AI-Powered Math Problem Solver

An intelligent multi-agent system that solves complex arithmetic word problems using AI. Built with [crewAI](https://crewai.com), this project uses four specialized AI agents that work together to understand, structure, solve, and explain mathematical problems step-by-step.

## What It Does

This system solves commercial arithmetic problems (profit/loss, cost price/selling price, discounts, markups) through a 4-stage pipeline:

1. **Question Analysis** - Detects problem type and extracts key data (numbers, percentages, relationships)
2. **JSON Structuring** - Converts extracted data into structured mathematical representations
3. **Problem Solving** - Solves equations step-by-step using deterministic logic and AI
4. **Visual Formatting** - Generates clean, human-readable explanations with the solution

### Example Problem

The system can solve problems like:
> "A shopkeeper sells a book at a profit of 10%. Later, he reduces the cost price by 4% and increases the selling price by ₹6. As a result, his profit percentage becomes 18.75%. Find the original cost price of the book."

## Prerequisites

- Python >=3.10 and <3.14
- UV package manager
- OpenAI API key (configured to use GPT-4)
- Gemini API key (optional, for alternative model)

## Installation

1. Install UV if you haven't already:
```bash
pip install uv
```

2. Install project dependencies:
```bash
crewai install
```

3. Configure your API keys in the `.env` file:
```
GEMINI_API_KEY=your_gemini_key_here
```

Note: The agents are configured to use `openai/gpt-4` in `agents.yaml`. Make sure you have access to the OpenAI API or modify the configuration to use a different model.

## How to Run

Run the math solver from the project root:

```bash
crewai run
```

Or use the Python module directly:

```bash
python -m math_agent.main
```

The system will process the example question and output a detailed solution with step-by-step reasoning.

## Project Structure

```
src/math_agent/
config/
  -agents.yaml      # Agent definitions and configurations
   -tasks.yaml       # Task pipeline definitions
tools/               # Custom tools for each agent
   -question_to_json_tool.py
crew.py             # Crew orchestration logic
main.py             # Entry point with example question
```

## Customization

To solve your own math problems:

1. Edit `src/math_agent/main.py` and replace the `question` variable with your problem
2. Modify `src/math_agent/config/agents.yaml` to adjust agent behavior or LLM models
3. Update `src/math_agent/config/tasks.yaml` to change the task pipeline

## Support

For questions about crewAI:
- [Documentation](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
