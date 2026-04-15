function abrirModal(id) {
    const btnConfirmar = document.getElementById("btnConfirmarEliminar");
    if (btnConfirmar) {
        
        btnConfirmar.href = "/eliminar_reserva/" + id;
    }
    document.getElementById('modalCancelar').style.display = 'flex';
}

function cerrarModal() {
    document.getElementById('modalCancelar').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('modalCancelar');
    if (event.target == modal) {
        cerrarModal();
    }
}