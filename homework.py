class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TRAINING_TYPE = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    calorie_1 = 18
    calorie_2 = 20
    TRAINING_TYPE = 'RUN'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        cal = (self.calorie_1 * self.get_mean_speed() - self.calorie_2)
        cal_2 = self.M_IN_KM * self.duration
        calories = cal * self.weight / cal_2 * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CF_WALK_1 = 0.035
    CF_WALK_2 = 2
    CF_WALK_3 = 0.029
    TRAINING_TYPE = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        cal_1 = self.CF_WALK_1 * self.weight
        cal_2 = self.get_mean_speed() ** self.CF_WALK_2 // self.height
        cal_3 = self.CF_WALK_3 * self.weight
        calories = (cal_1 + cal_2 * cal_3) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SW_1 = 1.1
    CF_SW_2 = 2
    LEN_STEP = 1.38
    TRAINING_TYPE = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        sp_1 = self.length_pool * self.count_pool
        self.speed = sp_1 / self.M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        cal_1 = self.get_mean_speed() + self.CF_SW_1
        calories = cal_1 * self.CF_SW_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_workout = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
