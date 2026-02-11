class DeepPracticalAgent(BaseAgent):
    """Designs hands‑on projects that learners can complete with minimal tools/materials."""
    
    def __init__(self):
        system_prompt = """You are a Deep Practical Agent.
        Create real‑world projects that a learner can do at home or in a local workshop.
        For dying trades, simulate the workflow using common substitutes if original tools are rare.
        Provide step‑by‑step instructions, estimated time, and a 'success criteria' checklist.
        """
        super().__init__("DeepPracticalAgent", system_prompt)

    def create_project(self, module_context: str, trade_type: str) -> dict:
        prompt = f"""
        Module context: {module_context}
        Trade type: {trade_type}
        
        Design a practical project that reinforces the module's skills.
        Make it achievable in under 2 hours with easily accessible supplies.
        Return JSON with fields: title, objective, materials, steps, success_criteria.
        """
        raw = self._call_llm(prompt)
        return eval(raw)  # simplified
