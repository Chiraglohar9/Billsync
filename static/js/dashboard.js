// Initialize Flatpickr
flatpickr(".custom-range-modal", {
  dateFormat: "Y-m-d",
  onChange: function (selectedDates, dateStr, instance) {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
      alert("Start date cannot be after end date.");
      instance.clear();
    }
  },
});

// Event listeners for modal
rangeSelector.addEventListener("change", function () {
  if (this.value === "custom") {
    modal.style.display = "flex";
  }
});

closeModal.addEventListener("click", function () {
  modal.style.display = "none";
});

applyRange.addEventListener("click", function () {
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  if (startDate && endDate) {
    alert(`Custom range applied: ${startDate} to ${endDate}`);
    modal.style.display = "none";
  } else {
    alert("Please select both start and end dates.");
  }
});

document.querySelectorAll(".sidebar ul li a").forEach((menuItem) => {
  menuItem.addEventListener("click", function () {
    document.querySelectorAll(".sidebar ul li a").forEach((item) => {
      item.classList.remove("active"); // Remove active class from all items
    });
    this.classList.add("active"); // Add active class to the clicked item
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".container > *"); // All sections inside the container
  const navLinks = document.querySelectorAll(".sidebar ul li a"); // Navigation links in the sidebar

  let currentActiveSection = null;
  let currentActiveLink = null;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if (currentActiveSection) {
            currentActiveSection.classList.remove("highlight"); // Remove highlight from previous section
          }
          if (currentActiveLink) {
            currentActiveLink.classList.remove("active"); // Remove active state from previous link
          }

          // Add highlight to the current section
          currentActiveSection = entry.target;
          currentActiveSection.classList.add("highlight");

          // Find and highlight the corresponding nav link
          const sectionId = entry.target.getAttribute("id");
          currentActiveLink = document.querySelector(
            `.sidebar ul li a[href="#${sectionId}"]`
          );
          if (currentActiveLink) {
            currentActiveLink.classList.add("active");
          }
        }
      });
    },
    { threshold: 0.5 } // Trigger when 50% of the section is visible
  );

  sections.forEach((section) => observer.observe(section)); // Observe all sections
});
