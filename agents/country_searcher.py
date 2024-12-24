import json
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.google_search import search_country_wikipedia
from output_parsers.wikipedia import Wikipedia, wikipedia_parser

load_dotenv()


def get_country_wikipedia_url(name: str) -> Wikipedia:
    # llm = ChatOllama(model="llama3.2")
    # llm = ChatOllama(model="mistral")
    llm = ChatOllama(model="gemma2")

    template = """    
        Given the country name, I want you to find the Wikipedia URL for the specified country and provide the answer as a raw URL:

        URL: "<the URL>"

        Country: {country_name}

        {format_instructions}
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["country_name"],
        partial_variables={
            "format_instructions": wikipedia_parser.get_format_instructions()
        },
    )
    agent_tools = [
        Tool(
            name="Crawl Google by country page on Wikipedia",
            description="useful for when you need to search the country page on Wikipedia",
            func=search_country_wikipedia,
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=agent_tools, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=True,
        # handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(country_name=name)}
    )

    try:
        return wikipedia_parser.parse(result["output"])
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse output as Wikipedia object: {result['output']}"
        ) from e


if __name__ == "__main__":
    url = get_country_wikipedia_url(name="Brazil")
    print("AI Search result:")
    print(url)
