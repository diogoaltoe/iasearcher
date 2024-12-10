from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import os

from dotenv import load_dotenv

information = """"
Ayrton Senna da Silva; 21 March 1960 – 1 May 1994) was a Brazilian racing driver, who competed in Formula One from 1984 to 1994. Senna won three Formula One World Drivers' Championship titles with McLaren, and—at the time of his death—held the record for most pole positions (65), among others; he won 41 Grands Prix across 11 seasons.

Born and raised in São Paulo, Senna began competitive kart racing aged 13; his first go-kart was built by his father using a lawnmower engine. After twice finishing runner-up at the Karting World Championship, Senna progressed to Formula Ford in 1981, dominating the British and European championships in his debut seasons. He then won the 1983 British Formula Three Championship amidst a close title battle with Martin Brundle, further winning the Macau Grand Prix that year. Senna signed for Toleman in 1984, making his Formula One debut at the Brazilian Grand Prix. After scoring several podium finishes in his rookie season, Senna moved to Lotus in 1985 to replace Nigel Mansell, taking his maiden pole position and victory at the rain-affected Portuguese Grand Prix, a feat he repeated in Belgium. He remained at Lotus for his 1986 and 1987 campaigns, scoring multiple wins in each and finishing third in the latter World Drivers' Championship.

Senna signed for McLaren in 1988 to partner Alain Prost; together, they won 15 of 16 Grands Prix held that season—driving the Honda-powered MP4/4—with Senna taking his maiden championship by three points after winning a then-record eight Grands Prix.[b] Their fierce rivalry culminated in title-deciding collisions at Suzuka in 1989 and 1990, despite Prost's move to Ferrari in the latter, with Prost winning the former title and Senna taking the following. Senna took seven victories, including his home Grand Prix in Brazil, as he secured his third title in 1991. The dominant Williams-Renault combination prevailed throughout his remaining two seasons at McLaren, with Senna achieving several race wins in each, including his record-breaking sixth Monaco Grand Prix victory in 1993 on his way to again finishing runner-up to Prost in the championship. Senna negotiated a move to Williams for his 1994 campaign, replacing the retired Prost to partner Damon Hill.
"""

if __name__ == "__main__":
    load_dotenv()

    print("hello LangChain")

    summary_template = """"
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": information})

    print(res)
