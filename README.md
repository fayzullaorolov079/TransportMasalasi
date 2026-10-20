# Transport masalasi — Python loyihasi

Ushbu loyiha transport masalasini to'rtta klassik usulda yechish uchun yozilgan:

1. Shimoliy-g'arbiy burchak usuli
2. Eng kichik xarajatlar usuli
3. Vogel approksimatsiya usuli (VAM)
4. Potensiallar usuli (MODI)

Loyiha standart Python kutubxonalaridan foydalanadi; qo'shimcha paket o'rnatish shart emas. Python 3.9 yoki undan yangi versiya tavsiya qilinadi.

## 1. Transport masalasi nima?

Transport masalasi — bir nechta ta'minotchidagi mahsulotni bir nechta iste'molchiga tashish miqdorlarini shunday taqsimlash masalasiki, barcha ta'minot va talab cheklovlari bajariladi hamda umumiy tashish xarajati eng kichik bo'ladi.

- `A_i` — i- ta'minotchi.
- `B_j` — j- iste'molchi.
- `c[i][j]` — `A_i` dan `B_j` ga bir birlik mahsulot tashish xarajati.
- `supply[i]` — `A_i` dagi mahsulot miqdori.
- `demand[j]` — `B_j` ning talab miqdori.
- `x[i][j]` — `A_i` dan `B_j` ga yuboriladigan miqdor.

Maqsad funksiyasi:

```text
Z = sum(c[i][j] * x[i][j])
```

Cheklovlar:

```text
Har bir ta'minotchi i uchun: sum_j x[i][j] = supply[i]
Har bir iste'molchi j uchun: sum_i x[i][j] = demand[j]
Barcha i, j uchun: x[i][j] >= 0
```

## 2. Yopiq va ochiq transport masalasi

### Yopiq masala

Agar jami ta'minot jami talabga teng bo'lsa, masala yopiq deyiladi:

```text
sum(supply) == sum(demand)
```

### Ochiq masala

Agar jami ta'minot va jami talab teng bo'lmasa, masala ochiq deyiladi.

- Talab ta'minotdan katta bo'lsa, yetishmayotgan miqdor uchun nol xarajatli **soxta ta'minotchi** qo'shiladi.
- Ta'minot talabdan katta bo'lsa, ortiqcha miqdor uchun nol xarajatli **soxta iste'molchi** qo'shiladi.

`transport_common.py` dagi `balance_problem()` bu ishni avtomatik bajaradi. Agar amaliy masalada soxta qator/ustun uchun boshqa xarajat (masalan, saqlash yoki yetishmovchilik jarimasi) berilgan bo'lsa, nol xarajatni shu qiymatga moslab o'zgartirish kerak.

## 3. Loyihadagi fayllar

- `transport_common.py` — umumiy funksiyalar, masalani muvozanatlash, xarajatni hisoblash va boshlang'ich rejalar.
- `northwest_corner.py` — shimoliy-g'arbiy burchak usuli.
- `least_cost.py` — eng kichik xarajatlar usuli.
- `vogel.py` — Vogel usuli.
- `potentials.py` — MODI/potensiallar usuli bilan rejani optimalgacha yaxshilash.
- `main.py` — usulni menyudan tanlab ishga tushirish.
- `README.md` — qo'llanma.

## 4. Berilgan namunaviy masala

Darsdagi rasmga mos ravishda xarajatlar jadvali:

| Ta'minotchi | B1 | B2 | B3 | Ta'minot |
|---|---:|---:|---:|---:|
| A1 | 4 | 6 | 8 | 40 |
| A2 | 5 | 3 | 7 | 60 |
| Talab | 30 | 20 | 50 | 100 |

Jami ta'minot: `40 + 60 = 100`.
Jami talab: `30 + 20 + 50 = 100`.
Demak, namuna yopiq transport masalasi.

Koddagi ma'lumotlarni o'zgartirish uchun har bir alohida `.py` fayl boshidagi `COSTS`, `SUPPLY`, `DEMAND` qiymatlarini yangilang. Yoki funksiyaga o'zingizning `costs`, `supply`, `demand` ro'yxatlaringizni argument qilib bering.

Misol:

```python
costs = [[4, 6, 8], [5, 3, 7]]
supply = [40, 60]
demand = [30, 20, 50]
```

## 5. 1-usul: Shimoliy-g'arbiy burchak

Bu usulda xarajatlar e'tiborga olinmaydi. Jadvalning chap yuqori katagidan boshlanib, mavjud ta'minot va talabning minimumi katakka ajratiladi:

```text
x[i][j] = min(qolgan supply[i], qolgan demand[j])
```

Qator ta'minoti tugasa keyingi qatorga, ustun talabi tugasa keyingi ustunga o'tiladi. Ikkalasi bir vaqtda tugasa diagonal bo'yicha davom etiladi.

Afzalligi: juda sodda va tez.
Kamchiligi: xarajatlarni hisobga olmagani sababli boshlang'ich reja qimmat bo'lishi mumkin.

Ishga tushirish:

```bash
python northwest_corner.py
```

## 6. 2-usul: Eng kichik xarajatlar

Faol qator va ustunlar ichidan birlik tashish xarajati eng kichik katak tanlanadi. Shu katakka mumkin bo'lgan eng katta miqdor ajratiladi. Ta'minot yoki talab tugagach, tegishli qator yoki ustun faol ro'yxatdan chiqariladi va jarayon takrorlanadi.

