import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import CourseCard from '../components/CourseCard.jsx'
import {
  fetchAllCourses,
  enroll,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from '../store/enrollmentSlice.js'

function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const navigate = useNavigate()
  const dispatch = useDispatch()

  // Step 146: components read via selectors, never `state.enrollment.courses` directly
  const courses = useSelector(selectCourses)
  const loading = useSelector(selectCoursesLoading)
  const error = useSelector(selectCoursesError)

  // Step 145: dispatch the thunk — no direct API calls in the component
  useEffect(() => {
    dispatch(fetchAllCourses())
  }, [dispatch])

  const filtered = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  function handleEnroll(course) {
    dispatch(enroll(course))
    navigate('/profile')
  }

  return (
    <section id="courses" aria-labelledby="courses-heading">
      <h2 id="courses-heading">Courses</h2>

      <label htmlFor="search-courses">Search courses</label>
      <input
        id="search-courses"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      {loading && <p role="status">Loading...</p>}
      {error && <p role="alert">Error: {error}</p>}

      {!loading && !error && (
        <div className="course-grid">
          {filtered.map((course) => (
            <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
          ))}
        </div>
      )}
    </section>
  )
}

export default CoursesPage
