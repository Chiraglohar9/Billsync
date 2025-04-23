document.addEventListener("DOMContentLoaded", function() {
    const savedEmail = localStorage.getItem("savedEmail");
    if (savedEmail) {
      const loginEmail = document.getElementById("login-email");
      if (loginEmail) {
        loginEmail.value = savedEmail;
        document.getElementById("remember-me").checked = true;
      }
    }
  });
  
  function saveLogin() {
    const remember = document.getElementById('remember').checked;
    if (remember) {
      localStorage.setItem('savedEmail', document.getElementById('username').value);
      localStorage.setItem('savedPassword', document.getElementById('password').value); // ❌ Not safe
    } else {
      localStorage.removeItem('savedEmail');
      localStorage.removeItem('savedPassword');
    }
    return true;
  }

  // Autofill if saved
  window.onload = function () {
    document.getElementById('username').value = localStorage.getItem('savedEmail') || '';
    document.getElementById('password').value = localStorage.getItem('savedPassword') || '';
  };
  
  function validatePassword() {
    const password = document.getElementById("signup-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    if (password !== confirmPassword) {
      document.getElementById("password-error").style.display = "block";
      return false;
    }
    return true;
  }
  
  function togglePassword(id) {
    const input = document.getElementById(id);
    if (input.type === "password") {
      input.type = "text";
    } else {
      input.type = "password";
    }
  }
  function onClick(e) {
    e.preventDefault();
    grecaptcha.enterprise.ready(async () => {
      const token = await grecaptcha.enterprise.execute('6LdphvMqAAAAAHT0RH58lRbJI4NlYFHsRDaxY14E', {action: 'LOGIN'});
    });
  }