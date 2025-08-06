(function () {
  document.addEventListener("DOMContentLoaded", function () {
    // Create additional floating particles
    function createParticle() {
      const particle = document.createElement("div");
      particle.style.position = "fixed";
      particle.style.width = "4px";
      particle.style.height = "4px";
      particle.style.background = "#4a9f4a";
      particle.style.borderRadius = "50%";
      particle.style.pointerEvents = "none";
      particle.style.zIndex = "-1";
      particle.style.opacity = "0.5";

      particle.style.left = Math.random() * window.innerWidth + "px";
      particle.style.top = window.innerHeight + "px";

      document.body.appendChild(particle);

      // Animate particle
      let position = window.innerHeight;
      const speed = 0.5 + Math.random() * 1;

      function animateParticle() {
        position -= speed;
        particle.style.top = position + "px";

        if (position < -10) {
          document.body.removeChild(particle);
        } else {
          requestAnimationFrame(animateParticle);
        }
      }

      animateParticle();
    }

    // Create particles periodically
    setInterval(createParticle, 3000);

    // Smooth scroll for navigation links
    document.querySelectorAll("nav a").forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
          targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });
  });
})();
