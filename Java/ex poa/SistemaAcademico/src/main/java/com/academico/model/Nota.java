package com.academico.model;

public class Nota {
    private int id;
    private int alunoId;
    private int disciplinaId;
    private double nota;
    private String semestre;
    private int ano;
    private Disciplina disciplina;
    
    public Nota() {}
    
    public Nota(int id, int alunoId, int disciplinaId, double nota, String semestre, int ano) {
        this.id = id;
        this.alunoId = alunoId;
        this.disciplinaId = disciplinaId;
        this.nota = nota;
        this.semestre = semestre;
        this.ano = ano;
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
    
    public int getDisciplinaId() { 
        return disciplinaId; 
    }
    
    public void setDisciplinaId(int disciplinaId) { 
        this.disciplinaId = disciplinaId; 
    }
    
    public double getNota() { 
        return nota; 
    }
    
    public void setNota(double nota) { 
        this.nota = nota; 
    }
    
    public String getSemestre() { 
        return semestre; 
    }
    
    public void setSemestre(String semestre) { 
        this.semestre = semestre; 
    }
    
    public int getAno() { 
        return ano; 
    }
    
    public void setAno(int ano) { 
        this.ano = ano; 
    }
    
    public Disciplina getDisciplina() { 
        return disciplina; 
    }
    
    public void setDisciplina(Disciplina disciplina) { 
        this.disciplina = disciplina; 
    }
}