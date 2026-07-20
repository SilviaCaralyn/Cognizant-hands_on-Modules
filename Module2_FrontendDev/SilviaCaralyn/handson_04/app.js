import { courses } from "./data.js";

// ========================================
// HANDS-ON 3
// ========================================

// Select Elements
const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortBtn = document.querySelector("#sort-btn");
const selectedCourse = document.querySelector("#selected-course");

// ----------------------------------------
// Render Courses
// ----------------------------------------

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

    const totalCredits = courseList.reduce(
        (sum, course) => sum + course.credits,
        0
    );

    totalCreditsElement.textContent =
        `Total Credits Enrolled: ${totalCredits}`;

}

// Initial Render
renderCourses(courses);

// ----------------------------------------
// Search Courses
// ----------------------------------------

searchInput.addEventListener("input", () => {

    const keyword = searchInput.value.toLowerCase();

    const filteredCourses = courses.filter(course =>
        course.name.toLowerCase().includes(keyword)
    );

    renderCourses(filteredCourses);

});



sortBtn.addEventListener("click", () => {

    const sortedCourses = [...courses];

    sortedCourses.sort((a, b) => b.credits - a.credits);

    renderCourses(sortedCourses);

});



courseGrid.addEventListener("click", (event) => {

    const card = event.target.closest(".course-card");

    if (!card) return;

    const id = Number(card.dataset.id);

    const course = courses.find(c => c.id === id);

    selectedCourse.textContent =
        `Selected Course: ${course.name} | Grade: ${course.grade}`;

});



function fetchUser(id) {

    return fetch(
        "https://jsonplaceholder.typicode.com/users/" + id
    )
        .then(response => response.json())
        .then(user => {

            console.log("User:", user.name);

        });

}

fetchUser(1);



async function fetchUserAsync(id) {

    try {

        const response = await fetch(
            "https://jsonplaceholder.typicode.com/users/" + id
        );

        const user = await response.json();

        console.log("Async User:", user.name);

    }

    catch (error) {

        console.error(error);

    }

}

fetchUserAsync(2);



function fetchAllCourses() {

    return new Promise(resolve => {

        setTimeout(() => {

            resolve(courses);

        }, 1000);

    });

}



async function loadCourses() {

    courseGrid.innerHTML = "<p>Loading courses...</p>";

    const data = await fetchAllCourses();

    renderCourses(data);

}

loadCourses();



Promise.all([

    fetch("https://jsonplaceholder.typicode.com/users/1")
        .then(res => res.json()),

    fetch("https://jsonplaceholder.typicode.com/users/2")
        .then(res => res.json())

])

.then(users => {

    console.log(users[0].name);

    console.log(users[1].name);

});


const loading = document.querySelector("#loading");
const notificationList = document.querySelector("#notification-list");
const errorMessage = document.querySelector("#error-message");
const retryBtn = document.querySelector("#retry-btn");



async function apiFetch(url) {

    const response = await fetch(url);

    if (!response.ok) {

        throw new Error("Failed to fetch data.");

    }

    return await response.json();

}



async function loadNotifications() {

    loading.style.display = "block";

    notificationList.innerHTML = "";

    errorMessage.textContent = "";

    retryBtn.style.display = "none";

    try {

        const posts = await apiFetch(
            "https://jsonplaceholder.typicode.com/posts?_limit=5"
        );

        loading.style.display = "none";

        posts.forEach(post => {

            const card = document.createElement("div");

            card.className = "notification-card";

            card.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.body}</p>
            `;

            notificationList.appendChild(card);

        });

    }

    catch (error) {

        loading.style.display = "none";

        errorMessage.textContent =
            "Unable to load notifications.";

        retryBtn.style.display = "inline-block";

    }

}

loadNotifications();



retryBtn.addEventListener("click", () => {

    loadNotifications();

});



async function axiosFetchPosts() {

    try {

        const response = await axios.get(
            "https://jsonplaceholder.typicode.com/posts",
            {
                params: {
                    userId: 1
                }
            }
        );

        console.log("Axios Posts");

        console.log(response.data);

    }

    catch (error) {

        console.log(error);

    }

}

axiosFetchPosts();



axios.interceptors.request.use(config => {

    console.log(
        "API call started:",
        config.url
    );

    return config;

});



console.log("Hands-On 4 Completed Successfully");