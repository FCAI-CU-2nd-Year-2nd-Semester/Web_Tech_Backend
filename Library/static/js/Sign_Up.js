// Sign_Up.js
document.getElementById('registerButton').addEventListener('click', () => {
    const email = document.querySelector('.input-email').value.trim();
    const password = document.querySelector('.input-status-update').value;
    const confirmPassword = document.querySelector('.input-status-confirm').value;

    if (!email || !password) {
        return alert('Please fill all fields.');
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return alert('Please enter a valid email address.');
    }

    if (password !== confirmPassword) {
        return alert('Passwords do not match!');
    }

    let users = JSON.parse(localStorage.getItem('users')) || [];

    if (users.some(u => u.email === email)) {
        return alert('Email is already registered.');
    }
    users.push({ email, password });
    localStorage.setItem('users', JSON.stringify(users));

    alert('Registered successfully! You can now log in.');
    window.location.href = 'login.html';
});
