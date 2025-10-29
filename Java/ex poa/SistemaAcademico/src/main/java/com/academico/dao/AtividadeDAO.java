package com.academico.dao;

import com.academico.model.AtividadeComplementar;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class AtividadeDAO {
    
    public List<AtividadeComplementar> listarPorAluno(int alunoId) throws SQLException {
        String sql = "SELECT * FROM atividades_complementares WHERE aluno_id = ? " +
                     "ORDER BY data_realizacao DESC";
        
        List<AtividadeComplementar> atividades = new ArrayList<>();
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, alunoId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    atividades.add(extrairAtividade(rs));
                }
            }
        }
        return atividades;
    }
    
    public int calcularHorasTotais(int alunoId) throws SQLException {
        String sql = "SELECT COALESCE(SUM(horas), 0) as total FROM atividades_complementares " +
                     "WHERE aluno_id = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, alunoId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("total");
                }
            }
        }
        return 0;
    }
    
    public boolean inserir(AtividadeComplementar atividade) throws SQLException {
        String sql = "INSERT INTO atividades_complementares " +
                     "(aluno_id, tipo, descricao, horas, data_realizacao, certificado) " +
                     "VALUES (?, ?, ?, ?, ?, ?)";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, atividade.getAlunoId());
            stmt.setString(2, atividade.getTipo());
            stmt.setString(3, atividade.getDescricao());
            stmt.setInt(4, atividade.getHoras());
            stmt.setDate(5, Date.valueOf(atividade.getDataRealizacao()));
            stmt.setString(6, atividade.getCertificado());
            
            return stmt.executeUpdate() > 0;
        }
    }
    
    public boolean excluir(int id) throws SQLException {
        String sql = "DELETE FROM atividades_complementares WHERE id = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, id);
            return stmt.executeUpdate() > 0;
        }
    }
    
    private AtividadeComplementar extrairAtividade(ResultSet rs) throws SQLException {
        AtividadeComplementar atividade = new AtividadeComplementar();
        atividade.setId(rs.getInt("id"));
        atividade.setAlunoId(rs.getInt("aluno_id"));
        atividade.setTipo(rs.getString("tipo"));
        atividade.setDescricao(rs.getString("descricao"));
        atividade.setHoras(rs.getInt("horas"));
        atividade.setDataRealizacao(rs.getDate("data_realizacao").toLocalDate());
        atividade.setCertificado(rs.getString("certificado"));
        return atividade;
    }
}