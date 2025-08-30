import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize contacts list
        self.contacts = []
        self.load_contacts()
        
        # Setup the GUI
        self.setup_gui()
        
        # Display contacts
        self.display_contacts()
    
    def setup_gui(self):
        # Create main frames
        self.search_frame = ttk.Frame(self.root, padding="10")
        self.search_frame.pack(fill=tk.X)
        
        self.list_frame = ttk.Frame(self.root, padding="10")
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = ttk.Frame(self.root, padding="10")
        self.button_frame.pack(fill=tk.X)
        
        # Search components
        ttk.Label(self.search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        # Contact list with scrollbar
        columns = ("Name", "Phone", "Email", "Address")
        self.contact_tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        for col in columns:
            self.contact_tree.heading(col, text=col)
            self.contact_tree.column(col, width=150, minwidth=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.contact_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons
        ttk.Button(self.button_frame, text="Add Contact", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="View Details", command=self.view_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Update Contact", command=self.update_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Exit", command=self.exit_app).pack(side=tk.RIGHT, padx=5)
    
    def add_contact(self):
        # Create a new window for adding a contact
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Contact")
        add_window.geometry("400x300")
        add_window.resizable(False, False)
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Form fields
        ttk.Label(add_window, text="Name:*").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(add_window, text="Phone:*").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        phone_entry = ttk.Entry(add_window, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(add_window, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        email_entry = ttk.Entry(add_window, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(add_window, text="Address:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        address_entry = ttk.Entry(add_window, width=30)
        address_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_contact():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            
            if not name or not phone:
                messagebox.showerror("Error", "Name and Phone are required fields!")
                return
            
            # Add contact to the list
            self.contacts.append({
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            })
            
            # Save and refresh
            self.save_contacts()
            self.display_contacts()
            add_window.destroy()
            messagebox.showinfo("Success", "Contact added successfully!")
        
        # Buttons
        button_frame = ttk.Frame(add_window)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_contact).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def view_contact(self):
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view!")
            return
        
        item = self.contact_tree.item(selected[0])
        contact_index = self.contact_tree.index(selected[0])
        contact = self.contacts[contact_index]
        
        # Create a details window
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Contact Details")
        detail_window.geometry("400x300")
        detail_window.resizable(False, False)
        
        # Display contact information
        info_frame = ttk.Frame(detail_window, padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(info_frame, text="Name:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=contact['name']).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Phone:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=contact['phone']).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Email:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=contact['email'] or "N/A").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Address:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=contact['address'] or "N/A").grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(detail_window, text="Close", command=detail_window.destroy).pack(pady=10)
    
    def update_contact(self):
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to update!")
            return
        
        item = self.contact_tree.item(selected[0])
        contact_index = self.contact_tree.index(selected[0])
        contact = self.contacts[contact_index]
        
        # Create an update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Contact")
        update_window.geometry("400x300")
        update_window.resizable(False, False)
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Form fields with existing data
        ttk.Label(update_window, text="Name:*").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(update_window, width=30)
        name_entry.insert(0, contact['name'])
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(update_window, text="Phone:*").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        phone_entry = ttk.Entry(update_window, width=30)
        phone_entry.insert(0, contact['phone'])
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(update_window, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        email_entry = ttk.Entry(update_window, width=30)
        email_entry.insert(0, contact['email'])
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(update_window, text="Address:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        address_entry = ttk.Entry(update_window, width=30)
        address_entry.insert(0, contact['address'])
        address_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_changes():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            
            if not name or not phone:
                messagebox.showerror("Error", "Name and Phone are required fields!")
                return
            
            # Update contact
            self.contacts[contact_index] = {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            }
            
            # Save and refresh
            self.save_contacts()
            self.display_contacts()
            update_window.destroy()
            messagebox.showinfo("Success", "Contact updated successfully!")
        
        # Buttons
        button_frame = ttk.Frame(update_window)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=update_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def delete_contact(self):
        selected = self.contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return
        
        item = self.contact_tree.item(selected[0])
        contact_name = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{contact_name}'?"):
            contact_index = self.contact_tree.index(selected[0])
            del self.contacts[contact_index]
            
            # Save and refresh
            self.save_contacts()
            self.display_contacts()
            messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def search_contacts(self, event=None):
        query = self.search_var.get().lower()
        
        # Clear current display
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        # Filter and display contacts
        for contact in self.contacts:
            if (query in contact['name'].lower() or 
                query in contact['phone'].lower() or
                query in contact['email'].lower() or
                query in contact['address'].lower()):
                
                self.contact_tree.insert("", tk.END, values=(
                    contact['name'],
                    contact['phone'],
                    contact['email'],
                    contact['address']
                ))
    
    def display_contacts(self):
        # Clear current display
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        # Add all contacts to the treeview
        for contact in self.contacts:
            self.contact_tree.insert("", tk.END, values=(
                contact['name'],
                contact['phone'],
                contact['email'],
                contact['address']
            ))
    
    def load_contacts(self):
        # Load contacts from a JSON file
        if os.path.exists('contacts.json'):
            try:
                with open('contacts.json', 'r') as f:
                    self.contacts = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.contacts = []
        else:
            self.contacts = []
    
    def save_contacts(self):
        # Save contacts to a JSON file
        with open('contacts.json', 'w') as f:
            json.dump(self.contacts, f, indent=4)
    
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()