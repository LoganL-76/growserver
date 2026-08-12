from django.db import models

class Grow(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Complete'),
    ], default= 'active')
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Plant(models.Model):
    grow = models.ForeignKey(Grow, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=100)
    strain = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.strain})"


class Harvest(models.Model):
    plant = models.ForeignKey(Grow, on_delete=models.CASCADE, related_name='harvests')
    date = models.DateField()
    wet_weight = models.FloatField(help_text="grams")
    dry_weight = models.FloatField(help_text="grams", null=True, blank=True)

    def __str__(self):
        return f"Harvest of {self.plant.name} on {self.date}"
    
class Expense(models.Model):
    grow = models.ForeignKey(Grow, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('nutrients', 'Nutrients'),
        ('equipment', 'Equipment'),
        ('labor', 'Labor'),
        ('other', 'Other'),
    ])
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - ${self.amount}"

class JournalEntry(models.Model):
    grow = models.ForeignKey(Grow, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    photo = models.ImageField(upload_to='journal_photos/', null=True, blank=True)

    def __str__(self):
        return f"Journal {self.grow.name} at {self.timestamp}"