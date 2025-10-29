package com.academico.service;

import com.academico.model.Nota;
import java.util.List;

/**
 * Interface Strategy para cálculo do Coeficiente de Rendimento (CR)
 * Permite diferentes implementações de cálculo
 */
public interface EstrategiaCR {
    
    /**
     * Calcula o CR baseado em uma lista de notas
     * @param notas Lista de notas do aluno
     * @return Valor do CR calculado
     */
    double calcular(List<Nota> notas);
}