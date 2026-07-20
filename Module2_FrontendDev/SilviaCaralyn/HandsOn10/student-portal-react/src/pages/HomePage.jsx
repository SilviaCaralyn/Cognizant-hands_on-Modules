import { Link } from 'react-router-dom'

function HomePage() {
  return (
    <section id="hero">
      <h1>Welcome to the Student Portal</h1>
      <p>View your courses, track grades, and manage your profile — all in one place.</p>
      <Link to="/courses"><button>Explore Courses</button></Link>
    </section>
  )
}

export default HomePage
