from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_PER_HR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (self.SPEED_MULTIPLIER * self.get_mean_speed()
             - self.SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.MIN_PER_HR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return (
            (self.WEIGHT_MULTIPLIER_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * (self.WEIGHT_MULTIPLIER_2 * self.weight))
            * self.duration * self.MIN_PER_HR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_SHIFT = 1.1
    WEGHT_MULTIPLIER = 2
    LEN_STEP = 1.38

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (
            (self.length_pool * self.count_pool)
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return (
            (self.get_mean_speed() + self.SPEED_SHIFT)
            * (self.WEGHT_MULTIPLIER * self.weight)
        )


WORKOUTS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}
TYPE_ERROR = ('Выбрано {workout_type}: это неверный тип тренировки. '
              'Попробуйте использовать один из '
              'предложенных: {tuples}')
DATA_ERROR = ('Выбрано {workout_type}. Ожидаемое число '
              'входных параметров {len_tuple}. '
              'Было введено: {len_data}.')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUTS:
        raise ValueError(TYPE_ERROR.format(workout_type=workout_type,
                         tuples=tuple(WORKOUTS)))
    if len(data) != len(fields(WORKOUTS[workout_type])):
        raise ValueError(DATA_ERROR.format(workout_type=workout_type,
                         len_tuple=len(fields(WORKOUTS[workout_type])),
                         len_data=len(data)))
    return WORKOUTS[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
