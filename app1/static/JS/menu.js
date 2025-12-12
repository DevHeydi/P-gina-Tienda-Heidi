// menu.js - Opcional para mejor experiencia en móviles
document.addEventListener("DOMContentLoaded", function() {
    const submenuContainers = document.querySelectorAll('.submenu-container');
    
    // Para móviles: toggle al hacer click
    if (window.innerWidth <= 992) {
        submenuContainers.forEach(container => {
            const toggle = container.querySelector('.submenu-toggle');
            const submenu = container.querySelector('.submenu');
            
            if (toggle && submenu) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Cerrar otros submenús
                    submenuContainers.forEach(other => {
                        if (other !== container) {
                            const otherSubmenu = other.querySelector('.submenu');
                            if (otherSubmenu) {
                                otherSubmenu.style.display = 'none';
                            }
                        }
                    });
                    
                    // Alternar submenú actual
                    if (submenu.style.display === 'block') {
                        submenu.style.display = 'none';
                    } else {
                        submenu.style.display = 'block';
                    }
                });
            }
        });
        
        // Cerrar submenús al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.submenu-container')) {
                document.querySelectorAll('.submenu').forEach(submenu => {
                    submenu.style.display = 'none';
                });
            }
        });
    }
});