#!/bin/bash
echo "Initializing restaurant menu data..."
docker exec -it $(docker ps -q -f name=restaurant-service) python -c "
import sys
sys.path.append('/code/app')
from models import MenuItem, Base
from database import engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    if db.query(MenuItem).count() == 0:
        menu_items = [
            {'name': 'Континентальный завтрак', 'description': 'Кофе, сок, круассан, джем', 'price': 450.00, 'category': 'breakfast', 'preparation_time': 10},
            {'name': 'Английский завтрак', 'description': 'Яичница, бекон, сосиски, тосты, фасоль', 'price': 650.00, 'category': 'breakfast', 'preparation_time': 15},
            {'name': 'Стейк Рибай', 'description': 'Стейк с овощами на гриле', 'price': 1200.00, 'category': 'main', 'preparation_time': 25},
            {'name': 'Салат Цезарь', 'description': 'Салат с курицей и соусом цезарь', 'price': 450.00, 'category': 'salads', 'preparation_time': 10},
            {'name': 'Тирамису', 'description': 'Классический итальянский десерт', 'price': 350.00, 'category': 'desserts', 'preparation_time': 5},
            {'name': 'Капучино', 'description': 'Кофе с молочной пенкой', 'price': 250.00, 'category': 'drinks', 'preparation_time': 5}
        ]
        for item in menu_items:
            db.add(MenuItem(**item))
        db.commit()
        print('✅ Added 6 menu items to restaurant!')
    else:
        print('✅ Menu already exists')
except Exception as e:
    print(f'❌ Error: {e}')
    db.rollback()
finally:
    db.close()
"

echo "Initializing amenity data..."
docker exec -it $(docker ps -q -f name=amenity-service) python -c "
import sys
sys.path.append('/code/app')
from models import Amenity, Base
from database import engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    if db.query(Amenity).count() == 0:
        amenities = [
            {'name': 'Трансфер из аэропорта', 'description': 'Комфортабельный автомобиль до отеля', 'price': 1500.00, 'category': 'transport', 'duration_minutes': 60},
            {'name': 'Спа-процедура', 'description': 'Расслабляющий массаж (60 минут)', 'price': 3000.00, 'category': 'spa', 'duration_minutes': 60},
            {'name': 'Экскурсия по городу', 'description': 'Обзорная экскурсия с гидом', 'price': 2000.00, 'category': 'tour', 'duration_minutes': 180},
            {'name': 'Аренда велосипеда', 'description': 'Аренда на 24 часа', 'price': 500.00, 'category': 'equipment', 'duration_minutes': 1440}
        ]
        for amenity in amenities:
            db.add(Amenity(**amenity))
        db.commit()
        print('✅ Added 4 amenities to service!')
    else:
        print('✅ Amenities already exist')
except Exception as e:
    print(f'❌ Error: {e}')
    db.rollback()
finally:
    db.close()
"

echo "Data initialization complete!"