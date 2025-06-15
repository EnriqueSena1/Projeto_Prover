document.addEventListener("DOMContentLoaded", function() {
    const addToCartButtons = document.querySelectorAll(".add-to-cart-button");
    const toast = document.getElementById("toast");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", async function() {
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const formData = new FormData();
            formData.append('exibir_no_carrinho', 'true'); // Campo booleano como string

            try {
                const response = await fetch(`/api/produtos/${button.value}/`, {
                    method: 'PATCH',
                    headers: {
                        'X-CSRFToken': csrf
                    },
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Erro ao atualizar produto');
                }

                // Mostra o toast
                toast.classList.remove("hidden");
                toast.classList.add("show");

                // Oculta após 1 segundo
                setTimeout(() => {
                    toast.classList.remove("show");
                    setTimeout(() => {
                        toast.classList.add("hidden");
                    }, 300); 
                }, 1000);
            } catch (error) {
                console.error(error);
                alert("Erro ao adicionar o produto ao carrinho.");
            }
        });
    });
});
