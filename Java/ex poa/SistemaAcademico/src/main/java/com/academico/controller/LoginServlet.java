package com.academico.controller;

import com.academico.dao.AlunoDAO;
import com.academico.model.Aluno;
import com.academico.util.APIViaCEP;
import org.json.JSONObject;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;

/**
 * Servlet 1: LoginServlet
 * Responsável por:
 * - Autenticação de usuários
 * - Logout
 * - Consulta de CEP (API ViaCEP)
 * - Atualização de endereço
 */
@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    
    private AlunoDAO alunoDAO = new AlunoDAO();
    
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        String action = req.getParameter("action");
        
        if ("login".equals(action)) {
            realizarLogin(req, resp);
        } else if ("consultarCep".equals(action)) {
            consultarCEP(req, resp);
        } else if ("atualizarEndereco".equals(action)) {
            atualizarEndereco(req, resp);
        } else {
            resp.sendRedirect("login.jsp");
        }
    }
    
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        String action = req.getParameter("action");
        
        if ("logout".equals(action)) {
            HttpSession session = req.getSession(false);
            if (session != null) {
                session.invalidate();
            }
            resp.sendRedirect("login.jsp");
        } else {
            resp.sendRedirect("login.jsp");
        }
    }
    
    /**
     * Realiza o login do usuário
     */
    private void realizarLogin(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        String email = req.getParameter("email");
        String senha = req.getParameter("senha");
        
        try {
            Aluno aluno = alunoDAO.autenticar(email, senha);
            
            if (aluno != null) {
                HttpSession session = req.getSession();
                session.setAttribute("aluno", aluno);
                session.setAttribute("alunoId", aluno.getId());
                session.setAttribute("alunoNome", aluno.getNome());
                
                resp.sendRedirect("dashboard.jsp");
            } else {
                req.setAttribute("erro", "Email ou senha inválidos");
                req.getRequestDispatcher("login.jsp").forward(req, resp);
            }
        } catch (Exception e) {
            e.printStackTrace();
            req.setAttribute("erro", "Erro ao realizar login: " + e.getMessage());
            req.getRequestDispatcher("login.jsp").forward(req, resp);
        }
    }
    
    /**
     * Consulta CEP usando a API ViaCEP
     */
    private void consultarCEP(HttpServletRequest req, HttpServletResponse resp) 
            throws IOException {
        
        String cep = req.getParameter("cep");
        
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        
        try {
            JSONObject endereco = APIViaCEP.buscarEnderecoPorCEP(cep);
            
            if (endereco != null) {
                resp.getWriter().write(endereco.toString());
            } else {
                JSONObject erro = new JSONObject();
                erro.put("erro", true);
                erro.put("mensagem", "CEP não encontrado");
                resp.getWriter().write(erro.toString());
            }
        } catch (Exception e) {
            JSONObject erro = new JSONObject();
            erro.put("erro", true);
            erro.put("mensagem", "Erro ao consultar CEP: " + e.getMessage());
            resp.getWriter().write(erro.toString());
        }
    }
    
    /**
     * Atualiza o endereço do aluno
     */
    private void atualizarEndereco(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("alunoId") == null) {
            resp.sendRedirect("login.jsp");
            return;
        }
        
        int alunoId = (int) session.getAttribute("alunoId");
        String cep = req.getParameter("cep");
        String endereco = req.getParameter("endereco");
        String cidade = req.getParameter("cidade");
        String estado = req.getParameter("estado");
        
        try {
            boolean sucesso = alunoDAO.atualizarEndereco(alunoId, cep, endereco, cidade, estado);
            
            if (sucesso) {
                Aluno aluno = alunoDAO.buscarPorId(alunoId);
                session.setAttribute("aluno", aluno);
                req.setAttribute("sucesso", "Endereço atualizado com sucesso!");
            } else {
                req.setAttribute("erro", "Erro ao atualizar endereço");
            }
        } catch (Exception e) {
            req.setAttribute("erro", "Erro ao atualizar endereço: " + e.getMessage());
        }
        
        req.getRequestDispatcher("dashboard.jsp").forward(req, resp);
    }
}