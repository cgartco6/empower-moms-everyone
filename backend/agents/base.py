from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from backend.config.settings import settings

class BaseAgent:
    """All agents inherit from this class."""
    def __init__(self, agent_name: str, system_prompt: str = ""):
        self.agent_name = agent_name
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.system_prompt = system_prompt

    def _call_llm(self, prompt: str, **kwargs) -> str:
        """Unified method to call the LLM with a formatted prompt."""
        formatted_prompt = prompt.format(**kwargs) if kwargs else prompt
        messages = [
            HumanMessage(content=f"{self.system_prompt}\n\n{formatted_prompt}")
        ]
        response = self.llm(messages)
        return response.content
