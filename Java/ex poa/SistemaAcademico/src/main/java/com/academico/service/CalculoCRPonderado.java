package com.academico.service;

import com.academico.model.Nota;
import java.util.List;

/**
 * Estratégia de cálculo do CR ponderado pela carga horária
 * Fórmula: CR = Σ(nota × carga_horária) / Σ(carga_horária)
 * 
 * Esta é a forma mais justa de cálculo, pois considera que
 * disciplinas com maior carga horária têm mais peso no CR.
 */
public class CalculoCRPonderado implements EstrategiaCR {
    
    @Override
    public double calcular(List<Nota> notas) {
        if (notas == null || notas.isEmpty()) {
            return 0.0;
        }
        
        double somaPonderada = 0.0;
        int somaCargaHoraria = 0;
        
        for (Nota nota : notas) {
            if (nota.getDisciplina() != null) {
                int cargaHoraria = nota.getDisciplina().getCargaHoraria();
                somaPonderada += nota.getNota() * cargaHoraria;
                somaCargaHoraria += cargaHoraria;
            }
        }
        
        if (somaCargaHoraria == 0) {
            return 0.0;
        }
        
        // Arredonda para 2 casas decimais
        return Math.round((somaPonderada / somaCargaHoraria) * 100.0) / 100.0;
    }
}