class InfluencerOutreachAgent(BaseAgent):
    def find_influencers(self, niche, min_followers=10000, max_followers=500000):
        # Use APIs (e.g., Heepsy, Upfluence) or manual search simulation
        return list_of_influencers
    
    def draft_outreach_email(self, influencer, offer):
        prompt = f"Write a personalised email to {influencer.name} offering a free course + commission..."
        return self._call_llm(prompt)
