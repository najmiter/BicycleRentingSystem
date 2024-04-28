import customtkinter as ctk

# a structural class for storing a bike item
class RentedBikeItem():
    def __init__(self, 
                 id: int, 
                 hours: float = -1,
                 location: str = '',
                 is_rented: bool = False):
        self.id = id
        self.rented_for_hours = hours
        self.pickup_location = location
        self.is_rented = is_rented

###############################################
###############################################
###############################################
# A manager class to manage renting and the
# returning of a bicycle
class BicycleRentalManager():
    # Total bikes available in our company
    TOTAL_BIKES = 50
    # If the customer returns the bike later than
    # the said duration, they must pay a fine of £5 
    FINE_PER_HOUR = 5
    # These are the locations where we offer
    # rented bikes pickups
    AvailableLocations: list[str] = [
        "Covent Garden",
        "Camden Market",
        "Westminster Bridge",
        "Shoreditch",
        "Green Park",
        "Tower Bridge",
        "Hyde Park",
        "Regent's Park",
        "South Bank",
        "Notting Hill",
        "Borough Market",
        "Kensington Gardens",
        "The Shard",
        "St. James's Park",
        "Brick Lane",
        "The British Museum",
        "Victoria Park",
        "Canary Wharf",
        "Richmond Park",
        "Chinatown"
    ]

    # This list stores the data about all the available
    # bikes in our company (i.e., their avialability)
    rented_bikes_data: list[RentedBikeItem] = [RentedBikeItem(i) for i in range(TOTAL_BIKES)]

    # a static method to rent a bike
    @classmethod
    def rent_bike(_, id: str, hours: str, location: str):
        # all the inputs must be valid
        if id and hours and location.lower() != 'pickup location':
            try:
                # try to convert these two inputs to numbers.
                # if they're not, they'll throw exceptions
                # that we can catch and handle them with
                # appropriate error messages in the UI
                id = int(id)
                hours = float(hours)

                # hours must be valid
                if hours <= 0: 
                    raise

                if id >= BicycleRentalManager.TOTAL_BIKES:
                    return {'status': 'failure', 'msg': f'⚠️ We only have bikes with ID less than {BicycleRentalManager.TOTAL_BIKES}'}

                if BicycleRentalManager.rented_bikes_data[id].is_rented:
                    return {'status': 'failure', 'msg': f'😊 This bike with id: {id} has already been rented.'}
                    
                # we set the requested bike's data to the given data accordingly
                BicycleRentalManager.rented_bikes_data[id] = (RentedBikeItem(id, hours, location, True))
                return {'status': 'success', 'msg': f'🥳 Bike with id: {id} has been rented for {hours} hour(s).'}
            except:
                return {'status': 'failure', 'msg': f'😢 Invalid ID or hours were input. Please try numerical inputs.'}
        else:
            return {'status': 'failure', 'msg': f'😢 Please fill in the required fields before submitting.'}

    # a static method to return the rented bike
    @classmethod
    def return_bike(_, id: int, hours: str):
        # validation of inputs (they can't be empty)
        if id and hours:
            try:
                # trying to convert them into numbers
                # so that we can check their correct types
                # before saving into the 'database'
                id = int(id)
                hours = float(hours)

                if id >= BicycleRentalManager.TOTAL_BIKES:
                    return {'status': 'failure', 'msg': f'⚠️ We only have bikes with ID less than {BicycleRentalManager.TOTAL_BIKES}'}

                bike = BicycleRentalManager.rented_bikes_data[id]
                # check if the bike was even rented in the first place
                if bike.is_rented:
                    agreed_duration = bike.rented_for_hours
                    rent = hours
                    # we check if the rent should include the fine
                    if rent > agreed_duration:
                        fine = rent - agreed_duration
                        rent = agreed_duration + (fine * BicycleRentalManager.FINE_PER_HOUR)

                    # we reset that bike back to available
                    BicycleRentalManager.rented_bikes_data[id] = RentedBikeItem(id)
                    return {'status': 'success', 'msg': f'🥳 Bike with id: {id} has been returned.\nPlease pay £{rent}!'}
                
                return {'status': 'failure', 'msg': f'😊 Bike with id: {id} has not been rented yet!'}
            except:
                return {'status': 'failure', 'msg': f'😢 Invalid ID or hours were input. Please try numerical inputs.'}
        else:
            return {'status': 'failure', 'msg': f'😢 Please fill in the required fields before submitting.'}

