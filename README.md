# Closed-Form-Matting
Closed-Form-Matting Code zum Verstehen 

Motivation: 
Mitte März 2024 habe ich mich mit Alpha-Matting im Rahmen einer Bachelorarbeit beschäftigt und hatte da das ein oder eine Problemschen gehabt. Und da ich weiß wie es ist sich wochenlang mit einem Thema zu beschäftigen ohne das Gefühl zu haben voran zu kommen, da alles unnötig kompliziert erklärt wird. Versuche ich hiermit CLosed-Form-Matting, für die deutschsprachigen Kollegen (Auf Englisch gibts eh genug Ressources zur Verfügung, die sollen sich damit zufrieden geben :) ), kurz und knackig, anhand eines Codebeispiels zu veranschaulichen. 

Ziel des CF-Algo:
  Wir versuchen ein Bild, mithilfe einer Trimap, durch das Verwenden vom Color-Line-Model in Vordergrund und Hintergrund zu unterteilen.

Grundlagen:
  Trimap: 
  -Die Unterteilung des Eingabebildes in 100% Vordergrund(weißer Teil), 100% Hintergrund(schwarzer Teil) und Unknown(grauer Teil) aufzuteilen.
  
  ![me](https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/30138eb8-6c60-42f3-af13-f6c1b5a29773)
  ![metri](https://github.com/IliasIhadian/Closed-Form-Matting/assets/74773501/1ece1560-cf44-49c1-9c14-b84dcee2be6e)

  Color-Line-Model:
  -Pixel vom Vordergrund und Hintergrund um einen Pixel im Unknown bilden eine lineare Funktion im RGB 3D Space. 

  Cost-Function:
  -Eine Cost Function (Kostenfunktion) in maschinellem Lernen ist eine mathematische Funktion, die die Fehler oder Unterschiede zwischen den vorhergesagten Werten eines Modells und den tatsächlichen Werten misst, um zu optimieren, wie gut das Modell funktioniert. Sie wird verwendet, um das Modell während des Trainings anzupassen, indem sie minimiert wird.

  Laplace Matrix:
  -Ist eine Matrix wo die Diagonale positive Werte besitzt und alle anderen Werte negativ sind.

Mathe-Stuff:
Auf die Einzelheiten der Mathematik hinter dem CF-Algo werde ich nicht eingehen, hierfür leite ich euch auf die letze Quelle. Wir versuchen $$\alpha = \lambdab_S(L + \lambdaD_S)^{-1}$$ auszurechnen.
$$b_S$$ ist ein Vektor, welcher für die markierten Pixel eine Alphawert hat und für die Unmarkierten eine 0.
$$D_S$$ ist eine Diagonalmatrix welche für die markierten Pixel eine 1 hat und für die unmarkierten eine 0.
$$L$$ ist eine Laplace Matrix, (i,j) Wert, so berechnet wird: $$L_{i j}=\sum_{k \mid(i, j) \in w_k}\left(\delta_{i j}-\frac{1}{\left|w_k\right|}\left(1+\left(I_i-\mu_k\right)\left(\Sigma_k+\frac{\epsilon}{\left|w_k\right|} I_3\right)^{-1}\left(I_j-\mu_k\right)\right)\right.$$
  

  

  


Quelle:

Das Paper welches CF-Algo zuallererst veröffentlicht hat:
  Titel: A Closed Form Solution to Natural Image Matting
  Authoren: Anat Levin Dani Lischinski Yair Weiss
  Erscheinungsjahr: 2006
  https://people.csail.mit.edu/alevin/papers/Matting-Levin-Lischinski-Weiss-CVPR06.pdf

Hilfreicher Prof welcher die Mathematik den CF-Algo und vorallem die Mathematik erklärt:
  https://www.youtube.com/watch?v=Mvd93DdgqAY


  
