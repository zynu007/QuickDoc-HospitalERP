document.addEventListener('DOMContentLoaded', function() {t
    const form = document.getElementById('signup-form');
    
    form.addEventListener('submit', function(event) {
        // Get password and confirm password fields
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');
        
        // Check if passwords match
        if (password1.value !== password2.value) {
            // Prevent form submission
            event.preventDefault();
            alert('Passwords do not match!');
            // Clears password fields
            password1.value = '';
            password2.value = '';
        }
    });
});
