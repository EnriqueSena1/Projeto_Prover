document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    // Toggle ativação/desativação do vendedor
    document.querySelectorAll(".toggle-status").forEach(function (toggle) {
        toggle.addEventListener("change", async function () {
            const vendedorItem = this.closest(".vendedor-item");
            const vendedorId = vendedorItem.dataset.vendedorId;
            const isAtivo = this.checked;

            const url = `/api/user/${vendedorId}/`;
            const method = "PUT";
            const body = { is_active: isAtivo };

            const result = await apiRequest(url, method, body, {
                "X-CSRFToken": csrfToken
            });

            if (result) {
                vendedorItem.classList.toggle("inativo", !isAtivo);
                
            } else {
                // Reverter o estado visual se falhou
                this.checked = !isAtivo;
                alert("Erro ao atualizar o status do vendedor.");
            }
        });
    });

});