document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("clienteInput");
    const sugestoes = document.getElementById("sugestoesClientes");
    const listaTodos = document.getElementById("todosClientes").querySelectorAll("li");
    const clienteIdSelecionado = document.getElementById("clienteIdSelecionado");
    const creditosRestantes = document.getElementById("creditosRestantes");
    const creditosPosCompra = document.getElementById("creditosPosCompra");
    const totalCompra = document.getElementById("totalCompra");

    // Recupera cliente salvo no localStorage
    const nomeSalvo = localStorage.getItem('clienteSelecionadoNome');
    const idSalvo = localStorage.getItem('clienteSelecionadoId');
    const creditoSalvo = localStorage.getItem('clienteSelecionadoCreditos');

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

            localStorage.setItem('clienteSelecionadoNome', e.target.textContent);
            localStorage.setItem('clienteSelecionadoId', e.target.dataset.id);
            localStorage.setItem('clienteSelecionadoCreditos', e.target.dataset.creditos);

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
    document.querySelectorAll('.mais').forEach(button => {
        button.addEventListener('click', async function () {
            const item = this.closest('.item-carrinho');
            const span = item.querySelector('.quantidade span');
            const inputId = item.querySelector('input[name="controleEstoque"]');
            const idProduto = inputId.value;
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const quantidadeAtual = parseInt(span.textContent);

            try {
                const response = await apiRequest(`/api/produtos/${idProduto}/`, 'GET', null, {
                    'X-CSRFToken': csrf
                });
                console.log(response)

                if (!response) {
                    alert('Erro ao buscar estoque');
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

    // Limpar localStorage ao fazer checkout
    document.querySelector(".checkout-btn").addEventListener("click", async function () {
        const clienteId = document.getElementById("clienteIdSelecionado").value;
        const itens = [];

        document.querySelectorAll('.item-carrinho').forEach(item => {
            const idProduto = item.querySelector('input[name="controleEstoque"]').value;
            const quantidade = parseInt(item.querySelector('.quantidade span').textContent);
            const precoText = item.querySelector('.info p').textContent;
            const precoUnitario = parseFloat(precoText.replace('R$', '').replace(',', '.').trim());

            itens.push({
                produto_id: idProduto,
                quantidade: quantidade,
                preco_unitario: precoUnitario
            });
        });

        const totalCompra = parseFloat(document.getElementById("totalCompra").textContent.replace('R$', '').replace(',', '.').trim());

        const dadosCompra = {
            cliente_id: clienteId,
            itens: itens,
            total_preco: totalCompra
        };

        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await apiRequest('/api/compras/', 'POST', dadosCompra, {
            'X-CSRFToken': csrf
        });

        if (response) {
            alert("Compra finalizada com sucesso!");
            // Limpa localStorage e redireciona
            localStorage.removeItem('clienteSelecionadoNome');
            localStorage.removeItem('clienteSelecionadoId');
            localStorage.removeItem('clienteSelecionadoCreditos');
            window.location.reload()
        } else {
            alert("Erro ao finalizar a compra.");
        }
    });
});

// Deletar item do carrinho
async function deletarCarrinho(idProduto) {
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData();
    formData.append('exibir_no_carrinho', 'false');

    try {
        const response = await fetch(`/api/produtos/${idProduto}/`, {
            method: 'PATCH',
            headers: {
                'X-CSRFToken': csrf
            },
            body: formData
        });

        if (!response.ok) throw new Error('Erro ao atualizar produto');

        window.location.reload();
    } catch (error) {
        console.error(error);
        alert("Erro ao remover do carrinho.");
    }
}

// Calcula o total da compra
function calcularTotalCompra() {
    let total = 0;

    document.querySelectorAll('.item-carrinho').forEach(item => {
        const precoText = item.querySelector('.info p').textContent;
        const preco = parseFloat(precoText.replace('R$', '').replace(',', '.').trim()) || 0;

        const quantidadeText = item.querySelector('.quantidade span').textContent;
        const quantidade = parseInt(quantidadeText) || 0;

        total += preco * quantidade;
    });

    document.getElementById("totalCompra").textContent = `R$ ${total.toFixed(2)}`;
    atualizarCreditoPosCompra();
}

// Atualiza o campo "Créditos após a compra"
function atualizarCreditoPosCompra() {
    const total = parseFloat(document.getElementById("totalCompra").textContent.replace('R$', '').replace(',', '.').trim()) || 0;
    const credito = parseFloat(document.getElementById("creditosRestantes").textContent.replace('R$', '').replace(',', '.').trim()) || 0;

    document.getElementById("creditosPosCompra").textContent = `R$ ${(credito - total).toFixed(2)}`;
}

// Atualiza tudo relacionado ao carrinho
function atualizarCarrinho() {
    calcularTotalCompra();
}


