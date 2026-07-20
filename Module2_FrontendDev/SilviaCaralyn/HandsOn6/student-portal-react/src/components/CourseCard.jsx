function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  return (
    <article className="course-card" tabIndex={0}>
      <h3>{name}</h3>
      <p>{code} — {credits} credits</p>
      <span className="grade-badge">Grade: {grade}</span>
      {onEnroll && (
        <button onClick={() => onEnroll({ id, name, code, credits, grade })}>
          Enroll
        </button>
      )}
    </article>
  )
}

export default CourseCard
