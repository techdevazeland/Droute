from flask import Blueprint, request, send_file
import shutil
import os
import time
import requests
import threading
droute = Blueprint('droute', __name__)
autocron_val = False
autocron_host = ""
def getsize_path(ruta):
    return sum(os.path.getsize(os.path.join(carpeta_actual, archivo))
               for carpeta_actual, subcarpetas, archivos in os.walk(ruta)
               for archivo in archivos)
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)
def unlink(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
if not os.path.exists("./blueprints/cloud"):
    os.mkdir("./blueprints/cloud")
def autocron_job(host):
    while True:
        time.sleep(10)
        requests.get("https://"+host)
code = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
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
        bottom:5px;
        z-index: 2;
        width:90%;
        text-align:center;
        margin:10px;
        background:#fff;
        border-radius:10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; /* Añade puntos suspensivos si el texto se desborda */
    }
@font-face {
    font-family: caption;
    src: url("./font/caption.ttf");
}
</style>
</head>
<body style="background:#EEE; margin:0px; font-family:caption;">
    <div style="display:flex; background:#FFF; justify-content: center; align-items: center;"><h3 style="margin-left:20px; color:#8098ff; flex:1;">Droute</h3><h3 style="margin-right:10px; background:#AAA; padding:10px; color:#FFF; border-radius:20px;" class="bi bi-trash3-fill" id="del"></h3><h3 style="margin-right:20px; background:#8098ff; padding:10px; color:#FFF; border-radius:20px;" class="bi bi-upload" onclick="upboard = document.getElementById('uploadpanel'); upboard.style.display = 'block';"></h3></div>
    <div id="uploadpanel" style="display:none;">
    <div style="position:fixed; top:0px; left:0px; right:0px; bottom:0px; background:#000; z-index:10; opacity:0.5;" onclick="upboard = document.getElementById('uploadpanel'); upboard.style.display = 'none';"></div>
    <div style="position:fixed; top:10%; left:10%; right:10%; background:#FFF; z-index:15; padding:20px; border-radius:20px;"><div style="display:flex;"><h3 style="color:#8098ff; flex:1;">Subir archivo</h3><h3 style="margin-right:10px;" class="bi bi-x-circle" onclick="upboard = document.getElementById('uploadpanel'); upboard.style.display = 'none';"></h3></div>
    <center><div style="width:70%; background:#8098ff; color:white; padding:30px; text-align:center; border-radius:20px; border:dashed 2px; padding-top:50px; padding-bottom:50px;" onclick="document.getElementById('inputFile').click()"><h3 id="progress">ESCOGER</h3></div></center>
    <input type="file" style="display:none;" id="inputFile">
    </div>
    </div>
    <div style="display:flex; background:#FFF; justify-content: center; align-items: center; padding:10px;" id="herr">
        <div style="background:#8098ff; padding:10px; color:white; flex:1; margin:5px; text-align:center; border-radius:10px;" class="bi bi-x-circle" onclick="deselect()"> DESELECCIONAR</div>
    </div>
    <div id="files">
        
    </div>
<!-- INFO -->

<script>

var seleccionado = "";
var dir = "./";
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
    requests('./delete?file='+files[i],  function(text) {console.log(text)});
    fil = document.getElementById(files[i]);
    fil.style.display = "none";
    seleccionado = "";
    content_del.style.background = "#AAA";
    content_del.style.color = "#FFF";
   herr = document.getElementById("herr");
herr.style.display = "none"; content_del.removeEventListener('click', delete_select);
    }
}

function requests(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(xhr.responseText);
        }
    };

    xhr.send(JSON.stringify({}));
}
setTimeout(function(){
    info = document.getElementById("info");
    info.style.display = "none";
},5000)
herr = document.getElementById("herr");
herr.style.display = "none";
function uploadFile() {
            const fileInput = document.getElementById('inputFile');
            const file = fileInput.files[0];
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            formData.append('file', file);

            xhr.upload.onprogress = function(event) {
                const progress = Math.round((event.loaded / event.total) * 100);
                document.getElementById('progress').innerText = `${progress}%`;
            };

            xhr.onload = function() {
                if (xhr.status == 200) {
                    console.log('File uploaded successfully');
                    document.getElementById("uploadpanel").style.display = "none";
                    document.getElementById('progress').innerText = 'ESCOGER';
                    window.location.href = "./";
                } else {
                    console.error('Error uploading file');
                    document.getElementById('progress').innerText = 'ERROR';
                }
            };

            xhr.open('POST', './upload', true);
            xhr.send(formData);
        }
