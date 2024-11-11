import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import OpenAI
from langchain_community.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize models with API keys and configurations
openai_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o", temperature=0.3)
llama_model = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.2-90b-text-preview")

def get_model(choice):
    """Returns the selected model instance."""
    if choice == "openai":
        return openai_model
    elif choice == "llama":
        return llama_model
    else:
        raise ValueError("Invalid choice. Please choose either 'openai' or 'llama'.")

if __name__ == "__main__":
    user_choice = input("Choose your model ('openai' or 'llama'): ").strip().lower()
    llm = get_model(user_choice)
    response = llm.invoke("Two most important ingredients in samosa are")
    print(response.content)
