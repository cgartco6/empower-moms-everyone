import json
from pathlib import Path
from jinja2 import Template

class CourseAssembler:
    """Bundles all generated materials into a polished, downloadable course."""
    
    def assemble(self, blueprint, materials):
        # 1. Create HTML course pages
        html_template = Template(Path("templates/course_page.html").read_text())
        rendered_pages = []
        for module in blueprint.modules:
            module_materials = [m for m in materials if m['module_id'] == module.id]
            page = html_template.render(
                title=blueprint.title,
                module=module,
                lessons=module_materials
            )
            rendered_pages.append(page)
        
        # 2. Generate SCORM manifest if needed
        # 3. Zip everything
        # 4. Return download link
        return {
            "download_url": "/downloads/course_123.zip",
            "preview_html": rendered_pages[0]
        }
