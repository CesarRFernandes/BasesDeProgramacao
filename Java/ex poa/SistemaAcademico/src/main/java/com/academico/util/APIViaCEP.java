package com.academico.util;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

/**
 * Classe para integração com a API ViaCEP
 * API pública que retorna informações de endereço baseado no CEP
 */
public class APIViaCEP {
    
    private static final String BASE_URL = "https://viacep.com.br/ws/";
    
    /**
     * Busca informações de endereço pelo CEP
     * @param cep CEP a ser consultado (apenas números)
     * @return JSONObject com os dados do endereço ou null se não encontrado
     */
    public static JSONObject buscarEnderecoPorCEP(String cep) {
        try {
            // Remove caracteres não numéricos do CEP
            cep = cep.replaceAll("[^0-9]", "");
            
            if (cep.length() != 8) {
                throw new IllegalArgumentException("CEP deve conter 8 dígitos");
            }
            
            // Monta a URL da API
            String urlString = BASE_URL + cep + "/json/";
            URL url = new URL(urlString);
            
            // Abre a conexão
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            
            // Verifica o código de resposta
            int responseCode = conn.getResponseCode();
            
            if (responseCode == 200) {
                // Lê a resposta
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(conn.getInputStream())
                );
                
                StringBuilder response = new StringBuilder();
                String line;
                
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                
                reader.close();
                conn.disconnect();
                
                // Converte para JSONObject
                JSONObject json = new JSONObject(response.toString());
                
                // Verifica se o CEP foi encontrado
                if (json.has("erro") && json.getBoolean("erro")) {
                    return null;
                }
                
                return json;
            } else {
                conn.disconnect();
                return null;
            }
            
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    
    /**
     * Busca apenas o logradouro pelo CEP
     */
    public static String buscarLogradouro(String cep) {
        JSONObject json = buscarEnderecoPorCEP(cep);
        return json != null ? json.optString("logradouro", "") : "";
    }
    
    /**
     * Busca apenas o bairro pelo CEP
     */
    public static String buscarBairro(String cep) {
        JSONObject json = buscarEnderecoPorCEP(cep);
        return json != null ? json.optString("bairro", "") : "";
    }
    
    /**
     * Busca apenas a cidade pelo CEP
     */
    public static String buscarCidade(String cep) {
        JSONObject json = buscarEnderecoPorCEP(cep);
        return json != null ? json.optString("localidade", "") : "";
    }
    
    /**
     * Busca apenas o estado (UF) pelo CEP
     */
    public static String buscarEstado(String cep) {
        JSONObject json = buscarEnderecoPorCEP(cep);
        return json != null ? json.optString("uf", "") : "";
    }
    
    /**
     * Retorna o endereço completo formatado
     */
    public static String buscarEnderecoCompleto(String cep) {
        JSONObject json = buscarEnderecoPorCEP(cep);
        
        if (json == null) {
            return "CEP não encontrado";
        }
        
        String logradouro = json.optString("logradouro", "");
        String bairro = json.optString("bairro", "");
        String cidade = json.optString("localidade", "");
        String estado = json.optString("uf", "");
        
        return String.format("%s, %s - %s/%s", logradouro, bairro, cidade, estado);
    }
}

/**
 * Exemplo de uso:
 * 
 * JSONObject endereco = APIViaCEP.buscarEnderecoPorCEP("01310100");
 * 
 * if (endereco != null) {
 *     String logradouro = endereco.getString("logradouro");
 *     String bairro = endereco.getString("bairro");
 *     String cidade = endereco.getString("localidade");
 *     String estado = endereco.getString("uf");
 * }
 * 
 * ou simplesmente:
 * 
 * String endereco = APIViaCEP.buscarEnderecoCompleto("01310100");
 */