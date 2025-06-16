let idProdutoParaExcluir = null;

// Mostra o toast de confirmação
function mostrarConfirmacaoRemocao(idProduto) {
    idProdutoParaExcluir = idProduto;

    const toast = document.getElementById("toast-confirm-remocao");
    toast.classList.remove("hidden");
    toast.classList.add("visible");
}

// Esconde o toast de confirmação
function esconderConfirmacaoRemocao() {
    const toast = document.getElementById("toast-confirm-remocao");
    toast.classList.remove("visible");
    toast.classList.add("hidden");

    idProdutoParaExcluir = null;
}
async function confirmarExclusaoProduto() {
    if (!idProdutoParaExcluir) return;

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const url = `/api/produtos/${idProdutoParaExcluir}/`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/json',
            },
        });

        esconderConfirmacaoRemocao();

        if (response.ok) {
            mostrarToastSucesso();
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert(`Erro ao excluir o produto. Código: ${response.status}`);
            console.error("Erro na exclusão:", response.statusText);
        }
    } catch (error) {
        alert("Erro ao excluir o produto.");
        console.error("Erro na requisição:", error);
    }
}

// Toast de sucesso no canto inferior
function mostrarToastSucesso() {
    const toastSucesso = document.getElementById("toast-produto-removido");
    toastSucesso.classList.remove("hidden");
    toastSucesso.classList.add("visible");

    setTimeout(() => {
        toastSucesso.classList.remove("visible");
        toastSucesso.classList.add("hidden");
    }, 1500);
}

// Delegação de eventos
document.addEventListener("click", function (e) {
    // Botão "Sim"
    if (e.target.closest(".btn-yes")) {
        confirmarExclusaoProduto();
    }

    // Botão "Não"
    if (e.target.closest(".btn-no")) {
        esconderConfirmacaoRemocao();
    }

    // Botão de excluir (ícone ou link)
    if (e.target.closest(".btn_excluir_produto")) {
        e.preventDefault();
        const btn = e.target.closest(".btn_excluir_produto");
        const id = btn.getAttribute("data-id");
        mostrarConfirmacaoRemocao(id);
    }
});
