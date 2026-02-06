// Auto-focus search input when dropdown opens
document.addEventListener('DOMContentLoaded', function() {
    // Use MutationObserver to detect when dropdown content appears
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                // Check if the added node is a dropdown content container
                if (node.nodeType === 1 && node.classList && 
                    node.classList.contains('dash-dropdown-content')) {
                    // Find the search input inside it
                    const searchInput = node.querySelector('.dash-dropdown-search');
                    if (searchInput) {
                        // Small delay to ensure dropdown is fully rendered
                        setTimeout(() => {
                            searchInput.focus();
                        }, 50);
                    }
                }
            });
        });
    });

    // Start observing the document body for added nodes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});