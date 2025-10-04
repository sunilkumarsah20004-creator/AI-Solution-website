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
    window.addEventListener("scroll", function () {
      const scrollTop =
        window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > 50) {
        navbarBg.style.backgroundColor = "#1F2937";
        navbarBg.style.borderBottomColor = "rgba(59, 130, 246, 0.2)";
        navbarBg.classList.remove("border-transparent");
      } else {
        navbarBg.style.backgroundColor = "transparent";
        navbarBg.style.borderBottomColor = "transparent";
        navbarBg.classList.add("border-transparent");
      }
    });
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
window.addEventListener("scroll", function () {
  const backToTop = document.getElementById("back-to-top");
  if (backToTop) {
    const scrollTop = window.pageYOffset;
    if (scrollTop > 300) {
      backToTop.classList.remove("opacity-0", "pointer-events-none");
      backToTop.classList.add("opacity-100");
    } else {
      backToTop.classList.add("opacity-0", "pointer-events-none");
      backToTop.classList.remove("opacity-100");
    }
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
