// AI Solutions - Main JavaScript File
// Optimized and cleaned version

// Set current year in footer
document.addEventListener("DOMContentLoaded", function () {
  const yearElement = document.getElementById("year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
});

// Navbar scroll effect
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("navbar");
  const navbarBg = document.getElementById("navbar-bg");

  if (navbar && navbarBg) {
    console.log("✅ Navbar scroll effect initialized"); // Debug

    // Function to update navbar based on scroll
    function updateNavbar() {
      const scrollTop =
        window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > 50) {
        console.log("📜 Scrolled down - applying dark navbar"); // Debug
        // Scrolled state - add dark background with blur
        navbarBg.style.backgroundColor = "rgba(17, 24, 39, 0.95)"; // bg-gray-900 with opacity
        navbarBg.style.backdropFilter = "blur(12px)";
        navbarBg.style.webkitBackdropFilter = "blur(12px)"; // Safari support
        navbarBg.style.borderBottomColor = "rgba(59, 130, 246, 0.3)";
        navbarBg.style.boxShadow =
          "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)";
        navbarBg.classList.remove("border-transparent");
      } else {
        console.log("⬆️ At top - applying transparent navbar"); // Debug
        // Top of page - transparent
        navbarBg.style.backgroundColor = "transparent";
        navbarBg.style.backdropFilter = "none";
        navbarBg.style.webkitBackdropFilter = "none";
        navbarBg.style.borderBottomColor = "transparent";
        navbarBg.style.boxShadow = "none";
        navbarBg.classList.add("border-transparent");
      }
    }

    // Run on page load
    updateNavbar();

    // Run on scroll
    window.addEventListener("scroll", updateNavbar);
  } else {
    console.error("❌ Navbar elements not found!", { navbar, navbarBg }); // Debug
  }
});

// Mobile navigation toggle
document.addEventListener("DOMContentLoaded", function () {
  const navBtn = document.getElementById("navBtn");
  const mobileNav = document.getElementById("mobileNav");
  const iconOpen = document.getElementById("navIconOpen");
  const iconClose = document.getElementById("navIconClose");

  if (navBtn && mobileNav && iconOpen && iconClose) {
    navBtn.addEventListener("click", () => {
      mobileNav.classList.toggle("hidden");
      iconOpen.classList.toggle("hidden");
      iconClose.classList.toggle("hidden");
    });
  }
});

// Toast notification system
function closeToast(button) {
  const toast = button.closest(".toast-item");
  if (toast) {
    toast.classList.remove("toast-enter");
    toast.classList.add("toast-exit");
    setTimeout(() => {
      toast.remove();
      const container = document.getElementById("toast-container");
      if (container && container.children.length === 0) {
        container.remove();
      }
    }, 400);
  }
}

// Auto-close toasts after 2 seconds
document.addEventListener("DOMContentLoaded", function () {
  const toasts = document.querySelectorAll("#toast-container .toast-item");
  toasts.forEach((toast) => {
    setTimeout(() => {
      const closeButton = toast.querySelector(".toast-close");
      if (closeButton) {
        closeToast(closeButton);
      }
    }, 2000);
  });
});

// Back to Top functionality
document.addEventListener("DOMContentLoaded", function () {
  const backToTop = document.getElementById("back-to-top");

  if (backToTop) {
    function updateBackToTop() {
      const scrollTop = window.pageYOffset;
      if (scrollTop > 300) {
        backToTop.classList.remove("opacity-0", "pointer-events-none");
        backToTop.classList.add("opacity-100");
      } else {
        backToTop.classList.add("opacity-0", "pointer-events-none");
        backToTop.classList.remove("opacity-100");
      }
    }

    // Run on page load
    updateBackToTop();

    // Run on scroll
    window.addEventListener("scroll", updateBackToTop);
  }
});

// Smooth scroll for anchor links
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
});
