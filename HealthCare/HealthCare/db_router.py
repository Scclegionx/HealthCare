class AuthRouter:
    """
    Router để xử lý các model liên quan đến authentication (Patient và Doctor)
    """
    route_app_labels = {'patients', 'doctors'}
    auth_app_labels = {'auth', 'contenttypes', 'admin', 'sessions'}

    def db_for_read(self, model, **hints):
        # Các bảng auth cơ bản -> MySQL (default)
        if model._meta.app_label in self.auth_app_labels:
            return 'default'
        # Model của patients hoặc doctors -> MySQL (default)
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        # Các model khác -> PostgreSQL
        return 'postgres'

    def db_for_write(self, model, **hints):
        # Các bảng auth cơ bản -> MySQL (default)
        if model._meta.app_label in self.auth_app_labels:
            return 'default'
        # Model của patients hoặc doctors -> MySQL (default)
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        # Các model khác -> PostgreSQL
        return 'postgres'

    def allow_relation(self, obj1, obj2, **hints):
        # Cho phép quan hệ giữa các model trong cùng một database
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        elif (
            obj1._meta.app_label not in self.route_app_labels and
            obj2._meta.app_label not in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Các bảng auth cơ bản -> MySQL (default)
        if app_label in self.auth_app_labels:
            return db == 'default'
        # patients và doctors -> MySQL (default)
        if app_label in self.route_app_labels:
            return db == 'default'
        # Các app khác -> PostgreSQL
        return db == 'postgres' 