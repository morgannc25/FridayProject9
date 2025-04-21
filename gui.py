import tkinter as tk
from tkinter import scrolledtext
import os
from dotenv import load_dotenv
import openai
import traceback

def get_completion_from_openai(prompt, api_key, model="gpt-3.5-turbo", max_tokens=200): # Updated model
    """
    Sends a prompt to the OpenAI API and returns the generated completion using the chat/completions endpoint.

    Args:
        prompt (str): The prompt to send to the API.
        api_key (str): The OpenAI API key.
        model (str, optional): The OpenAI model to use.  Defaults to "gpt-3.5-turbo".
        max_tokens (int, optional): The maximum number of tokens in the generated completion. Defaults to 200.

    Returns:
        str: The generated completion, or None if an error occurs.
    """
    print("get_completion_from_openai called with prompt:", prompt)
    print("API Key:", api_key)
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create( # Changed to ChatCompletion
            model=model,
            messages=[  # Changed to messages structure
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        print("OpenAI API Response Status Code:", response.status_code)
        print("OpenAI API Response:", response.text)
        response.raise_for_status()
        return response.choices[0].message.content.strip() # Changed data access
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        print(f"Error Details: {e.message}")
        return None
    except Exception as e:
        print(f"Error getting completion from OpenAI: {e}")
        traceback.print_exc()
        return None


def submit_prompt():
    """
    Handles the submission of the prompt, retrieves the completion from OpenAI,
    and displays it in the text area.
    """
    print("submit_prompt called")
    prompt_text = prompt_entry.get("1.0", tk.END).strip()
    completion_text.delete("1.0", tk.END)
    if not prompt_text:
        completion_text.insert(tk.END, "Please enter a prompt.")
        return

    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print("API Key (inside submit_prompt):", api_key)
    if not api_key:
        completion_text.insert(tk.END, "API key is missing. Please check your .env file.")
        return

    completion = get_completion_from_openai(prompt_text, api_key)
    print("Completion from get_completion_from_openai:", completion)
    if completion:
        completion_text.insert(tk.END, completion)
    else:
        completion_text.insert(tk.END, "Failed to get completion.")


def create_gui():
    """
    Creates the main GUI window and its elements.
    """
    root = tk.Tk()
    root.title("OpenAI Completion App")
    root.geometry("600x400")

    # Prompt Label and Text Area
    prompt_label = tk.Label(root, text="Prompt:", font=("Arial", 12))
    prompt_label.pack(pady=5, anchor="w")
    global prompt_entry
    prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=70, font=("Arial", 10), fg="white", bg="gray20")
    prompt_entry.pack(padx=10, pady=5)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit_prompt, font=("Arial", 12), bg="white", fg="black")
    submit_button.pack(pady=10)

    # Completion Label and Text Area
    completion_label = tk.Label(root, text="Completion:", font=("Arial", 12))
    completion_label.pack(pady=5, anchor="w")
    global completion_text
    completion_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=70, font=("Arial", 10), state=tk.DISABLED, fg="white", bg="gray20")
    completion_text.pack(padx=10, pady=5)

    return root


if __name__ == "__main__":
    load_dotenv()
    root = create_gui()
    root.mainloop()