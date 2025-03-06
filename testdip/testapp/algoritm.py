import datetime
import random
from django.db import transaction
from testapp.models import Schedule, Group, Predmets, Cabs

def generate_schedule(start_date, end_date):
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    # Удаляем расписание за указанный диапазон перед генерацией
    Schedule.objects.filter(date__range=[start_date, end_date]).delete()

    groups = Group.objects.all()
    cabs = list(Cabs.objects.all())  # Преобразуем в список для быстрого доступа

    try:
        with transaction.atomic():  # Начало транзакции (если ошибка — всё откатится)
            current_date = start_date
            while current_date <= end_date:
                weekday = weekdays[current_date.weekday()]

                if weekday == 'Вс':  # Пропускаем воскресенье
                    current_date += datetime.timedelta(days=1)
                    continue

                print(f"\nДата: {current_date} ({weekday})")

                used_subjects = {pair: set() for pair in range(1, 5)}  # Запоминаем предметы на каждой паре
                used_cabs = {pair: set() for pair in range(1, 5)}  # Запоминаем занятые кабинеты на каждой паре

                for group in groups:
                    available_subjects = list(Predmets.objects.filter(group=group, hours_remaining__gt=0))

                    if not available_subjects:
                        print(f"Группа {group} не имеет доступных предметов, пропускаем.")
                        continue

                    num_pairs = 4
                    available_cabs = list(cabs) if weekday != 'Сб' else [Cabs.objects.get_or_create(name='ДО')[0]]

                    for pair_number in range(1, num_pairs + 1):
                        if not available_subjects:
                            print(f"У группы {group} кончились предметы на {current_date}.")
                            break

                        # Выбираем предмет, который ещё не использовался на этой паре
                        subject_choices = [s for s in available_subjects if s.name not in used_subjects[pair_number]]
                        if not subject_choices:
                            print(f"Нет доступных предметов для группы {group} на пару {pair_number}.")
                            continue
                        subject = random.choice(subject_choices)
                        used_subjects[pair_number].add(subject.name)  # Запоминаем предмет на этой паре

                        # Определяем кабинет
                        cabinet = None

                        if subject.name.name == 'Физическая культура':
                            # Физкультура всегда в СЗ
                            cabinet = Cabs.objects.get_or_create(name='СЗ')[0]
                        elif weekday == 'Сб':
                            # По субботам все дистанционно
                            cabinet = Cabs.objects.get_or_create(name='ДО')[0]
                        else:
                            # Иначе ищем кабинет
                            assigned_cabs = [prep.Cab for prep in subject.name.prepod.all() if prep.Cab]
                            available_cabs_for_pair = [cab for cab in available_cabs if cab.id not in used_cabs[pair_number]]

                            if assigned_cabs:
                                # Если у преподов есть закрепленные кабинеты — берем из них
                                assigned_cabs = [cab for cab in assigned_cabs if cab.id not in used_cabs[pair_number]]
                                if assigned_cabs:
                                    cabinet = random.choice(assigned_cabs)

                            # Если ничего не выбрали — берем любой свободный
                            if not cabinet and available_cabs_for_pair:
                                cabinet = random.choice(available_cabs_for_pair)

                        if cabinet:
                            used_cabs[pair_number].add(cabinet.id)

                        # Записываем в расписание
                        Schedule.objects.create(
                            weekday=weekday,
                            date=current_date,
                            pair_number=pair_number,
                            group=group,
                            subject=subject,
                            cabinet=cabinet
                        )

                        print(f"{current_date} ({weekday}), {group}: {subject} в {cabinet if cabinet else 'Без кабинета'}")

                        # Обновляем часы предмета
                        subject.hours_used += 2
                        subject.hours_remaining -= 2
                        subject.pairs_remaining = subject.hours_remaining // 2
                        subject.save()

                        if subject.hours_remaining <= 0:
                            available_subjects.remove(subject)

                current_date += datetime.timedelta(days=1)

    except Exception as e:
        print(f"\nОшибка: {e}. Откат всех изменений за {start_date} - {end_date}!")
        Schedule.objects.filter(date__range=[start_date, end_date]).delete()  # Откат всего, если что-то пошло не так
