(() => {
  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-nav");

  if (menuButton && navigation) {
    const closeMenu = () => {
      navigation.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "Open navigation");
    };

    menuButton.addEventListener("click", () => {
      const willOpen = !navigation.classList.contains("is-open");
      navigation.classList.toggle("is-open", willOpen);
      menuButton.setAttribute("aria-expanded", String(willOpen));
      menuButton.setAttribute(
        "aria-label",
        willOpen ? "Close navigation" : "Open navigation",
      );
    });

    navigation.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (!link) return;

      const href = link.getAttribute("href");
      if (!href?.startsWith("#")) {
        closeMenu();
        return;
      }

      const target = document.querySelector(href);
      if (!target) return;

      event.preventDefault();
      closeMenu();

      const menuCollapseDelay = window.innerWidth <= 900 ? 200 : 0;
      window.setTimeout(() => {
        target.scrollIntoView({
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth",
          block: "start",
        });
        window.history.pushState(null, "", href);
      }, menuCollapseDelay);
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeMenu();
    });
  }

  const rebrandDialog = document.querySelector("#rebrand-dialog");
  const rebrandDismissButtons = document.querySelectorAll(
    "[data-dismiss-rebrand]",
  );

  if (rebrandDialog) {
    const storageKey = "guwa-rebrand-announcement-seen";
    const dismissRebrand = () => {
      try {
        window.sessionStorage.setItem(storageKey, "true");
      } catch (_) {
        // Storage can be unavailable in privacy-restricted browser contexts.
      }

      if (rebrandDialog.open) rebrandDialog.close();
    };

    rebrandDismissButtons.forEach((button) => {
      button.addEventListener("click", dismissRebrand);
    });

    rebrandDialog.addEventListener("cancel", () => {
      try {
        window.sessionStorage.setItem(storageKey, "true");
      } catch (_) {
        // The dialog can still close normally when storage is unavailable.
      }
    });

    let hasSeenAnnouncement = false;
    try {
      hasSeenAnnouncement =
        window.sessionStorage.getItem(storageKey) === "true";
    } catch (_) {
      // Show the announcement once for this page view as a safe fallback.
    }

    if (!hasSeenAnnouncement && typeof rebrandDialog.showModal === "function") {
      window.setTimeout(() => {
        if (!rebrandDialog.open) rebrandDialog.showModal();
      }, 420);
    }
  }

  const questCarousel = document.querySelector("[data-quest-carousel]");
  const carouselButtons = document.querySelectorAll(
    "[data-carousel-direction]",
  );

  if (questCarousel && carouselButtons.length) {
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    const updateCarouselButtons = () => {
      const maxScrollLeft =
        questCarousel.scrollWidth - questCarousel.clientWidth - 2;

      carouselButtons.forEach((button) => {
        const isPrevious = button.dataset.carouselDirection === "previous";
        button.disabled = isPrevious
          ? questCarousel.scrollLeft <= 2
          : questCarousel.scrollLeft >= maxScrollLeft;
      });
    };

    carouselButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const firstCard = questCarousel.querySelector(".quest-card");
        if (!firstCard) return;

        const gap = Number.parseFloat(
          window.getComputedStyle(questCarousel).columnGap,
        );
        const direction =
          button.dataset.carouselDirection === "previous" ? -1 : 1;

        questCarousel.scrollBy({
          left: direction * (firstCard.offsetWidth + gap),
          behavior: prefersReducedMotion ? "auto" : "smooth",
        });
      });
    });

    questCarousel.addEventListener("scroll", updateCarouselButtons, {
      passive: true,
    });
    window.addEventListener("resize", updateCarouselButtons);
    updateCarouselButtons();
  }

  const copyButton = document.querySelector("[data-copy-code]");
  const status = document.querySelector("#copy-status");

  if (copyButton && status) {
    copyButton.addEventListener("click", async () => {
      const code = copyButton.dataset.copyCode;
      if (!code) return;

      try {
        await navigator.clipboard.writeText(code);
        copyButton.textContent = "Copied";
        status.textContent = "Founder Pass code copied.";
      } catch (_) {
        status.textContent = `Copy this code: ${code}`;
      }
    });
  }
})();
