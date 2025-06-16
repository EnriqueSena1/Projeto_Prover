document.addEventListener("DOMContentLoaded", function () {
    const cadastroDialog = document.getElementById("cadastroDialog");
    const openDialogButton = document.getElementById("openDialogButton"); 
    const closeButton = document.querySelector(".close-button");
    const cadastroForm = document.getElementById("cadastroForm");
    const uploadInput = document.getElementById("fotoCliente");
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
        removerImagem(); 
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
        
        const nome = document.getElementById('nomeCliente').value.trim();
        if (!nome) {
            mostrarErro('nomeCliente', 'Nome do vendedor é obrigatório');
            isValid = false;
        }

        const email = document.getElementById("emailCliente").value.trim();
        if (!email || !/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(email)) {
            mostrarErro("emailCliente", "Email inválido ou obrigatório");
            isValid = false;
        }

        const confirmarEmail = document.getElementById("confirmarEmail").value.trim();
        if (email !== confirmarEmail) {
            mostrarErro("confirmarEmail", "Os emails não coincidem");
            isValid = false;
        }

        // Verificação de email existente (apenas se os emails coincidirem e forem válidos)
        if (isValid && email === confirmarEmail) {
            try {
                const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
                const vendedorId = document.getElementById("vendedorId")?.value?.trim();

                const response = await fetch("/validarEmail/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrf
                    },
                    body: JSON.stringify({ email, vendedorId })
                });

                const data = await response.json();
                if (data.existe) {
                    mostrarErro("emailCliente", "Este email já está em uso");
                    isValid = false;
                }
            } catch (error) {
                console.error("Erro ao verificar email:", error);
                mostrarErro("emailCliente", "Erro ao verificar email. Tente novamente.");
                isValid = false;
            }
        }

        const loja = document.getElementById('lojaVendedor').value.trim();
        if (!loja) {
            mostrarErro('lojaVendedor', 'Nome da loja é obrigatório');
            isValid = false;
        }

        const senha = document.getElementById('senhaCliente').value.trim();
        const vendedorId = document.getElementById('vendedorId')?.value?.trim();

        if (!vendedorId) {
            // Cadastro novo: senha é obrigatória
            if (!senha) {
                mostrarErro('senhaCliente', 'A senha é obrigatória');
                isValid = false;
            } else if (senha.length < 6) {
                mostrarErro('senhaCliente', 'A senha deve ter no mínimo 6 caracteres');
                isValid = false;
            }
        } else {
            // Edição: senha é opcional, mas se preenchida, deve ter no mínimo 6 caracteres
            if (senha && senha.length < 6) {
                mostrarErro('senhaCliente', 'A senha deve ter no mínimo 6 caracteres');
                isValid = false;
            }
        }

        // Verificação da imagem
        const imagemInput = document.getElementById('fotoCliente');
        const variavelControle = document.getElementById('vendedorId')?.value;

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
                formData.append("nome", nome);
                formData.append("email", email);
                formData.append("loja", loja);
                formData.append("senha", senha);
                formData.append("tipo", "vendedor");
                formData.append("is_active", true);


                const imagemFile = imagemInput.files[0];
                if (imagemFile) {
                    formData.append("img", imagemFile);
                }
                
                const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

                let vendedorId = document.getElementById('vendedorId') ? document.getElementById('vendedorId').value : null;
                let response;

                if (vendedorId) {
                    response = await fetch(`/api/user/${vendedorId}/`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrf
                        },
                        body: formData
                    });
                } else {
                    response = await fetch(`/api/user/`, {
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

    // Verifica se o botão openDialogButton existe antes de adicionar o event listener
    if (openDialogButton) {
        openDialogButton.addEventListener('click', abrirDialog);
    }
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

async function editarVendedor(idVendedor){
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Assumindo que você tem uma API para buscar os dados do vendedor
    const response = await fetch(`/api/user/${idVendedor}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrf
        }
    });
    const dados = await response.json();

    document.getElementById('nomeCliente').value = dados.first_name;
    document.getElementById('emailCliente').value = dados.email;
    document.getElementById('confirmarEmail').value = dados.email;
    document.getElementById('lojaVendedor').value = dados.loja;
    // Senha não deve ser preenchida por segurança
    
    if (dados.img) {
        const uploadLabel = document.querySelector('.upload-label');
        uploadLabel.classList.add("has-image");
        uploadLabel.style.backgroundImage = `url(${dados.img})`;
        uploadLabel.style.backgroundSize = "contain";
        uploadLabel.style.backgroundRepeat = "no-repeat";
        uploadLabel.style.backgroundPosition = "center";

        uploadLabel.innerHTML = `
            <button type="button" class="remove-image" onclick="removerImagem()">×</button>
        `;
    }

    document.getElementById('cadastroDialog').showModal();

    document.getElementById('vendedorId').value = idVendedor;
    
}


