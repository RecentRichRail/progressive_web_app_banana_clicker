document.addEventListener('DOMContentLoaded', (event) => {
    let count = 0;
    const countDisplay = document.getElementById('count');
    const clickButton = document.getElementById('clickButton');

    clickButton.addEventListener('click', () => {
        count++;
        countDisplay.textContent = count;
    });
});
