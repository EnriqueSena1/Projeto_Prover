document.addEventListener("DOMContentLoaded", function () {
    const openDialogButton = document.getElementById("openDialogButton");
    const cadastroDialog = document.getElementById("cadastroDialog");

    if (openDialogButton && cadastroDialog) {
        openDialogButton.addEventListener("click", function () {
            cadastroDialog.showModal();
        });
    }
});
