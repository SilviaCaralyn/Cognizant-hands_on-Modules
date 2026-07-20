import { useState, useEffect } from "react";
import "./App.css";

import Header from "./components/Header";
import Footer from "./components/Footer";
import CourseCard from "./components/CourseCard";
import StudentProfile from "./components/StudentProfile";

function App() {

  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    async function fetchCourses() {

      try {

        setLoading(true);

        const response = await fetch(
          "https://jsonplaceholder.typicode.com/posts"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch courses");
        }

        const posts = await response.json();

        const mappedCourses = posts.slice(0, 5).map((post, index) => ({
          id: post.id,
          name: post.title,
          code: `CS10${index + 1}`,
          credits: index % 2 === 0 ? 4 : 3,
          grade: "A"
        }));

        setCourses(mappedCourses);

      } catch (err) {

        setError("Unable to load courses.");

      } finally {

        setLoading(false);

      }

    }

    fetchCourses();

  }, []);

  useEffect(() => {

    console.log("Courses updated");

  }, [courses]);

  function handleEnroll(course) {

    const exists = enrolledCourses.some(
      enrolled => enrolled.id === course.id
    );

    if (!exists) {

      setEnrolledCourses([
        ...enrolledCourses,
        course
      ]);

    }

  }
    const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header
        siteName="Student Portal"
        enrolledCount={enrolledCourses.length}
      />

      <div className="container">

        <input
          type="text"
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        {loading && <h3>Loading...</h3>}

        {error && <h3>{error}</h3>}

        {!loading && !error && (
          <div className="course-grid">
            {filteredCourses.map(course => (
              <CourseCard
                key={course.id}
                {...course}
                onEnroll={handleEnroll}
              />
            ))}
          </div>
        )}

        <StudentProfile />

      </div>

      <Footer />
    </>
  );

}

export default App;