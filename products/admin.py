from django.contrib import admin
from django.utils.html import format_html
from .models import Product, WristSize


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ("image_preview", "name", "stone_type", "price", "is_featured", "collection", "category")
    list_display_links = ("name",)
    list_editable  = ("price", "is_featured")
    list_filter    = ("is_featured", "collection", "category", "stone_type")
    search_fields  = ("name", "stone_type", "material", "color")
    ordering       = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview_large", "whatsapp_link")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "collection", "category", "is_featured")
        }),
        ("Pricing", {
            "fields": ("price",)
        }),
        ("Stone & Material Details", {
            "fields": ("stone_type", "material", "bead_size", "color", "gender", "shape", "size_info")
        }),
        ("Image", {
            "fields": ("image_url", "image_preview_large")
        }),
        ("WhatsApp Link", {
            "fields": ("whatsapp_link",),
            "classes": ("collapse",)
        }),
    )

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                "<img src='{}' style='width:60px;height:45px;object-fit:cover;border-radius:6px;' />",
                obj.image_url
            )
        return "-"
    image_preview.short_description = "Image"

    def image_preview_large(self, obj):
        if obj.image_url:
            return format_html(
                "<img src='{}' style='max-width:300px;max-height:300px;object-fit:cover;border-radius:10px;margin-top:8px;' />",
                obj.image_url
            )
        return "-"
    image_preview_large.short_description = "Image Preview"

    actions = ["mark_featured", "unmark_featured"]

    @admin.action(description="Mark selected as Featured")
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} bracelet(s) marked as featured.")

    @admin.action(description="Remove from Featured")
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} bracelet(s) removed from featured.")


@admin.register(WristSize)
class WristSizeAdmin(admin.ModelAdmin):
    list_display = ("label", "cm", "inches")
    ordering = ("id",)


admin.site.site_header = "Uma Crystal Admin"
admin.site.site_title  = "Uma Crystal Admin"
admin.site.index_title = "Welcome to Uma Crystal Dashboard"
