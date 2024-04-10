import scipy
import numpy as np
from PIL import Image


"""
Schreib dein eigenes CF Programm
Ziel: alpha ausrechnen (alles hier auf diesem file)
"""

image  = np.array(Image.open( "lemur.png").convert("RGB"))/255.0
trimap = np.array(Image.open("lemur_trimap.png").convert(  "L"))/255.0

h, w, d = image.shape

#is_known = np.zeros((h,w), dtype=bool)





"""
Laplace-Matrix berechnen.
"""
#Radius des Fensters
r = 1
#Fehlerakzeptanz
epsilon = 1e-7
#Einfach ein Counter der später für die einträge in i,j,v benutzt wird
k = 0
#Anzahl der Pixel
n = h*w

size = 2*r+1
window_area = size * size

assert d == 3

n_v = (w - 2 * r) * (h - 2 * r) * window_area ** 2

# inner_array wird gespeichert y-wert
i = np.empty(n_v, dtype=np.int64)

# welche werte genau im inner array x-wert
j = np.empty(n_v,  dtype=np.int64)
v = np.empty(n_v, dtype=np.float64)



for y in range(r,h-r):
    for x in range(r,w-r):

        #Hier berechnen wir mu
        mu = np.zeros(3)
        for dc in range(3):
            # Hier berechnen wir den durchnitt von jeder Farben-Achse innerhalb des Fensters des pixels (x,y)
            mu[dc] = np.mean(image[y-r:y+r+1, x-r:x+r+1, dc])

        #Hier berechnen wir I - mu innerhalb des Fensters
        c = image[y-r:y+r+1, x-r:x+r+1]-mu

        #Hier berechnen wir die 3x3 Kovarianzmatrix für die verschiedenen Farb-achsen
        cov = np.zeros((3, 3))
        for p in range(3):
            for q in range(3):
                cov[p, q] = np.mean(c[:, :, p] * c[:, :, q])

        #Hier addieren wir die cov mit einer 3x3 Diagonalmatrix mit epsilon/window_area (Da cov 3x3)
        cov_tmp = cov + epsilon / window_area * np.eye(3)

        #Hier berechnen wir die Inverse der cov_tmp
        inv = np.linalg.inv(cov_tmp)

        #Hier gehen wir mit 2 Pixeln (dyi,dxi) (dyj,dxj) durch das Fenster
        for dyi in range(2*r +1):
            for dxi in range(2*r +1):
                for dyj in range(2*r +1):
                    for dxj in range(2*r +1):
                        # Hier berechnen wir wo die Values in der LM(laplace matrix) platziert werden sollen (i,j)
                        i[k] = (dxi + x - r) + (dyi + y - r)*w
                        j[k] = (dxj + x - r) + (dyj + y - r)*w
                        #print((dxi + x - r) + (dyi + y - r)*w)

                        #Hier berechnen wir das skalarprodukt von (I_i - mu_k)(inv_cov)(I_j - mu_k)
                        tmp = c[dyi, dxi].dot(inv).dot(c[dyj, dxj])

                        #Hier beenden wir die Formel für die LM
                        v[k] = (1.0 if (i[k] == j[k]) else 0.0) - (1 + tmp) / window_area

                        k += 1


#Hier bauen wir endlich die Laplace Matrix
L = scipy.sparse.csr_matrix((v, (i, j)), shape=(n, n))

'''
Nun könne wir nach alpha ausrechnen
'''

#Hier wird die Trimap aufgebaut
is_fg = (trimap > 0.9).flatten()
is_bg = (trimap < 0.1).flatten()
is_known = is_fg | is_bg
is_unknown = ~is_known

#Hier wird die Diagonalmatrix gebaut
d = is_known.astype(np.float64)
D = scipy.sparse.diags(d)

#Hier wird die Diagonalmatrix mit lambda multipliziert und mit LM addiert
lambda_value = 100.0
A = lambda_value * D + L

#Hier wird b_S berechnet
b = lambda_value * is_fg.astype(np.float64)

#Hier wird das LGS für alpha = lambda * b_S * (L + lambda * D_S)^{-1} berechnet
alpha = scipy.sparse.linalg.spsolve(A, b).reshape(h, w)

#Wir fusionieren die Alphawerte mit den dem Bild
cutout = np.concatenate([image, alpha[:, :, np.newaxis]], axis=2)

'''
Nun werden die Alpha-werte als Bild abgespeichert und ausgegeben
'''

#Hier clippen wir die werte wieder zurück zu 0-255 und konvertieren es zu uint8
alpha = np.clip(alpha*255, 0, 255).astype(np.uint8)

#Hier speichern wir Alphawerte als Bild ab
Image.fromarray(alpha).save("lemur_alpha.png")

#Hier werden die Bilder geöffnet und uns gezeigt
Image.fromarray(alpha).show(title="alpha")


'''
Nun wird der Vordergrund als Bild abgespeichert und ausgegeben
'''


#Hier clippen wir die werte wieder zurück zu 0-255 und konvertieren es zu uint8
cutout = np.clip(cutout*255, 0, 255).astype(np.uint8)

#Hier speichern wir Alphawerte als Bild ab
Image.fromarray(cutout).save("lemur_foreground.png")

#Hier werden die Bilder geöffnet und uns gezeigt
Image.fromarray(cutout).show(title="foreground")







