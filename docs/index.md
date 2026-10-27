# MarkovBox

Generatywny syntezator, który sam komponuje.

**MarkovBox** to generatywny syntezator z wbudowanym sekwencerem opartym na łańcuchach Markowa.
Większość syntezatorów gra tylko to, co zagra na nich człowiek. MarkovBox ma grać także wtedy, gdy
człowiek tylko kręci gałkami: sekwencer wytrenowany na korpusie plików MIDI generuje melodie o
regulowanej „przewidywalności”. Jedna gałka zmienia rząd modelu, druga temperaturę losowania, a
instrument płynnie przechodzi od wiernego cytowania korpusu do kontrolowanego chaosu.

## Cel i zakres

Celem projektu jest zaprojektowanie, zbudowanie i publiczne udostępnienie działającego
zamkniętego w obudowie syntezatora generatywnego, wraz z pomiarową charakteryzacją toru audio i oceną
odsłuchową generowanych sekwencji. Produkt obejmuje:

- silnik dźwięku: co najmniej synteza subtraktywna.
- sekwencer Markowa: parser MIDI, budowa macierzy przejść dla korpusu, sterowanie rzędem modelu i temperaturą.
- własne PCB i obudowę z druku 3D.
- publiczne repozytorium ze schematami, plikami PCB, firmware, obudowy i instrukcją złożenia.
- raport pomiarowy toru audio i nagrania demonstracyjne.
