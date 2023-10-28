# PageRank

Gestion des données distribuées à large échelle  
**Professeur**: MOLLI Pascal  
**Étudiants**: Alaoui Mdaghri Ahmed, Hbitouch Mohammed

[1. Environnement ](1-Environnement)  
[2. Exécutions pagerank - Pig vs PySpark](1-exécutions-pagerank---pig-vs-pyspark)  
[3. Meilleur pagerank](#2-meilleur-pagerank)  


# 1. Environnement
* **Type de machine** : changement des types de machines vers --worker-machine-type n2-standard-2 et --worker-machine-type n2-standard-2 à cause de restriction de RAM
* **Paramètres pagerank**: le nombre d'iterations a été fixé à **3**, et le facteur pagerank utilisé à {d = **0.85**}, pour les deux implémentations. 
* **Nombre de noeuds**: 2, 3, 4 . Le nombre de noeuds a été déterminé en raison des restrictions du quota et la puissance minimale requise pour le fonctionnement des algorithmes.
* **Données d'entrée**: le dataset [page_links_en.nt.bz2](http://downloads.dbpedia.org/3.5.1/en/page_links_en.nt.bz2), 
préchargé dans le bucket public **gs://public_lddm_data//page_links_en.nt.bz2**


# 2. Exécutions pagerank - Pig vs PySpark
<br>
<img align=center src= https://github.com/AlaouiMdaghriAhmed/PageRank/blob/4d535cf2bca3f5cf443720804c847c464db3ba9a/Capture%20d'%C3%A9cran%202023-10-28%20224925.png>
</br>


## PIG
| Nombre de noeuds | Temps d'exécution  | Dataproc Job id
| ------------- | -------------| ------------- |
| 2 | 1 h 49 min | edd09c524da84755a324e48497456f72 |
| 3 | 	1 h 17 min | 033d44f323734c3a944aa929fc53ba33 |
| 4 | 	1 h 17 minc |4b84501b8d1243f2bf1e255811a21e00 |


## PySpark
| Nombre de noeuds | Temps d'exécution | Dataproc Job id
| ------------- | ------------- | ------------- |
| 2 | 1 h 20 min | eb579fcf2c284e0b811da35256512628 |
| 3 | 58 min 53 s | 87b353ae70b5416e92652ac0797d0e7a |
| 4 | 59 min 24 s | fd63cf2456ef440099e806996090d4aa |






# 3. Meilleur pagerank
Nous avons obtenu que l'entité avec le meilleur pagerank c'est l'uri <http://dbpedia.org/resource/Living_people>, avec un pagerank de **36,794.33**. On présente ci-après le top 10 des uri ayant le meilleur pagerank, issue de 3 itérations de l'algorithme pagerank.
| Rank | Url  | Pagerank |
| ---- | ------------- | ------------- |
|1| **http://dbpedia.org/resource/Living_people** | **36794.33146754463**  |
|2| http://dbpedia.org/resource/United_States | 13201.340151981207  |
|3| http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census | 10371.162005541351  |
|4| http://dbpedia.org/resource/List_of_sovereign_states  | 5195.34736186218  |
|5| http://dbpedia.org/resource/United_Kingdom  | 4923.82130931521  |
|6| http://dbpedia.org/resource/Year_of_birth_missing_%28living_people%29  | 4615.7939763369795  |
|7| http://dbpedia.org/resource/France  | 4595.730518177778  |
|8| http://dbpedia.org/resource/Germany  | 4111.195621667528  |
|9| http://dbpedia.org/resource/Canada  | 3765.46156061246 |
|10| http://dbpedia.org/resource/Animal  | 3692.395898434714  |  





