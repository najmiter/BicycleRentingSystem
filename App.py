import customtkinter as ctk
from BicycleRentalSystem import BicycleRentalSystem


def update_selected_location(location):
    BicycleRentalSystem.SelectedLocation = location


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.brs = BicycleRentalSystem()
        
        self.title("Bicycle Rental System")
        self.geometry("880x640")

        self.main_app = ctk.CTkFrame(master=self)
        self.main_app.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.main_app, text="Bicycle Rental System", font=("Arial",24))
        self.label.pack(pady=12, padx=10)

        self.tabview = ctk.CTkTabview(master=self.main_app, width=500, height=400)
        self.tabview.pack(padx=20, pady=20)

        self.tabview.add("RENT") 
        self.tabview.add("RETURN")
        self.tabview.set("RENT") 

        # Renting a bike UI
        self.info_label = ctk.CTkLabel(master=self.tabview.tab('RENT'), 
                                       text="You will be charged £1 per hour. £5 for each extra hour.", 
                                       bg_color='#2482c3',
                                       corner_radius=50,
                                       font=("Arial", 14))
        self.info_label.pack(pady=12, padx=10)

        self.available_bikes_label = ctk.CTkLabel(master=self.tabview.tab('RENT'), 
                                       text=f"{len(self.brs.bicycle_ids.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}", 
                                       font=("Arial", 14))
        self.available_bikes_label.pack(pady=12, padx=10)

        self.bicycle_id_entry = ctk.CTkEntry(master=self.tabview.tab('RENT'), placeholder_text=f"Bicylce id < {BicycleRentalSystem.NUM_BIKES}")
        self.bicycle_id_entry.pack(pady=12, padx=10)

        self.duration_entry = ctk.CTkEntry(master=self.tabview.tab('RENT'), placeholder_text="Duration (in hours)")
        self.duration_entry.pack(pady=12, padx=10)

        self.location_menu = ctk.CTkOptionMenu(master=self.tabview.tab('RENT'), values=BicycleRentalSystem.Locations,
                                                command=update_selected_location,
                                                variable=ctk.StringVar(value="Pickup location"),
                                                fg_color='gray')
        self.location_menu.pack(pady=12, padx=10)

        self.rent_bike_button = ctk.CTkButton(master=self.tabview.tab('RENT'), text="Rent It", command=self.rent_bicycle)
        self.rent_bike_button.pack(pady=12, padx=10)

        # Returning the bike
        self.returned_bikes_label = ctk.CTkLabel(master=self.tabview.tab('RETURN'), 
                                       text=f"{len(self.brs.bicycle_ids.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}", 
                                       font=("Arial", 14))
        self.returned_bikes_label.pack(pady=12, padx=10)
        
        self.bicycle_id_entry_ret = ctk.CTkEntry(master=self.tabview.tab('RETURN'), placeholder_text="Bicylce id to return")
        self.bicycle_id_entry_ret.pack(pady=12, padx=10)

        self.duration_ret = ctk.CTkEntry(master=self.tabview.tab('RETURN'), placeholder_text="How long have you had it?")
        self.duration_ret.pack(pady=12, padx=10)

        self.rent_bike_button_ret = ctk.CTkButton(master=self.tabview.tab('RETURN'), text="Return It", command=self.return_bicycle)
        self.rent_bike_button_ret.pack(pady=12, padx=10)

        self.message = ctk.CTkLabel(master=self.main_app, text='', font=("Arial", 14))
        self.message.pack(pady=12, padx=12)


    def rent_bicycle(self):
        was_added = self.brs.rent_bicycle(
                        self.bicycle_id_entry.get().strip(), 
                        self.duration_entry.get().strip(),
                        BicycleRentalSystem.SelectedLocation)
        
        self.show_message(was_added['message'], was_added['status'])

        
    def return_bicycle(self):
        was_returend = self.brs.return_bicycle(
                            self.bicycle_id_entry_ret.get().strip(), 
                            self.duration_ret.get().strip())
        
        self.show_message(was_returend['message'], was_returend['status'])


    def show_message(self, msg, status):
        self.message.configure(require_redraw=True, text=msg, text_color=f'{'#5de144'if status == 'ok' else '#e1445d'}')
        self.returned_bikes_label.configure(require_redraw=True, text=f"{len(self.brs.bicycle_ids.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}")
        self.available_bikes_label.configure(require_redraw=True, text=f"{len(self.brs.bicycle_ids.keys())} rented out of {BicycleRentalSystem.NUM_BIKES}")

