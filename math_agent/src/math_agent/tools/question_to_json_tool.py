from crewai.tools import tool
import json
import re
import ast
import operator
import math
import traceback

@tool("question_auto_extractor_tool")
def question_auto_extractor_tool(question: str) -> str:
    text = question.lower()
    if "profit" in text or "loss" in text:
        problem_type = "profit_loss"
    elif "discount" in text:
        problem_type = "discount"
    elif "marked" in text or "markup" in text or "mark up" in text:
        problem_type = "marked_price"
    else:
        problem_type = "commercial_arithmetic"

    raw_vals = re.findall(r"₹\s?\d+|\d+\.?\d*%|\d+\.?\d*", question)

    features = {
        "has_markup": "mark" in text,
        "has_discount": "discount" in text,
        "has_profit_value": ("profit" in text and "₹" in text),
        "has_profit_percentage": ("profit" in text and "%" in text),
        "has_loss": "loss" in text,
        "has_change": ("increase" in text or "decrease" in text)
    }

    return json.dumps({
        "problem_type": problem_type,
        "raw_values": raw_vals,
        "key_features": features,
        "raw_question": question
    }, indent=2)


@tool("json_structuring_tool")
def json_structuring_tool(extracted_json: str) -> str:
    data = json.loads(extracted_json)
    raw = data["raw_values"]
    text = data["raw_question"].lower()

    values = {}
    variables = {"CP": "unknown"}
    equations = []

    for v in raw:
        if "%" in v:
            if "mark" in text:
                values["markup_percentage"] = v
            elif "discount" in text:
                values["discount_percentage"] = v
            elif "profit" in text:
                values["profit_percentage"] = v

        elif "₹" in v:
            if "profit" in text:
                values["profit_value"] = v
            else:
                values[f"amount_{v}"] = v

    if "markup_percentage" in values:
        p = float(values["markup_percentage"].replace("%", ""))/100
        variables["MP"] = f"CP * (1 + {p})"

    if "discount_percentage" in values:
        d = float(values["discount_percentage"].replace("%", ""))/100
        variables["SP"] = f"MP * (1 - {d})"

    if "profit_value" in values:
        equations.append("Profit = SP - CP")
        equations.append(f"Profit = {values['profit_value'].replace('₹','')}")

    if "profit_percentage" in values:
        p = float(values["profit_percentage"].replace("%", ""))/100
        equations.append(f"(SP - CP) / CP = {p}")

    return json.dumps({
        "problem_type": data["problem_type"],
        "values": values,
        "variables": variables,
        "equations": equations,
        "required_output": "Find cost price or selling price as required",
        "raw_question": data["raw_question"]
    }, indent=2)


@tool("visual_formatter_tool")
def visual_formatter_tool(solved_json: str) -> str:
    data = json.loads(solved_json)

    vals = data.get("values", {})
    steps = data.get("solution_template", [])
    final = data.get("final_answer", "Not found")

    output = "## Math Problem Solution\n\n"

    output += "### Given Values\n"
    for k, v in vals.items():
        output += f"- **{k.replace('_',' ').title()}**: {v}\n"

    output += "\n### Step-by-Step Solution\n"
    for step in steps:
        output += f"- {step}\n"

    output += f"\n### Final Answer: **{final}**\n"

    return output


@tool("generic_math_solver_tool")
def generic_math_solver_tool(json_input: str) -> str:
    data = json.loads(json_input)

    values = data.get("values", {})
    variables = data.get("variables", {})
    equations = data.get("equations", [])
    steps = []
    steps.append("Step 1: Begin interpreting extracted values.")

    profit_value = None
    profit_percentage = None
    markup_percentage = None
    discount_percentage = None

    if "profit_value" in values:
        try:
            profit_value = float(values["profit_value"].replace("₹", ""))
        except:
            pass

    if "profit_percentage" in values:
        try:
            profit_percentage = float(values["profit_percentage"].replace("%", "")) / 100
        except:
            pass

    if "markup_percentage" in values:
        try:
            markup_percentage = float(values["markup_percentage"].replace("%", "")) / 100
        except:
            pass

    if "discount_percentage" in values:
        try:
            discount_percentage = float(values["discount_percentage"].replace("%", "")) / 100
        except:
            pass

    steps.append(f"Step 2: Extracted parameters: markup={markup_percentage}, discount={discount_percentage}, profit_value={profit_value}, profit_percentage={profit_percentage}")

    CP = None
    SP_expr = "x"

    if markup_percentage is not None:
        SP_expr = f"x*(1+{markup_percentage})"
        steps.append(f"Marked Price: MP = x * (1 + {markup_percentage})")

    if discount_percentage is not None:
        SP_expr = f"{SP_expr}*(1-{discount_percentage})"
        steps.append(f"Selling Price: SP = MP * (1 - {discount_percentage})")

    steps.append(f"Combined SP expression: SP = {SP_expr}")

    try:
        expr = SP_expr.replace("x*", "")
        coefficient = eval(expr)

        steps.append(f"Step 3: Simplifying SP expression gives coefficient = {coefficient}")

        if profit_value is not None:
            steps.append("Step 4: Using formula Profit = SP - CP")
            denom = coefficient - 1
            if denom == 0:
                raise ValueError("Invalid equation: denominator zero")

            CP = profit_value / denom
            steps.append(f"Step 5: Solving → x = {CP}")
            steps.append(f"Final Answer: Cost Price = ₹{round(CP, 2)}")
            data["solution_template"] = steps
            return json.dumps(data, indent=2)

        if profit_percentage is not None:
            steps.append("Step 4: Using profit percentage formula (SP - CP)/CP = profit%")
            if (coefficient - 1) != profit_percentage:
                steps.append("Profit% alone does not determine CP. Need profit value or more equations.")
            else:
                steps.append("Profit% matches coefficient relationship, but CP cannot be numerically solved without more info.")

    except Exception as e:
        steps.append("Deterministic solver failed.")
        steps.append(str(e))
        steps.append(traceback.format_exc())

    steps.append("Step 6: Switching to GPT Solver Fallback.")

    from openai import OpenAI
    client = OpenAI()

    prompt = f"""
Solve this commercial arithmetic problem step by step.

Here is the extracted JSON:

{json.dumps(data, indent=2)}

Return only:
- A python dict with key "solution_template": [list of steps]
- No prose outside of JSON.

If information is missing to compute exact numeric answer, derive as far as possible.
"""

    gpt_resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        gpt_json = gpt_resp.choices[0].message.content
        gpt_out = json.loads(gpt_json)
        data["solution_template"] = gpt_out["solution_template"]
    except:
        steps.append("GPT fallback also failed. Returning partial solution.")
        data["solution_template"] = steps

    return json.dumps(data, indent=2)