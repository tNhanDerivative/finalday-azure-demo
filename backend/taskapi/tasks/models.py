from django.db import models


class Task(models.Model):
	STATUS_TODO = 'todo'
	STATUS_IN_PROGRESS = 'in_progress'
	STATUS_DONE = 'done'

	STATUS_CHOICES = [
		(STATUS_TODO, 'To Do'),
		(STATUS_IN_PROGRESS, 'In Progress'),
		(STATUS_DONE, 'Done'),
	]

	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
	createdAt = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
