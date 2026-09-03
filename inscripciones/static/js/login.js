const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        const username = form.querySelector('input[name="username"]');
        const password = form.querySelector('input[name="password"]');
        
        if (!username.value.trim() || !password.value.trim()) {
            e.preventDefault();
            alert('Por favor completa todos los campos');
            return false;
        }
    });
    
    document.querySelectorAll('input[type="text"], input[type="password"]').forEach(input => {
        input.classList.add('form-control');
        if (input.type === 'text') input.placeholder = 'Ingresa tu usuario';
        if (input.type === 'password') input.placeholder = 'Ingresa tu contraseña';
    });