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


def correlation(a1, a2):
    """
    Корреляция
    Rxy(t, τ) = sum( (x(t) - Mx)(y(t + τ)) ) / N - 1
    """
    r = np.correlate(a1, a2, mode='full')
    return r[int(len(r)/2):] if (a1 == a2).all() else r[:]


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


def generate_signal(harmonics, frequency, sampling):
    """
    Случайный сигнал...
    x(t) = sum( amp * sin(wp * t + phi) )
    :param harmonics: количество гармоник
    :param frequency: граничная частота
    :param sampling: степень дискретизации
    :return: сигнал
    """

    # Wгр / (n - 1) - шаг частоты для расчёта wp ниже
    step = frequency / (harmonics - 1)

    # создаём матрицу: строки - гармоники, столбцы - сигналы
    harmonics_matrix = np.zeros((harmonics, sampling))

    # генерируем гармоники, заполняем строки матрицы сигналами
    for h in range(harmonics):
        wp = frequency - h * step
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

    signal_one = generate_signal(number_of_harmonics, cutoff_frequency, sampling_rate)
    signal_two = generate_signal(number_of_harmonics, cutoff_frequency, sampling_rate)

    mx = mean(signal_one)
    dx = dispersion(signal_one)
    s = deviation(signal_one)

    rxx = correlation(signal_one, signal_one)
    rxy = correlation(signal_one, signal_two)

    fig, axs = plt.subplots(2, 2, constrained_layout=True)

    axs[0][0].plot(signal_one)
    axs[0][0].set_title(f'Случайный сигнал \'x\'\n\nMx = {mx}\nDx = {dx}\nσ = {s}\n')
    axs[0][0].set_xlabel('время')
    axs[0][0].set_ylabel('сигнал')
    axs[0][0].grid(True)

    axs[0][1].plot(rxx)
    axs[0][1].set_title(f'Автокорреляция Rxx\n')
    axs[0][1].set_xlabel('сигнал')
    axs[0][1].set_ylabel('сигнал')
    axs[0][1].grid(True)

    axs[1][0].plot(signal_two)
    axs[1][0].set_title(f'\nСлучайный сигнал \'y\'\n')
    axs[1][0].set_xlabel('время')
    axs[1][0].set_ylabel('сигнал')
    axs[1][0].grid(True)

    axs[1][1].plot(np.arange(-sampling_rate + 1, sampling_rate), rxy)
    axs[1][1].set_title(f'\nКорреляция Rxy\n')
    axs[1][1].set_xlabel('сигнал (τ - t)')
    axs[1][1].set_ylabel('корреляция')
    axs[1][1].grid(True)

    fig.canvas.set_window_title('')

    plt.show()
