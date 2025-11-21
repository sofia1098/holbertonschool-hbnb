document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Obtener los valores del formulario
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // Validación mínima
            if (!email || !password) {
                alert("Por favor completa todos los campos.");
                return;
            }

            // Intentar login
            await loginUser(email, password);
        });
    }
});

// Función para hacer login

async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();

            // Guardar JWT en cookie
            document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;

            // Redirigir al index
            window.location.href = "index.html";
        } else {
            const errorData = await response.json();
            alert("Login incorrecto: " + (errorData.error || response.statusText));
        }

    } catch (error) {
        console.error("Error de conexión:", error);
        alert("No se pudo conectar con el servidor.");
    }
}
