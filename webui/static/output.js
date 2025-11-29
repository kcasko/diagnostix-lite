document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".dx-tab");
    const bodies = document.querySelectorAll(".dx-tab-body");

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            bodies.forEach(b => b.classList.remove("active"));

            tab.classList.add("active");
            document.getElementById(tab.dataset.tab).classList.add("active");
        });
    });

    // Auto scroll to bottom for stdout
    const stdout = document.getElementById("dx-stdout");
    if (stdout) stdout.scrollTop = stdout.scrollHeight;
});

// Clipboard logic
function copyOutput() {
    const active = document.querySelector(".dx-tab-body.active pre");
    if (!active) return;
    navigator.clipboard.writeText(active.textContent);
}

