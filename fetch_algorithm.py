from openai import OpenAI
import re

def generate_swift_algorithm_exercise(api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    prompt = (
        "You are an expert Swift teacher creating a beginner-friendly algorithm exercise.\n"
        "Provide a clear problem description followed by a well-explained solution in Swift.\n"
        "Use markdown formatting with headings, code blocks, and comments inside the code to make it easy to read and understand."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=600,
        )
        text = response.choices[0].message.content.strip()
        
        # Extra formatting: clean up excessive blank lines (more than 2)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Optional: ensure code blocks are fenced properly
        # (Assuming GPT returns triple backticks correctly)
        
        # Add horizontal rules to separate sections if not present
        if "# Problem Description" in text and "# Solution" in text:
            text = text.replace("# Problem Description", "---\n# Problem Description")
            text = text.replace("# Solution", "---\n# Solution")
        
        return text
        
        return text
    except Exception as e:
        return f"Error generating exercise: {e}"
