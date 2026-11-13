# Yeşil Hidrojen vs Lityum Batarya Simülasyonu (Ağır Taşımacılık & Depolama)

Trilyon dolarlık enerji depolama ve lojistik savaşı: 40 tonluk Class-8 ağır vasıta tırda (800 km menzil) **Lityum Bataryalı Elektrikli Tır (BEV - Tesla Semi)** ile **Yeşil Hidrojen Yakıt Hücreli Tırı (FCEV - Mercedes GenH2)** karşılaştıran termodinamik ve kütle bilançosu simülasyon modeli.

---

## ⚡ Temel Bulgular

1. **Şebekeden Tekere (Well-to-Wheel) Verim Uçurumu (%75 vs %26):**  
   Güneş ve rüzgardan üretilen 100 kWh elektriğin **%75'i** bataryalı tırda tekerlekte faydalı harekete dönüşürken; yeşil hidrojen elektroliz, 700 bar sıkıştırma, lojistik ve yakıt hücresi kayıplarıyla **%26'ya** çakılmaktadır. Yani hidrojen aynı yolu gitmek için tam **3 kat** daha fazla yenilenebilir elektrik tüketir.
2. **Kütle Limiti ve Yük (Payload) Cezası:**  
   40 tonluk bir tırı 800 km yürütmek için 1.000+ kWh LFP batarya paketi yardımcı sistemlerle birlikte **8 ila 12 ton** çekmektedir. Bu durum taşınacak 25 tonluk faydalı yükün neredeyse beşte birini yok eder.
3. **Hidrojenin Fiziksel Üstünlüğü:**  
   Yeşil hidrojende aynı 800 km menzil sadece **80 kg H2 yakıt** ve 700 bar kompozit tankla sağlanır (toplam sistem ağırlığı ~2,6 ton). Yük kapasitesi neredeyse tamamen korunur.
4. **Mevsimsel ve Şebeke Depolaması:**  
   Binek araçlarda ve kısa mesafede batarya tartışmasız galipken; okyanus aşırı yük gemileri, 800+ km ağır yük tırları ve elektriğin 6 ay kayıpsız saklanması gereken kış depolamasında (tuz mağaraları) hidrojen tek fiziksel çıkış yoludur.

---

## 🔬 Fiziksel ve Termodinamik Parametreler

- **Mekanik İtiş Enerjisi (800 km):** `800 km * 1,5 kWh/km = 1.200 kWh`
- **Dizel Alt Isıl Değer (LHV):** 12.000 Wh/kg
- **Yeşil Hidrojen LHV:** 33.330 Wh/kg (33,33 kWh/kg)
- **LFP Batarya Paketi Enerji Yoğunluğu:** 125 Wh/kg
- **PEM Yakıt Hücresi Verimi:** %50
- **700 bar Type-IV Kompozit Tank Kütle Oranı:** ~%5,7 H2 ağırlık verimi

---

## 🚀 Kurulum ve Çalıştırma

```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Simülasyonu çalıştırın (Termodinamik ve kütle raporu üretir)
python simulation.py

# Farklı menzil veya ağırlık senaryosu deneyin
python simulation.py --range-km 1000 --gross-ton 44

# Karşılaştırma grafiklerini üretin
python simulation.py --plot
```

---

## 🌐 ENGLISH EXECUTIVE SUMMARY

### Green Hydrogen vs Lithium-Ion Battery Heavy Transport Simulation

A thermodynamic and mass-balance simulation model evaluating Battery-Electric (BEV) vs Fuel-Cell Electric (FCEV) drivetrains for 40-tonne Class-8 heavy-duty trucks over an 800 km highway cycle.

- **Well-to-Wheel Efficiency:** 75% for Li-ion vs 26% for Green Hydrogen (FCEVs demand 3x more renewable electricity).
- **Payload Capacity:** 1,000+ kWh battery weighs 8 to 12 tonnes, consuming up to 20% of commercial payload. An 80 kg H2 storage system preserves full 25-tonne payload capacity.
- **Strategic Verdict:** Batteries win passenger and short-haul transport. Green hydrogen is thermodynamics' only viable answer for long-haul freight, maritime shipping, and seasonal (6-month) salt-cavern grid storage.

---

## 📄 Lisans
MIT License. Açık kaynak araştırma ve eğitim amaçlıdır.
