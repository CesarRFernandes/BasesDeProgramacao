#crie um script que leia o nome, idade e altura de certa pessoa. No final do processamento, imprima uma mensagem para a pessoa, confirmando a idade e altura da pessoa
nome = input('Qual o seu nome: ')
idade = input('Qual a sua idade: ')
altura = input('Qual a sua altura: ')

print ('Seu nome é ',nome,' sua idade é ',idade,'sua altura é ', altura,' , correto ?')
confirmacao = bool (input('resposta: '))
if (confirmacao == True):{
    print('Perfeito')
} 
else :{
    print('Que pena')
}