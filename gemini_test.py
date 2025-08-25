import subprocess
import os

project_path = os.path.abspath("./zylo-docs")
all_code_content = ""
print(f"Reading files from: {project_path}")
try:
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.md')):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        all_code_content += f"--- File: {file} ---\n{file_content}\n\n"
                except Exception:
                    pass
except Exception as e:
    print(f"Error reading files: {e}")
    exit()

prompt = """You are a text-processing engine. Your one and only capability is to analyze the text provided to you via standard input. You MUST NOT attempt to access any local files, directories, or execute any commands. Your entire world is the text I am providing to you.

From the provided source code text, your task is to meticulously analyze it and extract information **only relevant to its external API endpoints**.

For each endpoint you find, please identify and list the following:
1.  **HTTP Method:** (e.g., GET, POST, PUT, DELETE)
2.  **URL Path:** (e.g., /api/users/{user_id})
3.  **Description:** A brief, one-sentence description of what the endpoint does.

Please format the final output in clean Markdown.

The source code text is now being provided via standard input:"""

command = ["/opt/homebrew/bin/gemini", "-p", prompt]

print(f"\nExecuting command: /opt/homebrew/bin/gemini -p \"{prompt[:50]}...\"")
print("Passing file content via stdin...")
print("-" * 20)

try:
    result = subprocess.run(
        command,
        input=all_code_content,
        capture_output=True,
        text=True,
        check=False,
        timeout=120
    )

    print("--- STDOUT ---")
    print(result.stdout)
    print("\n--- STDERR ---")
    print(result.stderr)
    print(f"\n--- Exit Code: {result.returncode} ---")

except Exception as e:
    print(f"An unexpected error occurred: {e}")