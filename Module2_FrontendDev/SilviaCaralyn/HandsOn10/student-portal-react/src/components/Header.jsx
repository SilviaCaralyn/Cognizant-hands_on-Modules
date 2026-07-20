import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectEnrolledCount } from '../store/enrollmentSlice.js'

function Header({ siteName }) {
  const enrolledCount = useSelector(selectEnrolledCount)

  return (
    <header className="site-header">
      <span className="site-title">{siteName}</span>
      <nav aria-label="Main navigation">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </nav>
      <span className="enrolled-count">Enrolled: {enrolledCount}</span>
    </header>
  )
}

export default Header
