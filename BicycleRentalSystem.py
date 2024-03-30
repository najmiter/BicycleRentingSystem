class BicycleRentalSystem:
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
    SelectedLocation = None
    ExtraChargesPerHour = 5

    def __init__(self):
        self.bicycle_ids = {}
        

    def rent_bicycle(self, bicycle_id, duration, pickup_loc):
        if bicycle_id and duration and pickup_loc:
            try:
                duration = int(duration)

                if bicycle_id not in self.bicycle_ids.keys():
                    self.bicycle_ids[bicycle_id] = (duration, pickup_loc)

                    return {'status': 'ok', 'message': f'Rented bicycle with id: {bicycle_id} for {duration} hour(s)'}
            
                return {'status': 'failure', 'message': f'The id: {bicycle_id} is already rented.\nPlease try some other bicycle :)'}
                
        
            except:
                return {'status': 'failure', 'message': f'Please provide the right duration number'}

        return {'status': 'failure', 'message': f'Please fill in all the required fields'}



    def return_bicycle(self, id, duration):
        duration = int(duration)
        if id in self.bicycle_ids:
            said_duration = self.bicycle_ids[id][0]
            rent = duration

            if duration > said_duration:
                duration -= said_duration
                rent = (duration * BicycleRentalSystem.ExtraChargesPerHour) + said_duration

            self.bicycle_ids.pop(id)
            return {'status': 'ok', 'message': f'Bicycle with id: {id} has been returned.\nPlease pay £{rent}.'}

        return {'status': 'failure', 'message': f"Bicycle with id: {id} hasn't been rented yet."}
                
