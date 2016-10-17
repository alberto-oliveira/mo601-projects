#include <stdio.h>
#include <stdlib.h>

int main(void){
    
    int * k;
    int * vec;
    
    k = (int*)calloc(10, sizeof(int));
    vec = (int*)calloc(10, sizeof(int));
    
    for(int i = 0; i < 10; i++){
        
        k[i] = i;
        vec[i] = k[i] * 10;
        
    }
    
    printf("k:");
    for(int i = 0; i < 10; i++){
        printf(" %d", k[i]);
    }
    printf("\n");
    
    printf("vec:");
    for(int i = 0; i < 10; i++){
        printf(" %d", vec[i]);
        
    }
    printf("\n");
    
    return 0;
    
}