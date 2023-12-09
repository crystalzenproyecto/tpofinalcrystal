
//MENU PRINCIPAL
const cerrarMenuBtn = document.getElementById('cerrar-menu');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

// Agrega un evento de clic al botón de cerrar el menú
cerrarMenuBtn.addEventListener('click', () => {
  navMenu.classList.toggle('nav-menu_visible');
});

// Muestra el menú desplegable al hacer clic en los items
navToggle.addEventListener('click', () => {
  navMenu.classList.toggle('nav-menu_visible');

  if (navMenu.classList.contains("nav-menu_visible")) {
    navToggle.setAttribute("aria-label", "Cerrar Menú");
  } else {
    navToggle.setAttribute("aria-label", "Abrir Menú");
  }
});



//VALIDACION DEL FORMULARIO DE SUSCRIPCION
document.getElementById("subscribe-form").addEventListener("submit", function (event) {
  const emailInput = document.getElementById("email");
  const email = emailInput.value.trim();

  if (!email.match(/^\S+@\S+\.\S+$/)) {
    alert("Por favor, ingresa una dirección de correo electrónico válida.");
    event.preventDefault();
  } else {
    alert("¡Gracias por suscribirte!");
  }
});

//VENTANA EMERGENTE PARA MOSTRAR LOS PRODUCTOS
function mostrarPopup(event, id, nombreImagen, titulo, precio) {
  event.preventDefault(); // Evita la acción predeterminada del enlace (recarga de la página)

  var popup = document.getElementById(id);
  var imagenPopup = popup.querySelector(".img-producto-popup");
  var tituloPopup = popup.querySelector(".titulo-popup");
  var precioPopup = popup.querySelector(".precio-popup");

  imagenPopup.src = nombreImagen; // Cambia la fuente de la imagen popup
  tituloPopup.textContent = titulo; // Asigna el título al elemento del popup
  precioPopup.textContent = precio;

  popup.style.display = 'block';
}


function ocultarPopup(event, id) {
  event.preventDefault();

  var popup = document.getElementById(id);
  popup.style.display = "none";
}


//REGISTRO CONTACTO
function enviarFormulario() {
  var nombre = document.getElementById("nombre").value;
  var correo = document.getElementById("correo").value;
  var mensaje = document.getElementById("mensaje").value;

  var data = {
    "nombre": nombre,
    "correo": correo,
    "mensaje": mensaje
  };

  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);

      // Muestra la alerta de SweetAlert si el registro fue exitoso
      Swal.fire({
        title: 'Registro exitoso',
        text: 'El registro ha sido realizado con éxito.',
        icon: 'success',
        position: 'center',
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          container: 'small-alert'
        },
      });

      // Puedes agregar aquí lógica adicional después de enviar el formulario
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}