const form = document.getElementById("prediction-form");
const button = document.getElementById("predict-button");
const errorBox = document.getElementById("error-message");
const placeholder = document.getElementById("result-placeholder");
const resultContent = document.getElementById("result-content");
const loadingState = document.getElementById("loading-state");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.hidden = true;

  const formData = new FormData(form);
  const payload = {};
  for (const [key, value] of formData.entries()) {
    if (value.trim() === "" || !Number.isFinite(Number(value))) {
      showError(`Please enter a valid number for ${key}.`);
      return;
    }
    payload[key] = Number(value);
  }

  button.disabled = true;
  placeholder.hidden = true;
  resultContent.hidden = true;
  loadingState.hidden = false;

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to make a prediction.");

    document.getElementById("price-dollars").textContent =
      Number(data.price_dollars).toLocaleString("en-US", {
        minimumFractionDigits: 2, maximumFractionDigits: 2
      });
    document.getElementById("price-thousands").textContent =
      `$${Number(data.price_thousands).toLocaleString("en-US", {
        minimumFractionDigits: 2, maximumFractionDigits: 2
      })} thousand`;
    loadingState.hidden = true;
    resultContent.hidden = false;
  } catch (error) {
    loadingState.hidden = true;
    placeholder.hidden = false;
    showError(error.message);
  } finally {
    button.disabled = false;
  }
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
}
