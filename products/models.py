from django.db import models


class Product(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=220, unique=True)

    # ── Tiered wholesale pricing (from AuraStone price sheet) ──────────────
    price       = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=True, blank=True,
                                      help_text="1 pc price (default display price)")
    price_10pc  = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=True, blank=True, help_text="Price per pc for 10 pcs")
    price_50pc  = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=True, blank=True, help_text="Price per pc for 50 pcs")
    price_100pc = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=True, blank=True, help_text="Price per pc for 100 pcs")
    price_unit  = models.CharField(max_length=50, default='per piece', blank=True)

    stone_type  = models.CharField(max_length=100, blank=True)
    material    = models.CharField(max_length=100, blank=True)
    bead_size   = models.CharField(max_length=50,  blank=True)
    color       = models.CharField(max_length=100, blank=True)
    gender      = models.CharField(max_length=50,  blank=True)
    shape       = models.CharField(max_length=50,  blank=True)
    size_info   = models.CharField(max_length=100, blank=True)
    image_url   = models.CharField(max_length=500, blank=True, default='')
    collection  = models.CharField(max_length=100, default='BEST SELLERS', blank=True)
    category    = models.CharField(max_length=100, default='Gemstone Bracelets')
    whatsapp_link = models.URLField(max_length=800, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WristSize(models.Model):
    label   = models.CharField(max_length=20)
    cm      = models.CharField(max_length=20)
    inches  = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.label} ({self.cm})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, default='')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
