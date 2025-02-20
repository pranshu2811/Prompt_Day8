import os
import google.generativeai as genai
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

#Fetch API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Debugging: Check if API key is loaded
if not GEMINI_API_KEY:
    raise ValueError("Error: GEMINI_API_KEY is missing! Check your .env file.")

#Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

### **Custom Prompt Library**
class PromptLibrary:
    """
    A library of structured prompts for different FAQ scenarios.
    """
    @staticmethod
    def best_practices_prompt(topic):
        return f"""
        You are a technical expert. Provide a structured, step-by-step guide on:
        **{topic}**
        
        Format:
        1. **Identify the Issue** - Explain common symptoms or causes.
        2. **Step-by-Step Resolution** - Outline best practices to fix the issue.
        3. **Preventive Measures** - Recommend ways to avoid the issue in the future.
        4. **Resources** - Suggest useful tools or documentation.
        
        Answer:
        """

    @staticmethod
    def troubleshooting_prompt(issue):
        return f"""
        You are a customer support agent assisting a user with the issue:
        **{issue}**
        
        Format:
        - **Issue Description**: Explain the problem in simple terms.
        - **Possible Causes**: List at least 3 potential reasons.
        - **Solutions**: Provide step-by-step instructions to fix it.
        - **When to Seek Help**: Suggest when to escalate the issue.
        
        Answer:
        """

    @staticmethod
    def definition_prompt(term):
        return f"""
        You are an AI assistant. Provide a **clear and concise definition** for:
        **{term}**
        
        - **Simple Explanation** (for beginners)
        - **Technical Explanation** (for advanced users)
        - **Examples of Use Cases**
        
        Answer:
        """

def generate_ai_response(prompt):
    """
    Generates AI response using Gemini API with a structured prompt.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        #Handle empty responses
        if not response or not response.text.strip():
            return "AI did not return a valid response. Try again with a different question."

        return response.text.strip()

    except Exception as e:
        return f"Error generating AI response: {e}"

def main():
    try:
        #Get user input for dynamic FAQ response
        user_query = input("\nEnter your FAQ question: ").strip().lower()

        #Select appropriate prompt type
        if "best practices" in user_query:
            prompt = PromptLibrary.best_practices_prompt(user_query)
        elif "troubleshooting" in user_query:
            prompt = PromptLibrary.troubleshooting_prompt(user_query)
        elif "define" in user_query or "what is" in user_query:
            prompt = PromptLibrary.definition_prompt(user_query)
        else:
            prompt = f"You are an AI assistant. Answer the following question in a structured manner:\n\n{user_query}\n\nAnswer:"

        print("\n Generating AI response...")
        ai_response = generate_ai_response(prompt)
        print(" AI Response:\n", ai_response)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
