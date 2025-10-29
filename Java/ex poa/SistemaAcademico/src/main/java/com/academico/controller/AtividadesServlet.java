package com.academico.controller;

import com.academico.dao.AtividadeDAO;
import com.academico.model.AtividadeComplementar;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.time.LocalDate;
import java.util.List;

/**
 * Servlet 3: AtividadesServlet
 * Responsável por:
 * - Listar atividades complementares
 * - Calcular total de horas cumpridas
 * - Adicionar novas atividades
 * - Excluir atividades
 */
@WebServlet("/atividades")
public class AtividadesServlet extends HttpServlet {
    
    private AtividadeDAO atividadeDAO = new AtividadeDAO();
    private static final int HORAS_OBRIGATORIAS = 200;
    
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
            List<AtividadeComplementar> atividades = atividadeDAO.listarPorAluno(alunoId);
            int horasCumpridas = atividadeDAO.calcularHorasTotais(alunoId);
            int horasFaltantes = Math.max(0, HORAS_OBRIGATORIAS - horasCumpridas);
            double percentualConcluido = (horasCumpridas * 100.0) / HORAS_OBRIGATORIAS;
            
            req.setAttribute("atividades", atividades);
            req.setAttribute("horasCumpridas", horasCumpridas);
            req.setAttribute("horasFaltantes", horasFaltantes);
            req.setAttribute("horasObrigatorias", HORAS_OBRIGATORIAS);
            req.setAttribute("percentualConcluido", Math.min(100, percentualConcluido));
            
            req.getRequestDispatcher("atividades.jsp").forward(req, resp);
        } catch (Exception e) {
            e.printStackTrace();
            req.setAttribute("erro", "Erro ao carregar atividades: " + e.getMessage());
            req.getRequestDispatcher("atividades.jsp").forward(req, resp);
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
            adicionarAtividade(req, resp);
        } else if ("excluir".equals(action)) {
            excluirAtividade(req, resp);
        } else {
            doGet(req, resp);
        }
    }
    
    /**
     * Adiciona uma nova atividade complementar
     */
    private void adicionarAtividade(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        int alunoId = (int) req.getSession().getAttribute("alunoId");
        
        try {
            AtividadeComplementar atividade = new AtividadeComplementar();
            atividade.setAlunoId(alunoId);
            atividade.setTipo(req.getParameter("tipo"));
            atividade.setDescricao(req.getParameter("descricao"));
            atividade.setHoras(Integer.parseInt(req.getParameter("horas")));
            atividade.setDataRealizacao(LocalDate.parse(req.getParameter("dataRealizacao")));
            atividade.setCertificado(req.getParameter("certificado"));
            
            boolean sucesso = atividadeDAO.inserir(atividade);
            
            if (sucesso) {
                req.setAttribute("sucesso", "Atividade adicionada com sucesso!");
            } else {
                req.setAttribute("erro", "Erro ao adicionar atividade");
            }
        } catch (Exception e) {
            req.setAttribute("erro", "Erro ao adicionar atividade: " + e.getMessage());
        }
        
        doGet(req, resp);
    }
    
    /**
     * Exclui uma atividade complementar
     */
    private void excluirAtividade(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        try {
            int id = Integer.parseInt(req.getParameter("id"));
            boolean sucesso = atividadeDAO.excluir(id);
            
            if (sucesso) {
                req.setAttribute("sucesso", "Atividade excluída com sucesso!");
            } else {
                req.setAttribute("erro", "Erro ao excluir atividade");
            }
        } catch (Exception e) {
            req.setAttribute("erro", "Erro ao excluir atividade: " + e.getMessage());
        }
        
        doGet(req, resp);
    }
}