document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const response = await fetch(
            "/api/users/login/",
            {
                method: "POST",

                credentials: "include",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: document.getElementById("email").value,
                    password: document.getElementById("password").value
                })
            }
        );

        if (response.ok) {

            window.location = "/";

        } else {

            const data = await response.json();

            document.getElementById("error").innerText =
                data.detail || "Wrong email or password.";
        }

    });

});