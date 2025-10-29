package com.academico.service;

import com.academico.model.Nota;
import java.util.List;

/**
 * Estratégia de cálculo do CR simples (média aritmética)
 * Fórmula: CR = Σ(notas) / quantidade_disciplinas
 * 
 * Esta forma de cálculo trata todas as disciplinas com o mesmo peso,
 * independente da carga horária.
 */
public class CalculoCRSimples implements EstrategiaCR {
    
    @Override
    public double calcular(List<Nota> notas) {
        if (notas == null || notas.isEmpty()) {
            return 0.0;
        }
        
        double somaNotas = 0.0;
        
        for (Nota nota : notas) {
            somaNotas += nota.getNota();
        }
        
        // Arredonda para 2 casas decimais
        return Math.round((somaNotas / notas.size()) * 100.0) / 100.0;
    }
}