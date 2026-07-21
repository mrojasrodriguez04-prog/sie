let empresas = [];
let paginaEmpresa = 1;
const registrosEmpresa = 4;

let infraestructuras = [];
let paginaInfra = 1;
const registrosInfra = 3;

function toggleSidebar(){

    document
    .getElementById("sidebar")
    .classList.toggle("active");

}




const sector =
document.getElementById("sector");

const subsector =
document.getElementById("subsector");

sector.addEventListener("change",function(){

    subsector.innerHTML =
    "<option value=''>Todos</option>";

    if(this.value==""){

        consultarEmpresas();

        return;

    }

    fetch("/consulta_empresas/get_subsectores/" + this.value)

    .then(r=>r.json())

    .then(datos=>{

        datos.forEach(s=>{

            subsector.innerHTML+=`

            <option
            value="${s.id}">

            ${s.nombre}

            </option>

            `;

        });

        consultarEmpresas();

    });

});




document
.getElementById("tipo_empresa")
.addEventListener(
"change",
consultarEmpresas
);

document
.getElementById("tamano")
.addEventListener(
"change",
consultarEmpresas
);

subsector.addEventListener(
"change",
consultarEmpresas
);
function consultarEmpresas(){

    let tipo_empresa =
    document.getElementById("tipo_empresa").value;

    let sector =
    document.getElementById("sector").value;

    let subsector =
    document.getElementById("subsector").value;

    let tamano =
    document.getElementById("tamano").value;

    let parametros =
    new URLSearchParams({

        tipo_empresa: tipo_empresa,

        sector: sector,

        subsector: subsector,

        tamano: tamano

    });

    fetch(

        "/consulta/buscar_empresas?" +
        parametros

    )

    .then(r => r.json())

    .then(datos => {

        let tabla =
        document.getElementById("tablaEmpresas");

        empresas = datos;
        paginaEmpresa = 1;
        mostrarEmpresas();

        // ACTUALIZA LOS BOTONES DE EXPORTACIÓN

        document.getElementById("btnExcel").href =
        "/consulta/exportar_excel?" +
        parametros.toString();

        document.getElementById("btnPdf").href =
        "/consulta/exportar_pdf?" +
        parametros.toString();

    });

}

function mostrarEmpresas(){

    let tabla = document.getElementById("tablaEmpresas");

    tabla.innerHTML = "";

    if(empresas.length==0){

        tabla.innerHTML=`
        <tr>
            <td colspan="3" style="text-align:center;padding:25px;">
                No se encontraron empresas.
            </td>
        </tr>
        `;

        document.getElementById("paginacionEmpresas").innerHTML="";
        return;
    }

    let inicio=(paginaEmpresa-1)*registrosEmpresa;
    let fin=inicio+registrosEmpresa;

    empresas.slice(inicio,fin).forEach(e=>{

        tabla.innerHTML+=`
        <tr>
            <td>${e.empresa}</td>
            <td>${e.producto}</td>
            <td>${e.empleados}</td>
        </tr>
        `;

    });

    let paginas=Math.ceil(empresas.length/registrosEmpresa);

    let html="";

    for(let i=1;i<=paginas;i++){

        html+=`
        <button onclick="irPaginaEmpresa(${i})">
            ${i}
        </button>
        `;

    }

    document.getElementById("paginacionEmpresas").innerHTML=html;

}

function irPaginaEmpresa(p){

    paginaEmpresa=p;

    mostrarEmpresas();

}

document
.querySelectorAll(".infra")
.forEach(c=>{

c.addEventListener(

"change",

consultarInfraestructura

);

});

function consultarInfraestructura(){

    let params = new URLSearchParams();

    document.querySelectorAll(".infra:checked").forEach(function(c){

        params.append("tecnologia", c.value);

    });

    let tabla = document.getElementById("tablaInfraestructura");

    if(params.toString()==""){

        tabla.innerHTML="";

        return;

    }

    fetch("/consulta/buscar_infraestructura?"+params)

    .then(r=>r.json())

    .then(datos=>{


            infraestructuras = datos;
            paginaInfra = 1;
            mostrarInfraestructura();

    });

}

document.querySelectorAll(".infra").forEach(function(c){

    c.addEventListener("change", consultarInfraestructura);

});

function mostrarInfraestructura(){

    let tabla=document.getElementById("tablaInfraestructura");

    tabla.innerHTML="";

    if(infraestructuras.length==0){

        tabla.innerHTML=`
        <tr>
            <td colspan="4" style="text-align:center;padding:25px;">
                No se encontraron empresas.
            </td>
        </tr>
        `;

        document.getElementById("paginacionInfra").innerHTML="";
        return;

    }

    let inicio=(paginaInfra-1)*registrosInfra;
    let fin=inicio+registrosInfra;

    infraestructuras.slice(inicio,fin).forEach(e=>{

        tabla.innerHTML+=`
        <tr>
            <td>${e.empresa}</td>
            <td>${e.sector}</td>
            <td>${e.tamano}</td>
            <td>${e.tecnologia}</td>
        </tr>
        `;

    });

    let paginas=Math.ceil(infraestructuras.length/registrosInfra);

    let html="";

    for(let i=1;i<=paginas;i++){

        html+=`
        <button onclick="irPaginaInfra(${i})">
            ${i}
        </button>
        `;

    }

    document.getElementById("paginacionInfra").innerHTML=html;

}

function irPaginaInfra(p){

    paginaInfra=p;

    mostrarInfraestructura();

}

consultarEmpresas();

consultarInfraestructura();