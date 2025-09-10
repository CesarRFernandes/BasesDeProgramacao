<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Currículo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 100%;
            max-width: 600px;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
            font-size: 1rem;
        }
        
        input[type="text"], 
        input[type="number"], 
        select, 
        textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        input[type="text"]:focus, 
        input[type="number"]:focus, 
        select:focus, 
        textarea:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
            font-family: inherit;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .checkbox-item:hover {
            background: #e9ecef;
        }
        
        .checkbox-item input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
            transform: scale(1.2);
        }
        
        .checkbox-item label {
            margin: 0;
            font-weight: normal;
            cursor: pointer;
        }
        
        .btn-submit {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .error-message {
            background: #fff5f5;
            color: #e53e3e;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #e53e3e;
            font-weight: 500;
        }
        
        .required {
            color: #e53e3e;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .checkbox-group {
                grid-template-columns: 1fr;
            }
        }
    </style>
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