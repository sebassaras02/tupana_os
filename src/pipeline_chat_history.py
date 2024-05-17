from chains.chain_generation import chain_coupling_with_memory
from chains.llm_answering import llm_result
from safety.sentiment_analysis_filter import get_sentiment_analysis
from safety.prompt_injection_filter import get_prompt_injection_analysis
import time
import asyncio

async def main(): 
    # measure the initilization time
    start = time.time()
    chain = await chain_coupling_with_memory()
    k = 0
    end = time.time()
    while True:
        if k == 0:
            print("Execution time needed", end - start, "seconds")
            query = input("Hola soy un chatbot de la empresa E-Search ¿En qué puedo ayudarte?: ")
            k += 1
        else:
            query = input("¿Algo más en lo que pueda ayudarte?: ")
            k += 1
        if query == 'salir':
            break
        else:
            # apply the sentiment analysis filter
            sentiment = 0
            prompt_injection = 0
            if sentiment == 1 and prompt_injection == 0:
                print("Lo siento, no puedo ayudarte con eso va en contra de los principios éticos en los que fui construido")
            elif prompt_injection == 1 and sentiment == 0:
                print("Lo siento, no puedo ayudarte con eso, se ha identificado como una amenza para mi funcionamiento como IA")
            elif prompt_injection == 1 and sentiment == 1:
                print("Lo siento, no puedo ayudarte con eso, la orden dada va en contra de los principios éticos en los que fui construido y se ha identificado como una amenza para mi funcionamiento como IA")
            else:
                res = llm_result(query, chain)
                print(res)
            
if __name__ == "__main__":
    asyncio.run(main())