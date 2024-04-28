import customtkinter as ctk

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
                


################################################
################################################
################################################
### Developed by Asad Ali ###

# function to update the location where the customer
# wants to pick up their rented bike from
def update_selected_location(location):
    BicycleRentalSystem.SelectedLocation = location


# this class inherits from the CTk class
# docs: https://customtkinter.tomschimansky.com/documentation/
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # a data member for accessing the methods for
        # renting and returning the bike
        self.brs = BicycleRentalSystem()
        
        # to set the title and the dimensions of the window
        self.title("Bicycle Rental System")
        self.geometry("880x640")

        # main frame of the app
        self.main_app = ctk.CTkFrame(master=self)
        self.main_app.pack(pady=20, padx=60, fill="both", expand=True)

        # creating and packing the name of the app on top
        self.label = ctk.CTkLabel(
            master=self.main_app, text="Bicycle Rental System", font=("Arial",24))
        self.label.pack(pady=12, padx=10)

        # we got two tabs: one for renting the bike, the other for retuning it
        self.tabview = ctk.CTkTabview(master=self.main_app, width=500, height=400)
        self.tabview.pack(padx=20, pady=20)

        # this will set the names of those two tabs
        self.tabview.add("RENT") 
        self.tabview.add("RETURN")
        # and by default we want to be in the `RENT` tab
        self.tabview.set("RENT") 

        ## Renting a bike UI
        # friendly message that extra hours will cost extra charges
        self.info_label = ctk.CTkLabel(
                            master=self.tabview.tab('RENT'), 
                            text="You will be charged £1 per hour. £5 for each extra hour.", 
                            bg_color='#2482c3',
                            corner_radius=50,
                            font=("Arial", 14))
        self.info_label.pack(pady=12, padx=10)

        # another message showing how much bikes (out of 100 in this case)
        # have been already rented
        self.available_bikes_label = ctk.CTkLabel(
                                        master=self.tabview.tab('RENT'), 
                                        text=f"{len(self.brs.rented_bikes.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}", 
                                        font=("Arial", 14))
        self.available_bikes_label.pack(pady=12, padx=10)

        # input field for the bike id
        self.bicycle_id_entry = ctk.CTkEntry(
                                    master=self.tabview.tab('RENT'), 
                                    placeholder_text=f"Bicylce id < {BicycleRentalSystem.NUM_BIKES}")
        self.bicycle_id_entry.pack(pady=12, padx=10)

        # input field for the duration of rental
        self.duration_entry = ctk.CTkEntry(
                                    master=self.tabview.tab('RENT'), 
                                    placeholder_text="Duration (in hours)")
        self.duration_entry.pack(pady=12, padx=10)

        # a dropdown for all the locations where our service
        # offers a bike pick up
        self.location_menu = ctk.CTkOptionMenu(master=self.tabview.tab('RENT'), values=BicycleRentalSystem.Locations,
                                                command=update_selected_location,
                                                variable=ctk.StringVar(value="Pickup location"),
                                                fg_color='gray')
        self.location_menu.pack(pady=12, padx=10)

        # the submit button that will call the `rent_bicycle` of `BicycleRentalSystem`
        self.rent_bike_button = ctk.CTkButton(
                                    master=self.tabview.tab('RENT'), 
                                    text="Rent It", 
                                    command=self.rent_bicycle)
        self.rent_bike_button.pack(pady=12, padx=10)

        ## Returning the bike
        # it's the same label showing how much have been rented already
        self.returned_bikes_label = ctk.CTkLabel(master=self.tabview.tab('RETURN'), 
                                       text=f"{len(self.brs.rented_bikes.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}", 
                                       font=("Arial", 14))
        self.returned_bikes_label.pack(pady=12, padx=10)
        
        # input for the id of the bike to be returned
        self.bicycle_id_entry_ret = ctk.CTkEntry(
                                        master=self.tabview.tab('RETURN'), 
                                        placeholder_text="Bicylce id to return")
        self.bicycle_id_entry_ret.pack(pady=12, padx=10)

        # how long was the bike held by the customer (duration)
        self.duration_ret = ctk.CTkEntry(
                                        master=self.tabview.tab('RETURN'), 
                                        placeholder_text="How long have you had it?")
        self.duration_ret.pack(pady=12, padx=10)

        # the submit button that will call `return_bicycle` of the `BicycleRentalSystem`
        self.rent_bike_button_ret = ctk.CTkButton(
                                        master=self.tabview.tab('RETURN'), 
                                        text="Return It", 
                                        command=self.return_bicycle)
        self.rent_bike_button_ret.pack(pady=12, padx=10)

        # this is a message label that appears below both tabs
        # showing the responses of the user inputs (failures and successes)
        self.message = ctk.CTkLabel(master=self.main_app, text='', font=("Arial", 14))
        self.message.pack(pady=12, padx=12)


    # our own wrapper method that just calls the `rent_bicycle`
    # of the `BicycleRentalSystem` after cleaning the inputs
    # and then updates the message with the response
    def rent_bicycle(self):
        was_added = self.brs.rent_bicycle(
                        self.bicycle_id_entry.get().strip(), 
                        self.duration_entry.get().strip(),
                        BicycleRentalSystem.SelectedLocation)
        
        self.show_message(was_added['message'], was_added['status'])

    
    # our own wrapper method that just calls the `return_bicycle`
    # of the `BicycleRentalSystem` after cleaning the inputs
    # and then updates the message with the response
    def return_bicycle(self):
        was_returend = self.brs.return_bicycle(
                            self.bicycle_id_entry_ret.get().strip(), 
                            self.duration_ret.get().strip())
        
        self.show_message(was_returend['message'], was_returend['status'])


    # this is where we update the message and give it a color
    # green if the action was a success, red otherwise
    def show_message(self, msg, status):
        self.message.configure(
            require_redraw=True, 
            text=msg, 
            text_color=f'{'#5de144'if status == 'ok' else '#e1445d'}')

        self.returned_bikes_label.configure(
            require_redraw=True, 
            text=f"{len(self.brs.rented_bikes.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}")

        self.available_bikes_label.configure(
            require_redraw=True, 
            text=f"{len(self.brs.rented_bikes.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}")


################################################
################################################
################################################

################# Main Program #################

def main():
    if __name__ == '__main__':
        app = MainApp()
        app.mainloop()


main()