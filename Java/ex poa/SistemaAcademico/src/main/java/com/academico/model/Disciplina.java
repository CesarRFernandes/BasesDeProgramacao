package com.academico.model;

public class Disciplina {
    private int id;
    private String codigo;
    private String nome;
    private int cargaHoraria;
    private int periodo;
    
    public Disciplina() {}
    
    public Disciplina(int id, String codigo, String nome, int cargaHoraria, int periodo) {
        this.id = id;
        this.codigo = codigo;
        this.nome = nome;
        this.cargaHoraria = cargaHoraria;
        this.periodo = periodo;
    }
    
    public int getId() { 
        return id; 
    }
    
    public void setId(int id) { 
        this.id = id; 
    }
    
    public String getCodigo() { 
        return codigo; 
    }
    
    public void setCodigo(String codigo) { 
        this.codigo = codigo; 
    }
    
    public String getNome() { 
        return nome; 
    }
    
    public void setNome(String nome) { 
        this.nome = nome; 
    }
    
    public int getCargaHoraria() { 
        return cargaHoraria; 
    }
    
    public void setCargaHoraria(int cargaHoraria) { 
        this.cargaHoraria = cargaHoraria; 
    }
    
    public int getPeriodo() { 
        return periodo; 
    }
    
    public void setPeriodo(int periodo) { 
        this.periodo = periodo; 
    }
}