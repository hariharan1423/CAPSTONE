document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const errorMessages = document.getElementById('errorMessages');
    errorMessages.innerHTML = ''; 

    let valid = true;

    
    if (username.length < 3) {
        valid = false;
        errorMessages.innerHTML += '<p>Username must be at least 3 characters long.</p>';
    }

    
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!emailPattern.test(email)) {
        valid = false;
        errorMessages.innerHTML += '<p>Please enter a valid email address.</p>';
    }

    
    if (password.length < 6) {
        valid = false;
        errorMessages.innerHTML += '<p>Password must be at least 6 characters long.</p>';
    }

    
    if (password !== confirmPassword) {
        valid = false;
        errorMessages.innerHTML += '<p>Passwords do not match.</p>';
    }

    
    if (valid) {
        alert('Registration successful!');
        
        document.getElementById('signupForm').reset();
    }
});
