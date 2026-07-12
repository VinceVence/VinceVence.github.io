(() => {
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
