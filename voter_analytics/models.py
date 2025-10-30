# File: models.py
# Author: Travis Falk(travisf@bu.edu), 10/29/2025
# Description: Model definitions for voter_analytics app

from django.db import models

# Create your models here.

class Voter(models.Model):
    """Store/represent the data from one registered voter in Newton, MA."""
    
    # identification
    last_name = models.TextField()
    first_name = models.TextField()
    
    # address
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField()
    
    # dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    
    # affiliation
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    
    # election participation (True/False for each)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    # voter score
    voter_score = models.IntegerField()
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.first_name} {self.last_name} ({self.street_number} {self.street_name}, {self.zip_code})'


def load_data():
    """Load data records from CSV file into Django model instances."""
    
    # delete existing records to prevent duplicates
    Voter.objects.all().delete()
    
    filename = "C:/Users/falkt/Downloads/newton_voters.csv"
    f = open(filename)
    f.readline()  # discard headers

    # loop through each line in the file
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Voter object with this record
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=(fields[11] == 'TRUE'),
                v21town=(fields[12] == 'TRUE'),
                v21primary=(fields[13] == 'TRUE'),
                v22general=(fields[14] == 'TRUE'),
                v23town=(fields[15] == 'TRUE'),
                voter_score=fields[16].strip(),
            )
            
            voter.save()  # commit to database
            print(f'Created voter: {voter}')
            
        except Exception as e:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')
