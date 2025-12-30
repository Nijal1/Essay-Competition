document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("paragraphContainer");
  const hiddenContent = document.getElementById("essayContent");
  const addBtn = document.getElementById("addParagraphBtn");
  const form = document.getElementById("essayForm");
  const essayTitle = document.getElementById("essayTitle");
  const submitBtn = document.getElementById("submitBtn");
  const previewBtn = document.getElementById("previewBtn");
  const previewModal = document.getElementById("previewModal");
  const closeModal = document.getElementById("closeModal");
  const previewTitle = document.getElementById("previewTitle");
  const previewContent = document.getElementById("previewContent");
  const username = document.getElementById("loggedInUser").value || "Guest";

  let paragraphCount = 0;

  // ------------------ Paragraph System ------------------
  function addNewParagraph() {
    paragraphCount++;
    const wrapper = document.createElement("div");
    wrapper.classList.add("paragraph-wrapper");
    wrapper.style.marginBottom = "12px";

    const textarea = document.createElement("textarea");
    textarea.classList.add("paragraph");
    textarea.placeholder = `Paragraph ${paragraphCount}`;
    textarea.rows = 5;
    textarea.style.width = "100%";

    wrapper.appendChild(textarea);
    container.appendChild(wrapper);
  }

  // Add first paragraph on load
  addNewParagraph();

  addBtn.addEventListener("click", () => {
    // Make existing paragraphs readonly
    document
      .querySelectorAll(".paragraph")
      .forEach((p) => p.setAttribute("readonly", true));
    addNewParagraph();
  });

  // ------------------ Helper: Get final essay text ------------------
  function getFinalText() {
    return Array.from(document.querySelectorAll(".paragraph"))
      .map((p) => p.value.trim())
      .filter((v) => v !== "")
      .join("\n\n");
  }

  // ------------------ Preview ------------------
  previewBtn.addEventListener("click", () => {
    const finalText = getFinalText();
    if (!essayTitle.value.trim() || !finalText.trim()) {
      alert("Please enter both title and content.");
      return;
    }

    previewTitle.textContent = essayTitle.value.trim();
    previewContent.textContent = finalText;

    previewModal.classList.add("active"); //  show modal
  });

  closeModal.addEventListener("click", () => {
    previewModal.classList.remove("active"); //  hide modal
  });

  // Close modal by clicking outside content
  previewModal.addEventListener("click", (e) => {
    if (e.target === previewModal) {
      previewModal.classList.remove("active");
    }
  });

  // ------------------ Save Draft as PDF ------------------
  const saveDraftBtn = document.getElementById("saveDraft");
  if (saveDraftBtn) {
    saveDraftBtn.addEventListener("click", () => {
      const finalText = getFinalText();
      if (!essayTitle.value.trim() || !finalText.trim()) {
        alert("Enter title and content first!");
        return;
      }

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();

      doc.setFontSize(14);
      doc.text(`Author: ${username}`, 10, 15);

      doc.setFontSize(18);
      doc.text(essayTitle.value.trim(), 10, 30);

      doc.setFontSize(12);
      const lines = doc.splitTextToSize(finalText, 180);
      doc.text(lines, 10, 45);

      doc.output("dataurlnewwindow");
    });
  }

  // ------------------ Submit Essay ------------------
  submitBtn.addEventListener("click", () => {
    const finalText = getFinalText();
    if (!essayTitle.value.trim() || !finalText.trim()) {
      alert("Please enter both title and content.");
      return;
    }

    hiddenContent.value = finalText; // Fill hidden textarea
    form.submit(); // Submit the form to Django
  });

  // Disable context menu & copy-paste
  // document.addEventListener("contextmenu", (e) => e.preventDefault());
  // document.addEventListener("keydown", (e) => {
  //   if (
  //     (e.ctrlKey || e.metaKey) &&
  //     ["c", "v", "x"].includes(e.key.toLowerCase())
  //   ) {
  //     e.preventDefault();
  //     alert("Copy-paste shortcuts are disabled.");
  //   }
  // });
});
