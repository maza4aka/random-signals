import numpy as np
import matplotlib.pyplot as plt


def mean(a):
    """
    Математические ожидание.
    Mx = sum(array) / array_len
    :param a: массив
    :return: ожидание
    """
    return np.mean(a)


def dispersion(a):
    """
    Дисперсия.
    Dx = sum( (array[i] - Mx)^2 ) / (array_len - 1)
    :param a: массив
    :return: дисперсия
    """
    return np.var(a)


def deviation(a):
    """
    Среднеквадратическое отклонение.
    σ = sqrt(Dx)
    :param a: массив
    :return: отклонение
    """
    return np.std(a)


def amplitude(lower, upper):
    """
    Случайная амплитуда.
    :return: амплитуда
    """
    return np.random.uniform(lower, upper)


def angle_phi(lower, upper):
    """
    Случайная фаза.
    :return: фаза
    """
    return np.random.uniform(lower, upper)


def next_frequency(n, step):
    """
    Расчёт частоты для следующей гармоники.
    w(n) = W - n * (W / (n - 1))
    :param n: номер гармоники
    :param step: шаг
    :return: частота
    """
    return cutoff_frequency - n * step


def generate_signal(harmonics, frequency, sampling):
    """
    Случайный сигнал...
    x(t) = sum( amp * sin(wp * t + phi) )
    :param harmonics: количество гармоник
    :param frequency: граничная частота
    :param sampling: степень дискретизации
    :return: сигнал
    """

    # W / (n - 1) - шаг частоты для расчёта w(n) функцией ниже
    step = frequency / (harmonics - 1)

    # создаём матрицу: строки - гармоники, столбцы - сигналы
    harmonics_matrix = np.zeros((harmonics, sampling))

    # генерируем гармоники, заполняем строки матрицы сигналами
    for h in range(harmonics):
        wp = next_frequency(h, step)
        for t in range(sampling):
            harmonics_matrix[h, t] = \
                amplitude(-5, 5) * np.sin(wp * t + angle_phi(0, 360))

    # суммируем гармоники.
    return np.array([np.sum(v) for v in harmonics_matrix.T])


if __name__ == '__main__':
    """
    Исследование случайных сигналов...
    """

    # количество генерируемых гармоник
    number_of_harmonics = 14

    # граничная/максимальная частота
    cutoff_frequency = 2000

    # степень дискретизации (количество точек на графике)
    sampling_rate = 256

    signal = generate_signal(number_of_harmonics, cutoff_frequency, sampling_rate)

    mx = mean(signal)
    dx = dispersion(signal)
    s = deviation(signal)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)

    axs.plot(signal)
    axs.set_title(f'Случайный сигнал\n\nMx = {mx}\nDx = {dx}\nσ = {s}\n')
    axs.set_xlabel('время')
    axs.set_ylabel('сигнал')
    axs.grid(True)

    fig.canvas.set_window_title('')

    plt.show()
