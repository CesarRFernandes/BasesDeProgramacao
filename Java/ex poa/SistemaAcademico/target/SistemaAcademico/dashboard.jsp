<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.academico.model.Aluno" %>
<%
    Aluno aluno = (Aluno) session.getAttribute("aluno");
    if (aluno == null) {
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Sistema Acadêmico</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>
    
    <div class="container">
        <div class="dashboard-header">
            <h1>Bem-vindo, <%= aluno.getNome() %>!</h1>
            <p class="subtitle">RA: <%= aluno.getRa() %> | Curso: <%= aluno.getCurso() %></p>
        </div>
        
        <% if (request.getAttribute("sucesso") != null) { %>
            <div class="alert alert-success">
                <%= request.getAttribute("sucesso") %>
            </div>
        <% } %>
        
        <% if (request.getAttribute("erro") != null) { %>
            <div class="alert alert-error">
                <%= request.getAttribute("erro") %>
            </div>
        <% } %>
        
        <div class="cards-grid">
            <div class="card">
                <div class="card-icon">📊</div>
                <h3>Minhas Notas</h3>
                <p>Visualize suas notas e calcule seu CR</p>
                <a href="notas" class="btn btn-primary">Acessar</a>
            </div>
            
            <div class="card">
                <div class="card-icon">🎓</div>
                <h3>Atividades Complementares</h3>
                <p>Gerencie suas horas complementares</p>
                <a href="atividades" class="btn btn-primary">Acessar</a>
            </div>
            
            <div class="card">
                <div class="card-icon">📍</div>
                <h3>Meu Endereço</h3>
                <p>
                    <% if (aluno.getEndereco() != null && !aluno.getEndereco().isEmpty()) { %>
                        <%= aluno.getEndereco() %><br>
                        <%= aluno.getCidade() %>/<%= aluno.getEstado() %><br>
                        CEP: <%= aluno.getCep() %>
                    <% } else { %>
                        Nenhum endereço cadastrado
                    <% } %>
                </p>
                <button type="button" class="btn btn-secondary" onclick="mostrarFormEndereco()">
                    <%= aluno.getEndereco() != null ? "Atualizar" : "Cadastrar" %>
                </button>
            </div>
        </div>
        
        <div id="formEndereco" class="modal" style="display: none;">
            <div class="modal-content">
                <span class="close" onclick="fecharFormEndereco()">&times;</span>
                <h2>Consultar CEP e Atualizar Endereço</h2>
                
                <form id="cepForm" class="form-horizontal">
                    <div class="form-group">
                        <label for="cep">CEP:</label>
                        <div class="input-group">
                            <input type="text" id="cep" name="cep" required 
                                   placeholder="00000-000" maxlength="9" class="form-control"
                                   value="<%= aluno.getCep() != null ? aluno.getCep() : "" %>">
                            <button type="button" class="btn btn-secondary" onclick="buscarCEP()">
                                Buscar CEP
                            </button>
                        </div>
                    </div>
                </form>
                
                <form action="login" method="post" id="enderecoForm">
                    <input type="hidden" name="action" value="atualizarEndereco">
                    <input type="hidden" name="cep" id="cepHidden">
                    
                    <div class="form-group">
                        <label for="endereco">Endereço:</label>
                        <input type="text" id="endereco" name="endereco" required 
                               class="form-control" placeholder="Rua, número"
                               value="<%= aluno.getEndereco() != null ? aluno.getEndereco() : "" %>">
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="cidade">Cidade:</label>
                            <input type="text" id="cidade" name="cidade" required 
                                   class="form-control"
                                   value="<%= aluno.getCidade() != null ? aluno.getCidade() : "" %>">
                        </div>
                        
                        <div class="form-group">
                            <label for="estado">Estado:</label>
                            <input type="text" id="estado" name="estado" required 
                                   maxlength="2" class="form-control"
                                   value="<%= aluno.getEstado() != null ? aluno.getEstado() : "" %>">
                        </div>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Salvar Endereço</button>
                </form>
            </div>
        </div>
    </div>
    
    <script src="js/main.js"></script>
    <script>
        function mostrarFormEndereco() {
            document.getElementById('formEndereco').style.display = 'block';
        }
        
        function fecharFormEndereco() {
            document.getElementById('formEndereco').style.display = 'none';
        }
        
        function buscarCEP() {
            const cep = document.getElementById('cep').value.replace(/\D/g, '');
            
            if (cep.length !== 8) {
                alert('CEP deve conter 8 dígitos');
                return;
            }
            
            fetch('login?action=consultarCep&cep=' + cep, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert(data.mensagem || 'CEP não encontrado');
                } else {
                    document.getElementById('endereco').value = data.logradouro || '';
                    document.getElementById('cidade').value = data.localidade || '';
                    document.getElementById('estado').value = data.uf || '';
                    document.getElementById('cepHidden').value = cep;
                }
            })
            .catch(error => {
                alert('Erro ao buscar CEP: ' + error);
            });
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('formEndereco');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>