<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sistema Acadêmico</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="login-body">
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>Sistema Acadêmico</h1>
                <p>Gerencie suas notas e atividades complementares</p>
            </div>
            
            <% if (request.getAttribute("erro") != null) { %>
                <div class="alert alert-error">
                    <%= request.getAttribute("erro") %>
                </div>
            <% } %>
            
            <form action="login" method="post" class="login-form">
                <input type="hidden" name="action" value="login">
                
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="seu.email@exemplo.com" class="form-control">
                </div>
                
                <div class="form-group">
                    <label for="senha">Senha:</label>
                    <input type="password" id="senha" name="senha" required 
                           placeholder="••••••••" class="form-control">
                </div>
                
                <button type="submit" class="btn btn-primary btn-block">Entrar</button>
            </form>
            
            <div class="login-footer">
                <p>Usuário de teste:</p>
                <p><strong>Email:</strong> joao@email.com</p>
                <p><strong>Senha:</strong> 123456</p>
            </div>
        </div>
    </div>
</body>
</html>