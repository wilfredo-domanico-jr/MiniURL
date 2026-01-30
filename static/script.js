async function shorten() {
  const url = document.getElementById("originalUrl").value.trim();
  const resultDiv = document.getElementById("result");

  if (!url) {
    resultDiv.innerHTML = '<p class="error">Please enter a URL.</p>';
    resultDiv.classList.add("show");
    return;
  }

  // Show loading state
  resultDiv.innerHTML =
    '<div style="text-align: center; padding: 20px;"><div class="loading"></div></div>';
  resultDiv.classList.add("show");

  try {
    const response = await fetch("/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();

    if (response.ok) {
      resultDiv.innerHTML = `
              <p class="result-label">Your shortened URL</p>
              <div class="short-url-container">
                <a href="${data.short_url}" target="_blank" class="short-url">${data.short_url}</a>
                <button class="copy-btn" onclick="copyToClipboard('${data.short_url}', this)">Copy</button>
              </div>
            `;
    } else {
      resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
    }
  } catch (err) {
    resultDiv.innerHTML = `<p class="error">Failed to shorten URL. Please try again.</p>`;
  }
}

function copyToClipboard(text, button) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      const originalText = button.textContent;
      button.textContent = "Copied!";
      button.classList.add("copied");

      setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove("copied");
      }, 2000);
    })
    .catch((err) => {
      alert("Failed to copy: " + err);
    });
}

// Allow Enter key to submit
document
  .getElementById("originalUrl")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      shorten();
    }
  });
