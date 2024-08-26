document.addEventListener("DOMContentLoaded", () => {
    // Function to handle flash message fade-out
    function handleFlashMessages() {
        setTimeout(() => {
            const flashMessages = document.querySelectorAll('.flash-message-container .alert');
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500); // Ensure this matches the opacity transition duration
            });
        }, 3000); // Hides after 3 seconds
    }

    handleFlashMessages();

    // Add page transition class for entry
    document.body.classList.add('auth-enter');

    window.addEventListener('load', () => {
        // Remove entry class and add exit class after a short delay
        document.body.classList.remove('auth-enter');
        document.body.classList.add('auth-enter-active');
    });

    // Listen for transition end to clean up classes
    document.body.addEventListener('transitionend', () => {
        if (document.body.classList.contains('auth-exit')) {
            document.body.classList.remove('auth-exit', 'auth-exit-active');
        }
    });
});
