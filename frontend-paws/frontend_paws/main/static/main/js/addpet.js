
function capitalizeWords(str) {
    return str.replace(/\b\w/g, char => char.toUpperCase());
}

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const cursorPos = input.selectionStart;
            input.value = capitalizeWords(input.value);
            input.setSelectionRange(cursorPos, cursorPos); // Keep cursor position
        });
    });
});

