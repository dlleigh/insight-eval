// ===========================
// INSIGHT EVALUATION - MAIN JAVASCRIPT
// Mobile menu and testimonials carousel
// ===========================

(function() {
  'use strict';

  // ===========================
  // MOBILE MENU TOGGLE
  // ===========================
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const nav = document.querySelector('nav');

  if (mobileMenuToggle && nav) {
    mobileMenuToggle.addEventListener('click', function() {
      nav.classList.toggle('active');

      // Toggle icon between bars and times
      const icon = this.querySelector('i');
      if (nav.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
      } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });

    // Close menu when clicking a link
    const navLinks = nav.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        nav.classList.remove('active');
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!nav.contains(event.target) && !mobileMenuToggle.contains(event.target)) {
        nav.classList.remove('active');
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });
  }

  // ===========================
  // TESTIMONIALS CAROUSEL
  // ===========================
  const testimonials = document.querySelectorAll('.testimonial');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');

  if (testimonials.length > 0 && prevBtn && nextBtn) {
    let currentIndex = 0;
    let isAnimating = false;

    function showTestimonial(newIndex) {
      if (isAnimating || newIndex === currentIndex) return;
      isAnimating = true;

      const currentEl = testimonials[currentIndex];
      const nextEl = testimonials[newIndex];

      // Start both animations simultaneously
      nextEl.classList.add('active');
      currentEl.classList.add('slide-out');
      currentEl.classList.remove('active');

      // Clean up after animation completes
      setTimeout(() => {
        currentEl.classList.remove('slide-out');
        currentIndex = newIndex;
        isAnimating = false;
      }, 400);
    }

    function nextTestimonial() {
      const newIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(newIndex);
    }

    function prevTestimonial() {
      const newIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
      showTestimonial(newIndex);
    }

    // Event listeners for buttons
    nextBtn.addEventListener('click', nextTestimonial);
    prevBtn.addEventListener('click', prevTestimonial);

    // Touch/swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    const testimonialsContainer = document.querySelector('.testimonials-container');

    if (testimonialsContainer) {
      testimonialsContainer.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
      }, false);

      testimonialsContainer.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      }, false);

      function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
          if (diff > 0) {
            // Swiped left - show next
            nextTestimonial();
          } else {
            // Swiped right - show previous
            prevTestimonial();
          }
        }
      }
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
      if (testimonials.length > 0) {
        if (e.key === 'ArrowLeft') {
          prevTestimonial();
        } else if (e.key === 'ArrowRight') {
          nextTestimonial();
        }
      }
    });

    // Auto-rotate every 15 seconds
    setInterval(nextTestimonial, 15000);
  }

  // ===========================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ===========================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');

      // Skip if it's just "#"
      if (href === '#') return;

      const target = document.querySelector(href);

      if (target) {
        e.preventDefault();
        const headerHeight = document.querySelector('header').offsetHeight;
        const targetPosition = target.getBoundingClientOffset().top + window.pageYOffset - headerHeight - 20;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

})();
