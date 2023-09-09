// Get references to the necessary elements
const form = document.querySelector('form');
const resultPopup = document.getElementById('result-popup');
const resultValue = document.getElementById('result-value');

// Get a reference to the car element
const carElement = document.querySelector('.car');

// Function to start the car animation
function startCarAnimation() {
    carElement.style.left = 'calc(100% + 50px)'; // Move the car to the right end of the screen
}

// Listen for the form submit event
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Perform your price prediction logic here
    // For now, let's assume you have the price stored in a variable called "predictedPrice"
    const predictedPrice = 21; // Replace with your actual prediction logic

    // Update the result value in the pop-up
    resultValue.textContent = predictedPrice;

    // Display the pop-up
    resultPopup.style.display = 'block';

    // Start the car animation
    startCarAnimation();
});
