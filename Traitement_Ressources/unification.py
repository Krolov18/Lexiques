# coding: utf-8
import typing


temps_actuel = 0

from collections import namedtuple


MakeSet = namedtuple('MakeSet', 'parent rang')


class Terme:
    pass


def union(x: MakeSet, y: MakeSet):
    xRacine = find(x)
    yRacine = find(y)
    if xRacine != yRacine:
        if xRacine.rang < yRacine.rang:
            xRacine.parent = yRacine
        else:
            yRacine = xRacine
            if xRacine.rang == yRacine:
                xRacine.rang += 1


def find(x: MakeSet):
    if x.parent:
        x.parent = find(x.parent)
    return x.parent


def apparait_dans(x: Variable, t: Terme):
    global temps_actuel
    temps_actuel += 1
    return apparait_dans_prim(x, t)


def apparait_dans_prim(x: Variable, t: Terme):
    if isinstance(t, Variable):
        return x, t
    elif isinstance(t, Liste):
        if t.temps_actuel == temps_actuel:
            return False
        else:
            t.temps_actuel = temps_actuel
            return apparait_liste(x, t.liste)


def apparait_liste(x: Variable, l: typing.Sequence[Terme]):
    if not l:
        return False
    else:
        if apparait_dans_prim(x, find(l[0])):
            return True
        else:
            return apparait_liste(x, l[1:])


def unifier(t1: Terme, t2: Terme):
    t1 = find(t1)
    t2 = find(t2)
    if t1 == t2:
        return True
    else:
        if isinstance(t1, Variable) and isinstance(t2, Variable):
            union(t1, t2)
        elif isinstance(x, Variable):
            pass
        elif isinstance(y, Variable):
            pass
        elif isinstance(t1, Liste) and isinstance(t2, Liste):
            if t1.name == t2.name:
                union(t1, t2)
                return unifier_listes(t1.liste, t2.liste)
            else:
                return False


def bellman_ford(graphe, source):
    distance = list()
    predecessor = list()
    u = None
    v = None

    for v in graphe.sommets:
        distance[v] = None
        predecessor[v] = None
    distance[source] = 0

    for i in range(len(graphe.sommets)):
        for (u, v, w) in graphe.aretes:  # on considère par défaut qu'un arc(edge) a trois params:source, dest, poids
            dist = distance[u] + w
            if dist < distance[v]:
                distance[v] = dist
                predecessor[v] = u

    for (x, y, z) in graphe.aretes:
        if (distance[x] + z) < distance[y]:
            raise LookupError('Cycle de poids négatif détecté.')

    chemin_plus_court = list()
    s = v
    while s != source:
        chemin_plus_court.append(s)
        s = predecessor[s]
    return chemin_plus_court


def tri_topologique(graphe):
    liste_sommets = [0] * len(graphe.sommets)
    t = 0
    tab_couleur = [0] * len(graphe.sommets)

    for x in graphe.sommets:
        if not tab_couleur[x]:
            parcours_profondeur_topologique(graphe, liste_sommets, x, t, tab_couleur)
        return liste_sommets


def parcours_profondeur_topologique(graphe, liste, x, t, couleur):
    debut = [0] * len(graphe.sommets)
    fin = [0] * len(graphe.sommets)

    couleur[x] = 1
    t += 1

    debut[x] = t
    for y in graphe.degre_sortant(x):
        if not couleur[y]:
            parcours_profondeur_topologique(graphe, liste, y, t, couleur)
    couleur[x] = 2
    t += 1
    fin[x] = t
    liste.append(x)


def dijkstra(graphe, source_initiale):
    import heapq
    d = [None] * len(graphe.sommets)
    source = None
    destination = None
    predecessor = [None] * len(graphe.sommets)
    d[source_initiale] = 0
    queue = graphe.sommets
    heapq.heapify(queue)
    while queue:
        source = heapq.heappop(queue)
        for (_, destination, poids) in graphe.aretes[source]:
            n_poids = d[source] + poids
            if d[destination] > n_poids:
                d[destination] = n_poids
                predecessor[destination] = source
    chemin_plus_court = list()
    s = destination
    while s != source_initiale:
        chemin_plus_court.append(s)
        s = predecessor[s]
    return chemin_plus_court


def floyd_warshall(graphe):
    from numpy import zeros
    w = zeros((len(graphe.sommets), len(graphe.sommets)), dtype=int)
    for k in range(1, len(graphe.sommets)):
        for i in range(1, len(graphe.sommets)):
            for j in range(1, len(graphe.sommets)):
                w[i,j] = min(w[i,j], w[i,k]+w[k,j])
    return w


def johnson(graphe):
    q = Sommet('q')
    graphe1 = graphe.add_sommet(q)
    h = bellman_ford(tmp, q)
    graphe2 = Graphe(graphe1.sommets, [(s, t, w + h[s] - h[t]) for (s, t, w) in graphe.aretes])
    for sommet in graphe.sommets:
        d[s,0] = dijkstra(graphe=graphe, sommet)
    for sommet in graphe.sommets:
        for somet in graphe.sommets:
            d[s, t] -= h[s]-h[t]
    return d


def main():
    pass

if __name__ == '__main__':
    main()