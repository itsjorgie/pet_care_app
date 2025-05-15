document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const name = form.querySelector("input[name='name']");
    const email = form.querySelector("input[name='email']");
    const password = form.querySelector("input[name='password']");
    const confirmPassword = form.querySelector("input[name='password_confirmation']");

    form.addEventListener("submit", function (e) {
        const nameRegex = /^[A-Za-z\s]{1,20}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Validate name
        if (!nameRegex.test(name.value)) {
            e.preventDefault();
            alert("Name must be letters and spaces only, and up to 20 characters.");
            name.focus();
            return;
        }

        // Validate email format
        if (!emailRegex.test(email.value)) {
            e.preventDefault();
            alert("Please enter a valid email format.");
            email.focus();
            return;
        }

        // Validate password match
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            alert("Passwords do not match.");
            confirmPassword.focus();
            return;
        }

        // Validate password length
        if (password.value.length > 20) {
            e.preventDefault();
            alert("Password must be up to 20 characters.");
            password.focus();
            return;
        }
    });
});
