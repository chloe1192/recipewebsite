document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
    deleteModal.addEventListener("show.bs.modal", event => {
        const button = event.relatedTarget;
        const recipeId = button.getAttribute("data-recipe-id");
        
        const form = document.getElementById("delete-form");
        form.action = `/delete_recipe/${recipeId}`;
        console.log(form.action)
    });

    // Recipe form stars
    document.querySelectorAll('.star-rating input').forEach(input => {
        input.addEventListener('change', () => {
            const stars = input.closest('.star-rating').querySelectorAll('label');
            stars.forEach((star, index) => {
                star.style.color = index < 5 - input.value ? '#ccc' : 'gold';
            });
        });
    });

});