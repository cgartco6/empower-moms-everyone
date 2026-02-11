import { useEffect, useState } from 'react';
import CourseCard from '../components/CourseCard';

export default function Courses() {
  const [freeCourses, setFreeCourses] = useState([]);
  const [paidCourses, setPaidCourses] = useState([]);
const [selectedCategory, setSelectedCategory] = useState('all');
const [selectedSubCategory, setSelectedSubCategory] = useState('all');

const categories = ['trending', 'traditional', 'rare', 'dying'];
const subCategories = {
  trending: ['trading', 'artificial intelligence', 'ecommerce', 'marketing', 'freelancing', 'cooking', 'sustainability'],
  // ... others
};

return (
  <div>
    <div className="filters">
      <select onChange={e => setSelectedCategory(e.target.value)}>
        <option value="all">All Categories</option>
        {categories.map(cat => <option key={cat}>{cat}</option>)}
      </select>
      {/* Dynamic subcategory dropdown */}
    </div>
    {/* Course grid */}
  </div>
);
  
  useEffect(() => {
    fetch('/api/v1/courses?is_free=true').then(res => res.json()).then(setFreeCourses);
    fetch('/api/v1/courses?is_free=false').then(res => res.json()).then(setPaidCourses);
  }, []);
  
  return (
    <div className="courses-page">
      <section className="free-courses">
        <h2>🎁 Try Before You Buy – Free Intro Courses</h2>
        <div className="course-grid">
          {freeCourses.map(course => (
            <CourseCard key={course.id} course={course} free={true} />
          ))}
        </div>
      </section>
      
      <section className="paid-courses">
        <h2>🔥 Full Courses – Start Earning Today</h2>
        <div className="course-grid">
          {paidCourses.map(course => (
            <CourseCard 
              key={course.id} 
              course={course} 
              priceZar={course.price_zar} 
              priceUsd={course.price_usd} 
            />
          ))}
        </div>
      </section>
    </div>
  );
}
