function toggleTheme() {
    document.body.classList.toggle("dark");
  }
  // Function to toggle light/dark theme
function toggleTheme() {
    document.body.classList.toggle("dark");
  }

  // Function to show the respective login form
  function showLoginForm(role) {
    const studentForm = document.getElementById("student-form");
    const adminForm = document.getElementById("admin-form");

    if (role === "student") {
      studentForm.style.display = "block";
      adminForm.style.display = "none";
    } else if (role === "admin") {
      adminForm.style.display = "block";
      studentForm.style.display = "none";
    }
  }

  // Toggle theme between dark and light
const themeToggleButton = document.getElementById('theme-toggle');

themeToggleButton.addEventListener('click', () => {
  const body = document.body;

  // Toggle between dark and light theme classes
  body.classList.toggle('dark');
  body.classList.toggle('light');

  // Change the icon on the theme toggle button
  if (body.classList.contains('dark')) {
    themeToggleButton.textContent = '🌙'; // Moon icon for dark mode
  } else {
    themeToggleButton.textContent = '🌞'; // Sun icon for light mode
  }
});
