from langchain.agents import create_agent
from langchain.tools import tool #decorator
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url # from another file
# import requests # web scraping
# from bs4 import BeautifulSoup # web scraping
# from tavily import TavilyClient
# import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain


def run_research_pipeline(topic:str)->dict:
    state={}

    # searchAgent Working
    print("\n"+" ="*50)
    print("Step-1 - search agent is working")
    print("\n"+" ="*50)

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information about {topic}")]
    })

    state["search_results"]=search_result['messages'][-1].content

    print("\n search result ", state["search_results"])


    # step-2 reader agent
    print("\n"+" ="*50)
    print("Step-2 - reader agent is scraping top resources")
    print("\n"+" ="*50)

    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages":[(
            "user",
            f"Based on the following search results about {topic}, "
            f"pick the most relevant URL and scrape it for deeper content.\n\n,"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state["scraped_content"]=reader_result['messages'][-1].content

    print('\nscraped content \n',state["scraped_content"])

    # step - 3-> writer chain
    print("\n"+" ="*50)
    print("Step-3 - writer is drafting the report")
    print("\n"+" ="*50)

    research_combined=(
        f"SEARCH RESULTS : \n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT : \n{state['scraped_content']}\n\n"
    )

    state['report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n Final Report \n",state['report'])

    #critic report

    # step -4-> critic chain
    print("\n"+" ="*50)
    print("Step-4 - critic is reviewing the report")
    print("\n"+" ="*50)

    state['feedback']=critic_chain.invoke({
        "report":state['report']
    })

    print("\n Critic Report \n",state['feedback'])

    return state

if __name__=="__main__":
    topic=input("\n Enter a research Topic : ")
    run_research_pipeline(topic)

    