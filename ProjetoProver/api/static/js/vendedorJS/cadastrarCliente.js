document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    document.querySelectorAll(".toggle-status").forEach(function (toggle) {
        toggle.addEventListener("change", async function () {
            const userItem = this.closest(".vendedor-item");
            const userId = userItem.dataset.vendedorId;
            const isAtivo = this.checked;

            const url = `/api/user/${userId}/`;
            const method = "PUT";
            const body = { is_active: isAtivo };

            const result = await apiRequest(url, method, body, {
                "X-CSRFToken": csrfToken
            });

            if (result) {
                userItem.classList.toggle("inativo", !isAtivo);
            } else {
                this.checked = !isAtivo;
                alert("Erro ao atualizar o status do usuário.");
            }
        });
    });
});
