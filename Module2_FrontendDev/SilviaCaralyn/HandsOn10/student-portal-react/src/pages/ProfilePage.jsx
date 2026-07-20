import { useSelector, useDispatch } from 'react-redux'
import { selectEnrolledCourses, unenroll } from '../store/enrollmentSlice.js'
import StudentProfile from '../components/StudentProfile.jsx'

function ProfilePage() {
  const enrolledCourses = useSelector(selectEnrolledCourses)
  const dispatch = useDispatch()

  return (
    <>
      <StudentProfile />

      <section aria-labelledby="enrolled-heading">
        <h2 id="enrolled-heading">Enrolled Courses ({enrolledCourses.length})</h2>
        {enrolledCourses.length === 0 && <p>No courses enrolled yet.</p>}
        <ul>
          {enrolledCourses.map((c) => (
            <li key={c.id}>
              {c.name} ({c.code}) — {c.credits} credits
              <button onClick={() => dispatch(unenroll(c.id))} style={{ marginLeft: '0.5rem' }}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}

export default ProfilePage
