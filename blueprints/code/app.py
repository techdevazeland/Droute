from flask import Blueprint, request

app = Blueprint('app', __name__)
code = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>Droute • Inicio</title>
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
        width: 120px;
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
        color:#3f4a7d;
        border-radius:10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; /* Añade puntos suspensivos si el texto se desborda */
    }
        @font-face {
    font-family: caption;
    src: url("./droute/font/caption.ttf");
}
    </style>
</head>
<body style="margin:0px; background:#8098ff; font-family:caption;">
    
    <div style="padding:20px; text-align:center;"><h1 style="color:white;"><span class="bi bi-alt"></span>Droute</h1></div>
    <div style="background:white; position:fixed; top:15%; bottom:0px; left:0px; right:0px; padding:20px; border-radius:20px 20px 0px 0px;">
        <center><h4>Bienvenido a Droute!!</h4><div style="width:80%; background:#8098ff; color:white; padding:10px; text-align:center; border-radius:20px;" onclick="window.location.href = './droute';">DASHBOARD</div><br><hr style="border-color:#8098ff; border:solid 1px #8098ff;"><br>
        <h3 style="color:#3f4a7d;">Facil, Rápido y Personalizable</h3>
        <div class="contenedor">
            <div class="cuadrado">
        <h1 class="logo bi bi-dpad-fill"></h1>
    <b class="name"></b>
    </div>
    <div class="cuadrado">
        <h1 class="logo bi bi-fast-forward"></h1>
    <b class="name"></b>
    </div>
    <div class="cuadrado">
        <h1 class="logo bi bi-pencil-square"></h1>
    <b class="name"></b>
    </div>
        </div>
        </center>
    </div>
    <div style="position:fixed; bottom:0px; left:0px; right:0px; background:#8098ff; font-size:0.3em; text-align:center; padding:5px;">Desplegado en {{HOST}}</div>
</body>
</html>
'''
@app.route('/')
def app_home():
    return code.replace("{{HOST}}", str(request.host))