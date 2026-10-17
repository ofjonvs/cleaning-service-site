from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Question(models.Model):
    order = models.PositiveIntegerField(default=0, help_text="Questions are shown lowest first")
    prompt = models.CharField(max_length=300)
    choices = models.TextField(
        blank=True,
        help_text="Optional: one choice per line for multiple choice. Leave blank for a typed answer.",
    )
    answers = models.CharField(
        max_length=300,
        help_text="Accepted answer(s), separated by | (case and accents are ignored), e.g. 'paris|paris france'",
    )
    image = CloudinaryField('image', folder='proposal/', blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True, help_text="Shown under the picture once she gets it right")
    hint = models.CharField(max_length=300, blank=True, help_text="Shown when she gets it wrong")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.order}. {self.prompt}'

    def choice_list(self):
        return [c.strip() for c in self.choices.splitlines() if c.strip()]

    def answer_list(self):
        return [a.strip() for a in self.answers.split('|') if a.strip()]


class Response(models.Model):
    answer = models.CharField(max_length=10)
    no_attempts = models.PositiveIntegerField(default=0, help_text="How many times she chased the 'no' button")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.answer} ({self.created_at:%b %d, %Y %I:%M %p})'
