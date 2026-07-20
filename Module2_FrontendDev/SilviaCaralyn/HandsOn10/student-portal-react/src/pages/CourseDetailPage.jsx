import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { enroll } from '../store/enrollmentSlice.js'
import { courses as localCourses } from '../data/courses.js'

function CourseDetailPage() {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const [course, setCourse] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
        if (!res.ok) throw new Error('Course not found')
        const post = await res.json()
        const fallback = localCourses[(Number(courseId) - 1) % localCourses.length]
        if (!cancelled) {
          setCourse({
            id: post.id,
            name: post.title.slice(0, 30),
            code: `CS${100 + Number(courseId)}`,
            credits: fallback.credits,
            grade: fallback.grade,
          })
        }
      } catch {
        if (!cancelled) setCourse(null)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [courseId])

  if (loading) return <p role="status">Loading course...</p>
  if (!course) return <p role="alert">Course not found.</p>

  function handleEnroll() {
    dispatch(enroll(course))
    navigate('/profile')
  }

  return (
    <section aria-labelledby="detail-heading">
      <h2 id="detail-heading">{course.name}</h2>
      <p>{course.code} — {course.credits} credits</p>
      <p>Grade: {course.grade}</p>
      <button onClick={handleEnroll}>Enroll</button>
    </section>
  )
}

export default CourseDetailPage
