async function Login(evento) {
    evento.preventDefault();

    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    const erroEmail = document.getElementById('erro-email');
    const erroSenha = document.getElementById('erro-senha');

    // Limpar erros antigos
    emailInput.classList.remove('erro');
    senhaInput.classList.remove('erro');
    erroEmail.textContent = '';
    erroSenha.textContent = '';

    const email = emailInput.value;
    const senha = senhaInput.value;
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const data = await apiRequest(
            '/api/login/',
            'POST',
            { email: email, senha: senha },
            { 'X-CSRFToken': csrf }
        );

        if (!data || !data.tipo) {
            throw new Error('Credenciais inválidas.');
        }

        // Redirecionamento
        switch (data.tipo) {
            case 'administrador':
                window.location.href = '/relatorio/';
                break;
            case 'vendedor':
                window.location.href = '/CarrinhoVend/';
                break;
            case 'cliente':
                window.location.href = '/HomeUser/';
                break;
            default:
                throw new Error("Usuário sem permissão.");
        }

    } catch (error) {
        // Estilo de erro visual
        emailInput.classList.add('erro');
        senhaInput.classList.add('erro');
        erroSenha.textContent = 'Email ou senha incorretos.';
    }
}

document.getElementById('loginForm').addEventListener('submit', Login);
