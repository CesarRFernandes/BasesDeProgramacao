package br.com.seuprojeto.dao;

public class TesteConexao {
    public static void main(String[] args) {
        ProfessorDAO dao = new ProfessorDAO();
        dao.listarProfessores(); 
    }
}