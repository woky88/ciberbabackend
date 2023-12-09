const URL = "https://woky88.pythonanywhere.com/"
const app = Vue.createApp({
  data() {
    return {
      cotizaciones: []  // Cambiado de 'productos' a 'cotizaciones'
    }
  },
  methods: {
    obtenerCotizaciones() {
      // Obtenemos el contenido de las cotizaciones
      fetch(URL + 'cotizaciones')
        .then(response => {
          if (response.ok) { return response.json(); }
        })
        .then(data => {
          this.cotizaciones = data;
        })
        .catch(error => {
          console.log('Error:', error);
          alert('Error al obtener las cotizaciones.');
        });
    },
    eliminarCotizacion(id) {
      if (confirm('¿Estás seguro de que quieres eliminar esta cotización?')) {
        fetch(URL + `cotizaciones/${id}`, { method: 'DELETE' })
          .then(response => {
            if (response.ok) {
              this.cotizaciones = this.cotizaciones.filter(cotizacion => cotizacion.id !== id);
              alert('Cotización eliminada correctamente.');
            }
          })
          .catch(error => {
            alert(error.message);
          });
      }
    }
  },
  mounted() {
    // Al cargar la página, obtenemos la lista de cotizaciones
    this.obtenerCotizaciones();
  }
});
app.mount('body');
