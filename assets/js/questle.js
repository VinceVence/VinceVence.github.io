(() => {
  const body = document.body;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const stepCards = Array.from(document.querySelectorAll(".step-card"));
  const privacyPoints = Array.from(document.querySelectorAll(".privacy-points span"));
  const heroDrawing = document.querySelector(".hero-showcase, .hero-drawing");

  body.classList.add("js-enabled");

  requestAnimationFrame(() => {
    body.classList.add("is-ready");
  });

  const revealCard = (card) => {
    card.classList.add("is-visible");
  };

  if ("IntersectionObserver" in window && !reduceMotion) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          revealCard(entry.target);
          observer.unobserve(entry.target);
        });
      },
      {
        rootMargin: "0px 0px -8%",
        threshold: 0.18,
      },
    );

    [...stepCards, ...privacyPoints].forEach((item) => observer.observe(item));
  } else {
    stepCards.forEach(revealCard);
    privacyPoints.forEach(revealCard);
  }

  const pulseCard = (card) => {
    window.clearTimeout(card.questlePulseTimer);
    card.classList.add("is-active");
    card.questlePulseTimer = window.setTimeout(() => card.classList.remove("is-active"), 760);
  };

  stepCards.forEach((card) => {
    card.addEventListener("pointerdown", () => pulseCard(card));
    card.addEventListener("focus", () => pulseCard(card));
    card.addEventListener("click", () => pulseCard(card));
    card.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      pulseCard(card);
    });
  });

  if (!heroDrawing || reduceMotion) return;

  let frame = 0;

  const setHeroVars = (x, y) => {
    heroDrawing.style.setProperty("--tilt-x", `${x * 5}deg`);
    heroDrawing.style.setProperty("--tilt-y", `${y * -5}deg`);
    heroDrawing.style.setProperty("--float-x", `${x * 7}px`);
    heroDrawing.style.setProperty("--float-y", `${y * 5}px`);
  };

  heroDrawing.addEventListener("pointermove", (event) => {
    const rect = heroDrawing.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;

    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => setHeroVars(x, y));
  });

  heroDrawing.addEventListener("pointerleave", () => {
    cancelAnimationFrame(frame);
    setHeroVars(0, 0);
  });
})();
