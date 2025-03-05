document.addEventListener('DOMContentLoaded', function() {
    const userTypeField = document.querySelector('select[name="user_type"]');
    const specialtyField = document.querySelector('select[name="specialty"]');
    const specialtyContainer = specialtyField.closest('.form-group') || specialtyField.parentElement;

    //Initially hide the specialty field
    specialtyContainer.style.display = 'none';

    userTypeField.addEventListener('change', function() {
        //show specialty field only when 'doctor' is selected
        if (this.value === 'doctor') {
            specialtyContainer.style.display = 'block';
            // specialty required when doctor is selected
            specialtyField.setAttribute('required', 'required');
        } else {
            specialtyContainer.style.display = 'none';
            // Remove required attribute when not a doctor
            specialtyField.removeAttribute('required');
        }
    });
});