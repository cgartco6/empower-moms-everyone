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
    """Main orchestrator – spawns agents, manages the whole course creation pipeline."""
    
    def __init__(self):
        self.strategic = StrategicIntelligenceAgent()
        self.workflow = DeepWorkflowAgent()
        self.content_agent = DeepContentAgent()
        self.video_agent = DeepVideoScriptAgent()
        self.quiz_agent = DeepQuizAgent()
        self.practical_agent = DeepPracticalAgent()
        self.image_helper = ImageGeneratorHelper()
        # ... other agents and helpers

    async def create_course(self, request: Dict[str, Any]):
        # 1. Strategic planning
        blueprint = self.strategic.create_blueprint(
            request['idea'], 
            request['category']
        )
        
        # 2. Workflow decomposition
        tasks = self.workflow.decompose_blueprint(blueprint.dict())
        
        # 3. Execute tasks in parallel (simplified sequential)
        course_materials = []
        for task in tasks:
            if task.agent_type == "content":
                material = self.content_agent.write_lesson(**task.params)
            elif task.agent_type == "practical":
                material = self.practical_agent.create_project(**task.params)
            # ... other agent assignments
            
            course_materials.append(material)
        
        # 4. Enhance with helpers (generate images, voiceovers, etc.)
        for material in course_materials:
            if "need_image" in material:
                image_url = self.image_helper.generate(material['image_prompt'])
                material['image'] = image_url
        
        # 5. Assemble final course package (HTML, SCORM, video)
        assembler = CourseAssembler()
        final_course = assembler.assemble(blueprint, course_materials)
        
        return final_course
