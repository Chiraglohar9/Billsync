document.addEventListener("DOMContentLoaded", function () {
    
    // Smooth Scrolling for Navbar Links
    document.querySelectorAll("nav ul li a").forEach(anchor => {
        anchor.addEventListener("click", function (event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: "smooth"
                });
            }
        });
    });

    // Contact Form Validation
    const contactForm = document.querySelector(".contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let name = contactForm.querySelector("input[type='text']").value.trim();
            let email = contactForm.querySelector("input[type='email']").value.trim();
            let message = contactForm.querySelector("textarea").value.trim();

            if (name === "" || email === "" || message === "") {
                alert("Please fill in all fields.");
                return;
            }

            if (!validateEmail(email)) {
                alert("Please enter a valid email address.");
                return;
            }

            alert("Message sent successfully!");
            contactForm.reset();
        });
    }

    // Email Validation Function
    function validateEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

});
