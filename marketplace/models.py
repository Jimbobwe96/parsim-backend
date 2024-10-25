from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Fields:
        profile_picture (ImageField): Optional image field for user's profile picture.
        bio (TextField): Optional text field for user bio; can be left blank.
        date_joined (DateTimeField): The date the user joined; defaults to current time.
        phone_number (CharField): User's contact number, defaults to placeholder.
        geolocation (CharField): Optional field for user's location data.
        groups (ManyToManyField): Group permissions for the user, linked to Django's Group model.
        user_permissions (ManyToManyField): Direct permissions for the user, linked to Django's Permission model.
    """
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True,) # maybe make just blank? no null
    date_joined = models.DateTimeField(null=True, blank=True, default=timezone.now) # make required later!!

    phone_number = models.CharField(max_length=15, default='000-0000-0000')
    geolocation = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='marketplace_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='marketplace_users', blank=True)


class Listing(models.Model):
    """
    Model representing an item listed for sale in the marketplace.
    
    Fields:
        seller (ForeignKey): The user listing the item.
        title (CharField): Title of the listing.
        slug (SlugField): URL-friendly version of the title. (derived from title)
        description (TextField): Detailed description of the item.
        condition (CharField): Condition of the item, chosen from predefined options.
        price (DecimalField): Price of the item.
        category (ForeignKey): The category to which the item belongs.
        date_posted (DateTimeField): Date the listing was posted.
        status (CharField): Current status of the listing, chosen from predefined options.
    """
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('gently_used', 'Gently Used'),
        ('worn', 'Worn')
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold')
    ]

    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='listings')
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='listings')
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')


    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        ordering = ['date_posted']

    def __str__(self) -> str:
        return self.title


class ListingImage(models.Model):
    """
    Model representing an image associated with a listing.
    
    Fields:
        listing (ForeignKey): The listing the image is associated with.
        image (ImageField): The image file.
        alt_text (CharField): Optional descriptive text for accessibility.
        uploaded_at (DateTimeField): Timestamp when the image was uploaded.
        is_featured (BooleanField): Indicates if this image is the primary image for the listing.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_images')
    image = models.ImageField(upload_to='listing_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['uploaded_at', 'listing', 'is_featured']
        verbose_name = 'ListingImage'
        verbose_name_plural = 'ListingImages'

    def __str__(self):
        return f"Image for {self.listing.title} uploaded at {self.uploaded_at}"


class Category(models.Model):
    """
    Model representing a category for organizing listings.
    
    Fields:
        name (CharField): The name of the category.
        description (TextField): Optional description of the category.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Model representing a message sent between users related to a listing.
    
    Fields:
        sender (ForeignKey): The user sending the message.
        receiver (ForeignKey): The user receiving the message.
        listing (ForeignKey): The listing the message is about.
        content (CharField): The content of the message.
        timestamp (DateTimeField): The time the message was sent.
        read (BooleanField): Indicates if the message has been read.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} about {self.listing.title}"


class Review(models.Model):
    """
    Model representing a review of a seller by a user.
    
    Fields:
        reviewer (ForeignKey): The user giving the review.
        seller (ForeignKey): The user receiving the review.
        rating (IntegerField): The rating given to the seller, from 1 to 5.
        comment (TextField): Optional text comment on the review.
        created_at (DateTimeField): When the review was created.
    """
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'seller')  # Ensure a reviewer can only leave one review per seller
        ordering = ['created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.rating} star review by {self.reviewer} for {self.seller.username}"
    

class Notification(models.Model):
    """
    Model representing a notification sent to a user.
    
    Fields:
        user (ForeignKey): The user receiving the notification.
        message (CharField): The content of the notification.
        is_read (BooleanField): Indicates if the notification has been read.
        created_at (DateTimeField): When the notification was created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user', 'created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"