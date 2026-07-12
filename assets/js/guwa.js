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
      if (event.target.closest("a")) closeMenu();
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeMenu();
    });
  }

  const copyButton = document.querySelector("[data-copy-code]");
  const status = document.querySelector("#copy-status");

  if (!copyButton || !status) return;

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
})();
