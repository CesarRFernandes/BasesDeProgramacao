package serializar;

import java.io.Serializable;

public class Professor implements Serializable {
    public String nome;
    private int idade;
    private String telefone;

    public Pessoa (Sting nome, int idade, String Telefone){
        super();
        this.nome = nome;
        this.idade = idade;
        this.telefone = telefone;
    }
    public String getNome (){
        return nome;
    }
    public void setNome(String nome){
        this.nome = nome;
    }
    public int getIdade (){
        return idade;
    }
    public void setIdade(int idade){
        this.idade = idade;
    }
    public String getTelefone (){
        return telefone;
    }
    public void setTelefone(String telefone){
        this.telefone = telefone;
    }
    @Override
    public String toString(){
        return "Pessoa [nome" + nome + ", idade" + idade + ", telefone" + telefone + "]";
    }
}
