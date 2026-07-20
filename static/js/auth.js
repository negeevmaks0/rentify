async function checkAuth() {
    const navbar = document.getElementById("navbar");

    if (!navbar) {
        return;
    }

    try {
        const response = await fetch(
            "/api/users/profile/",
            {credentials: "include"}
        );

        if (response.ok) {
            const user = await response.json();

            let links = `
                <a href="/" class="nav-link">
                    Home
                </a>
            `;

            if(user.role === "tenant"){
                links += `
                    <a href="/properties/" class="nav-link">
                        Properties
                    </a>

                    <a href="/bookings/" class="nav-link">
                        My bookings
                    </a>
                `;
            }

            if(user.role === "landlord"){
                links += `
                    <a href="/properties/cabinet/" class="nav-link">
                        My Cabinet
                    </a>
                `;
            }

            links += `
                <a href="/profile/" class="nav-link">
                    ${user.username}
                </a>

                <button
                    id="logoutBtn"
                    class="btn btn-outline-light ms-2">
                    Logout
                </button>
            `;

            navbar.innerHTML = links;

            document
                .getElementById("logoutBtn")
                .addEventListener(
                    "click",
                    logout
                );

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

    } catch(error) {console.log(error);}
}



async function logout(){
    await fetch(
        "/api/users/logout/",
        {
            method:"POST",
            credentials:"include",
        }
    );

    window.location="/login/";
}


document.addEventListener(
    "DOMContentLoaded",
    checkAuth
);