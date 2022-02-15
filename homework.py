from dataclasses import dataclass
from gettext import translation

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MY_PHRASE = 'text {key_to_insert:.3f} text'
    def get_message(self):
        data = (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')
        return self.MY_PHRASE.format(key_to_insert=data)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

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
    SHIFT_MULTIPLIER = 20
    TRANSLATON = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.SPEED_MULTIPLIER * self.get_mean_speed - self.SHIFT_MULTIPLIER) 
        * self.weight / (self.M_IN_KM * self.duration * self.TRANSLATON))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CF_1 = 0.035
    CF_2 = 0.029
    TRANSLATON = 60

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return ((self.CF_1 * self.weight + (self.get_mean_speed() ** 2 // self.height) 
        * (self.CF_2 * self.weight)) * self.duration * self.TRANSLATON)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_MULTIPLIER = 1.1
    SHIFT_MULTIPLIER = 2
    LEN_STEP = 1.38

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return ((self.length_pool * self.count_pool) 
        / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return (
            (self.get_mean_speed() + self.SPEED_MULTIPLIER) 
            * (self.SHIFT_MULTIPLIER * self.weight)
        )


TYPE_WORKOUTS = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TYPE_WORKOUTS[workout_type](*data)


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
