document.addEventListener("DOMContentLoaded", function () {
    const cadastroDialog = document.getElementById("cadastroDialog");
    const openDialogButton = document.getElementById("openDialogButton");
    const closeButton = document.querySelector(".close-button");
    const cadastroForm = document.getElementById("cadastroForm");
    const uploadInput = document.getElementById("fotoProduto");
    const uploadPreview = document.getElementById("uploadPreview");

    function abrirDialog() {
        cadastroDialog.showModal();
        document.body.style.overflow = 'hidden';
    }

    function fecharDialog() {
        cadastroDialog.close();
        document.body.style.overflow = 'auto';
        limparFormulario();
    }

    function limparFormulario() {
        cadastroForm.reset();
        uploadPreview.innerHTML = '';
        limparErros();
        removerImagem(); // Ensure image preview is cleared
    }

    function limparErros() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(error => error.textContent = '');
        
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => input.classList.remove('error'));
    }

    function mostrarErro(inputId, mensagem) {
        const input = document.getElementById(inputId);
        const errorId = `error${inputId.charAt(0).toUpperCase() + inputId.slice(1)}`;
        const errorElement = document.getElementById(errorId);

        if (input) {
            input.classList.add('error');
        }

        if (errorElement) {
            errorElement.textContent = mensagem;
        } 
    }

    async function handleSubmit(event) {
        event.preventDefault();
        limparErros();

        let isValid = true;
        
        const descricao = document.getElementById('descricaoProduto').value.trim();
        if (!descricao) {
            mostrarErro('descricaoProduto', 'Descrição é obrigatória');
            isValid = false;
        }

        const validade = document.getElementById('validadeProduto').value.trim();
        if (!validade) {
            mostrarErro('validadeProduto', 'Validade é obrigatória');
            isValid = false;
        }

        const quantidade = document.getElementById('quantidadeProduto').value.trim();
        if (!quantidade || isNaN(quantidade) || parseInt(quantidade) <= 0) {
            mostrarErro('quantidadeProduto', 'Quantidade deve ser um número positivo');
            isValid = false;
        }

        const valor = document.getElementById('precoProduto').value.trim();
        if (!valor || isNaN(parseFloat(valor.replace(',', '.')))) {
            mostrarErro('precoProduto', 'Preço é obrigatório e deve ser um número válido');
            isValid = false;
        }

        const tipoEmbalagem = document.getElementById('tipoEmbalagem').value.trim();
        if (!tipoEmbalagem) {
            mostrarErro('tipoEmbalagem', 'Tipo de embalagem é obrigatório');
            isValid = false;
        }

        const classificacao = document.getElementById('classificacaoProduto').value.trim();
        if (!classificacao) {
            mostrarErro('classificacaoProduto', 'Classificação é obrigatória');
            isValid = false;
        }
        // Verificação da imagem
        const imagemInput = document.getElementById('fotoProduto');
        const variavelControle = document.getElementById('produtoId')?.value;

        if (!imagemInput.files || imagemInput.files.length === 0) {
            if (!variavelControle) { // se for um cadastro novo, a imagem é obrigatória
                mostrarErro('foto', 'Imagem é obrigatória');
                isValid = false;
            }
            // se for edição e a imagem já existe no banco, não força nova imagem
        }


        if (isValid) {
            try {
                const formData = new FormData();
                formData.append("descricao", descricao);
                formData.append("valor", parseFloat(valor.replace(',', '.')));
                formData.append("validade", validade);
                formData.append("quantidade", parseInt(quantidade));
                formData.append("tipo_produto", tipoEmbalagem);
                formData.append("classe", classificacao);

                const imagemInput = document.getElementById('fotoProduto');
                const imagemFile = imagemInput.files[0];
                if (imagemFile) {
                    formData.append("imagem", imagemFile);
                }
                
                const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

                let produtoId = document.getElementById('produtoId') ? document.getElementById('produtoId').value : null;
                let response;

                if (produtoId) {
                    response = await fetch(`/api/produtos/${produtoId}/`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrf
                        },
                        body: formData
                    });
                } else {
                    response = await fetch(`/api/produtos/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrf
                        },
                        body: formData
                    });
                }

                if (response.ok) {
                    fecharDialog();
                    window.location.reload(); 
                } else {
                    const errorData = await response.json();
                    console.error('Erro no cadastro/edição:', errorData);
                    // Aqui você pode mostrar mensagens de erro específicas
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }
    }

    uploadInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const uploadLabel = document.querySelector('.upload-label');
                uploadLabel.classList.add('has-image');
                uploadLabel.style.backgroundImage = `url(${e.target.result})`;
                uploadLabel.style.backgroundSize = "contain";
                uploadLabel.style.backgroundRepeat = "no-repeat";
                uploadLabel.style.backgroundPosition = "center";
                uploadLabel.innerHTML = `
                    <button type="button" class="remove-image" onclick="removerImagem()">×</button>
                `;
            };
            reader.readAsDataURL(file);
        }
    });

    openDialogButton.addEventListener('click', abrirDialog);
    closeButton.addEventListener('click', fecharDialog);
    
    cadastroDialog.addEventListener('click', function(e) {
        if (e.target === cadastroDialog) {
            fecharDialog();
        }
    });
    
    cadastroForm.addEventListener('submit', handleSubmit);
});

function removerImagem() {
    const uploadLabel = document.querySelector('.upload-label');
    uploadLabel.classList.remove('has-image');
    uploadLabel.style.backgroundImage = '';
        
    uploadLabel.innerHTML = `
        <div class="upload-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="upload-text">
            <span class="upload-main-text">Arraste e solte o arquivo de imagem aqui para realizar upload</span>
            <span class="upload-sub-text">JPEG - PNG - WEBP</span>
        </div>
    `;
}

async function editarProduto(idProduto){
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Assumindo que você tem uma API para buscar os dados do produto
    const response = await fetch(`/api/produtos/${idProduto}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrf
        }
    });
    const dados = await response.json();

    document.getElementById('descricaoProduto').value = dados.descricao;
    document.getElementById('validadeProduto').value = dados.validade;
    document.getElementById('quantidadeProduto').value = dados.quantidade;
    document.getElementById('precoProduto').value = dados.valor.replace('.', ','); // Ajuste para o formato de exibição
    document.getElementById('tipoEmbalagem').value = dados.tipo_produto;
    document.getElementById('classificacaoProduto').value = dados.classe;
    
    if (dados.imagem) {
        const uploadLabel = document.querySelector('.upload-label');
        uploadLabel.classList.add("has-image");
        uploadLabel.style.backgroundImage = `url(${dados.imagem})`;
        uploadLabel.style.backgroundSize = "contain";
        uploadLabel.style.backgroundRepeat = "no-repeat";
        uploadLabel.style.backgroundPosition = "center";

        uploadLabel.innerHTML = `
            <button type="button" class="remove-image" onclick="removerImagem()">×</button>
        `;
    }

    document.getElementById('cadastroDialog').showModal();

    document.getElementById('produtoId').value = idProduto;
}




