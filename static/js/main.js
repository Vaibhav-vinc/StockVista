const ham = document.querySelector("button.hamburger");
ham.addEventListener("click", () => {
    if (ham.classList.contains("active")) {
        ham.classList.remove("active");
        document.querySelector("nav#menu-wrap").classList.remove("show");
    } else {
        ham.classList.add("active");
        document.querySelector("nav#menu-wrap").classList.add("show");
    }
});

const apiTemplate = document.getElementById("api-form-container");
const csvTemplate = document.getElementById("csv-form-container");

function RadioDisplay(value) {
    if (value === "csv") {
        csvTemplate.classList.remove("d-none");
        apiTemplate.classList.add("d-none");
    } else if (value === "api") {
        csvTemplate.classList.add("d-none");
        apiTemplate.classList.remove("d-none");
    }
}
