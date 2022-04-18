from django.db import models


class Client(models.Model):
    phone = models.CharField(max_length=11, verbose_name="Номер телефона")
    operator_id = models.CharField(max_length=20, verbose_name="Код мобильного оператора")
    tag = models.CharField(max_length=20, verbose_name="Тэг")
    timezone = models.CharField(max_length=10, verbose_name="Часовой пояс")

    class Meta:
        verbose_name_plural = "Клиенты"
        verbose_name = "Клиент"

    def __str__(self):
        return self.phone


class Mailing(models.Model):
    launch_at = models.DateTimeField(verbose_name="Дата и время запуска рассылки")
    text = models.TextField(verbose_name="Текст сообщения для доставки клиенту")
    mailing_filter = models.CharField(max_length=20, verbose_name="Фильтр для рассылки (код моб оператора + тэг)")
    terminate_at = models.DateTimeField(verbose_name="Дата и время окончания рассылки")

    class Meta:
        verbose_name_plural = "Рассылки"
        verbose_name = "Рассылки"
        ordering = ["launch_at"]

    def __str__(self):
        return f"pk={self.pk}, launch_at={self.launch_at}, text={self.text[0: 20]}, " \
               f"mailing_filter={self.mailing_filter}, terminate_at={self.terminate_at}"


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания (отправки)")
    status = models.CharField(max_length=10, verbose_name="Статус отправки")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="ID рассылки")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="ID клиента")

    class Meta:
        verbose_name_plural = "Сообщения"
        verbose_name = "Сообщение"
        ordering = ["-created_at"]

    def __str__(self):
        return f"pk={self.pk}, created_at={self.created_at}, client_id={self.client}, sendout_id={self.mailing}"
