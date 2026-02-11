from backend.agents.quality_assurance import QualityAssuranceAgent
from backend.models.review import QualityReview
from backend.utils.quality_scorer import QualityScorer

class CourseGenerator:
    def __init__(self):
        self.idea_gen = CourseIdeaGenerator()
        self.course_creator = SyntheticIntelligence()
        self.qa_agent = QualityAssuranceAgent()
    
    async def generate_paid_courses(self, count: int = 30, 
                                   specific_ideas: List[Dict] = None) -> List[Dict]:
        """
        Generate paid courses. If specific_ideas is provided, use those;
        otherwise generate ideas per category.
        """
        all_courses = []
        
        if specific_ideas:
            ideas = specific_ideas
        else:
            # Normal weighted category generation
            categories = ['trending', 'traditional', 'rare', 'dying']
            weights = [0.4, 0.2, 0.2, 0.2]
            ideas = []
            for cat, weight in zip(categories, weights):
                cat_count = max(1, int(count * weight))
                cat_ideas = self.idea_gen.generate_ideas(cat, count=cat_count, is_free=False)
                ideas.extend(cat_ideas)
        
        for idea in ideas:
            # Determine module count
            import random
            module_count = random.randint(4, 8)
            
            blueprint = {
                "title": idea['title'],
                "description": idea['description'],
                "category": idea.get('category', 'trending'),
                "sub_category": idea.get('sub_category'),
                "tags": idea.get('tags', []),
                "target_audience": idea.get('target_audience', 'everyone'),
                "modules": self._generate_module_titles(module_count, idea['title']),
                "is_free": False
            }
            
            # Generate full course
            course = await self.course_creator.create_course(blueprint, short_mode=False)
            
            # Apply pricing
            prices = PricingCalculator.calculate(module_count)
            course['price_zar'] = prices['price_zar']
            course['price_usd'] = prices['price_usd']
            
            # ---- QUALITY ASSURANCE STEP ----
            review = await self.qa_agent.review_course(course)
            course['quality_review'] = review
            course['quality_score'] = review['overall_score']
            
            # Only publish if passes threshold
            course['is_published'] = review.get('pass_recommendation', False)
            
            # Save to DB (including review)
            db_course = self._save_course_with_review(course, review)
            
            if db_course.is_published:
                all_courses.append(db_course)
            else:
                # Log failure, possibly trigger re‑generation
                print(f"Course '{course['title']}' failed QA (score {review['overall_score']}). Not published.")
        
        return all_courses
    
    def _save_course_with_review(self, course_data: dict, review: dict):
        """Save course and its QA review."""
        db = SessionLocal()
        try:
            course = Course(
                title=course_data['title'],
                description=course_data['description'],
                category=course_data['category'],
                sub_category=course_data.get('sub_category'),
                tags=course_data.get('tags', []),
                is_free=False,
                price_zar=course_data['price_zar'],
                price_usd=course_data['price_usd'],
                quality_score=review['overall_score'],
                is_published=review.get('pass_recommendation', False)
            )
            db.add(course)
            db.flush()
            
            # Save review
            db_review = QualityReview(
                course_id=course.id,
                reviewer_agent="QualityAssuranceAgent",
                score=review['overall_score'],
                feedback=json.dumps(review),
                passed=review.get('pass_recommendation', False)
            )
            db.add(db_review)
            
            db.commit()
            db.refresh(course)
            return course
        finally:
            db.close()
