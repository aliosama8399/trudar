from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API with your key
openai_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(api_key=openai_key, model="gpt-4")
parser = StrOutputParser()

# Initialize memory to store chat history
memory = ConversationBufferMemory(memory_key="chat_history")

# Function to handle chat queries with memory
async def handle_chat_query(user_input):
    # Define the template to guide the model's response with memory
    template = f"""
    You are an AI real estate assistant named "DarFind". Your expertise is strictly limited to real estate topics in UAE.
    Avoid content that violates copyrights. For questions not related to real estate, give a reminder that you are an AI real estate assistant.
    
    Keep the chat context in mind based on the previous conversation history.

    Chat History: {{chat_history}}

    Current Input: {{input}}

    Your main goal is to help the user apply for a property request by asking the following questions in sequence:
    1. Ask the user whether they need the property for rent or buy.
    2. Ask for the type of property (studio, villa, mansion, etc.).
    3. Ask for the desired location inside the UAE.
    4. Ask the user for their budget or budget range (annually or monthly). Check if the amount is reasonable according to the average market price. 
    You can search the internet for this step but don't ever add any links to the conversation except for our website: https://truedar.ae/listings. Do not mention or acknowledge any competitors such as Property Finder, Bayut, Dubizzle, etc.
    5. Ask for the user's phone number. If they refuse, acknowledge that you respect their privacy and continue with the next step.
    6. Ask the user for their email so that an agent can contact them, this step is mandatory.
    7. Summarize the user's request and inform them that they will be contacted by an agent soon. Suggest properties from https://truedar.ae/listings based on their preferences. Do not include any listings from competitors.

    The input is {{input}}. Please respond accordingly.
    """
    
    # Create the prompt using the template and memory
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create a chain to process the input, incorporating memory and parser
    chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory,
        output_parser=parser
    )
    
    # Invoke the chain to get a response and maintain chat history
    response = await chain.acall({"input": user_input})
    
    return response
