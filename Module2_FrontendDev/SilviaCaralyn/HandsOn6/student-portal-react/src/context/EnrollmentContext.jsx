/**
 * HANDS-ON 6 - Task 2: Context API for global state.
 *
 * NOTE: This context demonstrates the Task 2 pattern (prop-drilling-free
 * global state via createContext + useContext). The final app in this
 * project (Task 3) uses Redux Toolkit instead — see src/store/. Both
 * approaches solve the same problem; Redux is more scalable as state
 * complexity grows, which is why the app migrates to it in Task 3.
 * Swap <EnrollmentProvider> back into main.jsx if you want to run the
 * Context-only version instead of the Redux version.
 */
import { createContext, useState, useContext } from 'react'

export const EnrollmentContext = createContext(null)

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([])

  function enroll(course) {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    )
  }

  function remove(courseId) {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId))
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enroll, remove }}>
      {children}
    </EnrollmentContext.Provider>
  )
}

export function useEnrollment() {
  return useContext(EnrollmentContext)
}
