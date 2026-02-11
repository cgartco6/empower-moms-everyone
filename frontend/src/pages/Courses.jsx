// frontend/src/pages/Courses.jsx
import React, { useState, useEffect } from 'react';
import CourseCard from '../components/CourseCard';

export default function Courses() {
  const [freeCourses, setFreeCourses] = useState([]);
  const [paidCourses, setPaidCourses] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedSubCategory, setSelectedSubCategory] = useState('all');

  const categories = ['trending', 'traditional', 'rare', 'dying'];
  const subCategories = {
    trending: ['trading', 'artificial intelligence', 'ecommerce', 'marketing', 'freelancing', 'cooking', 'sustainability'],
    traditional: ['carpentry', 'sewing', 'baking', 'plumbing'],
    rare: ['bookbinding', 'blacksmithing', 'stained glass', 'leatherworking'],
    dying: ['wheelwright', 'hand-loom weaving', 'letterpress', 'cooper']
  };

  useEffect(() => {
    fetch('/api/v1/courses?is_free=true')
      .then(res => res.json())
      .then(setFreeCourses);
    fetch('/api/v1/courses?is_free=false')
      .then(res => res.json())
      .then(setPaidCourses);
  }, []);

  const filterCourses = (courses) => {
    return courses.filter(course => {
      if (selectedCategory !== 'all' && course.category !== selectedCategory) return false;
      if (selectedSubCategory !== 'all' && course.sub_category !== selectedSubCategory) return false;
      return true;
    });
  };

  return (
    <div className="courses-page">
      <section className="filters">
        <h2>Browse Courses</h2>
        <div className="filter-group">
          <label>Category</label>
          <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}>
            <option value="all">All Categories</option>
            {categories.map(cat => <option key={cat}>{cat}</option>)}
          </select>
        </div>
        {selectedCategory !== 'all' && (
          <div className="filter-group">
            <label>Sub‑category</label>
            <select value={selectedSubCategory} onChange={e => setSelectedSubCategory(e.target.value)}>
              <option value="all">All Sub‑categories</option>
              {subCategories[selectedCategory]?.map(sub => <option key={sub}>{sub}</option>)}
            </select>
          </div>
        )}
      </section>

      <section className="free-courses">
        <h2>🎁 Try Before You Buy – Free Intro Courses</h2>
        <div className="course-grid">
          {filterCourses(freeCourses).map(course => (
            <CourseCard key={course.id} course={course} free={true} />
          ))}
        </div>
      </section>

      <section className="paid-courses">
        <h2>🔥 Full Courses – Start Earning Today</h2>
        <div className="course-grid">
          {filterCourses(paidCourses).map(course => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      </section>
    </div>
  );
}
