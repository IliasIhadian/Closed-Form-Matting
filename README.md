# Closed-Form-Matting
Closed-Form-Matting Code zum Verstehen 

### Motivation: 
Mitte März 2024 habe ich mich mit Alpha-Matting im Rahmen meiner Bachelorarbeit beschäftigt und hatte da das ein oder eine Problemschen gehabt. Und da ich weiß wie es ist sich wochenlang mit einem Thema zu beschäftigen ohne das Gefühl zu haben voran zu kommen, da alles unnötig kompliziert erklärt wird. Versuche ich hiermit CLosed-Form-Matting, für die deutschsprachigen Kollegen (Auf Englisch gibts eh genug Ressources zur Verfügung, die sollen sich damit zufrieden geben :) ), kurz und knackig, anhand eines Codebeispiels zu veranschaulichen. 

### Ziel des CF-Algo:
  Wir versuchen ein Bild, mithilfe einer Trimap, durch das Verwenden vom Color-Line-Model in Vordergrund und Hintergrund zu unterteilen.

### Grundlagen:
  - Trimap: 
    - Die Unterteilung des Eingabebildes in 100% Vordergrund(weißer Teil), 100% Hintergrund(schwarzer Teil) und Unknown(grauer Teil) aufzuteilen.
  
  ![me](https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/30138eb8-6c60-42f3-af13-f6c1b5a29773)
  ![metri](https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/1ece1560-cf44-49c1-9c14-b84dcee2be6e)

  - Color-Line-Model:
    -Pixel vom Vordergrund und Hintergrund um einen Pixel im Unknown bilden eine lineare Funktion im RGB 3D Space. 

  - Cost-Function:
    - Eine Cost Function (Kostenfunktion) in maschinellem Lernen ist eine mathematische Funktion, die die Fehler oder Unterschiede zwischen den vorhergesagten Werten eines Modells und den tatsächlichen Werten misst, um zu optimieren, wie gut das Modell funktioniert. Sie wird verwendet, um das Modell während des Trainings anzupassen, indem sie minimiert wird.

  - Laplace Matrix:
    - Ist eine Matrix wo die Diagonale positive Werte besitzt und alle anderen Werte negativ sind.

### Mathe-Stuff:
Auf die Einzelheiten der Mathematik hinter dem CF-Algo werde ich nicht eingehen, hierfür leite ich euch auf die letze Quelle. Wir versuchen $$\alpha = \lambda b_S(L + \lambda D_S)^{-1}$$ auszurechnen. <br />
$$b_S$$ ist ein Vektor, welcher für die markierten Pixel eine Alphawert hat und für die Unmarkierten eine 0.
$$D_S$$ ist eine Diagonalmatrix welche für die markierten Pixel eine 1 hat und für die unmarkierten eine 0.
$$L$$ ist eine Laplace Matrix, (i,j) Wert, so berechnet wird: $$L_{i j}=\sum_{k \mid(i, j) \in w_k}\left(\delta_{i j}-\frac{1}{\left|w_k\right|}\left(1+\left(I_i-\mu_k\right)\left(\Sigma_k+\frac{\epsilon}{\left|w_k\right|} I_3\right)^{-1}\left(I_j-\mu_k\right)\right)\right.$$
  
## CF Algo Plan:

1. image + trimap laden
2. Laplacian matrix berechnen
    1. wir laufen durch das bild (for x → for y)
        1. berechnen mu der koordinaten für jede farbe
        2. und berechne daraus I - mu für jeden pixel I und speichern es in c
        3. berechnen die 3x3 kovarianzmatrix für die verschiedenen farben
        4. berechne die inverse dieser kovarianzmatrix
        5. nun gehen wir 2 mal durch das fenster mit (for dyi → for dxi → for dyj → for dxj)
            1. wir berechnen i und j (ya3ni x und y werte der laplace matrix) 
            (i,j stehen für die pixel I und J und sind die x,y koordinaten der Laplace Matrix)
            (wie legen wir das fenster auf den laplace? laplace ist ein 2d array wobei i ein inner array ist und j die werte innerhalb dieses inner array i = 0, j = 1 wäre 2 )
                ![form](https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/6db3342d-20e1-45c6-9c25-626229fcc3d3)

                ```python
                i[k] = (x + dxi - r) + (y + dyi - r)*w
                j[k] = (x + dxj - r) + (y + dyj - r)*w
                ```
                
            2. wir berechnen temp = (I_i - mu_k) * (inverse  kovarianzmatrix) * (I_j - mu_k)
            3. danach berechnen wir
                 ```python
                (1.0 if (i[k] == j[k]) else 0.0) - (1 + temp)/window_area
                ```
            4. und speichern das in v
3. diese formel anwenden <br />
    <img width="166" alt="arr" src="https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/3b237e95-4b39-4b07-83c4-a4deeed58720">

4. alpha werte ausgeben BOOM
  

  


### Quelle:

Das Paper welches CF-Algo zuallererst veröffentlicht hat: <br />
  **Titel**: A Closed Form Solution to Natural Image Matting <br />
  **Authoren**: Anat Levin Dani Lischinski Yair Weiss <br />
  **Erscheinungsjahr**: 2006  <br />
  [Paper](https://people.csail.mit.edu/alevin/papers/Matting-Levin-Lischinski-Weiss-CVPR06.pdf)

Hilfreicher Prof welcher die Mathematik den CF-Algo und vorallem die Mathematik erklärt: <br />
  [Youtube Video](https://www.youtube.com/watch?v=Mvd93DdgqAY)


  
