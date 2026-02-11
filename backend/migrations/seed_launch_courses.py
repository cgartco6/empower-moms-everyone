# backend/migrations/seed_launch_courses.py
import asyncio
from backend.services.course_generation import CourseGenerator
from backend.services.pricing.calculator import PricingCalculator
from backend.agents.quality_assurance import QualityAssuranceAgent

async def seed_launch_courses():
    """Generate the specific courses we want at launch."""
    generator = CourseGenerator()
    qa = QualityAssuranceAgent()

    premium_courses = [
        {
            "title": "Crypto Trading Bootcamp: From Zero to Consistent Profits",
            "description": "Master Bitcoin, Ethereum, and altcoin trading. Learn technical analysis, risk management, and how to automate your trades.",
            "category": "trending",
            "sub_category": "trading",
            "tags": ["crypto", "bitcoin", "trading", "investing"],
            "target_audience": "Complete beginners with no trading experience",
            "module_count": 8
        },
        {
            "title": "Forex Trading Bootcamp: Master the World's Largest Market",
            "description": "Trade currencies like a pro. Understand pips, leverage, fundamental analysis, and build a profitable forex strategy.",
            "category": "trending",
            "sub_category": "trading",
            "tags": ["forex", "currency trading", "FX"],
            "target_audience": "Aspiring forex traders",
            "module_count": 8
        },
        {
            "title": "AI for Entrepreneurs: Build No‑Code Apps & Automate Your Business",
            "description": "Leverage ChatGPT, Midjourney, and Zapier to create products, marketing, and customer service – without writing code.",
            "category": "trending",
            "sub_category": "artificial intelligence",
            "tags": ["AI", "no-code", "automation"],
            "target_audience": "Business owners, moms, solopreneurs",
            "module_count": 6
        },
        {
            "title": "Dropshipping Mastery: Build a 6‑Figure Store in 90 Days",
            "description": "From product research to Facebook ads. Real case studies and actionable checklists.",
            "category": "trending",
            "sub_category": "ecommerce",
            "tags": ["dropshipping", "shopify", "ecommerce"],
            "target_audience": "Aspiring ecommerce sellers",
            "module_count": 7
        },
        {
            "title": "Zero‑Waste Living: Practical Steps for a Sustainable Home",
            "description": "Reduce your carbon footprint, save money, and create eco‑friendly products yourself.",
            "category": "trending",
            "sub_category": "sustainability",
            "tags": ["eco", "zero waste", "green"],
            "target_audience": "Environmentally conscious individuals",
            "module_count": 5
        },
        {
            "title": "Social Media Marketing for Small Businesses",
            "description": "Grow your audience on Instagram, TikTok, and Pinterest without a big budget.",
            "category": "trending",
            "sub_category": "marketing",
            "tags": ["social media", "marketing"],
            "target_audience": "Small business owners",
            "module_count": 6
        },
        {
            "title": "Freelancing on Upwork & Fiverr: From Zero to First $5,000",
            "description": "Create a winning profile, write proposals that get hired, and build long‑term client relationships.",
            "category": "trending",
            "sub_category": "freelancing",
            "tags": ["freelance", "upwork", "fiverr"],
            "target_audience": "Beginners in freelancing",
            "module_count": 5
        },
        {
            "title": "Plant‑Based Cooking: Delicious Meals Anyone Can Make",
            "description": "Easy, affordable vegan recipes for families. Includes meal prep and grocery hacks.",
            "category": "trending",
            "sub_category": "cooking",
            "tags": ["vegan", "cooking", "healthy"],
            "target_audience": "Busy moms, health enthusiasts",
            "module_count": 5
        }
    ]

    published = []
    for spec in premium_courses:
        # Generate module structure (the AI will replace with real content)
        spec['modules'] = generator._generate_module_titles(spec['module_count'], spec['title'])
        # Create the course (AI generation)
        course_data = await generator.course_creator.create_course(spec, short_mode=False)
        # Apply pricing
        prices = PricingCalculator.calculate(spec['module_count'])
        course_data['price_zar'] = prices['price_zar']
        course_data['price_usd'] = prices['price_usd']
        # QA review
        review = await qa.review_course(course_data)
        print(f"QA for {course_data['title']}: {review['overall_score']}")
        course_data['quality_score'] = review['overall_score']
        course_data['is_published'] = True  # Force publish for launch
        db_course = generator._save_course_with_review(course_data, review)
        published.append(db_course)
        print(f"✅ Published: {db_course.title} (ZAR {db_course.price_zar})")

    # Generate additional 22 paid courses to reach 30 total
    print("Generating additional 22 paid courses...")
    additional = await generator.generate_paid_courses(22)
    print(f"✅ Generated {len(additional)} additional paid courses.")
    return published + additional

if __name__ == "__main__":
    asyncio.run(seed_launch_courses())
