% ===== BASE DE CONHECIMENTO =====

% tunel(Origem, Destino, Tipo).
tunel(entrada, sala1, seco).
tunel(sala1, sala2, alagado).
tunel(sala2, saida, seco).
tunel(sala1, sala4, seco).
tunel(sala4, saida, seco).
tunel(entrada, sala3, seco).
tunel(sala3, saida, seco).
tunel(sala2, sala4, alagado).

% Sala que o robô nunca pode entrar.
risco_desmoronamento(sala3).

% Comente ou remova este fato para o segundo teste.
capacidade(aquatico).

% ===== INTELIGÊNCIA DE NAVEGAÇÃO =====

% Os túneis podem ser percorridos nos dois sentidos.
conexao(A, B, Tipo) :- tunel(A, B, Tipo).
conexao(A, B, Tipo) :- tunel(B, A, Tipo).

% Túneis secos são sempre permitidos.
pode_atravessar(seco).

% Túneis alagados exigem capacidade aquática.
pode_atravessar(alagado) :-
    capacidade(aquatico).

% Predicado solicitado: verifica se existe uma rota segura.
rota_segura(Origem, Destino) :-
    caminho_seguro(Origem, Destino, [Origem]).

% Caso base: o robô chegou ao destino.
caminho_seguro(Destino, Destino, _).

% Busca um próximo passo seguro.
caminho_seguro(Atual, Destino, Visitadas) :-
    conexao(Atual, Proxima, Tipo),
    \+ risco_desmoronamento(Proxima),
    pode_atravessar(Tipo),
    \+ member(Proxima, Visitadas),
    caminho_seguro(Proxima, Destino, [Proxima | Visitadas]).