document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("reportForm");
    const successMessage = document.getElementById("successMessage");
    const nameField = document.getElementById("name");

    form.addEventListener("submit", function (event) {

        const anonymity = document.querySelector('input[name="anonymity"]:checked').value;

        // If non-anonymous, name must be filled
        if (anonymity === "non-anonymous" && nameField.value.trim() === "") {
            alert("Please enter your name for non-anonymous reporting.");
            event.preventDefault();
            return;
        }

        successMessage.innerText = "Submitting report...";
    });

});
