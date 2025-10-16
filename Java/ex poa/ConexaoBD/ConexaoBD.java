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