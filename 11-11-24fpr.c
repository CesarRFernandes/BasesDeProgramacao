#include <stdio.h>
#include <stdlib.h>

typedef struct No{
    int valor;
    struct No *prox;
} TNo;

typedef TNo* TLista;

int inserir (TLista *L, int numero);
int remover (TLista *L, int numero);
int alterar (TLista L, int velho, int novo);
int buscar (TLista L, int numero);
void exibir (TLista L);


int main (void)
{
    int v[5] = {1,10,0,25,9};
    int *p;
    int i;
}

int inserir (TLista *L; int numero)
{
    TLista novo;

    //passo 1: alocar memoria para nova
    novo = malloc (sizeof(TNo)); //memory allocation

    // verificando se teve erro
    if (novo == NULL) // ou: if (!novo)
    {
        return 0;
    }
    else 
    {
        //passo 2: armazenanod 'numero' na memoria alocada
        novo = numero;
        
        //passo 3: fazer o campo "prox" do novo  apontar

        return 1;
    }
}

int remover (TLista *L, int numero)
{

    if ((*l).valor == numero)
    {
        aux = *L;
        *L = (*L).prox;
        free (aux);
        cont ++;
    }

    if (*L != NULL)
    {
        pre = *L;
        pos = pre.prox;

        while ( pos != NULL)
        {
            if (pos.valor == numero)
            {
                pre.prox = pos.prox;
                free (pos);
            }
            else
            {
                pre = pos;
                pos = pos.prox;
            }
        }
    }
    return cont;
}
int alterar (TLista L, int velho, int novo)
{
    TLista i = L;
    int cont = 0;

    while (i != NULL)
    {
        if (i->valor)
    }
}
int buscar (TLista L, int numero)
{
    TLista i = L;
    
    while (i !=  NULL)
    {
        if(if->valor == numero)
    }
}
void exibir (TLista L)
{
    TLista i = L;

    if ( i == null)
    {
        printf("lista vazia");
    }
    else 
    {
        printf("\nLista:")
        while ( i != null)
        {
            printf ("%d", (*i).valor); //ou i->valor
            i = i->prox;
        }
    }
}