Afzalligi: tashish xarajatlarini boshidanoq hisobga oladi.
Kamchiligi: lokal ravishda arzon katakni tanlash global optimal yechimni kafolatlamaydi.

Teng xarajatlarda kod birinchi uchragan katakni tanlaydi.

Ishga tushirish:

```bash
python least_cost.py
```

## 7. 3-usul: Vogel approksimatsiya usuli (VAM)

Har bir faol qator va ustun uchun jarima (penalty) hisoblanadi. Jarima — eng kichik va ikkinchi eng kichik xarajatlar farqi. Qator yoki ustunda bitta katak qolgan bo'lsa, koddagi qoida bo'yicha uning jarimasi yagona xarajatga teng olinadi.

1. Har bir faol qator va ustun jarimasini hisoblang.
2. Eng katta jarimali qator yoki ustunni tanlang.
3. Undagi eng arzon katakka maksimal mumkin bo'lgan miqdorni ajrating.
4. Ta'minoti yoki talabi tugagan qator/ustunni chiqarib, takrorlang.

Afzalligi: ko'pincha boshqa sodda usullarga qaraganda yaxshiroq boshlang'ich reja beradi.
Kamchiligi: boshlang'ich reja optimal bo'lishi shart emas.

Ishga tushirish:

```bash
python vogel.py
```

## 8. 4-usul: Potensiallar usuli (MODI)

Potensiallar usuli boshlang'ich reja ustida ishlaydi va uni optimal yechimga yaxshilaydi. Kod boshlang'ich rejani odatda Vogel usuli orqali tuzadi.

### 8.1 Bazis kataklar

Muvozanatlangan, degeneratsiyasiz masalada bazis kataklar soni:

```text
m + n - 1
```

Bu yerda `m` — ta'minotchilar qatori, `n` — iste'molchilar ustuni soni. Agar musbat taqsimotli kataklar yetarli bo'lmasa yoki ular sikl hosil qilsa, MODI hisoblashida nol miqdorli epsilon-bazis katak kerak bo'lishi mumkin.

### 8.2 Potensiallarni hisoblash

Bazis kataklarda:

```text
u[i] + v[j] = c[i][j]
```

Odatda bitta potensial ixtiyoriy ravishda nol deb olinadi, masalan `u[0] = 0`, qolganlari tenglamalardan topiladi.

### 8.3 Bo'sh kataklarni baholash

Minimallashtirish masalasi uchun:

```text
delta[i][j] = c[i][j] - (u[i] + v[j])
```

- Barcha bo'sh kataklar uchun `delta >= 0` bo'lsa, reja optimal.
- Manfiy `delta` bo'lsa, eng manfiy baholi bo'sh katak bazisga kiritiladi.

### 8.4 Yopiq sikl va rejani yaxshilash

Kiruvchi katak orqali gorizontal/vertikal yo'nalishda bazis kataklar bo'ylab yopiq sikl topiladi. Sikldagi kataklarga navbat bilan `+` va `-` belgilar qo'yiladi.

Minus kataklardagi eng kichik taqsimot:

```text
theta = min(x[i][j] for minus kataklar)
```

Siklning `+` kataklariga `theta` qo'shiladi, `-` kataklaridan `theta` ayiriladi. Potensiallar qayta hisoblanadi va optimal shart bajarilguncha takrorlanadi.

Ishga tushirish:

```bash
python potentials.py
```

Boshlang'ich reja usulini tanlash:

```python
from potentials import solve

solve(initial="northwest")  # shimoliy-g'arbiy
solve(initial="least_cost") # eng kichik xarajat
solve(initial="vogel")      # Vogel
```

## 9. Bitta menyu orqali ishga tushirish

```bash
python main.py
```

Menyudan 1–4 oralig'ida usulni tanlang.

## 10. Kutiladigan natijalar va tekshiruv

Ushbu namunada shimoliy-g'arbiy burchak usuli quyidagi reja va xarajatni beradi:

```text
A1: [30, 10, 0]
A2: [0, 10, 50]
Jami xarajat = 560
```

Potensiallar usuli optimal rejani topganda quyidagi reja chiqishi kutiladi:

```text
A1: [30, 0, 10]
A2: [0, 20, 40]
Jami xarajat = 540
```

Tekshiruv:
- A1 dan yuborilgan jami: `30 + 10 = 40`
- A2 dan yuborilgan jami: `20 + 40 = 60`
- B1 ga kelgan jami: `30`
- B2 ga kelgan jami: `20`
- B3 ga kelgan jami: `10 + 40 = 50`
- Xarajat: `30*4 + 10*8 + 20*3 + 40*7 = 540`

## 11. Muhim eslatmalar

1. Bu kodlar o'quv maqsadida yozilgan.
2. Eng kichik xarajat va Vogel usullari boshlang'ich yechim beradi; ular yakka holda optimal yechim kafolatlamaydi.
3. Potensiallar usuli optimallikni tekshiradi va reja xarajatini yaxshilaydi.
4. Tengliklar va nol taqsimotlar sababli degeneratsiya paydo bo'lishi mumkin. Katta yoki murakkab masalalarda sikl/bazisni tekshirish uchun qo'shimcha sinovlar tavsiya etiladi.
5. Barcha sonlar hozircha butun sonli dars misoli uchun yozilgan, lekin kod kasr qiymatlarni ham qabul qiladi.
6. Masala kiritishida xarajatlar jadvali qatorlari `supply` bilan, ustunlari esa `demand` bilan mos kelishiga e'tibor bering.
