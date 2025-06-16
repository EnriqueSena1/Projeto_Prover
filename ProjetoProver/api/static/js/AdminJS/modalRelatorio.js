
document.addEventListener('DOMContentLoaded', function () {
    // Selecionar todas as linhas da tabela de movimentações
    const rows = document.querySelectorAll('.relatorio_movimentacao_conteudo tbody tr');
    const modal = document.getElementById('compraModal');
    const closeModal = document.querySelector('.close-modal');
    const modalItens = document.getElementById('modalItens');

    // Função para preencher o modal com os dados da compra
    function populateModal(compraId) {
        // Simulação de busca de dados (substitua por uma chamada API se necessário)
        const compra = {
            id: compraId,
            cliente: rows[compraId - 1].querySelector('td:first-child').textContent.trim(),
            data: rows[compraId - 1].querySelector('td:nth-child(2)').textContent.trim(),
            gasto: rows[compraId - 1].querySelector('td:nth-child(3)').textContent.trim(),
            status: 'Completado', // Substitua por um campo dinâmico se disponível
            itens: [
                { classificacao: 'Alimento', tipo_embalagem: 'Pacotes', descricao: 'Arroz', quantidade: 2, preco: 'R$ 50' }
                // Adicione mais itens dinamicamente via API ou contexto do Django
            ]
        };

        document.getElementById('modalClienteNome').textContent = compra.cliente;
        document.getElementById('modalData').textContent = compra.data;
        document.getElementById('modalGasto').textContent = compra.gasto;
        document.getElementById('modalStatus').textContent = compra.status;

        // Preencher a tabela de itens
        modalItens.innerHTML = '';
        compra.itens.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="padding: 10px;">${item.classificacao}</td>
                <td style="padding: 10px;">${item.tipo_embalagem}</td>
                <td style="padding: 10px;">${item.descricao}</td>
                <td style="padding: 10px;">${item.quantidade}</td>
                <td style="padding: 10px;">${item.preco}</td>
            `;
            modalItens.appendChild(row);
        });

        modal.style.display = 'block';
    }

    // Adicionar evento de clique às linhas
    rows.forEach((row, index) => {
        row.addEventListener('click', () => {
            populateModal(index + 1); // Ajuste para corresponder ao ID da compra
        });
    });

    // Fechar o modal
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Fechar o modal ao clicar fora
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
