const URL = "https://woky88.pythonanywhere.com/";

// Realizamos la solicitud GET al servidor para obtener todas las cotizaciones
fetch(URL + 'cotizaciones')
  .then(function (response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Error al obtener las cotizaciones.');
    }
  })
  .then(function (data) {
    let tablaCotizaciones = document.getElementById('tablaCotizaciones');

    for (let cotizacion of data) {
      let fila = document.createElement('tr');
      fila.innerHTML = `
        <td>${cotizacion.id}</td>
        <td>${cotizacion.nombre}</td>
        <td>${cotizacion.empresa}</td>
        <td>${cotizacion.correo}</td>
        <td align="right">${cotizacion.cantidad_empleados}</td>
        <td>${cotizacion.servicio}</td>
      `;
      tablaCotizaciones.appendChild(fila);
    }
  })
  .catch(function (error) {
    alert('Error al obtener las cotizaciones.');
    console.error('Error:', error);
  });
