# Quem sou eu? 
Esse repositório contém o código utilizado durante a disciplina de Projeto de Sistemas Operacionais (2018.2). 

Trata-se de um simulador de algoritmos de reposição de páginas. Foram implementados os algoritmos: FIFO, NRU, LRU, Aging, Second Chance e Belady. Após realizadas as simulações foram plotados gráficos onde pudemos visualizar o desempenho de cada algoritmo. No diretório 
[output](./python/output/) temos os resultados do simulador. 

## Como rodar? 
No diretório ```./python``` existe três scrits shell: plot_all, run_all e run_all_test. 
Ao fazer ```./run_all``` você irá fazer o processo de simulação e gerar os arquivos de saída. Com o ```./plot_all``` serão plotados os gráficos utilizando os arquivos de saída. O ```./run_all_test``` é utilizado para testar se tudo está OK antes de executar o ``` ./run_all```. A simulação é demorada, então é importante testar antes de rodar.
