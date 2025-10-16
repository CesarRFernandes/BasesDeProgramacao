package br.com.seuprojeto.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConexaoBD {

    private Connection con;

    public void iniciaBD() {
        try {
            String database = "jdbc:mysql://localhost/poaBD";
            String usuario = "admin";
            String senha = "teste";

            Class.forName("com.mysql.cj.jdbc.Driver");
            con = DriverManager.getConnection(database, usuario, senha);

            System.out.println("Conexão com o banco de dados estabelecida com sucesso!");
        } catch (Exception e) {
            System.out.println("Erro ao conectar ao banco de dados:");
            e.printStackTrace();
        }
    }

    public void fechaBD() {
        try {
            if (con != null) {
                con.close();
                System.out.println("Conexão fechada com sucesso!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public Connection getConexao() {
        return con;
    }
}
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