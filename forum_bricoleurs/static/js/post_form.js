document.addEventListener('DOMContentLoaded', function() {
    const addStepBtn = document.getElementById('add-step');
    const stepsContainer = document.getElementById('steps-container');
    let stepCount = document.querySelectorAll('.step-form').length;

    if (addStepBtn) {
        addStepBtn.addEventListener('click', function() {
            stepCount++;
            
            const stepForm = document.createElement('div');
            stepForm.className = 'step-form mb-3 card';
            stepForm.innerHTML = `
                <div class="card-body">
                    <h4>Étape ${stepCount}</h4>
                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea name="steps-${stepCount-1}-description" class="form-control" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Image</label>
                        <input type="file" name="steps-${stepCount-1}-image" class="form-control" accept="image/*">
                    </div>
                    <input type="hidden" name="steps-${stepCount-1}-order" value="${stepCount}">
                    <button type="button" class="btn btn-danger remove-step">Supprimer cette étape</button>
                </div>
            `;

            stepsContainer.appendChild(stepForm);
            updateFormsetManagement();
        });

        // Remove step functionality
        stepsContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-step')) {
                e.target.closest('.step-form').remove();
                updateStepNumbers();
                updateFormsetManagement();
            }
        });
    }

    function updateStepNumbers() {
        const steps = document.querySelectorAll('.step-form');
        steps.forEach((step, index) => {
            step.querySelector('h4').textContent = `Étape ${index + 1}`;
            const inputs = step.querySelectorAll('[name*="steps-"]');
            inputs.forEach(input => {
                input.name = input.name.replace(/steps-\d+/, `steps-${index}`);
            });
        });
    }

    function updateFormsetManagement() {
        const totalForms = document.querySelector('[name="steps-TOTAL_FORMS"]');
        if (totalForms) {
            totalForms.value = document.querySelectorAll('.step-form').length;
        }
    }
});