document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
    deleteModal.addEventListener("show.bs.modal", event => {
        const button = event.relatedTarget;
        const recipeId = button.getAttribute("data-recipe-id");
        
        const form = document.getElementById("delete-form");
        form.action = `/delete_recipe/${recipeId}`;
        console.log(form.action)
    });
});