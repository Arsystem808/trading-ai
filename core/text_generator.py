
  import random

def generate_ai_summary(analysis_result):
    """Генерирует человекоподобный вывод на основе анализа."""
    
    signal = analysis_result['signal']
    reason = analysis_result['reason']
    
    if signal == "SHORT":
        templates = [
            f"Вывод ИИ: {reason} Рекомендую рассмотреть возможность для продажи.",
            f"Вывод ИИ: Рынок показывает признаки слабости покупателей. {reason} Хороший момент для игры на понижение.",
            f"Вывод ИИ: Настроение меняется. {reason} Пора продавать.",
        ]
        return random.choice(templates)
        
    elif signal == "LONG":
        templates = [
            f"Вывод ИИ: {reason} Рекомендую рассмотреть возможность для покупки.",
            f"Вывод ИИ: Продавцы теряют силу. {reason} Открывается окно для входа в лонг.",
            f"Вывод ИИ: Похоже, мы нащупали дно. {reason} Пора покупать.",
        ]
        return random.choice(templates)
        
    else: # WAIT
        return f"Вывод ИИ: {reason} Лучше оставаться в стороне и наблюдать."
