const URL = "https://woky88.pythonanywhere.com/"

const app = Vue.createApp({
  data() {
    return {
      id: '',
      nombre: '',
      empresa: '',
      correo: '',
      cantidad_empleados: '',
      servicio: '',
      mostrarDatosCotizacion: false,
    };
  },
  methods: {
    obtenerCotizacion() {
      fetch(URL + 'cotizaciones/' + this.id)
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error('Error al obtener los datos de la cotización.')
          }
        })
        .then(data => {
          this.nombre = data.nombre;
          this.empresa = data.empresa;
          this.correo = data.correo;
          this.cantidad_empleados = data.cantidad_empleados;
          this.servicio = data.servicio;
          this.mostrarDatosCotizacion = true;
        })
        .catch(error => {
          console.log(error);
          alert('ID no encontrado.');
        })
    },
    guardarCambios() {
      const formData = new FormData();
      formData.append('nombre', this.nombre);
      formData.append('empresa', this.empresa);
      formData.append('correo', this.correo);
      formData.append('cantidadEmpleados', this.cantidad_empleados);
      formData.append('servicio', this.servicio);

      fetch(URL + 'cotizaciones/' + this.id, {
        method: 'PUT',
        body: formData,
      })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error('Error al guardar los cambios de la cotización.')
          }
        })
        .then(data => {
          alert('Cotización actualizada correctamente.');
          this.limpiarFormulario();
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Error al actualizar la cotización.');
        });
    },
    limpiarFormulario() {
      this.id = '';
      this.nombre = '';
      this.empresa = '';
      this.correo = '';
      this.cantidad_empleados = '';
      this.servicio = '';
      this.mostrarDatosCotizacion = false;
    }
  }
});

app.mount('#app');
