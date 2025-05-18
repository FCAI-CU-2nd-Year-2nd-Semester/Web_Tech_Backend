// authorization.js
document.querySelector(".input-email").addEventListener("input", CheckInputEmail);

function CheckInputEmail() {
    const input = document.querySelector(".input-email");
    const errorMessage = document.querySelector(".error-message-email");
    const email = input.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email || emailRegex.test(email)) {
        errorMessage.style.display = "none";
    } else {
        errorMessage.style.display = "block";
        errorMessage.textContent = "Invalid email address";
    }
}

document.getElementById('loginButton').addEventListener('click', () => {
    const email = document.querySelector('.input-email').value.trim();
    const password = document.querySelector('.input-password').value;

    if (!email || !password) {
        return alert('Please fill in all fields.');
    }
    if (document.querySelector('.error-message-email').style.display !== 'none') {
        return alert('Please enter a valid email address.');
    }

    // Admin check
    if (email === 'admin@gmail.com') {
        if (password === 'Gmw$4321') {
            alert('Admin login successful!');
            return window.location.href = 'Walid_part/author.html';
        } else {
            return alert('Invalid admin password. Please try again.');
        }
    }

    // Regular user check
    const users = JSON.parse(localStorage.getItem('users')) || [];
    const user = users.find(u => u.email === email && u.password === password);

    if (user) {
        alert('Login successful!');
        window.location.href = 'Walid_part/index.html';
    } else {
        alert('Invalid email or password. Please try again.');
    }
});
