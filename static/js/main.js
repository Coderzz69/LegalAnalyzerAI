document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission and show loading spinner
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('document-upload');
            if (!fileInput.files.length) {
                e.preventDefault();
                
                // Create and show toast instead of alert
                const toast = document.createElement('div');
                toast.className = 'position-fixed bottom-0 end-0 p-3';
                toast.style.zIndex = '1050';
                toast.innerHTML = `
                    <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="toast-header bg-danger text-white">
                            <i class="bi bi-exclamation-circle me-2"></i>
                            <strong class="me-auto">Error</strong>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            Please select a document to upload.
                        </div>
                    </div>
                `;
                document.body.appendChild(toast);
                
                // Remove toast after 3 seconds
                setTimeout(() => {
                    toast.remove();
                }, 3000);
                
                return;
            }
            
            // Create and show loading spinner with animated background
            const spinner = document.createElement('div');
            spinner.className = 'spinner-container';
            spinner.innerHTML = `
                <div class="position-absolute w-100 h-100" style="background: radial-gradient(circle, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.9) 100%);"></div>
                <div class="position-relative">
                    <div class="spinner-grow text-primary mx-1" role="status" style="width: 1.5rem; height: 1.5rem; animation-delay: 0s;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-info mx-1" role="status" style="width: 1.5rem; height: 1.5rem; animation-delay: 0.2s;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-primary mx-1" role="status" style="width: 1.5rem; height: 1.5rem; animation-delay: 0.4s;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="spinner-message mt-4">Analyzing your legal document with AI...</p>
                    <p class="text-muted small mt-2">This may take a few moments</p>
                </div>
            `;
            document.body.appendChild(spinner);
            
            // Show the spinner
            spinner.style.display = 'flex';
        });
    }
    
    // Add animated hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(-2px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add animation to card hover
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // Handle print button with animation
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            // Add print animation
            this.innerHTML = '<i class="bi bi-printer-fill me-1"></i>Printing...';
            this.classList.add('disabled');
            
            // Delay printing slightly to show animation
            setTimeout(() => {
                window.print();
                
                // Reset button after printing
                setTimeout(() => {
                    this.innerHTML = '<i class="bi bi-printer me-1"></i>Print';
                    this.classList.remove('disabled');
                }, 500);
            }, 300);
        });
    }
    
    // Initialize code highlighting if on results page with animation
    if (document.getElementById('clausesAccordion')) {
        // Add fade-in animation to code blocks
        const codeBlocks = document.querySelectorAll('pre code');
        codeBlocks.forEach((block, index) => {
            block.style.opacity = '0';
            block.style.transition = 'opacity 0.5s ease';
            
            // Highlight and fade in with delay based on index
            setTimeout(() => {
                hljs.highlightElement(block);
                block.style.opacity = '1';
            }, 100 * index);
        });
        
        // Add subtle animation to accordion items when opened
        const accordionButtons = document.querySelectorAll('.accordion-button');
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                if (this.classList.contains('collapsed')) {
                    const accordionBody = this.parentNode.nextElementSibling;
                    accordionBody.style.animation = 'fadeIn 0.5s ease';
                }
            });
        });
    }
    
    // Make alerts dismissible with fade effect
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.classList.add('d-none');
                }, 500);
            });
        }
    });
    
    // Add CSS animation keyframes for fade-in effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
});
