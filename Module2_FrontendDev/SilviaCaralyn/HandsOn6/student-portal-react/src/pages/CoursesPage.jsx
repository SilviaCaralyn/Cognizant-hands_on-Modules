import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import CourseCard from '../components/CourseCard.jsx'
import { courses as localCourses } from '../data/courses.js'
import { enroll } from '../store/enrollmentSlice.js'

function CoursesPage() {
  const [courses, setCourses] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const navigate = useNavigate()
  const dispatch = useDispatch()

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
        if (!res.ok) throw new Error(`Request failed with status ${res.status}`)
        const posts = await res.json()
        const mapped = posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS${100 + index}`,
          credits: localCourses[index % localCourses.length].credits,
          grade: localCourses[index % localCourses.length].grade,
        }))
        if (!cancelled) setCourses(mapped)
      } catch (err) {
        if (!cancelled) setError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const filtered = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  function handleEnroll(course) {
    dispatch(enroll(course))
    navigate('/profile') // Step 80: navigate to profile after enrolling
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
