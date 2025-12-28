document.addEventListener("DOMContentLoaded", function () {
  // Profile Dropdown
  const profileBtn = document.getElementById("profileBtn");
  const profileDropdown = document.getElementById("profileDropdown");

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      profileDropdown.classList.toggle("show");
      profileBtn.classList.toggle("active");
    });

    document.addEventListener("click", function (e) {
      if (
        !profileBtn.contains(e.target) &&
        !profileDropdown.contains(e.target)
      ) {
        profileDropdown.classList.remove("show");
        profileBtn.classList.remove("active");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && profileDropdown.classList.contains("show")) {
        profileDropdown.classList.remove("show");
        profileBtn.classList.remove("active");
      }
    });
  }

  // Mobile Menu Toggle
  const menuToggle = document.getElementById("menuToggle");
  const navMenu = document.getElementById("navMenu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function () {
      menuToggle.classList.toggle("active");
      navMenu.classList.toggle("show");
    });
  }

  // Messages auto-hide
  const messagesContainer = document.getElementById("messages-container");
  if (messagesContainer) {
    setTimeout(function () {
      messagesContainer.style.opacity = "0";
      messagesContainer.style.transition = "opacity 0.3s ease";
      setTimeout(function () {
        messagesContainer.style.display = "none";
      }, 300);
    }, 5000);
  }

  // Contact Form
  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("Thank you for your message! We will get back to you soon.");
      contactForm.reset();
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
        // Close mobile menu if open
        if (navMenu && navMenu.classList.contains("show")) {
          navMenu.classList.remove("show");
          menuToggle.classList.remove("active");
        }
      }
    });
  });
});
