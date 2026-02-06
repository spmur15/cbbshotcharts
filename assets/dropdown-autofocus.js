// Auto-focus search input when dropdown opens
document.addEventListener('DOMContentLoaded', function() {
    let focusAttempts = 0;
    let maxAttempts = 10;
    let focusInterval = null;

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
                        // Reset attempts counter
                        focusAttempts = 0;
                        
                        // Clear any existing interval
                        if (focusInterval) {
                            clearInterval(focusInterval);
                        }
                        
                        // Try to focus repeatedly until it sticks or max attempts reached
                        focusInterval = setInterval(() => {
                            if (document.activeElement !== searchInput && focusAttempts < maxAttempts) {
                                searchInput.focus();
                                focusAttempts++;
                            } else {
                                clearInterval(focusInterval);
                            }
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
    
    // Also stop the interval if dropdown closes
    const closeObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.removedNodes.forEach(function(node) {
                if (node.nodeType === 1 && node.classList && 
                    node.classList.contains('dash-dropdown-content')) {
                    if (focusInterval) {
                        clearInterval(focusInterval);
                    }
                }
            });
        });
    });
    
    closeObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
});