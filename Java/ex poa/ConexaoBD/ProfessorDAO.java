package br.com.seuprojeto.dao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class ProfessorDAO {

    public void listarProfessores() {
        ConexaoBD conexao = new ConexaoBD();
        conexao.iniciaBD();

        try {
            Connection con = conexao.getConexao();
            String sql = "SELECT id_professor, nome, cpf, especialidade, salario FROM professor";

            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            System.out.println("=== LISTA DE PROFESSORES ===");
            while (rs.next()) {
                int id = rs.getInt("id_professor");
                String nome = rs.getString("nome");
                String cpf = rs.getString("cpf");
                String especialidade = rs.getString("especialidade");
                double salario = rs.getDouble("salario");

                System.out.println(
                    "ID: " + id +
                    " | Nome: " + nome +
                    " | CPF: " + cpf +
                    " | Especialidade: " + especialidade +
                    " | Salário: R$ " + salario
                );
            }

            rs.close();
            stmt.close();

        } catch (Exception e) {
            System.out.println("Erro ao listar professores:");
            e.printStackTrace();
        } finally {
            conexao.fechaBD();
        }
    }
}