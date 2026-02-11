# tests/agents/test_strategic.py
from backend.agents.strategic import StrategicIntelligenceAgent

def test_blueprint_creation():
    agent = StrategicIntelligenceAgent()
    blueprint = agent.create_blueprint("How to repair vintage sewing machines", "dying")
    assert blueprint.title is not None
    assert len(blueprint.modules) >= 5
