
document.querySelector(".input-status-update").addEventListener("input", () => {
    checkInput();
    updateStatusBar();
    showIcon();
});

function checkInput() {
    const input = document.querySelector(".input-status-update")
    const statusbar = document.querySelector(".status-bar-container");
    const bartext = document.querySelector(".status-text");
    input.value = input.value.replace(/\s/g, "");
    if (input.value.trim() !== "") {
        statusbar.style.display = "block";
        bartext.style.display = "block";       
    } else {
        statusbar.style.display = "none";
        bartext.style.display = "none";
    }
}

function calculatePasswordStrength(password) {
    let strength = 0;

    // Criteria
    const length = password.length;
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSymbol = /[^A-Za-z0-9]/.test(password);

    // Character types
    if (hasLower) strength += 15;
    if (hasUpper) strength += 15;
    if (hasNumber) strength += 15;
    if (hasSymbol) strength += 15;

    // Length score
    if (length < 8 ) strength += ( 1.25 * length )
        else strength += 40;
     
    // Cap at 100
    return Math.min(strength, 100);
}


function updateStatusBar() {
    const input = document.querySelector(".input-status-update");
    const password = input.value;
    const strength = calculatePasswordStrength(password);
    const bartext = document.querySelector(".status-text");
    const statusBar = document.querySelector(".status-bar");
    statusBar.style.width = strength + "%";

    // Optional: change color based on strength
    if (strength < 40) {
        statusBar.style.backgroundColor = "red";
        bartext.innerHTML = "Weak Password";
        bartext.style.color = "red";
    } else if (strength < 80) {
        statusBar.style.backgroundColor = "orange";
        bartext.innerHTML = "Moderate Password";
        bartext.style.color = "orange";
    } else {
        statusBar.style.backgroundColor = "green";
        bartext.innerHTML = "Strong Password";
        bartext.style.color = "green";
        return true;
    }
}

function passwordVerify() {
    const input = document.querySelector(".input-status-update")
    const confirmInput = document.querySelector(".input-status-confirm")
    
    if (updateStatusBar() && input.value.trim() == confirmInput.value.trim()) {
        // Make the Change password or the regester bottom active
        return true;
    } else {
        // Make the Change password the regester bottom inactive
        return false;
    }
}
