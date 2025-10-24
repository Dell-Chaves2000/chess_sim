Simulação de Xadrez: Threads vs Processos
📋 Descrição do Projeto
Este projeto é uma aplicação gráfica em Python que demonstra a diferença de desempenho entre Threads e Processos através de uma simulação de movimentos aleatórios em um tabuleiro de xadrez. A aplicação permite comparar o tempo de execução de ambas as abordagens sob diferentes configurações.

🎯 Objetivo
Demonstrar visualmente como Threads e Processos se comportam em termos de desempenho quando executam tarefas similares, destacando as vantagens do compartilhamento de memória nas Threads.

🛠️ Tecnologias Utilizadas
Python 3.x

Tkinter (Interface gráfica)

Threading (Para threads)

Multiprocessing (Para processos)

Array (Buffer compartilhado)

🚀 Funcionalidades
✅ Tabuleiro de xadrez visual com peças Unicode

✅ Simulação paralela com Threads e Processos

✅ Configuração personalizável de parâmetros

✅ Log em tempo real das execuções

✅ Comparação de desempenho com resumo detalhado

✅ Buffer de complexidade fixo (90.000 elementos)

⚙️ Como Executar
Pré-requisitos
Python 3.6 ou superior

Nenhuma dependência externa necessária

Execução
bash
python chess_sim.py
🎮 Como Usar
Configure os parâmetros:

Jogadas por jogador: Número de movimentos que cada thread/processo executará

Intervalo entre jogadas: Tempo de espera entre movimentos (em milissegundos)

Clique em "Iniciar Simulação"

Observe os resultados:

Logs em tempo real no painel inferior

Movimentos no tabuleiro de xadrez

Resumo final com comparação de desempenho

📊 Parâmetros da Simulação
Configuráveis pelo Usuário:
Jogadas por jogador: 1-50 (padrão: 10)

Intervalo entre jogadas: 10-1000ms (padrão: 100ms)

Fixos:
Complexidade do buffer: 90.000 elementos

Número de jogadores: 2 (um por thread/processo)

🔧 Arquitetura do Código
Classes Principais:
ChessGame
Gerencia o tabuleiro e estado do jogo

Desenha o tabuleiro gráfico

Executa movimentos aleatórios

ChessApp
Interface principal Tkinter

Coordena as simulações

Exibe resultados e logs

Funções de Simulação:
simulate_threads()
Usa threading.Thread para execução paralela

Vantagem: Buffer compartilhado em memória

Operações: Leves e eficientes

simulate_processes()
Usa multiprocessing.Process para execução paralela

Desvantagem: Cópia do buffer para cada processo

Operações: Pesadas com overhead

📈 Resultados Esperados
Threads São Mais Rápidas Porque:
✅ Compartilham memória diretamente

✅ Operações leves e eficientes

✅ Menos overhead de criação

✅ Ideal para tarefas de E/S e simples

Processos São Mais Lentos Porque:
❌ Precisam copiar o buffer a cada jogada

❌ Overhead de comunicação entre processos

❌ Criação mais custosa

🎨 Representação das Peças
O tabuleiro usa caracteres Unicode para representar as peças:

Peça	Branca	Preta
Rei	♔	♚
Rainha	♕	♛
Torre	♖	♜
Bispo	♗	♝
Cavalo	♘	♞
Peão	♙	♟
🔄 Fluxo de Execução
Inicialização do tabuleiro

Configuração dos parâmetros

Execução das Threads (primeiro)

Execução dos Processos (com delay)

Coleta de métricas de tempo

Exibição do resumo comparativo

💡 Aprendizados
Threads são ideais para operações de E/S e tarefas leves

Processos são melhores para operações CPU-intensive pesadas

Compartilhamento de memória é crucial para desempenho

O GIL do Python influencia no paralelismo de threads

📝 Licença
Este projeto é para fins educacionais e pode ser livremente modificado e distribuído.

🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para:

Reportar issues

Sugerir melhorias

Adicionar novas funcionalidades

Desenvolvido com Python ♥️"# chess_sim" 
