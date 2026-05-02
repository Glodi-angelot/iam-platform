document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".iam-card");

    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.12}s`;
    });

    const deleteButtons = document.querySelectorAll(".delete-confirm");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            const username = this.dataset.username || "cet utilisateur";
            const confirmed = confirm(
                `Voulez-vous vraiment supprimer ${username} ? Cette action sera enregistrée dans les logs.`
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});