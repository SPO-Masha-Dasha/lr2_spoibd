# samplesite/db_router.py
"""
Роутер для автоматической диспетчеризации данных между базами.
Модели приложения 'bboard' направляются в БД 'secondary',
остальные - в 'default'.
"""

class SecondaryRouter:
    route_app_labels = {'bboard'}  # Приложение для второй БД

    def db_for_read(self, model, **hints):
        """Определяем БД для чтения"""
        if model._meta.app_label in self.route_app_labels:
            return 'secondary'
        return None  # None = использовать default

    def db_for_write(self, model, **hints):
        """Определяем БД для записи"""
        if model._meta.app_label in self.route_app_labels:
            return 'secondary'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешаем связи только между объектами из одной БД
        для поддержания целостности данных
        """
        if (obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels):
            return True  # Оба объекта в secondary
        elif (obj1._meta.app_label not in self.route_app_labels and
              obj2._meta.app_label not in self.route_app_labels):
            return True  # Оба объекта в default
        return False  # Объекты в разных БД - связь запрещена

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Определяем, куда применять миграции"""
        if app_label in self.route_app_labels:
            return db == 'secondary'  # bboard -> secondary
        return db == 'default'  # остальные -> default