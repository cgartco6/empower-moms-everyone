# backend/orchestrator/synthetic_intelligence.py
from typing import Dict, Any
from backend.agents.strategic import StrategicIntelligenceAgent
from backend.agents.workflow import DeepWorkflowAgent
from backend.agents.deep_agents.content import DeepContentAgent
from backend.agents.deep_agents.video_script import DeepVideoScriptAgent
from backend.agents.deep_agents.quiz import DeepQuizAgent
from backend.agents.deep_agents.practical import DeepPracticalAgent
from backend.agents.helpers.image_gen import ImageGeneratorHelper
from backend.services.course_assembly import CourseAssembler

class SyntheticIntelligence:
    """Main orchestrator – creates full courses or short intros."""

    def __init__(self):
        self.strategic = StrategicIntelligenceAgent()
        self.workflow = DeepWorkflowAgent()
        self.content_agent = DeepContentAgent()
        self.video_agent = DeepVideoScriptAgent()
        self.quiz_agent = DeepQuizAgent()
        self.practical_agent = DeepPracticalAgent()
        self.image_helper = ImageGeneratorHelper()
        # ... other agents

    async def create_course(self, blueprint: Dict[str, Any], short_mode: bool = False) -> Dict:
        """Generate a complete course with all materials."""
        # 1. If no blueprint.modules, use strategic agent
        if not blueprint.get('modules'):
            bp = self.strategic.create_blueprint(
                blueprint.get('idea', blueprint.get('title')),
                blueprint.get('category', 'trending')
            )
            blueprint['modules'] = bp.dict().get('modules', [])

        # 2. Short mode: keep only first module, limit lessons
        if short_mode:
            blueprint['modules'] = blueprint['modules'][:1]
            for mod in blueprint['modules']:
                mod['lesson_count'] = 3

        # 3. Decompose into tasks
        tasks = self.workflow.decompose_blueprint(blueprint)

        # 4. Execute tasks (simplified – parallel in real impl)
        course_materials = []
        for task in tasks:
            if task.agent_type == "content":
                material = self.content_agent.write_lesson(**task.params)
            elif task.agent_type == "video_script":
                material = self.video_agent.create_script(**task.params)
            elif task.agent_type == "quiz":
                material = self.quiz_agent.create_quiz(**task.params)
            elif task.agent_type == "practical":
                material = self.practical_agent.create_project(**task.params)
            else:
                material = {}
            course_materials.append(material)

        # 5. Enhance with helpers (images, etc.)
        for material in course_materials:
            if material.get('need_image'):
                img_url = await self.image_helper.generate(material['image_prompt'])
                material['image_url'] = img_url

        # 6. Assemble final structure
        assembler = CourseAssembler()
        final_course = assembler.assemble(blueprint, course_materials)
        return final_course
