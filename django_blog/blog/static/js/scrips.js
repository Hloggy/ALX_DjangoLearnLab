// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');

    // Check if user is authenticated
    const isAuthenticated = document.body.dataset.auth === 'true';

    // Get all navigation items
    const navItems = document.querySelectorAll('.nav-item');

    // Function to show or hide nav items based on auth status
    function updateNavigation() {
        navItems.forEach(item => {
            switch(item.id) {
                case 'nav-home':
                case 'nav-posts':
                    item.style.display = 'inline'; // Always show
                    break;
                case 'nav-profile':
                case 'nav-logout':
                    item.style.display = isAuthenticated ? 'inline' : 'none';
                    break;
                case 'nav-login':
                case 'nav-register':
                    item.style.display = isAuthenticated ? 'none' : 'inline';
                    break;
            }
        });
    }

    // Call the function to update navigation
    updateNavigation();
});
