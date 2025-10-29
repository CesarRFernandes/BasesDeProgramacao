package com.academico.dao;

import com.academico.model.Nota;
import com.academico.model.Disciplina;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class NotaDAO {
    
    public List<Nota> listarPorAluno(int alunoId) throws SQLException {
        String sql = "SELECT n.*, d.codigo, d.nome, d.carga_horaria, d.periodo " +
                     "FROM notas n " +
                     "INNER JOIN disciplinas d ON n.disciplina_id = d.id " +
                     "WHERE n.aluno_id = ? " +
                     "ORDER BY d.periodo, d.codigo";
        
        List<Nota> notas = new ArrayList<>();
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, alunoId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    notas.add(extrairNotaComDisciplina(rs));
                }
            }
        }
        return notas;
    }
    
    public boolean inserir(Nota nota) throws SQLException {
        String sql = "INSERT INTO notas (aluno_id, disciplina_id, nota, semestre, ano) " +
                     "VALUES (?, ?, ?, ?, ?)";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, nota.getAlunoId());
            stmt.setInt(2, nota.getDisciplinaId());
            stmt.setDouble(3, nota.getNota());
            stmt.setString(4, nota.getSemestre());
            stmt.setInt(5, nota.getAno());
            
            return stmt.executeUpdate() > 0;
        }
    }
    
    public boolean atualizar(Nota nota) throws SQLException {
        String sql = "UPDATE notas SET nota = ? WHERE id = ?";
        
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setDouble(1, nota.getNota());
            stmt.setInt(2, nota.getId());
            
            return stmt.executeUpdate() > 0;
        }
    }
    
    private Nota extrairNotaComDisciplina(ResultSet rs) throws SQLException {
        Nota nota = new Nota();
        nota.setId(rs.getInt("id"));
        nota.setAlunoId(rs.getInt("aluno_id"));
        nota.setDisciplinaId(rs.getInt("disciplina_id"));
        nota.setNota(rs.getDouble("nota"));
        nota.setSemestre(rs.getString("semestre"));
        nota.setAno(rs.getInt("ano"));
        
        Disciplina disciplina = new Disciplina();
        disciplina.setId(rs.getInt("disciplina_id"));
        disciplina.setCodigo(rs.getString("codigo"));
        disciplina.setNome(rs.getString("nome"));
        disciplina.setCargaHoraria(rs.getInt("carga_horaria"));
        disciplina.setPeriodo(rs.getInt("periodo"));
        
        nota.setDisciplina(disciplina);
        return nota;
    }
}