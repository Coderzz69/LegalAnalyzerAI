document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission and show loading spinner
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('document-upload');
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Please select a document to upload.');
                return;
            }
            
            // Create and show loading spinner
            const spinner = document.createElement('div');
            spinner.className = 'spinner-container';
            spinner.innerHTML = `
                <div class="spinner-border text-light" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="spinner-message">Analyzing your document...</p>
            `;
            document.body.appendChild(spinner);
            
            // Show the spinner
            spinner.style.display = 'flex';
        });
    }
    
    // Handle print button
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Initialize code highlighting if on results page
    if (document.getElementById('clausesAccordion')) {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    // Automatically open first accordion item
    const firstAccordionButton = document.querySelector('.accordion-button');
    if (firstAccordionButton) {
        // It's already open by default due to the HTML structure
    }
    
    // Make alerts dismissible
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                alert.classList.add('d-none');
            });
        }
    });
});
