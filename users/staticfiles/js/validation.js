// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the signup form element
    const form = document.getElementById('signup-form');
    
    // Add submit event listener to the form
    form.addEventListener('submit', function(event) {
        // Get password and confirm password fields
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');
        
        // Check if passwords match
        if (password1.value !== password2.value) {
            // Prevent form submission
            event.preventDefault();
            // Show error message
            alert('Passwords do not match!');
            // Clear password fields
            password1.value = '';
            password2.value = '';
        }
    });
});