def heuristica(tabuleiro):
    """
    Número de rainhas se atacando
    
    É calculado contando quantas rainhas estão na mesma linha
    e também contando nas diagonais.
    """
    horizontal = 0
    diagonal = 0
    for i in range(0,len(tabuleiro)):
        for j in range(i+1,len(tabuleiro)):
            if i != j:
                x = abs(i-j)
                y = abs(tabuleiro[i]-tabuleiro[j])
                if x == y:
                    diagonal += 1
            if tabuleiro[i]==tabuleiro[j]:
                horizontal += 1

    return horizontal + diagonal
