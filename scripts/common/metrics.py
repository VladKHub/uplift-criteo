import numpy as np

def qini_curve(y_true, uplift, treatment):
    """
    Возвращает (fractions, qini_values) для построения Qini-кривой.
    y_true: фактические исходы (visit или conversion)
    uplift: предсказанный uplift (чем выше — тем «убедительнее» воздействие)
    treatment: 0/1, был ли пользователь в treated-группе
    """
    order = np.argsort(-uplift)
    y_true, treatment = y_true[order], treatment[order]

    n = len(y_true)
    treated_cum = np.cumsum(y_true * treatment)
    control_cum = np.cumsum(y_true * (1 - treatment))
    n_treated = np.cumsum(treatment)
    n_control = np.cumsum(1 - treatment)

    # Защита от деления на ноль на первых шагах
    treated_rate = np.divide(treated_cum, n_treated, out=np.zeros_like(treated_cum, dtype=float), where=n_treated > 0)
    control_rate = np.divide(control_cum, n_control, out=np.zeros_like(control_cum, dtype=float), where=n_control > 0)

    qini = treated_rate - control_rate
    fractions = np.arange(1, n + 1) / n
    return fractions, qini

def qini_auc_score(y_true, uplift, treatment):
    """Площадь под Qini-кривой (нормированная)."""
    fractions, qini = qini_curve(y_true, uplift, treatment)
    return np.trapz(qini, fractions)