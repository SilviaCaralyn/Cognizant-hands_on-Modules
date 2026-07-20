import { useState } from "react";

function StudentProfile() {

  const [student, setStudent] = useState({
    name: "",
    email: "",
    semester: ""
  });

  function handleChange(event) {

    const { name, value } = event.target;

    setStudent({
      ...student,
      [name]: value
    });

  }

  return (

    <div className="student-profile">

      <h2>Student Profile</h2>

      <input
        type="text"
        name="name"
        placeholder="Enter Name"
        value={student.name}
        onChange={handleChange}
      />

      <input
        type="email"
        name="email"
        placeholder="Enter Email"
        value={student.email}
        onChange={handleChange}
      />

      <input
        type="text"
        name="semester"
        placeholder="Enter Semester"
        value={student.semester}
        onChange={handleChange}
      />

      <h3>Profile Preview</h3>

      <p><strong>Name:</strong> {student.name}</p>

      <p><strong>Email:</strong> {student.email}</p>

      <p><strong>Semester:</strong> {student.semester}</p>

    </div>

  );

}

export default StudentProfile;