document.addEventListener("DOMContentLoaded", () => {
    const signUpBtn = document.getElementById("signUpBtn");

    if (signUpBtn) {
        signUpBtn.addEventListener("click", (event) => {
            event.preventDefault();
            transitionToPage("/signup");  // Adjust URL to your Flask route
        });
    }

    function transitionToPage(newContentUrl) {
        const container = document.getElementById('page-container');
        
        // Start fade-out transition
        container.classList.add('fade-out');

        // After transition ends, fetch new content
        container.addEventListener('transitionend', function onTransitionEnd() {
            // Remove the event listener after it is triggered
            container.removeEventListener('transitionend', onTransitionEnd);

            // Fetch new page content
            fetch(newContentUrl)
                .then(response => response.text())
                .then(html => {
                    // Replace container content with new content
                    container.innerHTML = html;

                    // Remove fade-out class and activate the new content
                    container.classList.remove('fade-out');
                    container.classList.add('active');

                    // Reapply animations to new content
                    initializeAnimations();
                });
        });
    }

    function initializeAnimations() {
        // Immediate header animations
        gsap.from(".header__content", {
            duration: 1.5,
            opacity: 0,
            y: 50,
            ease: "power3.out",
            delay: 1
        });

        // Initialize ScrollTrigger for info cards
        gsap.from(".info-card", {
            duration: 1.5,
            opacity: 0,
            y: 50,
            stagger: 0.3,
            ease: "power3.out",
            scrollTrigger: {
                trigger: ".info-section",
                start: "top 80%",
                end: "bottom 20%",
                scrub: true,
                markers: false // Set to true if you want to see the trigger markers for debugging
            }
        });

        // ScrollReveal settings for info section
        ScrollReveal().reveal(".header__image img", {
            distance: "50px",
            origin: "right",
            duration: 1000,
        });

        ScrollReveal().reveal(".header__content h1", {
            distance: "50px",
            origin: "bottom",
            duration: 1000,
            delay: 500,
        });

        ScrollReveal().reveal(".header__content p", {
            distance: "50px",
            origin: "bottom",
            duration: 1000,
            delay: 1000,
        });

        ScrollReveal().reveal(".header__content form", {
            distance: "50px",
            origin: "bottom",
            duration: 1000,
            delay: 1500,
        });

        ScrollReveal().reveal(".header__content .bar", {
            distance: "50px",
            origin: "bottom",
            duration: 1000,
            delay: 2000,
        });

        ScrollReveal().reveal(".header__image__card", {
            duration: 1000,
            interval: 500,
            delay: 2500,
        });
    }

    initializeAnimations();
});