###############################################
###############################################
###############################################
# A class to make the UI and interact with user
# this class inherits from the `CTk` 
# class of `customtkinter` library
class App(ctk.CTk):
    MainColor = '#2c9f39'
    def __init__(self):
        super().__init__()
        # Window title
        self.title("Bicycle Renting System")
        self.geometry("700x450")
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("green")

        # Main layout of the app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # The sidebar (navbar) of the app
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Logo label in the sidebar
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="🚲 Bicycleeee",
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


        # Rent a bike tab navigation button
        self.rent_bike_nav_btn = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="🤝 Rent a Bike",
                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=App.MainColor,
                                               anchor="w", command=self.toggle_rent_bike)
        self.rent_bike_nav_btn.grid(row=1, column=0, sticky="ew")

        # Return a bike tab navigation button
        self.return_bike_nav_btn = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="💸 Return Bike",
                                                 fg_color="transparent", text_color=("gray10", "gray90"), hover_color=App.MainColor,
                                                 anchor="w", command=self.toggle_return_bike)
        self.return_bike_nav_btn.grid(row=2, column=0, sticky="ew")

        # Show all the data of the bikes navigation button
        self.show_all_data_nav_btn = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="📋 Show All Data",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=App.MainColor,
                                                   anchor="w", command=self.toggle_show_all_data)
        self.show_all_data_nav_btn.grid(row=3, column=0, sticky="ew")

        ### Rent a bike page (where all the inputs and data submission occurrs)
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        # Setting the heading and a subheading of the page
        self.set_title_of(self.home_frame, 'Bicycle Rental System', 'Rent a Bike')

        ## BIKE ID LABEL x INPUT
        self.bike_id_label = ctk.CTkLabel(self.home_frame, text="Bike ID:")
        self.bike_id_label.grid(row=1, column=0, padx=20, pady=5)
        self.bike_id_input = ctk.CTkEntry(self.bike_id_label, placeholder_text="Enter the bike ID", width=250)
        self.bike_id_input.grid(row=0, column=1, padx=20, pady=5)

        ## TIME LABEL x INPUT
        self.bike_rental_duration = ctk.CTkLabel(self.home_frame, text="Time:   ")
        self.bike_rental_duration.grid(row=2, column=0, padx=20, pady=5)
        self.bike_rental_input = ctk.CTkEntry(self.bike_rental_duration, placeholder_text="How long do you want the bike for", width=250)
        self.bike_rental_input.grid(row=0, column=1, padx=20, pady=5)

        ## LOCATION LABEL x INPUT
        self.bike_pickup_location_label = ctk.CTkLabel(self.home_frame, text="Pickup location:               ")
        self.bike_pickup_location_label.grid(row=3, column=0, padx=20, pady=5)
        self.bike_pickup_location_input = ctk.CTkOptionMenu(self.bike_pickup_location_label, 
                                                            values=BicycleRentalManager.AvailableLocations, 
                                                            variable=ctk.StringVar(value="Pickup location"),
                                                            fg_color=App.MainColor)
        self.bike_pickup_location_input.grid(row=0, column=1, padx=20, pady=5)

        ## RENT THE BIKE BUTTON
        self.rent_bike_label = ctk.CTkButton(self.home_frame, corner_radius=10, border_spacing=8, text="RENT NOW",
                                             text_color=("gray10", "gray90"), fg_color=App.MainColor, width=20,
                                            anchor="w", command=self.rent_bike)
        self.rent_bike_label.grid(row=4, column=0, padx=20, pady=10)

        ## RESPONSE MESSAGE LABEL
        # This will display the response message when a bike is requested
        # This could be a success or a failure
        self.response_msg = ctk.CTkLabel(self.home_frame, text='', width=150, corner_radius=10, height=30)
        self.response_msg.grid(row=5, column=0, padx=20, pady=5)

        ### RETURN BIKE PAGE
        self.return_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.return_frame.grid_columnconfigure(0, weight=1)

        # Title of the page and its subtitle
        self.set_title_of(self.return_frame, 'Bicycle Rental System', 'Return a Bike')

        ## BIKE ID INPUT x LABEL
        self.bike_id_label_ret = ctk.CTkLabel(self.return_frame, text="Bike ID:")
        self.bike_id_label_ret.grid(row=1, column=0, padx=20, pady=5)
        self.bike_id_input_ret = ctk.CTkEntry(self.bike_id_label_ret, placeholder_text="Enter the bike ID", width=250)
        self.bike_id_input_ret.grid(row=0, column=1, padx=20, pady=5)

        ## TIME INPUT x LABEL
        self.bike_rental_duration_ret = ctk.CTkLabel(self.return_frame, text="Time:   ")
        self.bike_rental_duration_ret.grid(row=2, column=0, padx=20, pady=5)
        self.bike_rental_input_ret = ctk.CTkEntry(self.bike_rental_duration_ret, placeholder_text="How long do you want the bike for", width=250)
        self.bike_rental_input_ret.grid(row=0, column=1, padx=20, pady=5)

        ## RENT THE BIKE BUTTON
        # It will handle the returning of the bike
        self.rent_bike_label_ret = ctk.CTkButton(self.return_frame, corner_radius=10, border_spacing=8, text="RETURN NOW",
                                             text_color=("gray10", "gray90"), fg_color=App.MainColor, width=20,
                                            anchor="w", command=self.return_bike)
        self.rent_bike_label_ret.grid(row=3, column=0, padx=20, pady=10)

        ## RESPONSE MESSAGE LABEL
        # This is the message label to display the response of
        # the returning of a rented bike
        self.response_msg_ret = ctk.CTkLabel(self.return_frame, text='', width=150, corner_radius=10, height=40)
        self.response_msg_ret.grid(row=4, column=0, padx=20, pady=10)

        ### SHOW_ALL_DATA PAGE
        self.show_all_data = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color='transparent')
        self.show_all_data.grid_columnconfigure(0, weight=1)

        # Default page to show when the application is launched (i.e., 'Rent a Bike' Page)
        self.select_frame_by_name("rent_bike_nav")

    # This method handles the navigation buttons clicks
    # and displays the corresponding page
    def select_frame_by_name(self, name):
        # Setting the active page and its button's background color in the sidebar
        self.rent_bike_nav_btn.configure(fg_color=App.MainColor if name == "rent_bike_nav" else "transparent")
        self.return_bike_nav_btn.configure(fg_color=App.MainColor if name == "return_bike_nav" else "transparent")
        self.show_all_data_nav_btn.configure(fg_color=App.MainColor if name == "show_all_data_nav" else "transparent")
        # Whichever page is selected will be displayed in the
        # second column of the app and others will be cleared (if any)
        if name == "rent_bike_nav":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "return_bike_nav":
            self.return_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.return_frame.grid_forget()
        if name == 'show_all_data_nav':
            # Create/recreate a label to show all the data about bikes
            self.show_all_data = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color='transparent')
            self.show_all_data.grid(row=0, column=1, sticky="nsew")
            # A label on the top to show the number of total bikes
            # and the avialable bikes
            l = ctk.CTkLabel(self.show_all_data, 
                            text=f'{sum(1 for bike in BicycleRentalManager.rented_bikes_data if not bike.is_rented)} out of {BicycleRentalManager.TOTAL_BIKES} bikes are available', 
                            width=150, corner_radius=10, height=30)
            
            l.grid(row=0, column=1, padx=20, pady=5)
            # Then we show the status of all the bikes and
            # whether or not they've been rented (color coded)
            for i, bikes in enumerate(BicycleRentalManager.rented_bikes_data):
                l = ctk.CTkLabel(self.show_all_data, 
                            text=f'Bike #{i}: ', height=30)
                l.grid(row=i+1, column=1, padx=20, pady=5)
                l2 = ctk.CTkLabel(l, 
                            text='RENTED' if bikes.is_rented else 'AVAILABLE', 
                            fg_color='#b21515' if bikes.is_rented else '#009f22',
                            width=150, corner_radius=10, height=30)
                l2.grid(row=0, column=1, padx=20, pady=5)
        else:
            self.show_all_data.grid_forget()
            self.show_all_data.destroy()

    # Handlers of the navigation buttons
    # They basically decide which page to
    # show on the right side of the app
    def toggle_rent_bike(self):
        self.select_frame_by_name("rent_bike_nav")

    def toggle_return_bike(self):
        self.select_frame_by_name("return_bike_nav")

    def toggle_show_all_data(self):
        self.select_frame_by_name("show_all_data_nav")

    # A helper method to reduce/eliminate code repitition
    def set_title_of(self, frame, title, subtitle):
        self.title = ctk.CTkLabel(frame, text=title, font=('Arial', 24))
        self.title.grid(row=0, column=0, padx=20, pady=15)
        self.subtitle = ctk.CTkLabel(self.title, text=f'- {subtitle} -', font=('Arial', 16))
        self.subtitle.grid(row=1, column=0, padx=20, pady=5)

    # A wrapper method to get the latest values
    # of input fields and clean any leading spaces
    def rent_bike(self):
        response = BicycleRentalManager.rent_bike(
                        self.bike_id_input.get().strip(),
                        self.bike_rental_input.get().strip(),
                        self.bike_pickup_location_input.get().strip()
                    )

        # This will show the respnose message (color coded)
        self.response_msg.configure(True, 
                                    text=response['msg'],
                                    fg_color='#009f22' if response['status'] == 'success' else '#b21515')
        
    # A wrapper method to get the input values
    # and strip any leading spaces before sending
    # them to the `return_bike` of `BicycleRentalManager`
    def return_bike(self):
        response = BicycleRentalManager.return_bike(
                        self.bike_id_input_ret.get().strip(),
                        self.bike_rental_input_ret.get().strip()
                    )
        
        # This will show the respnose message (color coded)
        self.response_msg_ret.configure(True, 
                                    text=response['msg'],
                                    fg_color='#009f22' if response['status'] == 'success' else '#b21515')
    


# Create and run the mainloop of the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
