package com.academico.model;

import java.time.LocalDate;

public class AtividadeComplementar {
    private int id;
    private int alunoId;
    private String tipo;
    private String descricao;
    private int horas;
    private LocalDate dataRealizacao;
    private String certificado;
    
    public AtividadeComplementar() {}
    
    public AtividadeComplementar(int id, int alunoId, String tipo, String descricao, 
                                 int horas, LocalDate dataRealizacao) {
        this.id = id;
        this.alunoId = alunoId;
        this.tipo = tipo;
        this.descricao = descricao;
        this.horas = horas;
        this.dataRealizacao = dataRealizacao;
    }
    
    public int getId() { 
        return id; 
    }
    
    public void setId(int id) { 
        this.id = id; 
    }
    
    public int getAlunoId() { 
        return alunoId; 
    }
    
    public void setAlunoId(int alunoId) { 
        this.alunoId = alunoId; 
    }
    
    public String getTipo() { 
        return tipo; 
    }
    
    public void setTipo(String tipo) { 
        this.tipo = tipo; 
    }
    
    public String getDescricao() { 
        return descricao; 
    }
    
    public void setDescricao(String descricao) { 
        this.descricao = descricao; 
    }
    
    public int getHoras() { 
        return horas; 
    }
    
    public void setHoras(int horas) { 
        this.horas = horas; 
    }
    
    public LocalDate getDataRealizacao() { 
        return dataRealizacao; 
    }
    
    public void setDataRealizacao(LocalDate dataRealizacao) { 
        this.dataRealizacao = dataRealizacao; 
    }
    
    public String getCertificado() { 
        return certificado; 
    }
    
    public void setCertificado(String certificado) { 
        this.certificado = certificado; 
    }
}