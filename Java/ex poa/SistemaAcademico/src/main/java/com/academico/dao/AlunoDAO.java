package com.academico.dao;

import com.academico.model.Aluno;
import java.sql.*;

public class AlunoDAO {
    
    public Aluno autenticar(String email, String senha) throws SQLException {
        String sql = "SELECT * FROM alunos WHERE email = ? AND senha = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, email);
            stmt.setString(2, senha);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return extrairAluno(rs);
                }
            }
        }
        return null;
    }
    
    public Aluno buscarPorId(int id) throws SQLException {
        String sql = "SELECT * FROM alunos WHERE id = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return extrairAluno(rs);
                }
            }
        }
        return null;
    }
    
    public boolean atualizarEndereco(int id, String cep, String endereco, 
                                     String cidade, String estado) throws SQLException {
        String sql = "UPDATE alunos SET cep = ?, endereco = ?, cidade = ?, estado = ? WHERE id = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, cep);
            stmt.setString(2, endereco);
            stmt.setString(3, cidade);
            stmt.setString(4, estado);
            stmt.setInt(5, id);
            
            return stmt.executeUpdate() > 0;
        }
    }
    
    private Aluno extrairAluno(ResultSet rs) throws SQLException {
        Aluno aluno = new Aluno();
        aluno.setId(rs.getInt("id"));
        aluno.setNome(rs.getString("nome"));
        aluno.setEmail(rs.getString("email"));
        aluno.setRa(rs.getString("ra"));
        aluno.setCurso(rs.getString("curso"));
        aluno.setPeriodoAtual(rs.getInt("periodo_atual"));
        aluno.setCep(rs.getString("cep"));
        aluno.setEndereco(rs.getString("endereco"));
        aluno.setCidade(rs.getString("cidade"));
        aluno.setEstado(rs.getString("estado"));
        return aluno;
    }
}