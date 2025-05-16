document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const email = form.email.value.trim();
        const password = form.password.value.trim();

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (email.length > 30) {
            alert("Email must not exceed 30 characters.");
            event.preventDefault();
            return;
        }

        if (!emailRegex.test(email)) {
            alert("Please enter a valid email format.");
            event.preventDefault();
            return;
        }

        if (password.length > 30) {
            alert("Password must not exceed 30 characters.");
            event.preventDefault();
            return;
        }
    });
});

