document.addEventListener("DOMContentLoaded", () => {
    const signUpBtn = document.getElementById("GetStarted"); // Corrected ID

    if (signUpBtn) {
        console.log('Get Started button found'); // Debugging line
        signUpBtn.addEventListener("click", (event) => {
            event.preventDefault();
            window.location.href = "/signup";  // Adjust URL to your Flask route
        });
    } else {
        console.error('Get Started button not found'); // Debugging line
    }
});
