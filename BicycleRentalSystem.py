class BicycleRentalSystem:
    # Array (list) of locations where a bike can be picked from
    Locations = [
        "South Bank Riverside",
        "Regent's Park",
        "Greenwich Park",
        "King's Cross Station",
        "Covent Garden Market",
        "Shoreditch High Street",
        "Borough Market",
        "Kensington Gardens",
        "Canary Wharf",
        "Notting Hill"
    ]
    # Total number of bikes we have
    NUM_BIKES = 100
    # Currently selected location for renting the bike
    SelectedLocation = None
    # Extra charges if the bikes is returned after the said time
    ExtraChargesPerHour = 5

    def __init__(self):
        # record of all the rented bikes so far
        self.rented_bikes = {}
        

    def rent_bicycle(self, bicycle_id, duration, pickup_loc):
        # a simple check that all the inputs have been filled
        if bicycle_id and duration and pickup_loc:
            # converting to a `float` might end up in a failure
            # because the value in `duration` was not a number
            try:
                duration = float(duration)

                # checking if the bike hasn't already been rented
                # and the bike's `id` is a valid (less than total bikes, i.e., 100)
                if bicycle_id not in self.rented_bikes.keys() and int(bicycle_id) < BicycleRentalSystem.NUM_BIKES:
                    self.rented_bikes[bicycle_id] = (duration, pickup_loc)

                    # success response with a message
                    return {'status': 'ok', 'message': f'Rented bicycle with id: {bicycle_id} for {duration} hour(s)'}
            
                # failed to rent the bike response with a message
                return {'status': 'failure', 'message': 
                        f'The id: {bicycle_id} is not available.\nPlease try some other bicycle :)'}
                
        
            except:
                # failed to convert `duration` to a `float` response with a message
                return {'status': 'failure', 'message': f'Please provide the right duration number'}

        # failure response because not all the fields were filled
        return {'status': 'failure', 'message': f'Please fill in all the required fields'}



    def return_bicycle(self, id, duration):
        try:
            # duration might not be a valid number
            # hence it should be in this `try` block
            duration = float(duration)
            # check if the bike was rented or not
            if id in self.rented_bikes:
                # then check the said duration
                said_duration = self.rented_bikes[id][0]
                # rent should be the duration (for now)
                rent = duration

                if duration > said_duration:
                    # but if the duration is greater than the said duration
                    # that means the customer must pay the extra fine
                    duration -= said_duration
                    rent = (duration * BicycleRentalSystem.ExtraChargesPerHour) + said_duration

                # now that the bike's been returned, we should remove it from
                # the rented bikes database.
                self.rented_bikes.pop(id)
                return {'status': 'ok', 'message': f'Bicycle with id: {id} has been returned.\nPlease pay £{rent}.'}

            return {'status': 'failure', 'message': f"Bicycle with id: {id} hasn't been rented yet."}
        
        except:
            return {'status': 'failure', 'message': f"Duration: {duration} is not a number."}
                
