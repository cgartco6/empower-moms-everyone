# backend/agents/__init__.py
from backend.agents.strategic import StrategicIntelligenceAgent
from backend.agents.workflow import DeepWorkflowAgent
from backend.agents.deep_agents.content import DeepContentAgent
from backend.agents.deep_agents.video_script import DeepVideoScriptAgent
from backend.agents.deep_agents.quiz import DeepQuizAgent
from backend.agents.deep_agents.practical import DeepPracticalAgent
from backend.agents.deep_agents.localisation import DeepLocalisationAgent
from backend.agents.helpers.image_gen import ImageGeneratorHelper
from backend.agents.helpers.voiceover import VoiceoverHelper
from backend.agents.helpers.translator import TranslationHelper
from backend.agents.helpers.formatter import FormatterHelper
from backend.agents.course_idea_generator import CourseIdeaGenerator
from backend.agents.quality_assurance import QualityAssuranceAgent
from backend.agents.refund_prevention import RefundPreventionAgent

__all__ = [
    "StrategicIntelligenceAgent",
    "DeepWorkflowAgent",
    "DeepContentAgent",
    "DeepVideoScriptAgent",
    "DeepQuizAgent",
    "DeepPracticalAgent",
    "DeepLocalisationAgent",
    "ImageGeneratorHelper",
    "VoiceoverHelper",
    "TranslationHelper",
    "FormatterHelper",
    "CourseIdeaGenerator",
    "QualityAssuranceAgent",
    "RefundPreventionAgent",
]
