// Configuración global - Kafeehaus
window.APP_CONFIG = {
    apiBaseUrl: '/api',
    pages: {
        home: '/',
        login: '/iniciarsesion', 
        menu: '/menu',
        cart: '/carrito',
        payment: '/pago',
        admin: '/adminpanel'
    }
};

// Función para navegar
function navigateTo(pageKey) {
    const pagePath = APP_CONFIG.pages[pageKey];
    if (pagePath) {
        window.location.href = pagePath;
    } else {
        window.location.href = '/';
    }
}

// Función para llamadas API
async function apiCall(endpoint, options = {}) {
    const url = APP_CONFIG.apiBaseUrl + endpoint;
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };
    
    if (config.body && typeof config.body !== 'string') {
        config.body = JSON.stringify(config.body);
    }
    
    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en API Call:', error);
        throw error;
    }
}

// Función simple para mostrar errores
function showError(message) {
    alert('Error: ' + message);
}

//console.log('✅ Configuración cargada');