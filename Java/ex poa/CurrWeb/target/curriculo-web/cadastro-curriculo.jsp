<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Currículo</title>
    <link rel="stylesheet" href="css/cadastro-curriculo.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 Cadastro de Currículo</h1>
            <p>Preencha os dados abaixo para gerar seu mini-CV</p>
        </div>

        <% String erro = (String) request.getAttribute("erro"); %>
        <% if (erro != null) { %>
            <div class="error-message">
                ⚠️ <%= erro %>
            </div>
        <% } %>

        <form action="processar-curriculo" method="post">
            <div class="form-group">
                <label for="nome">Nome Completo <span class="required">*</span></label>
                <input type="text" id="nome" name="nome" required
                       placeholder="Digite seu nome completo"
                       value="<%= request.getParameter("nome") != null ? request.getParameter("nome") : "" %>">
            </div>

            <div class="form-group">
                <label for="idade">Idade <span class="required">*</span></label>
                <input type="number" id="idade" name="idade" min="16" max="100" required
                       placeholder="Digite sua idade"
                       value="<%= request.getParameter("idade") != null ? request.getParameter("idade") : "" %>">
            </div>

            <div class="form-group">
                <label for="escolaridade">Escolaridade</label>
                <select id="escolaridade" name="escolaridade">
                    <option value="Ensino Fundamental">Ensino Fundamental</option>
                    <option value="Ensino Médio">Ensino Médio</option>
                    <option value="Ensino Técnico">Ensino Técnico</option>
                    <option value="Ensino Superior Incompleto">Ensino Superior Incompleto</option>
                    <option value="Ensino Superior Completo" selected>Ensino Superior Completo</option>
                    <option value="Pós-Graduação">Pós-Graduação</option>
                    <option value="Mestrado">Mestrado</option>
                    <option value="Doutorado">Doutorado</option>
                </select>
            </div>

            <div class="form-group">
                <label>Áreas de Interesse</label>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="tecnologia" name="areaInteresse" value="Tecnologia">
                        <label for="tecnologia">💻 Tecnologia</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="marketing" name="areaInteresse" value="Marketing">
                        <label for="marketing">📈 Marketing</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="vendas" name="areaInteresse" value="Vendas">
                        <label for="vendas">💼 Vendas</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="rh" name="areaInteresse" value="Recursos Humanos">
                        <label for="rh">👥 Recursos Humanos</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="financeiro" name="areaInteresse" value="Financeiro">
                        <label for="financeiro">💰 Financeiro</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="design" name="areaInteresse" value="Design">
                        <label for="design">🎨 Design</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="educacao" name="areaInteresse" value="Educação">
                        <label for="educacao">📚 Educação</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="saude" name="areaInteresse" value="Saúde">
                        <label for="saude">🏥 Saúde</label>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label for="experiencia">Experiência Profissional</label>
                <textarea id="experiencia" name="experiencia"
                          placeholder="Descreva sua experiência profissional, projetos relevantes ou habilidades..."></textarea>
            </div>

            <button type="submit" class="btn-submit">
                Gerar Currículo
            </button>
        </form>
    </div>
</body>
</html>