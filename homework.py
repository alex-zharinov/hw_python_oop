from typing import List, Dict, ClassVar, Type, Tuple, Union
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    mess: str = ''

    def get_message(self) -> str:
        self.mess = (f'Тип тренировки: {self.training_type}; '
                     f'Длительность: {self.duration:.3f} ч.; '
                     f'Дистанция: {self.distance:.3f} км; '
                     f'Ср. скорость: {self.speed:.3f} км/ч; '
                     f'Потрачено ккал: {self.calories:.3f}.')
        return (self.mess)


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    H_IN_M: ClassVar[int] = 60

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
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1: float = 18
        COEFF_CALORIE_2: float = 20
        return ((COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1: float = 0.035
        COEFF_CALORIE_2: float = 0.029
        return ((COEFF_CALORIE_1 * self.weight + (self.get_mean_speed()**2
                // self.height) * COEFF_CALORIE_2 * self.weight)
                * self.duration * self.H_IN_M)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1: float = 1.1
        COEFF_CALORIE_2: float = 2
        return ((self.get_mean_speed() + COEFF_CALORIE_1)
                * COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_map: Dict[str, Type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    return class_map[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    mess: str = info.get_message()
    print(mess)


if __name__ == '__main__':
    packages: List[Tuple[str, List[Union[int, float]]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
