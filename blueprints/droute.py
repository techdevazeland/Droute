from flask import Blueprint, request, send_file
import shutil
import os
import time
import requests
import threading
droute = Blueprint('droute', __name__)
autocron_val = False
autocron_host = ""
def autocron_job():
    global autocron_val
    global autocron_host
    while True:
        time.sleep(30)
        if autocron_val:
            requests.get("https://"+autocron_host)
t = threading.Thread(target=autocron_job)
t.start()
code = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Droute</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<style>
    .contenedor {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding:10px;
    }
    .cuadrado {
        width: 100px;
        height: 100px;
        background-color: #8098ff;
        margin: 5px;
        border-radius:10px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .logo {
        position: relative;
        z-index: 1;
        color:#FFF;
        font-size:3em;
    }
    .name {
        position: absolute;
        z-index: 2;
        width:90%;
        text-align:center;
        margin:10px;
        overflow-x:auto;
        background:#fff;
        border-radius:10px;
    }
@font-face {
    font-family: caption;
    src: url("./font/caption.ttf");
}
</style>
</head>
<body style="background:#EEE; margin:0px; font-family:caption;">
    <div style="display:flex; background:#FFF; justify-content: center; align-items: center;"><h3 style="margin-left:20px; color:#8098ff; flex:1;">Droute</h3><h3 style="margin-right:10px; background:<!-- AUTOCRON_COLOR -->; padding:10px; color:#FFF; border-radius:20px;" class="bi bi-alarm-fill" id="autocron" onclick="window.location.href = './autocron';"></h3><h3 style="margin-right:10px; background:#AAA; padding:10px; color:#FFF; border-radius:20px;" class="bi bi-trash3-fill" id="del"></h3><h3 style="margin-right:20px; background:#8098ff; padding:10px; color:#FFF; border-radius:20px;" class="bi bi-upload" id="seleccionarArchivo"></h3></div>
    <div style="display:flex; background:#FFF; justify-content: center; align-items: center; padding:10px;" id="herr">
        <div style="background:#8098ff; padding:10px; color:white; flex:1; margin:5px; text-align:center; border-radius:10px;" class="bi bi-play-circle"></div>
        <div style="background:#8098ff; padding:10px; color:white; flex:1; margin:5px; text-align:center; border-radius:10px;" class="bi bi-info-circle"></div>
    </div>
<div class="contenedor">
    <!-- FILES -->
</div>
<form action="./upload" method="POST">
<input type="file" id="archivoInput" style="display:none;">
<input type="submit" id="submitInput" style="display:none;">
</form>
<!-- INFO -->

<script>

var seleccionado = "";

function gestionarNombres(nombre) {
  if (seleccionado.includes(nombre)) {
    seleccionado = seleccionado.replace(new RegExp(nombre + "/", ""), "");
  } else {
    seleccionado += nombre + "/";
  }
}

function addlist(valor) {
var content_del = document.getElementById("del");
var content = document.getElementById(valor);
var herr = document.getElementById("herr");
var logo = document.getElementById(valor+"-logo");
console.log(content.style.background)
if (content.style.background == "rgb(128, 152, 255)" || content.style.background == "") {
    content.style.background = "#FFF";
    logo.style.color = "#EEE";
} else {
    content.style.background = "#8098ff";
    logo.style.color = "#FFF";
}
gestionarNombres(valor)
if (seleccionado == "") {

    content_del.style.background = "#AAA";
    content_del.style.color = "#FFF";
    content_del.removeEventListener('click', delete_select);
    herr.style.display = "none";
} else {
    content_del.style.background = "#ff2b35";
    content_del.style.color = "#FFF";
    content_del.addEventListener('click', delete_select);
    herr.style.display = "flex";
}
}
function delete_select() {
var content_del = document.getElementById("del");
    files = seleccionado.split('/')
    for (let i = 0; i < files.length; i++) {
    requests('./delete', {'file':files[i]}, function(text) {console.log(text)});
    fil = document.getElementById(files[i]);
    fil.style.display = "none";
    seleccionado = "";
    content_del.style.background = "#AAA";
    content_del.style.color = "#FFF";
   herr = document.getElementById("herr");
herr.style.display = "none"; content_del.removeEventListener('click', delete_select);
    }
}
// Obtener el botón div y el botón input
var divSeleccionarArchivo = document.getElementById('seleccionarArchivo');
var inputArchivo = document.getElementById('archivoInput');
var inputSubmit = document.getElementById('submitInput');

divSeleccionarArchivo.addEventListener('click', function() {
inputArchivo.click();
});

inputArchivo.addEventListener('change', function() {
    const archivo = inputArchivo.files[0]; // Obtener el archivo seleccionado
    inputSubmit.click()
});

function requests(url, datos, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(xhr.responseText);
        }
    };

    xhr.send(JSON.stringify(datos));
}
setTimeout(function(){
    info = document.getElementById("info");
    info.style.display = "none";
},5000)
herr = document.getElementById("herr");
herr.style.display = "none";
</script>
</body>
</html>
'''
@droute.route('/')
def app_home():
    global autocron_val
    global autocron_host
    autocron_host = request.host
    autocron_color = "#AAA"
    if autocron_val:
        autocron_color = "#8098FF"
    info = ""
    if "info" in request.args:
        info = f'''<div style="position:fixed; bottom:0px; left:0px; right:0px; background:#8098ff; text-align:center; padding:10px;" id="info">{request.args["info"]}</div>'''
    files = sorted(os.listdir("./blueprints/code"))
    ftext = ""
    for f in files:
        if os.path.isfile("./blueprints/code/"+f):
            ftext += f'''<div class="cuadrado" onclick="addlist('{f}')" id="{f}">
        <h1 class="logo bi bi-file-earmark" id="{f}-logo"></h1>
    <b class="name">{f}</b>
    </div>
    '''
    return code.replace("<!-- FILES -->", ftext).replace("<!-- INFO -->", info).replace("<!-- AUTOCRON_COLOR -->", autocron_color)
@droute.route('/autocron')
def autocrondef():
    global autocron_val
    global autocron_host
    if autocron_val:
        autocron_val = False
        return "<script>window.location.href = './?info=Autocron apagado!';</script>"
    else:
        autocron_val = True
        return "<script>window.location.href = './?info=Autocron encendido!';</script>"
@droute.route('/delete', methods=["GET"])
def deletefile():
    data = request.args
    file = data["file"]
    os.remove("./blueprints/code/"+file)
    return "eliminado"
@droute.route("/font/<file>")
def fontget(file):
    return send_file("./blueprints/font/"+file)
@droute.route("/upload", methods=["POST"])
def uploadfile():
    print(request.files)
    file = request.files['file']
    file.save("./blueprints/code/"+file.filename)
    return "<script>window.location.href = './?info=Archivo "+file+" subido correctamente!!';</script>"