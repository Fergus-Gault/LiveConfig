// Add active class to current nav item
document.addEventListener('DOMContentLoaded', function() {
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
      link.classList.add('active');
    }
  });

  // Add animation to success messages
  const showSuccess = (message) => {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
      <strong>${message}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
      alert.classList.remove('show');
      setTimeout(() => alert.remove(), 300);
    }, 3000);
  };

  // Add form submission handler
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      if (this.action.includes('/save')) return; // Let save action go through normal submission
      
      e.preventDefault();
      const formData = new FormData(this);
      const url = this.action || window.location.href;
      
      fetch(url, {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          // For update forms, just update the input value
          const valueInput = this.querySelector('input[name="value"]');
          if (valueInput) {
            showSuccess('Value updated successfully!');
          } else {
            showSuccess('Action completed successfully!');
            // For trigger forms, reset the form
            this.reset();
          }
        } else {
          throw new Error('Network response was not ok');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
        alert.setAttribute('role', 'alert');
        alert.innerHTML = `
          <strong>Error!</strong> Something went wrong.
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.body.appendChild(alert);
      });
    });
  });
});
