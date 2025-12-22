document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('confirmModal');
    const cancelBtn = document.getElementById('cancelBtn');
    const confirmBtn = document.getElementById('confirmBtn');
    let targetForm = null;

    // Handle Cancel
    if (cancelBtn) {
        cancelBtn.onclick = () => {
            modal.style.display = 'none';
            targetForm = null;
        };
    }

    // Handle Confirm
    if (confirmBtn) {
        confirmBtn.onclick = () => {
            if (targetForm) {
                targetForm.submit();
            }
        };
    }

    // Click outside to close
    if (modal) {
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        };
    }

    // Attach to all delete forms
    document.querySelectorAll('form[action*="/delete"]').forEach(form => {
        form.onsubmit = (e) => {
            e.preventDefault();
            targetForm = form;
            if (modal) {
                modal.style.display = 'flex';
            } else {
                // Fallback if modal is missing for some reason
                if (confirm('Are you sure you want to delete this?')) {
                    form.submit();
                }
            }
        };
    });
});
