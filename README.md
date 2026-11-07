# Gesture Media Control

Web kamerasından algılanan el/hareket bilgilerini masaüstü medya kısayollarına
dönüştüren iki deneysel bilgisayarlı görü prototipi.

## Yaklaşımlar

- `motion_gestures.py`: Arka plan farkı ve kontur takibiyle sağ/sol hareket ve
  sabit bekleme jestlerini algılar.
- `yolo_hand_control.py`: Kullanıcının yerel YOLO modelini kullanarak el algılar.

Algılanan jestler önceki parça, sonraki parça ve oynat/duraklat klavye
kısayollarını tetikler.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python motion_gestures.py
```

YOLO sürümü için `best.pt` adlı bir el algılama modeli yerel olarak sağlanmalıdır.
Model ağırlıkları ve kamera kayıtları depoya dahil edilmemiştir.

> Uygulama gerçek klavye girdileri üretir. Denemeden önce aktif uygulamanızı ve
> medya oynatıcınızın kısayollarını kontrol edin.

