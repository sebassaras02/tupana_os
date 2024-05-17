from chains.chain_generation import chain_coupling
from chains.llm_answering import llm_result
from safety.sentiment_analysis_filter import get_sentiment_analysis
from safety.prompt_injection_filter import get_prompt_injection_analysis

def main(): 
    chain = chain_coupling()
    k = 0
    while True:
        if k == 0:
            query = input("Hola soy un chatbot de la empresa E-Search ¿En qué puedo ayudarte?: ")
            k += 1
        else:
            query = input("¿Algo más en lo que pueda ayudarte?: ")
            k += 1
        if query == 'salir':
            break
        else:
            # apply the sentiment analysis filter
            sentiment = get_sentiment_analysis(query)
            prompt_injection = get_prompt_injection_analysis(query)
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
    main()