document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
    deleteModal.addEventListener("show.bs.modal", event => {
        const button = event.relatedTarget;
        const recipeId = button.getAttribute("data-recipe-id");
        
        const form = document.getElementById("delete-form");
        form.action = `/delete_recipe/${recipeId}`;
        console.log(form.action)
    });

    // Recipe form stars
    document.querySelectorAll('.star-rating input').forEach(input => {
        input.addEventListener('change', () => {
            const stars = input.closest('.star-rating').querySelectorAll('label');
            stars.forEach((star, index) => {
                star.style.color = index < 5 - input.value ? '#ccc' : 'gold';
            });
        });
    });

});

/**
 * Recipe Website - Main JavaScript
 */

// ============ DOCUMENT READY ============
document.addEventListener('DOMContentLoaded', function() {
    console.log('Site de Receitas carregado com sucesso!');
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize alerts auto-dismiss
    initAlerts();
    
    // Initialize animations
    initAnimations();
    
    // Initialize recipe page features
    initRecipePage();
});


// ============ BOOTSTRAP TOOLTIPS ============
function initTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


// ============ AUTO-DISMISS ALERTS ============
function initAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5 seconds
    });
}


// ============ SCROLL ANIMATIONS ============
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe all cards
    document.querySelectorAll('.card, .recipe-card').forEach(card => {
        observer.observe(card);
    });
}


// ============ RECIPE PAGE FEATURES ============
function initRecipePage() {
    // Checkbox for ingredients (mark as used)
    document.querySelectorAll('.ingredient-item .form-check-input').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.parentElement.parentElement.style.opacity = '0.6';
                this.parentElement.querySelector('label').style.textDecoration = 'line-through';
            } else {
                this.parentElement.parentElement.style.opacity = '1';
                this.parentElement.querySelector('label').style.textDecoration = 'none';
            }
        });
    });
    
    // Share button
    const shareBtn = document.getElementById('shareBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', async function() {
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: document.querySelector('.recipe-hero h1')?.textContent || 'Receita',
                        text: 'Confira esta receita incrível!',
                        url: window.location.href
                    });
                } catch (err) {
                    console.log('Erro ao compartilhar:', err);
                }
            } else {
                // Fallback: copy URL
                navigator.clipboard.writeText(window.location.href);
                alert('Link copiado para a área de transferência!');
            }
        });
    }
}


// ============ IMAGE PREVIEW ============
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(previewId).src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}


// ============ FORM VALIDATION ============
(function () {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();


// ============ SEARCH FUNCTIONALITY ============
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const searchTerm = e.target.value.toLowerCase();
            console.log('Buscando por:', searchTerm);
            // Adicionar lógica de busca aqui
        }, 300));
    }
}


// ============ DEBOUNCE UTILITY ============
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


// ============ SMOOTH SCROLL ============
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});


// ============ BACK TO TOP BUTTON ============
const backToTopBtn = document.createElement('button');
backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
backToTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle';
backToTopBtn.style.display = 'none';
backToTopBtn.style.width = '50px';
backToTopBtn.style.height = '50px';
backToTopBtn.style.zIndex = '1000';
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTopBtn.style.display = 'block';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});


// ============ LAZY LOADING IMAGES ============
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img.lazy').forEach(img => {
        imageObserver.observe(img);
    });
}


// ============ NAVBAR SCROLL EFFECT ============
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll && currentScroll > 100) {
        // Scrolling down
        navbar.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        navbar.style.transform = 'translateY(0)';
    }
    
    lastScroll = currentScroll;
});


// ============ COPY TO CLIPBOARD ============
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado para a área de transferência!');
    }).catch(err => {
        console.error('Falha ao copiar:', err);
    });
}


// ============ TOAST NOTIFICATION ============
function showToast(message, type = 'success') {
    const toastContainer = document.createElement('div');
    toastContainer.className = 'position-fixed top-0 end-0 p-3';
    toastContainer.style.zIndex = '11';
    
    toastContainer.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Notificação</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    document.body.appendChild(toastContainer);
    
    setTimeout(() => {
        toastContainer.remove();
    }, 3000);
}


// ============ PRINT RECIPE ============
function printRecipe() {
    window.print();
}


// ============ EXPORT FUNCTIONS ============
window.recipeWebsite = {
    previewImage,
    copyToClipboard,
    showToast,
    printRecipe
};
