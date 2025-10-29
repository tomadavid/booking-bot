from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from parser import Output
from datetime import datetime
from modules import schedule_event
import os

"""
    Orchestrator -> LLM decides the nature of the request (scheduling/canceling/rescheduling)
    Program's flow follows according to the type of request

    Makes use of an output parser to limit the LLM's response solely to the 
    booking system's functionality
"""

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def orchestrator(query):

    # LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    # Output parser
    parser = PydanticOutputParser(pydantic_object=Output)

    # prompt instructions (limit as much the LLM)
    prompt = PromptTemplate(
        template=(
        "You are an assistant that extracts scheduling intents from text.\n\n"
                "User message: {query}\n\n"
                "Return ONLY valid JSON with the following structure:\n"
                "{format_instructions}\n\n"
                "If the user wants to schedule something, set schedule=true.\n"
                "If the user wants to cancel something, set cancel=true.\n"
                "If not applicable, set schedule=false or cancel=false.\n"
                "Fill schedule_datetime or cancel_datetime when possible in ISO format (YYYY-MM-DDTHH:MM:SS).\n" \
                "If no year is specified, the year is the current. Here is the current time: {current_time}\n"
                "Classify the request as invalid if the request does not fulfill the needs of booking/cancelation"
            ),
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions(), 
                           "current_time": datetime.now().isoformat()}
    )

    # generate LLM response
    chain = prompt | llm | parser
    output = chain.invoke({"query": query})

    # for out-of-context requests
    if output.invalid_request == True:
        return "Sorry, I did not understand :(\nPlease write something like this:\n\nI want to <Book/Cancel> my appointment for 11th September 2001"

    # rescheduling
    #if output.schedule == True and output.cancel == True:
        #return rescedule_event(output)
    
    # scheduling
    if output.schedule == True:
        return schedule_event(output)
    
    # canceling
    #if output.cancel == True:
        #return cancel_event(output)
