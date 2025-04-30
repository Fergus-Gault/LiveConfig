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
      // For save action, use normal submission with page refresh
      if (this.action.includes('/save')) {
        return;
      }
      
      // For reload action, send fetch request and update form values
      if (this.action.includes('/reload')) {
        e.preventDefault();
        const reloadBtn = this.querySelector('.reload-button');
        if (reloadBtn) {
          reloadBtn.innerHTML = '<i class="bi bi-arrow-repeat spin me-1"></i> Reloading...';
          reloadBtn.disabled = true;
        }
        
        fetch(this.action, {
          method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showSuccess('Configuration reloaded successfully!');
            
            // Instead of refreshing the page, fetch the current page again to get updated HTML
            fetch(window.location.pathname)
              .then(response => response.text())
              .then(html => {
                // Create a new DOM from the fetched HTML
                const parser = new DOMParser();
                const newDoc = parser.parseFromString(html, 'text/html');
                
                // Find all form inputs and update their values
                const currentForms = document.querySelectorAll('form');
                currentForms.forEach(form => {
                  const valueInput = form.querySelector('input[name="value"]');
                  if (valueInput) {
                    // Get identifiers to find the matching form in the new document
                    const instanceName = form.querySelector('input[name="instance_name"]')?.value;
                    const attributeName = form.querySelector('input[name="attribute"]')?.value;
                    const variableName = form.querySelector('input[name="name"]')?.value;
                    
                    if (instanceName && attributeName) {
                      // For classes.html - build a more specific selector
                      const selector = `form input[name="instance_name"][value="${instanceName}"][type="hidden"] + input[name="attribute"][value="${attributeName}"]`;
                      const matchingAttrInput = newDoc.querySelector(selector);
                      if (matchingAttrInput) {
                        const newForm = matchingAttrInput.closest('form');
                        if (newForm) {
                          const newValue = newForm.querySelector('input[name="value"]')?.value;
                          if (newValue !== undefined) {
                            valueInput.value = newValue;
                          }
                        }
                      }
                    } else if (variableName) {
                      // For variables.html - build a more specific selector
                      const selector = `form input[name="name"][value="${variableName}"]`;
                      const matchingVarInput = newDoc.querySelector(selector);
                      if (matchingVarInput) {
                        const newForm = matchingVarInput.closest('form');
                        if (newForm) {
                          const newValue = newForm.querySelector('input[name="value"]')?.value;
                          if (newValue !== undefined) {
                            valueInput.value = newValue;
                          }
                        }
                      }
                    }
                  }
                });
                
                // Reset reload button
                if (reloadBtn) {
                  reloadBtn.innerHTML = '<i class="bi bi-arrow-clockwise me-1"></i> Reload';
                  reloadBtn.disabled = false;
                }
              });
          } else {
            throw new Error('Failed to reload configuration');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          const alert = document.createElement('div');
          alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
          alert.setAttribute('role', 'alert');
          alert.innerHTML = `
            <strong>Error!</strong> Failed to reload configuration.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          `;
          document.body.appendChild(alert);
          
          // Reset button state
          if (reloadBtn) {
            reloadBtn.innerHTML = '<i class="bi bi-arrow-clockwise me-1"></i> Reload';
            reloadBtn.disabled = false;
          }
        });
        return;
      }
      
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
