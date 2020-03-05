1. termeszetes nyelvek entropiaja
entropia	H(X) = sum(i=1,n)[p(xi) * log(2, 1/p(xi))]
redundancia	R(X) = 1 - H(X)/log(2,n)

kisbetusites
lemmatizalas?

relativ gyakorisag szamolasa

bigrammoknal 1/2 * H(X)
trigrammoknal 1/3 * H(X)

2. bmp RLE tomoritese
bmp formatum felepitese
encoder, decoder
decoder: vagy kepmegjelenito vagy RLE -> bmp
kulonvenni a channeleket, s kulon tomoriteni

3. Huffman kodolas
(a) binaris Huffman
tetszoleges file-ra

kell egy statisztika a szimbolumok elofordulasainak valoszinusegere
szimbolumok: byteok vagy byte alatti bitsorozatok
a legkisebb valoszinusegeket osszevonjuk

(b) s-aris Huffman
elso lepesben k-t kell osszevonjunk
n egyseg, s kodolasi szimbolum
k = (n - 2) mod (s - 1) + 2

(c) adaptiv Huffman
nem tudjuk elore a valoszinusegeket, s az adatfolyam bejovetele kozben szamoljuk ujra mindig
testverpar tulajdonsag:
a csomopontok felsorolhatoak csokkeno sorrendben a gyokertol

a kezdeti fa teljesen kiegyensulyozott
kodolas:
amikor jon egy szimbolum, akkor az aktualis fa alapjan kodoljuk, majd updateljuk a fat
dekodolas:
a dekodolas ugyanigy tortenik, a kezdeti fabol kiindulva
FGK algoritmus
