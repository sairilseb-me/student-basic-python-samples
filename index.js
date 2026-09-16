// Same ideas as B_request_basics.py, but from the browser using fetch().
// Make sure A_api_server.py is already running before clicking the button.

const BASE_URL = "http://127.0.0.1:5000";

async function requestExample() {
    console.log("=== GET request: fetch all students ===");
    let response = await fetch(`${BASE_URL}/api/students`);
    console.log("Status code:", response.status);
    console.log("JSON body:", await response.json());

    console.log("=== GET request: fetch ONE student ===");
    response = await fetch(`${BASE_URL}/api/students/juan-dela-cruz`);
    console.log("Status code:", response.status);
    console.log("JSON body:", await response.json());

    console.log("=== POST request: sign/clear a student ===");
    response = await fetch(`${BASE_URL}/api/students/maria-santos/sign`, {
        method: "POST",
    });
    console.log("Status code:", response.status);
    console.log("JSON body:", await response.json());
}

async function getSpecificStudent(studentId) {
    console.log(`=== GET request: fetch student with ID ${studentId} ===`);
    let response = await fetch(`${BASE_URL}/api/students/${studentId}`);
    let result = await response.json();
    let showResult = `The Student's name is ${result.name} and their status is ${result.status}.`;
    document.querySelector('#result-specific-student').innerHTML = showResult;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#button1").addEventListener("click", requestExample);
    document.querySelector("#button2").addEventListener("click", () => {
        const studentId = document.querySelector("input").value;
        getSpecificStudent(studentId);
    });
});
