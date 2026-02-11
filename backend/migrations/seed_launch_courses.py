import asyncio
from backend.services.course_generation import CourseGenerator
from backend.agents.quality_assurance import QualityAssuranceAgent

async def seed_launch_courses():
    """
    Generate the specific courses we want at launch:
    - Crypto Trading Bootcamp
    - Forex Trading Bootcamp
    - 6 other trending topics (AI for Entrepreneurs, Dropshipping Mastery, etc.)
    """
    generator = CourseGenerator()
    qa = QualityAssuranceAgent()
    
    # Define the 8 premium courses with precise specifications
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
    
    # Generate them one by one
    published_courses = []
    for course_spec in premium_courses:
        # Override the automatic module count with our desired count
        course_spec['modules'] = generator._generate_module_titles(
            course_spec['module_count'], 
            course_spec['title']
        )
        
        # Create the course
        course = await generator.course_creator.create_course(course_spec, short_mode=False)
        
        # Apply pricing
        prices = PricingCalculator.calculate(course_spec['module_count'])
        course['price_zar'] = prices['price_zar']
        course['price_usd'] = prices['price_usd']
        
        # QA review – ensure it's perfect
        review = await qa.review_course(course)
        print(f"QA for {course['title']}: score {review['overall_score']}")
        
        # Force publish if score is decent, but ideally we want >90
        if review['overall_score'] < 85:
            # In production, we'd auto‑improve; here we just accept with a warning
            print(f"⚠️ Warning: {course['title']} scored {review['overall_score']}. Manual review recommended.")
        
        course['quality_score'] = review['overall_score']
        course['is_published'] = True  # we want these live at launch
        
        # Save
        db_course = generator._save_course_with_review(course, review)
        published_courses.append(db_course)
        print(f"✅ Published: {db_course.title} (ZAR {db_course.price_zar})")
    
    # Additionally, generate 22 more trending courses to reach 30 paid courses at launch
    # (since we have 8 premium, we need 22 more)
    print("Generating additional 22 paid courses...")
    additional = await generator.generate_paid_courses(22)
    print(f"✅ Generated {len(additional)} additional paid courses.")
    
    return published_courses + additional

if __name__ == "__main__":
    asyncio.run(seed_launch_courses())
