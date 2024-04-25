document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');

  form.addEventListener('submit', function(event) {
      event.preventDefault();

      // Validación de campos vacíos
      const inputs = form.querySelectorAll('input');
      let camposVacios = false;
      inputs.forEach(function(input) {
          if (input.value.trim() === '') {
              camposVacios = true;
          }
      });

      // Validación de contraseña
      const passInput = document.getElementById('inputpass');
      const passConfirmInput = document.getElementById('inputpassconfirm');
      const passValue = passInput.value.trim();
      const passConfirmValue = passConfirmInput.value.trim();
      const passRegex = /^(?=.*[A-Z].*[A-Z])(?=.*\d{4,})(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{9,21}$/;
      const isValidPass = passRegex.test(passValue);
      const passMatch = passValue === passConfirmValue;

      // Validación de fecha de nacimiento
      const birthDateInput = document.getElementById('inputdate');
      const birthDateValue = new Date(birthDateInput.value);
      const minAgeDate = new Date();
      minAgeDate.setFullYear(minAgeDate.getFullYear() - 13);
      const isOver13 = birthDateValue <= minAgeDate;

      // Validación de checkbox
      const checkbox = document.getElementById('checkterms');
      const isChecked = checkbox.checked;

      // Mostrar mensaje de "Registrado Exitosamente" si todas las validaciones son exitosas
      if (!camposVacios && isValidPass && passMatch && isOver13 && isChecked) {
          alert('Registrado Exitosamente');
          form.submit(); // Envío del formulario
      } else {
          // Mostrar alertas correspondientes si las validaciones fallan
          if (camposVacios) {
              alert('Todos los campos deben ser completados de forma obligatoria');
          } else if (!isValidPass) {
              alert('La contraseña debe tener entre 9 y 21 caracteres, al menos 4 números, 2 letras mayúsculas y un carácter especial.');
          } else if (!passMatch) {
              alert('Las Contraseñas no coinciden, favor de escribir nuevamente');
          } else if (!isOver13) {
              alert('Debes ser mayor de 13 años para poder registrarte');
          } else if (!isChecked) {
              alert('Por favor acepte las condiciones de término');
          }
      }
  });
});

