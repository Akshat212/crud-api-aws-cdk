class Message:
    @staticmethod
    def success(message, data=None):
        return {"status": "success", "message": message, "data": data}

    @staticmethod
    def error(message):
        return {"status": "error", "message": message}