input_email = document.getElementById('input_email');
nombre = document.getElementById('nombre');
mascota_select = document.getElementById('mascotas');
tipo = document.getElementById('tipo_mascota');
email = input_email.value;


function get_data(elem) {

    nombre.readonly = false;
    nombre.value = '';
    email = elem.value;
    fetch('/select/' + elem.value).then(function(response) {
        response.json().then(function(data) {
            usuario = data.info;
            optionHTML = '';
            for (datos of usuario) {
                optionHTML +=
                    '<option value="' +
                    datos.nombre_mascota +
                    '">' +
                    datos.nombre_mascota +
                    '</option>';
                nombre.value = datos.name;
            }
            mascota_select.innerHTML = optionHTML;
            if (nombre.value != '') {
                nombre.readonly = true;
            }
        });
    });
}

function get_data_masc(elem) {

    // if (elem.value == 'Nueva mascota'){
    //     html_2 = '<div class="form-floating mb-3" ><input type="text" class="form-control" id="validationServer03" name="mascota"><label for="validationServer03">Nombre de mascota</label></div><div class="form-floating mb-3"><input type="text" class="form-control" id="validationServer03" name="tipo_mascota"><label for="validationServer03">Tipo de mascota</label></div>'
    //     mascota.setAttribute('hidden', true)
    //     mascota.insertAdjacentHTML("afterend",html_2)
    // }
    tipo.value = '';
    fetch('/mascota_select/' + email + '/' + elem.value).then(function(response) {
        response.json().then(function(data) {
            usuario = data.info;
            tipo.value = usuario.tipo_mascota;
        });
    });
}


function download(id) {
    var doc = new jsPDF('p', 'pt');
    headerImgData = document.getElementById('myChart');
    doc.setProperties({
        title: id
    });

    var header = function(data) {
        doc.setFontSize(18);
        doc.setTextColor(40);
        doc.setFontStyle('normal');
        doc.addImage(headerImgData, 'PNG', data.settings.margin.left, 60, 500, 250);
        doc.text("Informe de Ventas", data.settings.margin.left, 50);
    };

    var res = doc.autoTableHtmlToJson(document.getElementById(id));
    var options = {
        beforePageContent: header,
        theme: 'plain',
        pageBreak: 'auto',
        startY: doc.autoTableEndPosY() + 320,

    };

    doc.autoTable(res.columns, res.data, options);


    var blob = doc.output("blob");
    window.open(URL.createObjectURL(blob));

}

lista = document.getElementById('lista');
subtotal = document.getElementById('subtotal');
iva = document.getElementById('iva');
total = document.getElementById('total');

function add(type) {
    var elem;


    if (type == 'MEDICINA' || type == 'RECETA') {
        elem = document.getElementById('lista_medicinas').value;
    }
    if (type == 'SERVICIO') {
        elem = document.getElementById('lista_servicios').value;
    }


    fetch('/add/' + type + '/' + elem).then(function(response) {
        response.json().then(function(data) {
            opcion = data.info;
            id = type + '_' + elem;

            optionHTML =
                '<div id="div_' +
                id +
                '" class="row text-start"><div class="col-3">' +
                type +
                '</div><div class="col-3">' +
                opcion.nombre +
                '</div><div class="col-3">Precio: $' +
                opcion.precio +
                '</div><div id="' +
                id +
                '" onclick="remove(this)" class="col-3 text-end x"><i class="fa-solid fa-xmark"></i></div></div>';
            lista.innerHTML += optionHTML;

            if (type == 'MEDICINA') {
                if (opcion.stock == 0) {
                    meds = document.getElementById('lista_medicinas');
                    meds.removeChild(
                        meds.querySelector('option[value="' + opcion.id + '"]')
                    );
                }
            }
            if (type == 'MEDICINA' || type == 'SERVICIO') {
                sub = (parseFloat(subtotal.value) + parseFloat(opcion.precio)).toFixed(2);
                subtotal.value = sub;
                actualizar();
            }
        });
    });
}


function remove(elem) {
    id = elem.id;
    params = id.split('_');
    type = params[0];
    elem = params[1];
    div = document.getElementById('div_' + id);
    fetch('/remove/' + type + '/' + elem).then(function(response) {
        response.json().then(function(data) {
            opcion = data.info;
            if (type == 'MEDICINA' || type == 'SERVICIO') {

                sub = (parseFloat(subtotal.value) - parseFloat(opcion.precio)).toFixed(2);

                subtotal.value = sub;
                actualizar();
            }
            div.remove();
            meds = document.getElementById('lista_medicinas');
            if (
                type == 'MEDICINA' &&
                meds.querySelector('option[value="' + opcion.id + '"]') == null
            ) {
                meds.innerHTML +=
                    '<option value="' + opcion.id + '">' + opcion.nombre + '</option>';
            }
        });
    });
}

function actualizar() {
    iva.value = (parseFloat(subtotal.value) * 0.16).toFixed(2);
    total.value = (parseFloat(subtotal.value) + parseFloat(iva.value)).toFixed(2);
}

function tabla(dict) {
    var data_from_python = JSON.parse(dict);
    var ctx = document.getElementById('myChart');
    // eslint-disable-next-line no-unused-vars
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(data_from_python),
            datasets: [{
                data: Object.values(data_from_python),
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#6398e3',
                borderWidth: 4,
                pointBackgroundColor: '#6398e3'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            legend: {
                display: false
            }
        }
    });
}

function buscar(id, table_id) {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue, j, count, tamanio;
    input = document.getElementById(id);
    filter = input.value.toLowerCase();
    table = document.getElementById(table_id);
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        count = 0;
        tamanio = tr[i].getElementsByTagName("td").length - 1

        for (j = 0; j < tamanio; j++) {
            td = tr[i].getElementsByTagName("td")[j];

            if (td) {
                txtValue = td.textContent.toLowerCase() || td.innerText.toLowerCase();
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    // tr[i].style.display = "";
                } else {
                    count++;
                    // tr[i].style.display = "none";

                }

            }

        }
        if (count === tamanio) {
            tr[i].style.display = "none";
        } else {
            tr[i].style.display = "";
        }
    }
}

function search() {
    const searchbox = document.getElementById('searchbox');
    const buscar = searchbox.value.toLowerCase();

    $("#list td").each((id, elem) => {
        if (elem.innerText.toLowerCase().includes(buscar)) {
            elem.style.display = "block";
        } else {
            elem.style.display = "none";
        }
    });

}

function solo_desplegar_uno(id) {
    // Declare variables
    var tabla_recetas, num_tr, div_medicinas, div_servicios;
    tabla_recetas = document.getElementById("table");
    num_tr = tabla_recetas.getElementsByTagName("tr").length;
    for (let k = 1; k < num_tr; k++) {
        div_medicinas = document.getElementById("medicinas" + k);
        div_servicios = document.getElementById("servicios" + k);
        if ("medicinas" + k === id) {
            if (div_medicinas.className === 'collapse') {
                div_medicinas.className = "collapse show";

            } else {
                div_medicinas.className = "collapse";
            }
        } else {
            div_medicinas.className = "collapse";
        }
        if ("servicios" + k === id) {
            if (div_servicios.className === 'collapse') {
                div_servicios.className = "collapse show";

            } else {
                div_servicios.className = "collapse";
            }
        } else {
            div_servicios.className = "collapse"
        }

        // div_servicios.style.display = "none";
        // div_medicinas.style.display = "none";
    }




}