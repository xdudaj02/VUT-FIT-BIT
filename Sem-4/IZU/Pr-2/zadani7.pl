uloha7([], 0).
uloha7([H|T], R) :- H > 0, uloha7(T, P), R is P+1.
uloha7([H|T], R) :- H < 0, uloha7(T, P), R is P-1.
