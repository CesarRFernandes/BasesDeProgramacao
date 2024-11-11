#include <stdio.h>

typedef struct No{
    int valor;
    struct No *prox;
} TNo;

int inserir (TNo *L; int valor);
int remover (TNo *L, int valor);
int alterar (TNo *L, int velho, int novo);
int buscar (TNo *L, int valor);
void exibir (TNo *L);


int main (void)
{
    int v[5] = {1,10,0,25,9};
    int *p;
    int i;
}

