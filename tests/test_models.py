"""
Tests for Brand Model.
"""

import ddt
from django.core.exceptions import ValidationError
from django.test import TestCase
from brands.tests.factories import BrandFactory
from brands.models import Brand  # Import the actual Brand model


@ddt.ddt
class TestBrandModel(TestCase):
    """ BrandModel tests. """
    
    def setUp(self):
        super().setUp()
        self.brand1 = BrandFactory.create(name='Brand One', short_name='brandone', category='Electronics', availability=True)
        self.brand2 = BrandFactory.create(name='Brand Two', short_name='brandtwo', category='Fashion', availability=False)

    def test_create_brand(self):
        """ Test that a brand can be created successfully. """
        brand = BrandFactory.create(name='New Brand', short_name='newbrand')
        self.assertIsNotNone(brand.id)

    def test_read_brand(self):
        """ Test that we can read a brand from the database. """
        brand = Brand.objects.get(id=self.brand1.id)
        self.assertEqual(brand.name, self.brand1.name)

    def test_update_brand(self):
        """ Test that we can update a brand's name successfully. """
        new_name = 'Updated Brand'
        self.brand1.name = new_name
        self.brand1.save()
        updated_brand = Brand.objects.get(id=self.brand1.id)
        self.assertEqual(updated_brand.name, new_name)

    def test_delete_brand(self):
        """ Test that we can delete a brand. """
        brand_id = self.brand1.id
        self.brand1.delete()
        with self.assertRaises(Brand.DoesNotExist):
            Brand.objects.get(id=brand_id)

    def test_list_all_brands(self):
        """ Test listing all brands. """
        all_brands = Brand.objects.all()
        self.assertIn(self.brand1, all_brands)
        self.assertIn(self.brand2, all_brands)

    def test_find_by_name(self):
        """ Test finding a brand by name. """
        results = Brand.objects.filter(name__icontains='Brand One')
        self.assertIn(self.brand1, results)

    def test_find_by_category(self):
        """ Test finding brands by category. """
        results = Brand.objects.filter(category='Electronics')
        self.assertIn(self.brand1, results)
        self.assertNotIn(self.brand2, results)

    def test_find_by_availability(self):
        """ Test finding brands by availability. """
        available_brands = Brand.objects.filter(availability=True)
        self.assertIn(self.brand1, available_brands)
        self.assertNotIn(self.brand2, available_brands)

    @ddt.data(
        [" ", ",", "@", "(", "!", "#", "$", "%", "^", "&", "*", "+", "=", "{", "[", "ó"]
    )
    def test_clean_error(self, invalid_char_list):
        """
        Verify that the clean method raises a validation error if the brand short name
        consists of special characters or spaces.
        """
        for char in invalid_char_list:
            self.brand1.short_name = f'shortname{char}'
            with self.assertRaises(ValidationError):
                self.brand1.clean()

    @ddt.data(
        ["shortnamewithoutspace", "shortName123", "short_name", "short-name", "short.name"]
    )
    def test_clean_success(self, valid_short_name_list):
        """
        Verify that the clean method returns None if the brand short name is valid.
        """
        for valid_short_name in valid_short_name_list:
            self.brand1.short_name = valid_short_name
            self.assertIsNone(self.brand1.clean())

