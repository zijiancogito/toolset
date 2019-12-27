#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define MAX 10001
int Global0[MAX],Global1[MAX];
void Function0()
{
    int LocalVar0,LocalVar1;
    memset(Global0,0,sizeof(Global0));
    Global0[0]=Global0[1]=1;
    for(LocalVar0=4;LocalVar0<=MAX;LocalVar0+=2)
        Global0[LocalVar0]=1;
    for(LocalVar0=3;LocalVar0<=sqrt(MAX);LocalVar0++){
        for(LocalVar1=LocalVar0*LocalVar0;LocalVar1<=MAX;LocalVar1+=LocalVar0)
            Global0[LocalVar1]=1;
    }
}
void Function1()
{
    int LocalVar0,LocalVar1,LocalVar2,LocalVar3;
    memset(Global1,0,sizeof(Global1));
    for(LocalVar0=1;LocalVar0<=MAX;LocalVar0++){
        LocalVar3=1;
        for(LocalVar1=2;LocalVar1<=sqrt(LocalVar0);LocalVar1++){
            if(LocalVar0%LocalVar1==0){
                LocalVar3++;
            LocalVar2=LocalVar0/LocalVar1;
            if(LocalVar2!=LocalVar1)
                LocalVar3++;
            }
        }
        if(LocalVar0!=1)
            LocalVar3++;
        if(Global0[LocalVar3]==0)
            Global1[LocalVar0]=1;
    }
}
int main()
{
    Function0();
    Function1();
    int LocalVar0,LocalVar1,LocalVar2,LocalVar3,LocalVar4;
    scanf("%d",&LocalVar0);
    while(LocalVar0--){
        scanf("%d %d",&LocalVar2,&LocalVar3);
        LocalVar4=0;
        for(LocalVar1=LocalVar2;LocalVar1<=LocalVar3;LocalVar1++){
            if(Global1[LocalVar1]==1){
                if(LocalVar4==1)
                    printf(" ");
                LocalVar4=1;
                printf("%d",LocalVar1);
            }
        }
        if(LocalVar4==0)
            printf("-1\n");
        else
            printf("\n");
    }
    return 0;
}
