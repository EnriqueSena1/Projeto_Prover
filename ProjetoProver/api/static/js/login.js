async function Login(evento) {
    evento.preventDefault();

    const email = document.getElementById('email').value;
    console.log(email)
    const senha = document.getElementById('senha').value;
    console.log(senha)
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    

    try {
        console.log("entrou")
        const data = await apiRequest(
            '/api/login/',
            'POST',
            { email: email, senha: senha },
            { 'X-CSRFToken': csrf }
        );
        console.log(data) // aqui me retorna none... o que errei? ainda fala credenciais invalidas

        if (!data) {
            throw new Error('Email ou senha inválidos.');
        }

        // Verificação baseada no campo "tipo" do CustomUser
        switch (data.tipo) {
            case 'administrador':
                window.location.href = '/HomeAdm/';
                break;
            case 'vendedor':
                window.location.href = '/HomeVend/';
                break;
            case 'cliente':
                window.location.href = '/HomeUser/';
                break;
            default:
                alert("Usuário sem permissão.");
        }

    } catch (error) {
        console.error('Erro ao logar:', error);
        alert(error.message || 'Erro desconhecido.');
    }
}

// Vincula a função ao formulário
document.getElementById('loginForm').addEventListener('submit', Login);
