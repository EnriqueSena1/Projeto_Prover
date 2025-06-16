// Selecionando os elementos do popup e formulário
document.addEventListener("DOMContentLoaded", function () {
    // Elementos do DOM
    const cadastroDialog = document.getElementById('cadastroDialog');
    const openDialogButton = document.getElementById('openDialogButton');
    const closeButton = document.getElementById('closeButton');
    const cadastroForm = document.getElementById('cadastroForm');
    const uploadInput = document.getElementById('fotoCliente');
    const uploadPreview = document.getElementById('uploadPreview');
    const clientesContainer = document.getElementById('lista-clientes');

    // Função para abrir o dialog
    function abrirDialog() {
        cadastroDialog.showModal();
        document.body.style.overflow = 'hidden';
    }

    // Função para fechar o dialog
    function fecharDialog() {
        cadastroDialog.close();
        document.body.style.overflow = 'auto';
        limparFormulario();
    }

    // Função para limpar o formulário
    function limparFormulario() {
        cadastroForm.reset();
        uploadPreview.innerHTML = '';
        limparErros();
    }

    // Função para limpar mensagens de erro
    function limparErros() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(error => error.textContent = '');
        
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => input.classList.remove('error'));
    }

    // Função para mostrar erro
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

    // Validação de email
    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    // Função para processar o cadastro
    async function handleSubmit(event) {
        event.preventDefault();
        limparErros();

        let isValid = true;
        
        // Validar nome
        const nome = document.getElementById('nomeCliente').value.trim();
        if (!nome) {
            mostrarErro('nomeCliente', 'Nome é obrigatório');
            isValid = false;
        }

        // Validar email
        const email = document.getElementById('emailCliente').value.trim();
        if (!email) {
            mostrarErro('emailCliente', 'Email é obrigatório');
            isValid = false;
        } else if (!validarEmail(email)) {
            mostrarErro('emailCliente', 'Email inválido');
            isValid = false;
        }

        // Validar confirmação de email
        const confirmarEmail = document.getElementById('confirmarEmail').value.trim();
        if (!confirmarEmail) {
            mostrarErro('confirmarEmail', 'Confirmação de email é obrigatória');
            isValid = false;
        } else if (email !== confirmarEmail) {
            mostrarErro('confirmarEmail', 'Emails não coincidem');
            isValid = false;
        } else {
        // Verificar se email já existe
        try {
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const clienteId = document.getElementById('clienteId')?.value?.trim();

            const response = await fetch('/validarEmail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf
                },
                body: JSON.stringify({ email, clienteId })
            });

            const data = await response.json();
            if (data.existe) {
                mostrarErro('emailCliente', 'Este email já está em uso');
                isValid = false;
            }
        } catch (error) {
            console.error('Erro ao verificar email:', error);
            mostrarErro('emailCliente', 'Erro ao verificar email. Tente novamente.');                isValid = false;
        }
    }

    // Validar senha
    const senha = document.getElementById('senhaCliente').value;
    const clienteId = document.getElementById('clienteId')?.value?.trim();

    if (!clienteId) {
        if (!senha) {
            mostrarErro('senhaCliente', 'Senha é obrigatória');
            isValid = false;
        } else if (senha.length < 6) {
            mostrarErro('senhaCliente', 'Senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }
    } else {
        // Edição → senha opcional
        if (senha && senha.length < 6) {
            mostrarErro('senhaCliente', 'Senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }
    }

    // Validar saldo
    const saldo = document.getElementById('saldoCliente').value.trim();
    if (!saldo) {
        mostrarErro('saldoCliente', 'Saldo é obrigatório');
        isValid = false;
    } else if (isNaN(parseFloat(saldo.replace(',', '.')))) {
        mostrarErro('saldoCliente', 'Saldo deve ser um número válido');
        isValid = false;
    }

    const imagemInput = document.getElementById('fotoCliente');
    const variavelControle = document.getElementById('clienteId')?.value;

    if (!imagemInput.files || imagemInput.files.length === 0) {
        if (!variavelControle) { // se for um cadastro novo, a imagem é obrigatória
            mostrarErro('foto', 'Imagem é obrigatória');
            isValid = false;
        }
        // se for edição e a imagem já existe no banco, não força nova imagem
    }

    // Se a validação passou, enviar os dados
    if (isValid) {
        try {
            let nome_cliente = document.getElementById('nomeCliente').value;
            let email_cliente = document.getElementById('emailCliente').value;
            let senha_cliente = document.getElementById('senhaCliente').value;
            let saldo_cliente = document.getElementById('saldoCliente').value;
            let imagemInput = document.getElementById('fotoCliente');
            let imagemFile = imagemInput.files[0];

            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Criação do formData para envio com imagem
            const formData = new FormData();
            formData.append("nome", nome_cliente);
            formData.append("email", email_cliente);
            formData.append("senha", senha_cliente);
            formData.append("saldo", saldo_cliente);
            formData.append("is_active", true);

            if (imagemFile) {
                formData.append("img", imagemFile);
            }
                
            let editar_valor = null
            editar_valor = document.getElementById('clienteId').value
            let response ;
            if (editar_valor){
                response = await fetch(`/api/user/${editar_valor}/`, {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': csrf
                    },
                    body: formData
                });

                editar_valor = null
            }else{
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
                console.error('Erro no cadastro:', errorData);
                // Aqui você pode mostrar mensagens de erro específicas
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
                
        }
    }
    }

    // imagem 
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

    // Event listeners
    openDialogButton.addEventListener('click', abrirDialog);
    closeButton.addEventListener('click', fecharDialog);
    clientesContainer.addEventListener('click', function(e) {
    if (e.target.classList.contains('icon-editar')) {
      const idCliente = e.target.getAttribute('data-id');
      if (idCliente) {
        editarCliente(idCliente);
      }
    }
  });
    
    // Fechar dialog clicando no backdrop
    cadastroDialog.addEventListener('click', function(e) {
        if (e.target === cadastroDialog) {
            removerImagem();
            fecharDialog();
        }
    });
    
    // CORREÇÃO: Registrar o event listener apenas uma vez
    cadastroForm.addEventListener('submit', handleSubmit);
});

// Função para remover imagem
function removerImagem() {
    let verificar = document.getElementById("openDialogButton").value

    const uploadLabel = document.querySelector('.upload-label');
    uploadLabel.classList.remove('has-image');
    uploadLabel.style.backgroundImage = '';
        
    // Restaura o conteúdo original
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

async function editarCliente(idUsuario){
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const dados = await apiRequest(`/api/user/${idUsuario}/`, 'GET', null, { 'X-CSRFToken': csrf });

    document.getElementById('nomeCliente').value = dados.first_name
    document.getElementById('emailCliente').value = dados.email
    document.getElementById("confirmarEmail").value = dados.email
    document.getElementById('saldoCliente').value = dados.saldo;
    
    if (dados.img) {
        const uploadBox = document.querySelector('.upload-label');
        uploadBox.classList.add("has-image");
        uploadBox.style.backgroundImage = `url(${dados.img})`;
        uploadBox.style.backgroundSize = "contain";
        uploadBox.style.backgroundRepeat = "no-repeat";
        uploadBox.style.backgroundPosition = "center";

        uploadBox.innerHTML = `
            <button type="button" class="remove-image" onclick="removerImagem()">×</button>
        `;
    }

    document.getElementById('cadastroDialog').showModal()

    document.getElementById('clienteId').value = idUsuario;
}

