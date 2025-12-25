document.addEventListener('DOMContentLoaded', () => {
    const sizeButtons = document.querySelectorAll('.size-btn');
    const sizeInput = document.getElementById('selected-size');
    const form = document.getElementById('add-to-cart-form');

    sizeButtons.forEach(button => {
        button.addEventListener('click', () => {
            sizeButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            sizeInput.value = button.dataset.size;
        });
    });

    form.addEventListener('submit', (e) => {
        if (!sizeInput.value) {
            e.preventDefault();
            alert('Пожалуйста, выберите размер обуви');
        }
    });
});