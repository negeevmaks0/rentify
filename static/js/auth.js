
async function checkAuth() {

    const navbar = document.getElementById("navbar");

    if (!navbar) {
        return;
    }

    const response = await fetch(
        "/api/users/profile/",
        {
            credentials: "include"
        }
    );

    if (response.ok) {

        const user = await response.json();

        navbar.innerHTML = `
            <a href="/" class="nav-link">Home</a>

            <a href="/profile/" class="nav-link">
                ${user.username}
            </a>

            <button
                id="logoutBtn"
                class="btn btn-outline-light ms-2">
                Logout
            </button>
        `;

        document
            .getElementById("logoutBtn")
            .addEventListener("click", logout);

    } else {

        navbar.innerHTML = `
            <a href="/login/" class="nav-link">
                Login
            </a>

            <a href="/register/" class="nav-link">
                Register
            </a>
        `;
    }
}


async function logout() {

    await fetch(
        "/api/users/logout/",
        {
            method: "POST",
            credentials: "include",
            headers:{
                "X-CSRFToken": getCookie("csrftoken")
            }
        }
    );

    window.location = "/";
}


document.addEventListener(
    "DOMContentLoaded",
    checkAuth
);