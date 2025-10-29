<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.academico.model.Nota, java.util.List" %>
<%
    if (session.getAttribute("aluno") == null) {
        response.sendRedirect("login.jsp");
        return;
    }
    
    List<Nota> notas = (List<Nota>) request.getAttribute("notas");
    Double cr = (Double) request.getAttribute("cr");
    Double percentual = (Double) request.getAttribute("percentual");
    String classificacao = (String) request.getAttribute("classificacao");
    Integer totalDisciplinas = (Integer) request.getAttribute("totalDisciplinas");
    
    if (cr == null) cr = 0.0;
    if (percentual == null) percentual = 0.0;
    if (classificacao == null) classificacao = "Sem dados";
    if (totalDisciplinas == null) totalDisciplinas = 0;
%>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minhas Notas - Sistema Acadêmico</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>
    
    <div class="container">
        <h1>Minhas Notas</h1>
        
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
        
        <div class="cr-section">
            <div class="cr-card">
                <h2>Coeficiente de Rendimento (CR)</h2>
                <div class="cr-value">
                    <%= String.format("%.2f", cr) %>
                </div>
                <div class="cr-details">
                    <p><strong>Classificação:</strong> <%= classificacao %></p>
                    <p><strong>Aproveitamento:</strong> <%= String.format("%.1f", percentual) %>%</p>
                    <p><strong>Disciplinas Cursadas:</strong> <%= totalDisciplinas %></p>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: <%= Math.min(percentual, 100) %>%"></div>
                </div>
            </div>
        </div>
        
        <div class="notas-section">
            <h2>Histórico de Notas</h2>
            
            <% if (notas != null && !notas.isEmpty()) { %>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Período</th>
                                <th>Código</th>
                                <th>Disciplina</th>
                                <th>Carga Horária</th>
                                <th>Nota</th>
                                <th>Semestre/Ano</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <% 
                            int periodoAtual = -1;
                            for (Nota nota : notas) {
                                boolean novoPeriodo = nota.getDisciplina().getPeriodo() != periodoAtual;
                                if (novoPeriodo) {
                                    periodoAtual = nota.getDisciplina().getPeriodo();
                                }
                                
                                String statusClass = nota.getNota() >= 6.0 ? "status-aprovado" : "status-reprovado";
                                String statusText = nota.getNota() >= 6.0 ? "Aprovado" : "Reprovado";
                            %>
                            <tr <%= novoPeriodo ? "class='periodo-novo'" : "" %>>
                                <td><%= nota.getDisciplina().getPeriodo() %>º</td>
                                <td><%= nota.getDisciplina().getCodigo() %></td>
                                <td><%= nota.getDisciplina().getNome() %></td>
                                <td><%= nota.getDisciplina().getCargaHoraria() %>h</td>
                                <td class="nota-valor"><%= String.format("%.2f", nota.getNota()) %></td>
                                <td><%= nota.getSemestre() %>/<%= nota.getAno() %></td>
                                <td><span class="status-badge <%= statusClass %>"><%= statusText %></span></td>
                            </tr>
                            <% } %>
                        </tbody>
                    </table>
                </div>
            <% } else { %>
                <div class="empty-state">
                    <p>Nenhuma nota cadastrada ainda.</p>
                </div>
            <% } %>
        </div>
        
        <div class="info-section">
            <h3>📊 Como o CR é Calculado?</h3>
            <p>O Coeficiente de Rendimento (CR) é calculado pela média ponderada das notas, 
               considerando a carga horária de cada disciplina:</p>
            <div class="formula">
                CR = Σ(nota × carga_horária) / Σ(carga_horária)
            </div>
            
            <h4>Classificação:</h4>
            <ul class="classificacao-list">
                <li><strong>Excelente:</strong> CR ≥ 9.0</li>
                <li><strong>Ótimo:</strong> 8.0 ≤ CR < 9.0</li>
                <li><strong>Bom:</strong> 7.0 ≤ CR < 8.0</li>
                <li><strong>Regular:</strong> 6.0 ≤ CR < 7.0</li>
                <li><strong>Insuficiente:</strong> CR < 6.0</li>
            </ul>
        </div>
    </div>
</body>
</html>