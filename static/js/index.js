function fecharPopup() {
        const popup = document.getElementById('popup-alerta');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    setTimeout(fecharPopup, 5000);