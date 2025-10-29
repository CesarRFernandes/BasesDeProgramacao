package com.academico.service;

import com.academico.model.Nota;
import java.util.List;

/**
 * Classe contexto do padrão Strategy
 * Permite escolher diferentes estratégias de cálculo do CR em tempo de execução
 * 
 * PADRÃO DE PROJETO: STRATEGY
 * - Define uma família de algoritmos (cálculo de CR)
 * - Encapsula cada um deles (CalculoCRPonderado, CalculoCRSimples)
 * - Torna-os intercambiáveis (pode trocar a estratégia dinamicamente)
 */
public class CalculadoraCR {
    
    private EstrategiaCR estrategia;
    
    /**
     * Construtor padrão - usa cálculo ponderado
     */
    public CalculadoraCR() {
        this.estrategia = new CalculoCRPonderado();
    }
    
    /**
     * Construtor que permite escolher a estratégia
     */
    public CalculadoraCR(EstrategiaCR estrategia) {
        this.estrategia = estrategia;
    }
    
    /**
     * Permite trocar a estratégia em tempo de execução
     */
    public void setEstrategia(EstrategiaCR estrategia) {
        this.estrategia = estrategia;
    }
    
    /**
     * Calcula o CR usando a estratégia configurada
     */
    public double calcularCR(List<Nota> notas) {
        return estrategia.calcular(notas);
    }
    
    /**
     * Calcula o percentual de aproveitamento baseado no CR
     * @param cr Coeficiente de Rendimento
     * @return Percentual de 0 a 100
     */
    public double calcularPercentualAproveitamento(double cr) {
        return Math.round((cr / 10.0) * 100.0 * 100.0) / 100.0;
    }
    
    /**
     * Retorna a classificação baseada no CR
     * @param cr Coeficiente de Rendimento
     * @return String com a classificação do desempenho
     */
    public String classificarDesempenho(double cr) {
        if (cr >= 9.0) {
            return "Excelente";
        } else if (cr >= 8.0) {
            return "Ótimo";
        } else if (cr >= 7.0) {
            return "Bom";
        } else if (cr >= 6.0) {
            return "Regular";
        } else {
            return "Insuficiente";
        }
    }
}