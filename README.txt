# Weather Task Loyihasi

## Loyiha Haqida Batadsil
Bu loyiha ob-havo ma'lumotlarini ko‘rsatuvchi va koproq vaqt bilan birga oluvchi web-ilova bo‘lib,
Django frameworki asosida yaratildi. Loyiha PostgreSQL ma'lumotlar omboridan foydalanadim va bu har 10
daqiqada ob-havo ma'lumotlarini yangilab turadi. Web-sayt foydalanuvchilarga shaharlar bo‘yicha ob-havo
ma'lumotlarini ko‘rish, oxirgi 6 ta yozuvni ko‘rish va ma'lumotlarni oxirgi 200 ta malumotni CSV formatida
eksport qilish imkonini beradi. Buni 200 ta qilganim sababi bu test holatida bolgani sababli har bir
shahar uchun hozircha 200 ta malumot yozib qolganini eskisidan o'chirib keladi .

## Ishlatilgan API-lar
1. **OpenWeatherMap API**:
   - URL: `https://api.openweathermap.org/data/2.5/weather`
   - Maqsad: Shaharlar uchun ob-havo ma'lumotlarini olish (harorat, ta'rif, ikonka va boshqalar).
   - API kalitim: `24c1bd2e851cf62a4e0f1b708fdc5ca3` (openweathermap Web sayitga kirib akaunt ochib unikal
   bolgan kalit oldim).

## Loyihada Nimalar Qilindi
- **models.py**: `WeatherData` modeli ob-havo ma'lumotlarini (shahar, harorat, ta'rif, ikonka, vaqt) saqlaydi.
    `SearchHistory` modeli esa qidirilgan shaharlarni va ularning vaqtini saqlaydi.
- **tasks.py**: Har 10 daqiqada `fetch_weather_data` funksiyasi OpenWeatherMap API orqali yangi ma'lumotlarni
    olib, har bir shahar uchun maksimal 200 ta yozuvni saqlaydi va eskilarini o‘chirib tashlaydi.
    `start_scheduler` funksiyasi bu jarayonni avtomatik boshqaradi.
- **views.py**: `home` funksiyasi ob-havo ma'lumotlarini ko‘rsatadi va oxirgi 6 ta yozuvni jadvalda chiqaradi.
    `export_weather_csv` funksiyasi foydalanuvchi tanlagan vaqt oralig‘idagi ma'lumotlarni CSV sifatida eksport
     qiladi.
- **urls.py**: Loyiha uchun URL yo‘llarini boshqaradi, jumladan API endpointlarini ko'rsatadi.
- **index.html**: Foydalanuvchi interfeysi yani frontend qismi bunda mikroserrver bolgani uchun natijalar yaxshi
    va aniq , chiroyli chiqishi uchun jinja dan foydalanib web sayitini tayorladim. Bundan tashqari
    shahar qidiruvi, oxirgi 6 ta yozuvni ko‘rsatish va vaqt oralig‘i bo‘yicha eksport qilish imkonini beradi.
- **requirements.txt**: Loyiha uchun zarur bo‘lgan barcha tashqi kutubxonalar ro‘yxati.

## Qo‘shimcha Ma'lumotlar
- **SearchHistory Modeli**: Bu model foydalanuvchi qidirgan shaharlarni saqlaydi va loyiha ichida dinamik
    ravishda popular shaharlarni ko‘rsatish uchun ishlatiladi.
- **Rivojlanish Imkoniyati**: Ushbu web-sayt o‘z-o‘zidan rivojlanishi mumkin. Yani bunda foydalanuvchi agar
    angi shahar kiritsa bizdagi SearchHistory da bolmasa unga saqlaydi bu esa o'z - o'zini rivojlantiradi
