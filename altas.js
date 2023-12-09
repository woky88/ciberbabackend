const URL = "https://woky88.pythonanywhere.com/"

document.getElementById('formulario').addEventListener('submit', function (event) {
  event.preventDefault(); // Evitamos que se envie el form

  // Validaciones
  if (!validarFormulario()) {
    alert("Por favor, completa todos los campos requeridos.");
    return;
  }

  var formData = new FormData(this); // Usamos 'this' para referirnos al formulario

  // Realizamos la solicitud POST al servidor
  fetch(URL + 'formulario_datos', {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error al enviar el formulario.');
      }
    })
    .then(() => {
      alert('Formulario enviado correctamente.');
      // Limpieza del formulario, si es necesaria
      this.reset(); // Reinicia el formulario
    })
    .catch(error => {
      alert('Error al enviar el formulario.');
      console.error('Error:', error);
    });
});

function validarFormulario() {
  const nombre = document.getElementById('nombre').value.trim();
  const empresa = document.getElementById('empresa').value.trim();
  const correo = document.getElementById('correo').value.trim();
  const cantidadEmpleados = document.getElementById('cantidadEmpleados').value.trim();
  const servicio = document.getElementById('servicio').value.trim();

  // Verifica que ninguno de los campos esté vacío
  return nombre && empresa && correo && cantidadEmpleados && servicio;
}
