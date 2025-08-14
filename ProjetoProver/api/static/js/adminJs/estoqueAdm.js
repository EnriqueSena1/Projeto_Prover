let idProdutoParaExcluir = null;

// Cache dos elementos
const toastConfirmacao = document.getElementById("toast-confirm-remocao");
const toastSucesso = document.getElementById("toast-produto-removido");
const btnYes = document.querySelector(".btn-yes");

// Função para alternar visibilidade de um elemento
function alternarVisibilidade(elemento, mostrar) {
    elemento.classList.toggle("hidden", !mostrar);
    elemento.classList.toggle("visible", mostrar);
}

// Mostra o toast de confirmação
function mostrarConfirmacaoRemocao(idProduto) {
    idProdutoParaExcluir = idProduto;
    alternarVisibilidade(toastConfirmacao, true);
}

// Esconde o toast de confirmação
function esconderConfirmacaoRemocao() {
    alternarVisibilidade(toastConfirmacao, false);
    idProdutoParaExcluir = null;
}

// Toast de sucesso
function mostrarToastSucesso() {
    alternarVisibilidade(toastSucesso, true);

    setTimeout(() => {
        alternarVisibilidade(toastSucesso, false);
    }, 1500);
}

// Confirma a exclusão via API
async function confirmarExclusaoProduto() {
    if (!idProdutoParaExcluir) return;

    btnYes.disabled = true; // Previne múltiplos cliques

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const url = `/api/produtos/${idProdutoParaExcluir}/`;

    try {
         const response = await fetch(url, {
            method: 'PATCH', // ← PATCH no lugar de DELETE
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ativo: false // ← só atualiza o campo ativo
            })
        });

        if (response.ok) {
            mostrarToastSucesso();

            // Opcional: remover da DOM sem recarregar
            // document.querySelector(`[data-id="${idProdutoParaExcluir}"]`).closest(".produto").remove();

            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            alert(`Erro ao excluir o produto. Código: ${response.status}`);
            // console.error("Erro na exclusão:", response.statusText);
        }
    } catch (error) {
        alert("Erro ao excluir o produto.");
        // console.error("Erro na requisição:", error);
    } finally {
        esconderConfirmacaoRemocao();
        btnYes.disabled = false;
    }
}

// Delegação de eventos
document.addEventListener("click", function (e) {
    const target = e.target;

    if (target.closest(".btn-yes")) {
        confirmarExclusaoProduto();
        return;
    }

    if (target.closest(".btn-no")) {
        esconderConfirmacaoRemocao();
        return;
    }

    const btnExcluir = target.closest(".btn_excluir_produto");
    if (btnExcluir) {
        e.preventDefault();
        mostrarConfirmacaoRemocao(btnExcluir.getAttribute("data-id"));
    }
});
