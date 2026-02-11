import { useEffect, useState } from 'react';
import CourseCard from '../components/CourseCard';

export default function Courses() {
  const [freeCourses, setFreeCourses] = useState([]);
  const [paidCourses, setPaidCourses] = useState([]);
  
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
