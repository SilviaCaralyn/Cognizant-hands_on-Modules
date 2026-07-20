import { useState } from 'react'

function StudentProfile() {
  const [profile, setProfile] = useState({ name: '', email: '', semester: '' })

  function handleChange(e) {
    const { name, value } = e.target
    setProfile((prev) => ({ ...prev, [name]: value }))
  }

  return (
    <section id="profile" aria-labelledby="profile-heading">
      <h2 id="profile-heading">Student Profile</h2>
      <form onSubmit={(e) => e.preventDefault()}>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" value={profile.name} onChange={handleChange} />

        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" value={profile.email} onChange={handleChange} />

        <label htmlFor="semester">Semester</label>
        <input id="semester" name="semester" type="number" min="1" max="8" value={profile.semester} onChange={handleChange} />
      </form>
      <p>Preview: {profile.name || '—'} | {profile.email || '—'} | Semester {profile.semester || '—'}</p>
    </section>
  )
}

export default StudentProfile
