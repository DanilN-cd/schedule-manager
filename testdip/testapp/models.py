from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# на предмет нужно как то назначить группу, проверить чтобы в списке предметов могли быть предметы с одинковым названием

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=5)
    master = models.ForeignKey('Prepods', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='master')
    kurator = models.ForeignKey('Prepods', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='kurator')
    def __str__(self):
        return f"{self.name}"
    # def __str__(self):
    #     if self.master:
    #         return f"{self.name} - ({self.master})"
    #     return f"{self.name} - (Мастер не назначен)"
        # return self.name
class Prepods(models.Model):
    name = models.CharField(max_length=50)
    predmet = models.ManyToManyField('PredM', blank=True,)
    Cab = models.ForeignKey('Cabs', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    

    
class PredM(models.Model):
    ind = models.CharField(max_length=50,default='0')
    name = models.CharField(max_length=50)
    prepod = models.ManyToManyField('Prepods', blank=True)

    def __str__(self):
        preps = ", ".join([prepod.name for prepod in self.prepod.all()])
        return f"{self.ind} - {self.name} "
    


class Predmets(models.Model):
    name = models.ForeignKey('PredM', on_delete=models.CASCADE, related_name='pred_name')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, blank=True, null=True)
    hours_1sem = models.IntegerField(default=0) # 1 семестр
    hours_2sem = models.IntegerField(default=0) # 2 семестр
    hours_total = models.IntegerField(default=0)  # Общее количество часов на семестр
    hours_used = models.IntegerField(default=0)  # Уже использованные часы
    hours_remaining = models.IntegerField(default=0)  # Оставшиеся часы
    pairs_remaining = models.IntegerField(default=0)  # Оставшиеся пары

    def __str__(self):
        return f"{self.name}"
    # def __str__(self):
    #     return f"{self.group} - {self.name}"
    
class Cabs(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.name}"
    
@receiver(m2m_changed, sender=Prepods.predmet.through)
def sync_predm_prepods(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if not reverse:  # Если связь изменена через Prepods
            for pk in pk_set:
                predm = PredM.objects.get(pk=pk)
                if action == 'post_add':
                    predm.prepod.add(instance)
                elif action == 'post_remove':
                    predm.prepod.remove(instance)
        else:  # Если связь изменена через PredM
            for pk in pk_set:
                prepod = Prepods.objects.get(pk=pk)
                if action == 'post_add':
                    prepod.predmet.add(instance)
                elif action == 'post_remove':
                    prepod.predmet.remove(instance)

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
    ]

    weekday = models.CharField(max_length=2, choices=DAYS_OF_WEEK, verbose_name="День недели")
    date = models.DateField(verbose_name="Дата")
    pair_number = models.PositiveSmallIntegerField(verbose_name="Номер пары")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")
    subject = models.ForeignKey('Predmets', on_delete=models.DO_NOTHING, verbose_name="Предмет")
    cabinet = models.ForeignKey('Cabs', on_delete=models.DO_NOTHING, verbose_name="Кабинет", blank=True, null=True)

    def __str__(self):
        return f"{self.date} ({self.weekday}) - Пара {self.pair_number}: {self.group} - {self.subject.name} в {self.cabinet}"