from backend.agents.base import BaseAgent

class DeepContentAgent(BaseAgent):
    """Generates rich, easy‑to‑understand lesson content with mnemonics and real‑world examples."""
    
    def __init__(self):
        system_prompt = """You are a Deep Content Agent specialised in writing course lessons.
        Your content must be:
        - Very easy to understand (8th‑grade level)
        - Memorable: use analogies, stories, rhymes, or acronyms
        - Practical: include "Try it now" micro‑exercises
        """
        super().__init__("DeepContentAgent", system_prompt)

    def write_lesson(self, module_title: str, lesson_title: str, learning_goal: str) -> str:
        prompt = f"""
        Module: {module_title}
        Lesson: {lesson_title}
        Learning goal: {learning_goal}
        
        Write the full lesson content (about 500 words). 
        Include a 'Fun Fact' sidebar, a mnemonic, and a 2‑minute practical activity.
        """
        return self._call_llm(prompt)
