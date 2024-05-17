from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple


ethical_principle = ConstitutionalPrinciple(
    name="Principio Ético",
    critique_request="El modelo debe obligatoriamente solo hablar acerca de cosas de forma ética y justa.",
    revision_request="Reescribe la salida del modelo para que sea ética y justa en caso de que la respuesta no sea apropiada en términos éticos y justos.",
)
