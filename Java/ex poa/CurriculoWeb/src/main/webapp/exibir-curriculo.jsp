<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini-CV - <%= request.getAttribute("nome") %></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', serif;
            background: #f5f7fa;
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }
        
        .cv-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
            animation: fadeIn 0.8s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .cv-header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
        }
        
        .cv-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="40%"><stop offset="0%" stop-color="%23ffffff" stop-opacity="0.1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
            opacity: 0.3;
        }
        
        .cv-header h1 {
            font-size: 3rem;
            font-weight: 300;
            margin-bottom: 10px;
            z-index: 1;
            position: relative;
        }
        
        .cv-header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            z-index: 1;
            position: relative;
        }
        
        .cv-content {
            padding: 40px;
        }
        
        .cv-section {
            margin-bottom: 35px;
            border-left: 4px solid #3498db;
            padding-left: 20px;
        }
        
        .cv-section h2 {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .cv-section .icon {
            font-size: 1.3rem;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }
        
        .info-item h3 {
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .info-item p {
            color: #555;
            font-size: 1.1rem;
        }
        
        .areas-interesse {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        
        .area-tag {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 2px 5px rgba(52, 152, 219, 0.3);
        }
        
        .experiencia-box {
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'Arial', sans-serif;
            line-height: 1.7;
            color: #444;
        }
        
        .actions {
            text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 0 10px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }
        
        .btn-secondary {
            background: #95a5a6;
            color: white;
            box-shadow: 0 4px 15px rgba(149, 165, 166, 0.3);
        }
        
        .btn-secondary:hover {
            transform: translateY(-2px);
            background: #7f8c8d;
            box-shadow: 0 6px 20px rgba(149, 165, 166, 0.4);
        }
        
        .print-info {
            text-align: center;
            margin-bottom: 20px;
            color: #666;
            font-style: italic;
        }
        
        @media print {
            body {
                background: white;
                font-size: 12pt;
            }
            
            .cv-container {
                box-shadow: none;
                border-radius: 0;
                max-width: none;
            }
            
            .actions, .print-info {
                display: none;
            }
            
            .cv-header {
                background: #2c3e50 !important;
                -webkit-print-color-adjust: exact;
            }
        }
        
        @media (max-width: 768px) {
            .cv-header h1 {
                font-size: 2rem;
            }
            
            .cv-content {
                padding: 20px;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
            
            .areas-interesse {
                justify-content: center;
            }
            
            .btn {
                display: block;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <div class="cv-container">
        <div class="cv-header">
            <h1><%= request.getAttribute("nome") %></h1>
            <p class="subtitle">Currículo Profissional</p>
        </div>
        
        <div class="cv-content">
            <div class="print-info">
                💡 Use Ctrl+P para imprimir este currículo
            </div>
            
            <div class="cv-section">
                <h2><span class="icon">ℹ️</span> Informações Pessoais</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <h3>Idade</h3>
                        <p><%= request.getAttribute("idade") %> anos</p>
                    </div>
                    <div class="info-item">
                        <h3>Escolaridade</h3>
                        <p><%= request.getAttribute("escolaridade") %></p>
                    </div>
                </div>
            </div>
            
            <div class="cv-section">
                <h2><span class="icon">🎯</span> Áreas de Interesse</h2>
                <div class="areas-interesse">
                    <% 
                    String areas = (String) request.getAttribute("areasInteresse");
                    if (areas != null && !areas.equals("Não informado")) {
                        String[] areasArray = areas.split(", ");
                        for (String area : areasArray) {
                    %>
                        <span class="area-tag"><%= area %></span>
                    <% 
                        }
                    } else {
                    %>
                        <span class="area-tag" style="background: #95a5a6;">Não informado</span>
                    <% } %>
                </div>
            </div>
            
            <div class="cv-section">
                <h2><span class="icon">💼</span> Experiência Profissional</h2>
                <div class="experiencia-box">
                    <%= request.getAttribute("experiencia") != null && 
                        !request.getAttribute("experiencia").equals("Não informado") 
                        ? request.getAttribute("experiencia") 
                        : "Experiência não informada. Candidato(a) pode estar iniciando a carreira profissional ou buscando uma transição de área." %>
                </div>
            </div>
        </div>
        
        <div class="actions">
            <a href="cadastro-curriculo.jsp" class="btn btn-primary">
                📝 Novo Currículo
            </a>
            <a href="javascript:window.print()" class="btn btn-secondary">
                🖨️ Imprimir
            </a>
        </div>
    </div>
    
    <script>
        // Animação de entrada suave
        document.addEventListener('DOMContentLoaded', function() {
            const sections = document.querySelectorAll('.cv-section');
            sections.forEach((section, index) => {
                setTimeout(() => {
                    section.style.opacity = '0';
                    section.style.transform = 'translateY(20px)';
                    section.style.transition = 'all 0.5s ease';
                    
                    setTimeout(() => {
                        section.style.opacity = '1';
                        section.style.transform = 'translateY(0)';
                    }, 100);
                }, index * 200);
            });
        });
        
        // Função para melhorar a impressão
        window.addEventListener('beforeprint', function() {
            document.body.style.background = 'white';
        });
        
        window.addEventListener('afterprint', function() {
            document.body.style.background = '#f5f7fa';
        });
    </script>
</body>
</html>