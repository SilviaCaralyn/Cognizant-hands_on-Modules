import { courses } from "./data.js";


console.log(courses);

// Destructuring
courses.forEach(course => {
    const { name, credits } = course;
    console.log(`${name} - ${credits} credits`);
});

// map()
const formattedCourses = courses.map(
    course => `${course.code} — ${course.name} (${course.credits} credits)`
);

console.log(formattedCourses);

// filter()
const creditCourses = courses.filter(course => course.credits >= 4);

console.log(creditCourses);

console.log(`Number of courses with 4 or more credits: ${creditCourses.length}`);

// reduce()
const totalCredits = courses.reduce(
    (total, course) => total + course.credits,
    0
);

console.log(`Total Credits: ${totalCredits}`);




const courseGrid = document.querySelector(".course-grid");

courses.forEach(course => {

    const article = document.createElement("article");

    article.className = "course-card";

    article.innerHTML = `
        <h3>${course.name}</h3>
        <p>Course Code: ${course.code}</p>
        <span>Credits: ${course.credits}</span>
    `;

    courseGrid.appendChild(article);

});

const totalCreditsElement = document.querySelector("#total-credits");

const totalCreditsValue = courses.reduce(
    (total, course) => total + course.credits,
    0
);

totalCreditsElement.textContent = `Total Credits Enrolled: ${totalCreditsValue}`;
const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");

function renderCourses(courseList) {

    courseGrid.innerHTML = "";

    courseList.forEach(course => {

        const article = document.createElement("article");

        article.className = "course-card";

        article.dataset.id = course.id;

        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Course Code: ${course.code}</p>
            <span>Credits: ${course.credits}</span>
        `;

        courseGrid.appendChild(article);

    });

    const total = courseList.reduce(
        (sum, course) => sum + course.credits,
        0
    );

    totalCreditsElement.textContent =
        `Total Credits: ${total}`;
}

renderCourses(courses);
const sortBtn = document.querySelector("#sort-btn");

sortBtn.addEventListener("click", () => {

    const sortedCourses = [...courses];

    sortedCourses.sort((a, b) => b.credits - a.credits);

    renderCourses(sortedCourses);

});

const selectedCourse = document.querySelector("#selected-course");

courseGrid.addEventListener("click", (event) => {

    const clickedCard = event.target.closest(".course-card");

    if (!clickedCard) {
        return;
    }

    const courseId = Number(clickedCard.dataset.id);

    const selected = courses.find(course => course.id === courseId);

    selectedCourse.textContent =
        `Selected Course: ${selected.name} | Grade: ${selected.grade}`;

});