inputFile = document.getElementById("inputFile");
inputFile.addEventListener('change', function() {
    uploadFile()
});
function deselect() {
    files = seleccionado.split('/');
    for (let i = 0; i < files.length; i++) {
    gestionarNombres(files[i]);
    content = document.getElementById(files[i]);
    logo = document.getElementById(files[i]+'-logo');
    content.style.background = '#8098ff';
    logo.style.color = '#FFF';
    var content_del = document.getElementById('del');
    content_del.style.background = '#AAA';
    content_del.style.color = '#FFF';
    content_del.removeEventListener('click', delete_select);
    var herr = document.getElementById('herr');
    herr.style.display = 'none';
    }
}
function getFiles() {
    setTimeout(function(){
    files = document.getElementById("files");
    dirsect = document.getElementById("dirsect");
    requests("./files?dir="+dir, function(response){
        files.innerHTML = response;
        dirsect.innerHTML = dir;
    })
},1000)

}
getFiles()
</script>
</body>
<div style="height:80px; background:#FFF; opacity:0;"></div>
<div style="height:40px; background:#FFF; position:fixed; bottom:0px; left:0px; right:0px; display:flex; padding:20px; justify-content: center; align-items: center; z-index:20;">
    <div class="bi bi-archive" style="flex:1; text-align:center; background:#8098ff; padding:10px; color:white; border-radius:20px; margin:5px;"></div>
    <div class="bi bi-terminal" style="flex:1; text-align:center; background:#AAA; padding:10px; color:white; border-radius:20px; margin:5px;"></div>
    <div class="bi bi-boxes" style="flex:1; text-align:center; background:#AAA; padding:10px; color:white; border-radius:20px; margin:5px;"></div>
</div>
</html>

'''
@droute.route('/')
def app_home():
    global autocron_val
    autocron_host = request.host
    print(autocron_host)
    if not autocron_val:
        t = threading.Thread(target=autocron_job, args=(autocron_host,))
        t.start()
        autocron_val = True
    autocron_color = "#AAA"
    if autocron_val:
        autocron_color = "#8098FF"
    info = ""
    if "info" in request.args:
        info = f'''<div style="position:fixed; bottom:0px; left:0px; right:0px; background:#8098ff; text-align:center; padding:10px;" id="info">{request.args["info"]}</div>'''
    return code.replace("<!-- INFO -->", info).replace("<!-- AUTOCRON_COLOR -->", autocron_color)
@droute.route('/files')
def files():
    files = sorted(os.listdir("./blueprints/cloud"))
    ftext = f''' <div style="margin:5px; background:#DDD; padding:5px; text-align:center; border-radius:20px;">
        <i>{sizeof_fmt(getsize_path("./blueprints/cloud"))} / 15GiB</i>
    </div>
    <div class="contenedor">'''
    for f in files:
            if os.path.isfile("./blueprints/cloud/"+f):
                ftext += f'''<div class="cuadrado" onclick="addlist('{f}')" id="{f}">
        <h1 class="logo bi bi-file-earmark" id="{f}-logo"></h1>
    <b class="name">{f}</b>
    </div>
    '''
    ftext += '''</div>'''
    return ftext
@droute.route('/delete', methods=["GET"])
def deletefile():
    data = request.args
    file = data["file"]
    if not file == "":
        os.remove("./blueprints/cloud/"+file)
    return "eliminado"
@droute.route("/font/<file>")
def fontget(file):
    return send_file("./blueprints/font/"+file)
@droute.route("/upload", methods=["POST"])
def upload():
    print(request.files)
    file = request.files['file']
    filename = str(file.filename).replace(" ", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")
    file.save("./blueprints/cloud/"+filename)
    return "Archivo "+filename+" subido correctamente!!"