<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.academico.model.AtividadeComplementar, java.util.List, java.time.format.DateTimeFormatter" %>
<%
    if (session.getAttribute("aluno") == null) {
        response.sendRedirect("login.jsp");
        return;
    }
    
    List<AtividadeComplementar> atividades = (List<AtividadeComplementar>) request.getAttribute("atividades");
    Integer horasCumpridas = (Integer) request.getAttribute("horasCumpridas");
    Integer horasFaltantes = (Integer) request.getAttribute("horasFaltantes");
    Integer horasObrigatorias = (Integer) request.getAttribute("horasObrigatorias");
    Double percentualConcluido = (Double) request.getAttribute("percentualConcluido");
    
    if (horasCumpridas == null) horasCumpridas = 0;
    if (horasFaltantes == null) horasFaltantes = 200;
    if (horasObrigatorias == null) horasObrigatorias = 200;
    if (percentualConcluido == null) percentualConcluido = 0.0;
    
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
%>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atividades Complementares - Sistema Acadêmico</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>
    
    <div class="container">
        <h1>Atividades Complementares</h1>
        
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
        
        <div class="horas-section">
            <div class="horas-card">
                <h2>Progresso das Horas Complementares</h2>
                
                <div class="horas-stats">
                    <div class="stat">
                        <div class="stat-value cumpridas"><%= horasCumpridas %></div>
                        <div class="stat-label">Horas Cumpridas</div>
                    </div>
                    
                    <div class="stat">
                        <div class="stat-value faltantes"><%= horasFaltantes %></div>
                        <div class="stat-label">Horas Faltantes</div>
                    </div>
                    
                    <div class="stat">
                        <div class="stat-value total"><%= horasObrigatorias %></div>
                        <div class="stat-label">Total Obrigatório</div>
                    </div>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-large">
                        <div class="progress-fill-large" 
                             style="width: <%= Math.min(percentualConcluido, 100) %>%">
                            <%= String.format("%.1f", percentualConcluido) %>%
                        </div>
                    </div>
                </div>
                
                <% if (horasFaltantes == 0) { %>
                    <div class="alert alert-success">
                        🎉 Parabéns! Você completou as horas complementares obrigatórias!
                    </div>
                <% } else if (percentualConcluido >= 75) { %>
                    <div class="alert alert-info">
                        👍 Você está quase lá! Faltam apenas <%= horasFaltantes %> horas!
                    </div>
                <% } %>
                
                <button type="button" class="btn btn-primary" onclick="mostrarFormAtividade()">
                    ➕ Adicionar Nova Atividade
                </button>
            </div>
        </div>
        
        <div class="atividades-section">
            <h2>Minhas Atividades</h2>
            
            <% if (atividades != null && !atividades.isEmpty()) { %>
                <div class="atividades-grid">
                    <% for (AtividadeComplementar ativ : atividades) { %>
                    <div class="atividade-card">
                        <div class="atividade-header">
                            <span class="tipo-badge"><%= ativ.getTipo() %></span>
                            <span class="horas-badge"><%= ativ.getHoras() %>h</span>
                        </div>
                        <h3><%= ativ.getDescricao() %></h3>
                        <p class="atividade-data">
                            📅 <%= ativ.getDataRealizacao().format(formatter) %>
                        </p>
                        <% if (ativ.getCertificado() != null && !ativ.getCertificado().isEmpty()) { %>
                        <p class="atividade-cert">📄 <%= ativ.getCertificado() %></p>
                        <% } %>
                        <form action="atividades" method="post" style="display: inline;"
                              onsubmit="return confirm('Deseja realmente excluir esta atividade?');">
                            <input type="hidden" name="action" value="excluir">
                            <input type="hidden" name="id" value="<%= ativ.getId() %>">
                            <button type="submit" class="btn btn-danger btn-small">Excluir</button>
                        </form>
                    </div>
                    <% } %>
                </div>
            <% } else { %>
                <div class="empty-state">
                    <p>Nenhuma atividade cadastrada ainda.</p>
                    <p>Comece adicionando suas primeiras atividades complementares!</p>
                </div>
            <% } %>
        </div>
        
        <div class="info-section">
            <h3>📋 Tipos de Atividades Aceitas</h3>
            <ul class="atividades-aceitas">
                <li><strong>Cursos:</strong> Cursos de extensão, atualização, aperfeiçoamento</li>
                <li><strong>Palestras:</strong> Participação em palestras, seminários, congressos</li>
                <li><strong>Workshops:</strong> Workshops e oficinas na área</li>
                <li><strong>Eventos:</strong> Participação em eventos acadêmicos</li>
                <li><strong>Projetos:</strong> Participação em projetos de pesquisa ou extensão</li>
                <li><strong>Monitoria:</strong> Atividades de monitoria acadêmica</li>
                <li><strong>Voluntariado:</strong> Trabalho voluntário relacionado à área</li>
            </ul>
        </div>
    </div>
    
    <div id="formAtividade" class="modal" style="display: none;">
        <div class="modal-content">
            <span class="close" onclick="fecharFormAtividade()">&times;</span>
            <h2>Adicionar Atividade Complementar</h2>
            
            <form action="atividades" method="post">
                <input type="hidden" name="action" value="adicionar">
                
                <div class="form-group">
                    <label for="tipo">Tipo de Atividade:</label>
                    <select id="tipo" name="tipo" required class="form-control">
                        <option value="">Selecione...</option>
                        <option value="Curso">Curso</option>
                        <option value="Palestra">Palestra</option>
                        <option value="Workshop">Workshop</option>
                        <option value="Evento">Evento</option>
                        <option value="Projeto">Projeto</option>
                        <option value="Monitoria">Monitoria</option>
                        <option value="Voluntariado">Voluntariado</option>
                        <option value="Outro">Outro</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="descricao">Descrição:</label>
                    <input type="text" id="descricao" name="descricao" required 
                           placeholder="Ex: Curso de Java Avançado" class="form-control">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="horas">Horas:</label>
                        <input type="number" id="horas" name="horas" required min="1" 
                               class="form-control" placeholder="40">
                    </div>
                    
                    <div class="form-group">
                        <label for="dataRealizacao">Data de Realização:</label>
                        <input type="date" id="dataRealizacao" name="dataRealizacao" 
                               required class="form-control">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="certificado">Certificado (opcional):</label>
                    <input type="text" id="certificado" name="certificado" 
                           placeholder="Ex: Certificado #12345" class="form-control">
                </div>
                
                <button type="submit" class="btn btn-primary">Adicionar Atividade</button>
            </form>
        </div>
    </div>
    
    <script>
        function mostrarFormAtividade() {
            document.getElementById('formAtividade').style.display = 'block';
        }
        
        function fecharFormAtividade() {
            document.getElementById('formAtividade').style.display = 'none';
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('formAtividade');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>