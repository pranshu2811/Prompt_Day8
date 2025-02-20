import os
import google.generativeai as genai
import textwrap
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API Keys & Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Debugging: Check if variables are loaded
if not GEMINI_API_KEY:
    raise ValueError(" Missing GEMINI_API_KEY in .env file!")

if not PINECONE_API_KEY:
    raise ValueError(" Missing PINECONE_API_KEY in .env file!")

if not PINECONE_ENVIRONMENT:
    raise ValueError(" Missing PINECONE_ENVIRONMENT in .env file!")

if not PINECONE_INDEX_NAME:
    raise ValueError(" Missing PINECONE_INDEX_NAME in .env file!")

print(" Environment variables loaded successfully!")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


class NLPExperiment:
    def __init__(self):
        pass

    def summarization_prompt(self, text, style="concise"):
        """
        Generates different types of summarization prompts.
        """
        if style == "concise":
            prompt = f"""Summarize the following text concisely:\n
            {textwrap.fill(text, width=80)}\n
            Summary:"""
        elif style == "detailed":
            prompt = f"""Summarize the following text in detail:\n
            {textwrap.fill(text, width=80)}\n
            Detailed Summary:"""
        elif style == "key_points":
            prompt = f"""Extract the 3 most important points from the text:\n
            {textwrap.fill(text, width=80)}\n
            Key Points:\n1.\n2.\n3."""
        elif style == "role_based":
            prompt = f"""You are a journalist. Summarize the following text for a news article:\n
            {textwrap.fill(text, width=80)}\n
            News Summary:"""
        else:
            prompt = "Invalid summarization style selected."
        return prompt

    def qa_prompt(self, context, question, format="default"):
        """
        Generates different types of Question Answering prompts.
        """
        if format == "default":
            prompt = f"""Use the following context to answer the question:\n
            Context: {textwrap.fill(context, width=80)}\n
            Question: {question}\n
            Answer:"""
        elif format == "step_by_step":
            prompt = f"""Use logical reasoning to answer the question step by step:\n
            Context: {textwrap.fill(context, width=80)}\n
            Question: {question}\n
            Step-by-step explanation:\n1.\n2.\n3.\n\nFinal Answer:"""
        elif format == "bullet_points":
            prompt = f"""Answer in bullet points based on the given context:\n
            Context: {textwrap.fill(context, width=80)}\n
            Question: {question}\n
            Answer:\n- """
        elif format == "role_based":
            prompt = f"""You are a history professor. Answer the question in a detailed manner:\n
            Context: {textwrap.fill(context, width=80)}\n
            Question: {question}\n
            Explanation:"""
        else:
            prompt = "Invalid Q&A format selected."
        return prompt

    def get_gemini_response(self, prompt):
        """
        Calls Gemini API to generate a response based on the given prompt.
        """
        try:
            model = genai.GenerativeModel("gemini-pro")  # Using Gemini Pro Model
            response = model.generate_content(prompt)
            return response.text if response else "No response from model."
        except Exception as e:
            return f" Error calling Gemini API: {str(e)}"


# Interactive Execution for Testing Different Prompts
if __name__ == "__main__":
    nlp_exp = NLPExperiment()

    sample_text = """Artificial Intelligence (AI) is transforming industries such as healthcare, 
    finance, and education by automating tasks, enhancing decision-making, and improving efficiency."""

    print("\n🔹 Summarization Experiment")
    summary_style = input("Choose summary style (concise/detailed/key_points/role_based): ").strip()
    summary_prompt = nlp_exp.summarization_prompt(sample_text, summary_style)
    print("\n🔹 Generated Prompt:\n", summary_prompt)
    
    print("\n🔹 Gemini API Response:")
    print(nlp_exp.get_gemini_response(summary_prompt))

    print("\n🔹 Q&A Experiment")
    user_question = input("Enter your question: ").strip()
    qa_format = input("Choose Q&A format (default/step_by_step/bullet_points/role_based): ").strip()
    qa_prompt = nlp_exp.qa_prompt(sample_text, user_question, qa_format)
    print("\n🔹 Generated Prompt:\n", qa_prompt)

    print("\n🔹 Gemini API Response:")
    print(nlp_exp.get_gemini_response(qa_prompt))
