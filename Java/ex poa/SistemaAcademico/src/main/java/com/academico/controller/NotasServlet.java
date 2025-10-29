package com.academico.controller;

import com.academico.dao.NotaDAO;
import com.academico.model.Nota;
import com.academico.service.CalculadoraCR;
import com.academico.service.CalculoCRPonderado;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.util.List;

/**
 * Servlet 2: NotasServlet
 * Responsável por:
 * - Listar notas do aluno
 * - Calcular o CR usando o padrão Strategy
 * - Adicionar novas notas
 * - Atualizar notas existentes
 */
@WebServlet("/notas")
public class NotasServlet extends HttpServlet {
    
    private NotaDAO notaDAO = new NotaDAO();
    private CalculadoraCR calculadora = new CalculadoraCR(new CalculoCRPonderado());
    
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("alunoId") == null) {
            resp.sendRedirect("login.jsp");
            return;
        }
        
        int alunoId = (int) session.getAttribute("alunoId");
        
        try {
            List<Nota> notas = notaDAO.listarPorAluno(alunoId);
            
            // Calcula o CR usando o padrão Strategy
            double cr = calculadora.calcularCR(notas);
            double percentual = calculadora.calcularPercentualAproveitamento(cr);
            String classificacao = calculadora.classificarDesempenho(cr);
            
            req.setAttribute("notas", notas);
            req.setAttribute("cr", cr);
            req.setAttribute("percentual", percentual);
            req.setAttribute("classificacao", classificacao);
            req.setAttribute("totalDisciplinas", notas.size());
            
            req.getRequestDispatcher("notas.jsp").forward(req, resp);
        } catch (Exception e) {
            e.printStackTrace();
            req.setAttribute("erro", "Erro ao carregar notas: " + e.getMessage());
            req.getRequestDispatcher("notas.jsp").forward(req, resp);
        }
    }
    
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("alunoId") == null) {
            resp.sendRedirect("login.jsp");
            return;
        }
        
        String action = req.getParameter("action");
        
        if ("adicionar".equals(action)) {
            adicionarNota(req, resp);
        } else if ("atualizar".equals(action)) {
            atualizarNota(req, resp);
        } else {
            doGet(req, resp);
        }
    }
    
    /**
     * Adiciona uma nova nota
     */
    private void adicionarNota(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        int alunoId = (int) req.getSession().getAttribute("alunoId");
        
        try {
            Nota nota = new Nota();
            nota.setAlunoId(alunoId);
            nota.setDisciplinaId(Integer.parseInt(req.getParameter("disciplinaId")));
            nota.setNota(Double.parseDouble(req.getParameter("nota")));
            nota.setSemestre(req.getParameter("semestre"));
            nota.setAno(Integer.parseInt(req.getParameter("ano")));
            
            boolean sucesso = notaDAO.inserir(nota);
            
            if (sucesso) {
                req.setAttribute("sucesso", "Nota adicionada com sucesso!");
            } else {
                req.setAttribute("erro", "Erro ao adicionar nota");
            }
        } catch (Exception e) {
            req.setAttribute("erro", "Erro ao adicionar nota: " + e.getMessage());
        }
        
        doGet(req, resp);
    }
    
    /**
     * Atualiza uma nota existente
     */
    private void atualizarNota(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        try {
            Nota nota = new Nota();
            nota.setId(Integer.parseInt(req.getParameter("notaId")));
            nota.setNota(Double.parseDouble(req.getParameter("nota")));
            
            boolean sucesso = notaDAO.atualizar(nota);
            
            if (sucesso) {
                req.setAttribute("sucesso", "Nota atualizada com sucesso!");
            } else {
                req.setAttribute("erro", "Erro ao atualizar nota");
            }
        } catch (Exception e) {
            req.setAttribute("erro", "Erro ao atualizar nota: " + e.getMessage());
        }
        
        doGet(req, resp);
    }
}