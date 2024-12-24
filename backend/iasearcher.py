from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from dotenv import load_dotenv

from agents.country_searcher import get_country_wikipedia_url
from external.wikipedia_crawler import get_country_details
from output_parsers.summary import Summary, summary_parser


def ia_search_for(name: str) -> Summary:
    try:
        wikipedia = get_country_wikipedia_url(name)
        country_data = get_country_details(wikipedia.url)

        summary_template = """"
            Given the information {information} about a country, and using only provided information, I want you to create:
            1. a short summary
            2. flag url
            3. two interesting facts about it

            {format_instructions}
        """

        summary_prompt_template = PromptTemplate(
            input_variables=["information"],
            template=summary_template,
            partial_variables={
                "format_instructions": summary_parser.get_format_instructions()
            },
        )

        # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        # llm = ChatOllama(model="llama3.2")
        # llm = ChatOllama(model="mistral")
        llm = ChatOllama(model="gemma2")

        chain = summary_prompt_template | llm | summary_parser
        return chain.invoke(input={"information": country_data})
    except Exception as e:
        return None    

if __name__ == "__main__":
    load_dotenv()

    print("Starts AI Searcher")
    res = ia_search_for("Brazil")
    print(res)
