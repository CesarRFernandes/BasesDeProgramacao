// Formatação de CEP
document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    
    if (cepInput) {
        cepInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 5) {
                value = value.slice(0, 5) + '-' + value.slice(5, 8);
            }
            
            e.target.value = value;
        });
    }
});

// Validação de formulários
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    
    if (!form) return false;
    
    const inputs = form.querySelectorAll('[required]');
    let valido = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ef4444';
            valido = false;
        } else {
            input.style.borderColor = '#e5e7eb';
        }
    });
    
    return valido;
}

// Confirmação de exclusão
function confirmarExclusao(mensagem) {
    return confirm(mensagem || 'Deseja realmente excluir este item?');
}

// Exibir mensagem temporária
function exibirMensagem(mensagem, tipo) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo}`;
    alertDiv.textContent = mensagem;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        alertDiv.style.transition = 'opacity 0.5s';
        
        setTimeout(() => {
            document.body.removeChild(alertDiv);
        }, 500);
    }, 3000);
}

// Validar nota (0-10)
function validarNota(input) {
    let valor = parseFloat(input.value);
    
    if (isNaN(valor) || valor < 0) {
        input.value = 0;
    } else if (valor > 10) {
        input.value = 10;
    }
}

// Validar horas (positivo)
function validarHoras(input) {
    let valor = parseInt(input.value);
    
    if (isNaN(valor) || valor < 1) {
        input.value = 1;
    }
}

// Aplicar máscaras automaticamente
document.addEventListener('DOMContentLoaded', function() {
    // Máscara para campos de nota
    const notaInputs = document.querySelectorAll('input[name="nota"]');
    notaInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validarNota(this);
        });
    });
    
    // Máscara para campos de horas
    const horasInputs = document.querySelectorAll('input[name="horas"]');
    horasInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validarHoras(this);
        });
    });
});

// Animação de progresso
function animarProgresso() {
    const progressBars = document.querySelectorAll('.progress-fill, .progress-fill-large');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

// Executar animação ao carregar a página
window.addEventListener('load', animarProgresso);

// Função para ordenar tabelas
function ordenarTabela(tabela, coluna) {
    const tbody = tabela.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aText = a.cells[coluna].textContent.trim();
        const bText = b.cells[coluna].textContent.trim();
        
        return aText.localeCompare(bText, 'pt-BR', { numeric: true });
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Auto-fechar alerts após 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});