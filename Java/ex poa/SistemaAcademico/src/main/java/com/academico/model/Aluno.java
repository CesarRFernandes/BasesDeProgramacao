package com.academico.model;

public class Aluno {
    private int id;
    private String nome;
    private String email;
    private String senha;
    private String ra;
    private String curso;
    private int periodoAtual;
    private String cep;
    private String endereco;
    private String cidade;
    private String estado;
    
    public Aluno() {}
    
    public Aluno(int id, String nome, String email, String ra) {
        this.id = id;
        this.nome = nome;
        this.email = email;
        this.ra = ra;
    }
    
    // Getters e Setters
    public int getId() { 
        return id; 
    }
    
    public void setId(int id) { 
        this.id = id; 
    }
    
    public String getNome() { 
        return nome; 
    }
    
    public void setNome(String nome) { 
        this.nome = nome; 
    }
    
    public String getEmail() { 
        return email; 
    }
    
    public void setEmail(String email) { 
        this.email = email; 
    }
    
    public String getSenha() { 
        return senha; 
    }
    
    public void setSenha(String senha) { 
        this.senha = senha; 
    }
    
    public String getRa() { 
        return ra; 
    }
    
    public void setRa(String ra) { 
        this.ra = ra; 
    }
    
    public String getCurso() { 
        return curso; 
    }
    
    public void setCurso(String curso) { 
        this.curso = curso; 
    }
    
    public int getPeriodoAtual() { 
        return periodoAtual; 
    }
    
    public void setPeriodoAtual(int periodoAtual) { 
        this.periodoAtual = periodoAtual; 
    }
    
    public String getCep() { 
        return cep; 
    }
    
    public void setCep(String cep) { 
        this.cep = cep; 
    }
    
    public String getEndereco() { 
        return endereco; 
    }
    
    public void setEndereco(String endereco) { 
        this.endereco = endereco; 
    }
    
    public String getCidade() { 
        return cidade; 
    }
    
    public void setCidade(String cidade) { 
        this.cidade = cidade; 
    }
    
    public String getEstado() { 
        return estado; 
    }
    
    public void setEstado(String estado) { 
        this.estado = estado; 
    }
}