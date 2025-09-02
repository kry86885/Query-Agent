import sqlite3
import google.generativeai as genai

# Use your actual API key
genai.configure(api_key="YOUR_API_KEY")

# Connect to SQLite database
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# Example schema: adapt this if needed
def get_schema(cursor):
    schema = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for tbl, in cursor.fetchall():
        schema += f"\nTable: {tbl}\n"
        cursor.execute(f"PRAGMA table_info({tbl});")
        for col in cursor.fetchall():
            schema += f"- {col[1]} ({col[2]})\n"
    return schema

def ask_gemini_with_schema(question):
    schema = get_schema(cursor)

    prompt = f"""
You are an expert SQL generator.
Use the following SQLite schema to generate SQL queries.

Schema:
{schema}

User Question:
{question}

Please respond with:

Intro: <describe what it does>
Query:
<your valid SQLite SELECT query>
Explanation: <step-by-step explanation>
"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        text = response.text
    except:
        text = response.candidates[0].content.parts[0].text

    # Extract SQL
    import re
    match = re.search(r"(SELECT[\s\S]*?;)", text, re.IGNORECASE)
    sql_query = match.group(1) if match else None

    results = []
    if sql_query:
        print(sql_query)
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
        except Exception as e:
            results = [("Error executing SQL:", str(e))]

    return text, results

# Example usage
question = "Find the total purchase amount for each customer in 2024."
answer, results = ask_gemini_with_schema(question)
def refine_answer_llm(question, results):
    prompt = f"""
You are an assistant that converts SQL query results into natural, conversational answers.

User Question: {question}
SQL Results: {results}

Instructions:
- Do not mention SQL or technical details.
- Provide a clear, human-like response directly answering the question.
- If results are numeric counts, say them naturally (e.g., "There are 5 customers from USA").
- If results are a list of rows, summarize them in simple sentences.
- If no results, say politely that nothing was found.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
# print("Gemini Response:\n", answer)
print("\nFinal Answer:\n", refine_answer_llm(question,results))