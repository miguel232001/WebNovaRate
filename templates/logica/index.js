document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencia al botón
    const startButton = document.getElementById('startButton');

    // Agregar evento de clic al botón
    startButton.addEventListener('click', function() {
        // Efecto visual al hacer clic
        this.style.transform = 'scale(0.95)';

        // Simular navegación a la página de login
        console.log('Navegando a la página de login...');

        // Aquí iría la lógica de navegación real
        // Por ejemplo: window.location.href = 'login.html';

        // Restaurar el tamaño del botón después de un breve momento
        setTimeout(() => {
            this.style.transform = '';
        }, 200);

        // Mostrar mensaje de transición (en una aplicación real, esto sería una navegación)
        showTransitionMessage();
    });

    // Efecto de escritura para el tagline
    const tagline = document.querySelector('.tagline');
    const originalText = tagline.textContent;
    tagline.textContent = '';

    let charIndex = 0;
    const typeWriter = () => {
        if (charIndex < originalText.length) {
            tagline.textContent += originalText.charAt(charIndex);
            charIndex++;
            setTimeout(typeWriter, 50);
        }
    };

    // Iniciar el efecto de escritura después de un breve retraso
    setTimeout(typeWriter, 1000);

    // Función para mostrar mensaje de transición
    function showTransitionMessage() {
        // Crear elemento de mensaje
        const message = document.createElement('div');
        message.textContent = 'Redirigiendo al login...';
        message.style.position = 'fixed';
        message.style.top = '20px';
        message.style.left = '50%';
        message.style.transform = 'translateX(-50%)';
        message.style.backgroundColor = 'rgba(36, 208, 241, 0.9)';
        message.style.color = 'white';
        message.style.padding = '10px 20px';
        message.style.borderRadius = '5px';
        message.style.zIndex = '1000';
        message.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.2)';

        // Agregar mensaje al documento
        document.body.appendChild(message);

        // Eliminar mensaje después de 2 segundos
        setTimeout(() => {
            document.body.removeChild(message);
        }, 2000);
    }

    // Efecto de parpadeo suave para el botón
    setInterval(() => {
        startButton.style.boxShadow = `
            0 0 ${5 + Math.random() * 5}px rgba(36, 208, 241, 0.7),
            inset 0 0 ${5 + Math.random() * 5}px rgba(36, 208, 241, 0.2)
        `;
    }, 3000);
});