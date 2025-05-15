function capitalizeWords(str) {
    return str.replace(/\b\w/g, char => char.toUpperCase());
}

document.addEventListener('DOMContentLoaded', () => {
    const reasonField = document.querySelector('textarea[name="reason"]');
    reasonField.addEventListener('input', () => {
        const cursorPos = reasonField.selectionStart;
        reasonField.value = capitalizeWords(reasonField.value);
        reasonField.setSelectionRange(cursorPos, cursorPos);
    });
});