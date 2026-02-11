// frontend/src/components/CourseCard.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function CourseCard({ course, free = false }) {
  // In a real app, get user's preferred currency from context/geolocation
  const currency = 'ZAR'; // or 'USD'
  const price = course[`price_${currency.toLowerCase()}`];

  return (
    <div className="course-card">
      <div className="course-image">
        <img src={course.thumbnail || '/default-course.jpg'} alt={course.title} />
      </div>
      <div className="course-info">
        <h3>{course.title}</h3>
        <p className="description">{course.description}</p>
        <div className="tags">
          {course.tags?.map(tag => <span key={tag} className="tag">{tag}</span>)}
        </div>
        <div className="meta">
          <span className="category">{course.category}</span>
          {course.sub_category && <span className="sub-category">{course.sub_category}</span>}
        </div>
        <div className="price">
          {free ? (
            <span className="free">FREE</span>
          ) : (
            <span className="paid">{currency} {price}</span>
          )}
        </div>
        <Link to={`/courses/${course.id}`} className="btn-view">View Course</Link>
      </div>
    </div>
  );
}
