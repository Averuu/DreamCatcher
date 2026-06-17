class PlayerResume:
    # Пороги очков для разблокировки игр
    GAME_THRESHOLDS = {
        "gardener": 0,
        "delivery": 50,
        "analyst": 100
    }

    def __init__(self):
        self.total_score = 0
        self.unlocked_games = ["gardener"]   # начинаем с садовника (не убийца)

    def add_score(self, points: int) -> None:
        """Добавляет очки и проверяет, не открылись ли новые игры."""
        self.total_score += points
        self._update_unlocked_games()

    def _update_unlocked_games(self) -> None:
        """Приватный метод: разблокирует игры при достижении порогов."""
        for game, threshold in self.GAME_THRESHOLDS.items():
            if game not in self.unlocked_games and self.total_score >= threshold:
                self.unlocked_games.append(game)

    def to_dict(self) -> dict:
        """Сохранение в json"""
        return {
            "total_score": self.total_score,
            "unlocked_games": self.unlocked_games
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerResume":
        """загрузка из json"""
        obj = cls()
        obj.total_score = data.get("total_score", 0)
        obj.unlocked_games = data.get("unlocked_games", ["gardener"])
        return obj