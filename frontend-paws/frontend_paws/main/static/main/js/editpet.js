function capitalizeFirstLetter(input) {
    let words = input.value.split(' ');
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1).toLowerCase();
    }
    input.value = words.join(' ');
}

document.addEventListener("DOMContentLoaded", function() {
    const nameInput = document.querySelector('input[name="name"]');
    const speciesInput = document.querySelector('input[name="species"]');
    const breedInput = document.querySelector('input[name="breed"]');

    nameInput.addEventListener('input', function() {
        capitalizeFirstLetter(nameInput);
    });

    speciesInput.addEventListener('input', function() {
        capitalizeFirstLetter(speciesInput);
    });

    breedInput.addEventListener('input', function() {
        capitalizeFirstLetter(breedInput);
    });
});
