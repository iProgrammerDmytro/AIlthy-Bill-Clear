const form = document.getElementById("billForm");
const billInput = document.getElementById("billInput");
const emailInput = document.getElementById("emailInput");
const phoneInput = document.getElementById("phoneInput");
const output = document.getElementById("outputText");
const outputBox = document.getElementById("outputContainer");
const submitBtn = document.getElementById("submitBtn");

let busy = false;

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  if (busy) return;
  busy = true;

  /* 🔄 UI state */
  NProgress.start();
  submitBtn.disabled = true;
  submitBtn.querySelector(".btn-label").textContent = "Working…";

  try {
    const [contactRes, simplifyRes] = await Promise.all([
      postJSON("/api/contact/subscribe", {
        email: emailInput.value.trim(),
        phone: phoneInput.value.trim() || null,
      }),
      postJSON("/api/bill/simplify", { text: billInput.value.trim() }),
    ]);

    /* 🎯 Display result */
    output.innerHTML = marked.parse(simplifyRes.result);
    outputBox.hidden = false;
  } catch (err) {
    outputBox.hidden = false;
    output.textContent = err.message || "Something went wrong.";
  } finally {
    NProgress.done();
    submitBtn.disabled = false;
    submitBtn.querySelector(".btn-label").textContent = "Simplify my bill";
    busy = false;
  }
});

/* Helper */
async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error((await res.text()) || `HTTP ${res.status}`);
  return res.json();
}
