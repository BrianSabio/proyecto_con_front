document.getElementById('crear_producto').addEventListener('submit', function (event) {
    event.preventDefault();
    //previene recarga de página al ejecutar 'submit'
    const descripcion = document.getElementById('descripcion').value;
    const cantidad = document.getElementById('cantidad').value;
    const precio = document.getElementById('precio').value;
    const imagen = document.getElementById('imagen').value;
    const proveedor = document.getElementById('proveedor').value;
    //se guardan los valores ingresados en el formulario

    fetch('http://localhost:5000/productos', {
    //se genera una solicitud HTTP que se comunica con 'app.py' para crear nuevo recurso
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            //contenido de solicitud de tipo json
        },
        body: JSON.stringify({ descripcion, cantidad, precio, imagen, proveedor })
        //se envían datos del formulario convertidos en texto json
    })
    //se crea una 'promesa' en la solicitud HTTP a resolver

    .then(response => response.json())
    //toma la respuesta a la solicitud y la convierte en json
    .then(data => alert(data.mensaje))
    //toma la respuesta formato json y muestra un mensaje
    .catch(error => console.error('Error:', error));
    //controla si hay error en la solicitud y lo muestra por consola
});

document.getElementById('consultar_producto').addEventListener('submit', function (event) {
    event.preventDefault();
    const codigo = document.getElementById('codigo_consultar').value;

    fetch(`http://localhost:5000/productos/${codigo}`)
    .then(response => response.json())
    .then(data => {
        if (data.mensaje) {
            document.getElementById('producto_info').innerText = data.mensaje;
        } else {
            const productoInfo = `
                Código: ${data.codigo}
                Descripción: ${data.descripcion}
                Cantidad: ${data.cantidad}
                Precio: ${data.precio}
                Imagen: ${data.imagen}
                Proveedor: ${data.proveedor}
            `;
            document.getElementById('producto_info').innerText = productoInfo;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('modificar_producto').addEventListener('submit', function (event) {
    event.preventDefault();
    const codigo = document.getElementById('codigo_actualizar').value;
    const descripcion = document.getElementById('descripcion_actualizar').value;
    const cantidad = document.getElementById('cantidad_actualizar').value;
    const precio = document.getElementById('precio_actualizar').value;
    const imagen = document.getElementById('imagen_actualizar').value;
    const proveedor = document.getElementById('proveedor_actualizar').value;

    fetch(`http://localhost:5000/productos/${codigo}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ descripcion, cantidad, precio, imagen, proveedor })
    })
    .then(response => response.json())
    .then(data => alert(data.mensaje))
    .catch(error => console.error('Error:', error));
});

document.getElementById('eliminar_producto').addEventListener('submit', function (event) {
    event.preventDefault();
    const codigo = document.getElementById('codigo_eliminar').value;

    fetch(`http://localhost:5000/productos/${codigo}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => alert(data.mensaje))
    .catch(error => console.error('Error:', error));
});
