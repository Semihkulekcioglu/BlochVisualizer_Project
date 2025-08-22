# Bloch Visualizer

Eğitim ve hızlı prototipleme için tek kübit Bloch küresi görselleştiricisi. Temel kapıları (`H, X, Y, Z, S, T`) ve açılı dönme kapılarını (`RX, RY, RZ`) uygulayın; yalnızca son durumu görüntüleyin ya da bir kapı dizisinin tüm ara durumlarını aynı küre üzerinde iz (trajectory) olarak çizin. İsterseniz her adımı ayrı görseller olarak dışa aktarın.

## Özellikler
- Tek kübit kuantum durumunu Bloch küresinde vektör olarak görselleştirme
- Kapı dizileri ve kapı başına açı desteği, ör. `--sequence "H,RY:1.5708,RZ:0.5,X"`
- Tüm ara durumları tek küre üzerinde iz olarak çizme (`--trajectory`)
- Her adımı dosyaya kaydetme (`--save-steps <klasor>`)
- Son görselleştirmeyi dosyaya kaydetme (`--save <dosya>`) veya etkileşimli pencerede gösterme

## Gereksinimler
- Python 3.9+
- Bağımlılıklar: `requirements.txt`

## Kurulum
```bash
# Depo kökünden
cd BlochVisualizer
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Hızlı Başlangıç
- Tek kapı ve kaydetme:
```bash
python bloch_visualizer.py --gate H --save demo.png
```
- Kapı dizisi ve yalnızca son durum:
```bash
python bloch_visualizer.py --sequence "H,RY:1.5708,RZ:0.5,X" --save final.png
```
- İz çizimi ve adımları klasöre kaydetme:
```bash
python bloch_visualizer.py --sequence "H,RY:1.5708,RZ:0.5,X" --trajectory --save-steps steps
```
- Etkileşimli pencere (kaydetmeden):
```bash
python bloch_visualizer.py --gate H
```

## Komut Satırı Referansı
```text
opsiyonel argümanlar:
  --gate {H,X,Y,Z,S,T,RX,RY,RZ}
        Tek kübit kapısı (RX/RY/RZ için --angle kullanın).
  --angle SAYI
        Dönme kapıları için radyan cinsinden açı.
  --sequence METIN
        Virgülle ayrılmış kapılar; açıları iki nokta ile: "H,RY:1.57,RZ:0.5".
  --trajectory
        Tüm ara durumları aynı küre üzerinde iz olarak çizer.
  --save DOSYA
        Pencere yerine çıktıyı DOSYA'ya kaydeder.
  --save-steps KLASOR
        Her adımı PNG olarak KLASOR içine kaydeder (yoksa oluşturulur).
```

## Çıktı
<img width="640" height="640" alt="Output" src="https://github.com/user-attachments/assets/fa2174ba-2fff-480b-be38-2c17ba943d91" />

## Notlar
- Kapsam: tek kübit; ölçüm, gürültü ve çoklu kübit kapsam dışıdır.
- Uyum: Qiskit sürümleriyle uyum için matplotlib tabanlı çizim kullanılır.

## Lisans
MIT Lisansı — `LICENSE` dosyasına bakın.
