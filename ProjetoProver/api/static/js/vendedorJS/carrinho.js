function showToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.classList.remove("hidden");
        toast.classList.add("visible");

        // Se for toast de confirmação, exibe o overlay
        if (toast.classList.contains("confirm")) {
            document.getElementById("toast-overlay").classList.add("visible");
        }
    }
}

function hideToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.classList.remove("visible");
        toast.classList.add("hidden");

        // Se for toast de confirmação, esconde o overlay
        if (toast.classList.contains("confirm")) {
            document.getElementById("toast-overlay").classList.remove("visible");
        }
    }
}

// Helper para toast de confirmação (genérico - agora no escopo global)
function showConfirmToast(toastId, message) {
    return new Promise(resolve => {
        const toast = document.getElementById(toastId);
        if (!toast) {
            console.error(`Toast com ID ${toastId} não encontrado.`);
            resolve(false);
            return;
        }
        toast.querySelector(".toast-message").textContent = message;
        showToast(toastId);

        const btnYes = toast.querySelector(".btn-yes");
        const btnNo = toast.querySelector(".btn-no");

        const handleYes = () => {
            hideToast(toastId);
            btnYes.removeEventListener("click", handleYes);
            btnNo.removeEventListener("click", handleNo);
            resolve(true);
        };

        const handleNo = () => {
            hideToast(toastId);
            btnYes.removeEventListener("click", handleYes);
            btnNo.removeEventListener("click", handleNo);
            resolve(false);
        };

        btnYes.addEventListener("click", handleYes);
        btnNo.addEventListener("click", handleNo);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("clienteInput");
    const sugestoes = document.getElementById("sugestoesClientes");
    const listaTodos = document.getElementById("todosClientes").querySelectorAll("li");
    const clienteIdSelecionado = document.getElementById("clienteIdSelecionado");
    const creditosRestantes = document.getElementById("creditosRestantes");
    const creditosPosCompra = document.getElementById("creditosPosCompra");
    const totalCompra = document.getElementById("totalCompra");

    // Lógica para fechar toasts de sucesso/informação
    document.querySelectorAll(".toast-close-button").forEach(button => {
        button.addEventListener("click", function() {
            const toast = this.closest(".toast");
            if (toast) {
                hideToast(toast.id);
            }
        });
    });

    // Recupera cliente salvo no localStorage
    const nomeSalvo = localStorage.getItem("clienteSelecionadoNome");
    const idSalvo = localStorage.getItem("clienteSelecionadoId");
    const creditoSalvo = localStorage.getItem("clienteSelecionadoCreditos");

    if (nomeSalvo && idSalvo && creditoSalvo) {
        input.value = nomeSalvo;
        clienteIdSelecionado.value = idSalvo;
        creditosRestantes.textContent = `R$ ${parseFloat(creditoSalvo).toFixed(2)}`;
    }

    calcularTotalCompra();

    // Filtro de clientes no autocomplete
    input.addEventListener("input", function () {
        const texto = this.value.toLowerCase();
        sugestoes.innerHTML = "";

        if (texto === "") return;

        let contador = 0;
        listaTodos.forEach(item => {
            const nome = item.textContent.toLowerCase();
            if (nome.includes(texto) && contador < 5) {
                const li = document.createElement("li");
                li.textContent = item.textContent;
                li.dataset.id = item.dataset.id;
                li.dataset.creditos = item.dataset.creditos;
                sugestoes.appendChild(li);
                contador++;
            }
        });
    });

    // Clique em sugestão
    sugestoes.addEventListener("click", function (e) {
        if (e.target.tagName === "LI") {
            input.value = e.target.textContent;
            clienteIdSelecionado.value = e.target.dataset.id;

            const creditos = parseFloat(e.target.dataset.creditos);
            creditosRestantes.textContent = `R$ ${creditos.toFixed(2)}`;
            atualizarCreditoPosCompra();

            localStorage.setItem("clienteSelecionadoNome", e.target.textContent);
            localStorage.setItem("clienteSelecionadoId", e.target.dataset.id);
            localStorage.setItem("clienteSelecionadoCreditos", e.target.dataset.creditos);

            sugestoes.innerHTML = "";
        }
    });

    // Fechar sugestões ao clicar fora
    document.addEventListener("click", function (e) {
        if (!sugestoes.contains(e.target) && e.target !== input) {
            sugestoes.innerHTML = "";
        }
    });

    // Controle de quantidade (+ / -)
    document.querySelectorAll(".mais").forEach(button => {
        button.addEventListener("click", async function () {
            const item = this.closest(".item-carrinho");
            const span = item.querySelector(".quantidade span");
            const inputId = item.querySelector("input[name=\"controleEstoque\"]");
            const idProduto = inputId.value;
            const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

            const quantidadeAtual = parseInt(span.textContent);

            try {
                const response = await apiRequest(`/api/produtos/${idProduto}/`, "GET", null, {
                    "X-CSRFToken": csrf
                });
                console.log(response)

                if (!response) {
                    alert("Erro ao buscar estoque");
                    return;
                }

                const estoqueDisponivel = response.quantidade;  
                

                if (quantidadeAtual < estoqueDisponivel) {
                    span.textContent = quantidadeAtual + 1;
                    atualizarCarrinho();
                } else {
                    alert(`Estoque máximo atingido. Disponível: ${estoqueDisponivel}`);
                }

            } catch (error) {
                console.error(error);
                alert("Erro ao verificar estoque.");
            }
        });
    });
    document.querySelectorAll(".menos").forEach(button => {
        button.addEventListener("click", function () {
            const item = this.closest(".item-carrinho");
            const span = item.querySelector(".quantidade span");
            let quantidadeAtual = parseInt(span.textContent);

            if (quantidadeAtual > 1) {
                quantidadeAtual--;
                span.textContent = quantidadeAtual;
                atualizarCarrinho();
            }
        });
    });



    // Limpar localStorage ao fazer checkout
    document.querySelector(".checkout-btn").addEventListener("click", async function () {
        const confirmed = await showConfirmToast("toast-confirm-compra", "Deseja finalizar a compra?");

        if (confirmed) {
            const clienteId = document.getElementById("clienteIdSelecionado").value;
            const itens = [];

            document.querySelectorAll(".item-carrinho").forEach(item => {
                const idProduto = item.querySelector("input[name=\"controleEstoque\"]").value;
                const quantidade = parseInt(item.querySelector(".quantidade span").textContent);
                const precoText = item.querySelector(".info p").textContent;
                const precoUnitario = parseFloat(precoText.replace("R$", "").replace(",", ".").trim());

                itens.push({
                    produto_id: idProduto,
                    quantidade: quantidade,
                    preco_unitario: precoUnitario
                });
            });

            const totalCompra = parseFloat(document.getElementById("totalCompra").textContent.replace("R$", "").replace(",", ".").trim());

            const dadosCompra = {
                cliente_id: clienteId,
                itens: itens,
                total_preco: totalCompra
            };

            const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

            const response = await apiRequest("/api/compras/", "POST", dadosCompra, {
                "X-CSRFToken": csrf
            });

            if (response) {
                showToast("toast-compra-realizada");
                // Limpa localStorage e redireciona
                localStorage.removeItem("clienteSelecionadoNome");
                localStorage.removeItem("clienteSelecionadoId");
                localStorage.removeItem("clienteSelecionadoCreditos");
                setTimeout(() => {
                    window.location.reload();
                }, 1500); // Atraso para o toast ser visível
            } else {
                alert("Erro ao finalizar a compra."); // Manter alert para erro de API
            }
        }
    });
});

async function deletarCarrinho(idProduto) {
    // 1. Exibe o toast de confirmação e aguarda a resposta do usuário
    const confirmed = await showConfirmToast("toast-confirm-remocao", "Deseja remover o produto?");

    // 2. Verifica se o usuário confirmou a ação
    if (confirmed) {
        const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const formData = new FormData();
        formData.append("exibir_no_carrinho", "false");

        try {
            // 3. Envia a requisição PATCH para atualizar o produto
            const response = await fetch(`/api/produtos/${idProduto}/`, {
                method: "PATCH",
                headers: {
                    "X-CSRFToken": csrf
                },
                body: formData
            });

            if (!response.ok) throw new Error("Erro ao atualizar produto");

            // 4. Exibe toast de sucesso após a remoção
            showToast("toast-produto-removido");

            // 5. Recarrega a página após um pequeno atraso para que o toast seja visível
            setTimeout(() => {
                window.location.reload();
            }, 1500); // Atraso de 1.5 segundos

        } catch (error) {
            console.error(error);
            // 6. Exibe alert de erro em caso de falha (manter alert para erros de API)
            alert("Erro ao remover do carrinho.");
        }
    } else {
        // 7. Não faz nada se a remoção for cancelada, sem toast de erro.
        console.log("Remoção cancelada pelo usuário.");
    }
}

// Calcula o total da compra
function calcularTotalCompra() {
    let total = 0;

    document.querySelectorAll(".item-carrinho").forEach(item => {
        const precoText = item.querySelector(".info p").textContent;
        const preco = parseFloat(precoText.replace("R$", "").replace(",", ".").trim()) || 0;

        const quantidadeText = item.querySelector(".quantidade span").textContent;
        const quantidade = parseInt(quantidadeText) || 0;

        total += preco * quantidade;
    });

    document.getElementById("totalCompra").textContent = `R$ ${total.toFixed(2)}`;
    atualizarCreditoPosCompra();
}

// Atualiza o campo "Créditos após a compra"
function atualizarCreditoPosCompra() {
    const total = parseFloat(document.getElementById("totalCompra").textContent.replace("R$", "").replace(",", ".").trim()) || 0;
    const credito = parseFloat(document.getElementById("creditosRestantes").textContent.replace("R$", "").replace(",", ".").trim()) || 0;

    document.getElementById("creditosPosCompra").textContent = `R$ ${(credito - total).toFixed(2)}`;
}

// Atualiza tudo relacionado ao carrinho
function atualizarCarrinho() {
    calcularTotalCompra();
}

