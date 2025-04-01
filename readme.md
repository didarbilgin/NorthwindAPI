**api.py** ->API uç noktalarını oluşturmak için FastAPI kullanılacak. Bu dosya, ürün listeleme, tahmin yapma ve model eğitme gibi işlevleri sağlayacak.

**test_api.py** -> API uç noktalarınızı test etmek için bir test dosyası

**data_processing.py** ->Bu dosya, verilerinizi işlemek, temizlemek ve özellik mühendisliği yapmak için kullanılan fonksiyonları içerir.

**database.py** -> Bu dosya, PostgreSQL veritabanına bağlanmanızı sağlar ve verileri çekmek için gerekli fonksiyonları içerir.

**model.py** -> Makine öğrenmesi modeli burada eğitilecek ve kaydedilecektir.


**/NORTHWINDAPI**
    /app
        database.py           # Veri tabanı bağlantı ve veri işleme işlemleri
        data_processing.py    # Veri ön işleme ve özellik mühendisliği
        model.py              # Makine öğrenmesi modeli
        api.py                # FastAPI uygulaması
    /tests
        test_api.py           # API uç noktalarının testleri
        test_model.py         # Modelin doğruluğunu test etme
    requirements.txt
    README.md
