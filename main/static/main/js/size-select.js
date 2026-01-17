document.addEventListener('DOMContentLoaded', function() {
    const sizeButtons = document.querySelectorAll('.size-btn');
    const selectedSizeInput = document.getElementById('selected-size');

    sizeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            selectedSizeInput.value = this.getAttribute('data-size');

            // Визуальное выделение выбранного размера
            sizeButtons.forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Проверка перед отправкой формы
    const form = document.getElementById('add-to-cart-form');
    form.addEventListener('submit', function(e) {
        if (!selectedSizeInput.value) {
            e.preventDefault();
            alert('Пожалуйста, выберите размер');
        }
    });
});

