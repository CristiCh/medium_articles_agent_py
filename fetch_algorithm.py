from openai import OpenAI
import html
import re
import os

def load_previous_titles(history_path: str) -> set:
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_title(title: str, history_path: str):
    with open(history_path, 'a') as f:
        f.write(title + "\n")

def generate_swift_algorithm_exercise(api_key: str, history_path="exercise_history.txt", max_retries=5) -> str:
    client = OpenAI(api_key=api_key)

    previous_titles = load_previous_titles(history_path)

    difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
    level = difficulty_levels[len(previous_titles) % len(difficulty_levels)]

    for attempt in range(max_retries):
        prompt = (
            f"You are an expert Swift teacher creating a {level.lower()}-level algorithm exercise.\n"
            "Generate a unique problem, including a clear problem description followed by a well-explained solution in Swift.\n"
            "Use markdown formatting with headings, code blocks, and comments in the code.\n"
            "Do not reuse previous exercises or common tutorials.\n"
            "Keep it original and instructive."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=700,
            )

            text = response.choices[0].message.content.strip()
            text = re.sub(r'\n{3,}', '\n\n', text)

            if "# Problem Description" in text and "# Solution" in text:
                text = text.replace("# Problem Description", "---\n# Problem Description")
                text = text.replace("# Solution", "---\n# Solution")

            title_match = re.search(r"#\s*Problem Description\s*\n(.*)", text)
            if title_match:
                title_line = title_match.group(1).strip()
            else:
                title_line = text.splitlines()[0].strip()

            if title_line in previous_titles:
                print(f"[WARN] Duplicate exercise detected (attempt {attempt+1}), retrying...")
                continue

            def format_code_blocks(md: str) -> str:
                return re.sub(
                    r"```(?:swift)?\n([\s\S]*?)```",
                    lambda m: (
                        f"<div style=\"background:#1e1e1e; color:#f8f8f2; font-family:Menlo, monospace; "
                        f"font-size:14px; padding:15px; border-radius:8px; margin:20px 0; white-space:pre-wrap;\">"
                        f"{html.escape(m.group(1))}</div>"
                    ),
                    md
                )

            def format_output_blocks(md: str) -> str:
                return re.sub(
                    r"(//\s*Output:.*?)\n",
                    lambda m: (
                        f"<div style=\"background:#f5f5f5; color:#000; font-family:Courier New, monospace; "
                        f"padding:10px; border-left:4px solid #ccc; margin:10px 0;\">"
                        f"{html.escape(m.group(1))}</div>\n"
                    ),
                    md
                )

            text = format_code_blocks(text)
            text = format_output_blocks(text)

            save_title(title_line, history_path)

            print(f"[INFO] New {level} exercise generated: {title_line}")
            return text

        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1} failed: {e}")
            break

    return "⚠️ Could not generate a new Swift algorithm exercise. Please try again later."
