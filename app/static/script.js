const form = document.getElementById("billForm");
const billInput = document.getElementById("billInput");
const emailInput = document.getElementById("emailInput");
const phoneInput = document.getElementById("phoneInput");
const outputText = document.getElementById("outputText");

let busy = false;

form.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  if (busy) return;
  busy = true;
  outputText.textContent = "Processing…";

  const billText = billInput.value.trim();
  if (!billText) {
    outputText.textContent = "Please paste a bill snippet first.";
    busy = false;
    return;
  }

  /* helper that throws if fetch != 2xx ------------------------------ */
  const fetchJson = async (url, payload) => {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const errMsg = await res.text();
      throw new Error(errMsg || `HTTP ${res.status}`);
    }
    return res.json();
  };

  /* ⏱️ run both requests in parallel ------------------------------- */

  const subscribe = (async () => {
    const email = emailInput.value.trim();
    if (!email) return "skipped";
    const phone = phoneInput.value.trim() || null;
    return fetchJson("/api/contact/subscribe", { email, phone });
  })();

  const simplify = fetchJson("/api/bill/simplify", { text: billText });

  const [contactRes, simpRes] = await Promise.allSettled([subscribe, simplify]);

  /* update UI ------------------------------------------------------- */

  if (simpRes.status === "fulfilled") {
    outputText.innerHTML = marked.parse(simpRes.value.result);
  } else {
    outputText.textContent =
      simpRes.reason?.message || "Could not simplify bill.";
  }

  if (contactRes.status === "rejected") {
    console.warn("Contact capture failed:", contactRes.reason);
    // optional toast/snackbar here
  }

  busy = false;
});
