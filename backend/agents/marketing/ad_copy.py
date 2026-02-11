class AdCopyAgent(BaseAgent):
    def generate_ad_variants(self, course_title, audience, platform):
        prompt = f"""
        Create 5 high‑converting Facebook/Instagram ad copies for:
        Course: {course_title}
        Target audience: {audience}
        Platform: {platform}
        
        Each copy must include:
        - Hook (first 3 seconds attention grabber)
        - Pain point
        - Solution (the course)
        - Clear call‑to‑action
        """
        return self._call_llm(prompt)
