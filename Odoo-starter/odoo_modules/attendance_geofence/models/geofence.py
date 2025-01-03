from odoo import models, fields, api
from math import radians, sin, cos, sqrt, atan2

class Geofence(models.Model):
    _name = 'hr.geofence'
    _description = 'Geofence'

    name = fields.Char(string='Name', required=True, help="Name of the geofence")
    latitude = fields.Float(string='Latitude', digits=(10, 8), required=True, help="Latitude of the geofence center")
    longitude = fields.Float(string='Longitude', digits=(11, 8), required=True, help="Longitude of the geofence center")
    radius = fields.Float(string='Radius (meters)', required=True, help="Radius of the geofence in meters")
    work_location_ids = fields.Many2many('hr.work.location', string='Work Locations', help="Work locations associated with this geofence")

    def check_point_in_geofence(self, lat, lon):
        R = 6371000  # Earth's radius in meters

        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(lat), radians(lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distance = R * c

        return distance <= self.radius