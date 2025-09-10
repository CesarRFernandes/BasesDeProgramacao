<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu currículo - <%= request.getAttribute("nome") %></title>
    <link rel="stylesheet" href="css/exibir-currilo.css">
</head>
<body>
    <div class="cv-container">
        <div class="cv-header">
            <h1><%= request.getAttribute("nome") %></h1>
            <p class="subtitle">Currículo Profissional</p>
        </div>

        <div class="cv-content">
            <div class="print-info">
                💡 Use Ctrl+P para imprimir este currículo
            </div>

            <div class="cv-section">
                <h2><span class="icon">ℹ️</span> Informações Pessoais</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <h3>Idade</h3>
                        <p><%= request.getAttribute("idade") %> anos</p>
                    </div>
                    <div class="info-item">
                        <h3>Escolaridade</h3>
                        <p><%= request.getAttribute("escolaridade") %></p>
                    </div>
                </div>
            </div>

            <div class="cv-section">
                <h2><span class="icon">🎯</span> Áreas de Interesse</h2>
                <div class="areas-interesse">
                    <%
                    String areas = (String) request.getAttribute("areasInteresse");
                    if (areas != null && !areas.equals("Não informado")) {
                        String[] areasArray = areas.split(", ");
                        for (String area : areasArray) {
                    %>
                        <span class="area-tag"><%= area %></span>
                    <%
                        }
                    } else {
                    %>
                        <span class="area-tag" style="background: #95a5a6;">Não informado</span>
                    <% } %>
                </div>
            </div>

            <div class="cv-section">
                <h2><span class="icon">💼</span> Experiência Profissional</h2>
                <div class="experiencia-box">
                    <%= request.getAttribute("experiencia") != null &&
                        !request.getAttribute("experiencia").equals("Não informado")
                        ? request.getAttribute("experiencia")
                        : "Experiência não informada. Candidato(a) pode estar iniciando a carreira profissional ou buscando uma transição de área." %>
                </div>
            </div>
        </div>

        <div class="actions">
            <a href="cadastro-curriculo.jsp" class="btn btn-primary">
                📝 Novo Currículo
            </a>
            <a href="javascript:window.print()" class="btn btn-secondary">
                🖨️ Imprimir
            </a>
        </div>
    </div>

    <script src="js/exibir-curriculo.js"></script>
</body>
</html>