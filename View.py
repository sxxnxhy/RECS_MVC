import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # Import the Python Imaging Library
import os
import math

from calculationSubstation import CalculationSubstation


class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Railway Electrification Calculation Simulator")
        self.window.geometry("480x580")
        self.transport_type = tk.StringVar(value="Mode of transportation")
        self.type_of_calculation = tk.StringVar(value="Type of calculation")

        #script_dir = os.path.dirname(os.path.abspath(__file__))
        #ico_path = os.path.join(script_dir, "images/train.icns")
        #self.window.iconbitmap(default=ico_path)                    #for windows
        #self.window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file=ico_path))

        self.create_first_page()

    def create_first_page(self):
        tk.OptionMenu(self.window, self.transport_type, "Main railway 3 kV DC", "Main railway 2x25 kV AC", "Light railway 1.5 kV DC", "Metro", "Tram").pack(pady=50)
        tk.OptionMenu(self.window, self.type_of_calculation, "Substation", "Traction system", "Short circuit").pack(pady=50)
        tk.Button(self.window, text="OK", command=self.go_to_second_page).pack(pady=150)

    def go_to_second_page(self):
        if self.transport_type.get() == "Mode of transportation":
            messagebox.showerror("Invalid input", "Please select a mode of transportation.")
            return
        if self.transport_type.get() in ("Main railway 2x25 kV AC", "Light railway 1.5 kV DC", "Metro", "Tram"):
            messagebox.showerror("Invalid input", "This mode of transportation is not available yet.")
            return
        if self.type_of_calculation.get() == "Type of calculation":
            messagebox.showerror("Invalid input", "Please select a type of calculation")
            return

        self.window.destroy()

        if self.transport_type.get() == "Main railway 3 kV DC" and self.type_of_calculation.get() == "Substation":
            self.window = TransportPageForTrain(self.type_of_calculation.get())
        elif self.transport_type.get() == "Main railway 3 kV DC" and self.type_of_calculation.get() == "Traction system":
            self.window = PageForTraction(self.type_of_calculation.get())
        elif self.transport_type.get() == "Main railway 3 kV DC" and self.type_of_calculation.get() == "Short circuit":
            self.window = PageForShortCircuit(self.type_of_calculation.get())

    def run(self):
        self.window.mainloop()


class TransportPageForTrain:
    def __init__(self, type_of_calculation):
        self.window = tk.Tk()
        self.window.title("Main railway 3 kV DC - Substation")
        self.window.geometry("1300x800")
        self.type_of_calculation = type_of_calculation
        self.type_of_calculations = tk.StringVar(value="Type of Calculation")
        self.parameter_1 = tk.StringVar(value="Rated voltage on the HV side (kV)")
        self.parameter_2 = tk.StringVar(value="Short-circuit power of the power supply system on the HV side (MVA)")
        self.parameter_3 = tk.StringVar(value="rated power of the HV/MV transformer (MVA)")
        self.parameter_4 = tk.StringVar(value="Percentage short-circuit voltage of the MV/LV transformer (%)")
        self.parameter_5 = tk.StringVar(value="Rated voltage on the MV side (kV)")
        self.parameter_6_1 = tk.StringVar(value="Type and cross-section of the MV line")
        self.parameter_6_2 = tk.StringVar(value="Type of MV line")
        self.parameter_6_3 = tk.StringVar(value="Cross-section of the MV line (mm^2)")
        self.parameter_7 = tk.StringVar(value="Length of the MV line (km)")
        self.parameter_8 = tk.StringVar(value="Unit reactance of the MV line (Ω/km)")
        self.parameter_9 = tk.StringVar(value="Type of rectifier unit")
        self.parameter_10 = tk.StringVar(value="Number of rectifier units")
        self.create_page()

    def create_page(self):
        self.canvas = tk.Canvas(self.window, width=1200, height=230)
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=15)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "images/TS.png")

        train_img = Image.open(img_path)
        new_width = train_img.width // 1.8
        new_height = train_img.height // 1.8
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        global _image
        _image = train_img_tk

        # Create a Frame for each
        tk.Label(self.window, text="HV line", font=("Helvetica", 12, "bold")).grid(row=3, column=0, padx=10, pady=10)
        frame1 = tk.Frame(self.window, bd=2, relief="groove")
        frame1.grid(row=4, column=0, padx=10, pady=10)
        label1 = tk.Label(frame1, text="Rated voltage\non the HV side (kV)")
        label1.pack()
        self.parameter_1.set("Choose")
        option_menu1 = tk.OptionMenu(frame1, self.parameter_1, "110")
        option_menu1.pack()

        tk.Label(self.window, text="PCC Transformer", font=("Helvetica", 12, "bold")).grid(row=3, column=1, padx=10, pady=10)
        frame2 = tk.Frame(self.window, bd=2, relief="groove")
        frame2.grid(row=4, column=1, padx=10, pady=10)
        label2 = tk.Label(frame2, text="Short-circuit power of the power\nsupply system on the HV side (MVA)")
        label2.pack()
        self.parameter_2.set("")
        entry2 = tk.Entry(frame2, textvariable=self.parameter_2)
        entry2.pack()

        frame3 = tk.Frame(self.window, bd=2, relief="groove")
        frame3.grid(row=5, column=1, padx=10, pady=10)
        label3 = tk.Label(frame3, text="Rated power of the\nHV/MV transformer (MVA)")
        label3.pack()
        self.parameter_3.set("Choose")
        option_menu3 = tk.OptionMenu(frame3, self.parameter_3, "40", "32", "25", "20", "16", "10", "6")
        option_menu3.pack()

        frame4 = tk.Frame(self.window, bd=2, relief="groove")
        frame4.grid(row=6, column=1, padx=10, pady=10)
        label4 = tk.Label(frame4, text="Percentage short-circuit voltage\nof the MV/LV transformer (%)")
        label4.pack()
        self.parameter_4.set("")
        entry4 = tk.Entry(frame4, textvariable=self.parameter_4)
        entry4.pack()

        frame5 = tk.Frame(self.window, bd=2, relief="groove")
        frame5.grid(row=7, column=1, padx=10, pady=10)
        label5 = tk.Label(frame5, text="Rated voltage on the MV side (kV)")
        label5.pack()
        self.parameter_5.set("Choose")
        option_menu5 = tk.OptionMenu(frame5, self.parameter_5, "30", "20", "15")
        option_menu5.pack()

        tk.Label(self.window, text="MV line", font=("Helvetica", 12, "bold")).grid(row=3, column=2, padx=10, pady=10)
        frame6 = tk.Frame(self.window, bd=2, relief="groove")
        frame6.grid(row=4, column=2, padx=10, pady=10)
        label6 = tk.Label(frame6, text="Type of the MV line")
        label6.pack()
        self.parameter_6_1.set("Choose")
        option_menu6 = tk.OptionMenu(frame6, self.parameter_6_1, "Cu cable", "Al cable", "Overhead AFL-6")
        option_menu6.pack()

        frame7 = tk.Frame(self.window, bd=2, relief="groove")
        frame7.grid(row=5, column=2, padx=10, pady=10)
        label7 = tk.Label(frame7, text="Cross-section of the MV line (mm^2)")
        label7.pack()
        self.parameter_6_2.set("Choose")
        option_menu7 = tk.OptionMenu(frame7, self.parameter_6_2, "3x120", "3x150", "3x185", "3x240", "3x300", "3x70", "3x95")
        option_menu7.pack()

        frame8 = tk.Frame(self.window, bd=2, relief="groove")
        frame8.grid(row=6, column=2, padx=10, pady=10)
        label8 = tk.Label(frame8, text="Length of the MV line (km)")
        label8.pack()
        self.parameter_7.set("")
        entry8 = tk.Entry(frame8, textvariable=self.parameter_7)
        entry8.pack()

        tk.Label(self.window, text="Rectifier unit", font=("Helvetica", 12, "bold")).grid(row=3, column=3, padx=10, pady=10)
        frame9 = tk.Frame(self.window, bd=2, relief="groove")
        frame9.grid(row=4, column=3, padx=10, pady=10)
        label9 = tk.Label(frame9, text="Unit reactance of the MV line (Ω/km)")
        label9.pack()
        self.parameter_8.set("")
        entry9 = tk.Entry(frame9, textvariable=self.parameter_8)
        entry9.pack()

        frame10 = tk.Frame(self.window, bd=2, relief="groove")
        frame10.grid(row=5, column=3, padx=10, pady=10)
        label10 = tk.Label(frame10, text="Type of the rectifier unit")
        label10.pack()
        self.parameter_9.set("Choose")
        option_menu10 = tk.OptionMenu(frame10, self.parameter_9, "PD17", "PD1.7", "PD16", "PD12", "PK17")
        option_menu10.pack()

        frame11 = tk.Frame(self.window, bd=2, relief="groove")
        frame11.grid(row=6, column=3, padx=10, pady=10)
        label11 = tk.Label(frame11, text="Number of the rectifier units")
        label11.pack()
        self.parameter_10.set("Choose")
        option_menu11 = tk.OptionMenu(frame11, self.parameter_10, "1", "2", "3", "4", "5")
        option_menu11.pack()
        #Calculate button
        tk.Button(self.window, text="Calculate", command=self.show_result).place(x=550, y=640)
        #Go back button
        tk.Button(self.window, text="Go back", command=self.go_back).place(x=553, y=720)


    def go_back(self):
        self.window.destroy()
        app = Application()
        app.run()

    def run(self):
        self.window.mainloop()


    def show_result(self):
        result_window = tk.Toplevel(self.window)
        result_window.title("Calculation Result")
        result_window.geometry("500x300")

        error_message = tk.Label(result_window, text="Error, Please review the input fields carefully!\nMake sure to use a period for decimals instead of a comma.", font=("Helvetica", 12, "bold"), fg="red")
        error_message.pack()

        #변수 이름 정리
        parameter_9_value = self.parameter_9.get()
        parameter_10_value = float(self.parameter_10.get())
        parameter_2_value = float(self.parameter_2.get())
        parameter_3_value = float(self.parameter_3.get())
        parameter_4_value = float(self.parameter_4.get())
        parameter_5_value = float(self.parameter_5.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_7_value = float(self.parameter_7.get())
        parameter_6_1_value = self.parameter_6_1.get()
        parameter_6_2_value = self.parameter_6_2.get()


        substation = CalculationSubstation()

        result_a = [round(num, 2) for num in substation.calculation_a(parameter_9_value, parameter_10_value, parameter_5_value)]
        result_a_str = ', '.join(map(str, result_a))
        tk.Label(result_window, text=f"MV line current [A]: {result_a_str}").pack()

        error_message_1 = tk.Label(result_window, text="An error has occured, and the calculation cannot be completed.\nPlease double check the input fileds carefully.", font=("Helvetica", 12, "bold"), fg="red")
        error_message_1.pack()



        result_b, result_b_1, result_b_2, result_b_3 = substation.calculation_b(parameter_2_value, parameter_3_value, parameter_4_value, parameter_5_value, parameter_8_value, parameter_7_value)
        result_b = [round(num, 2) for num in result_b]
        result_b_1 = [round(num, 2) for num in result_b_1]
        result_b_2 = [round(num, 2) for num in result_b_2]
        result_b_3 = [round(num, 2) for num in result_b_3]
        result_b_str = ', '.join(map(str, result_b))
        result_b_1_str = ', '.join(map(str, result_b_1))
        result_b_2_str = ', '.join(map(str, result_b_2))
        result_b_3_str = ', '.join(map(str, result_b_3))
        tk.Label(result_window, text=f"Short-circuit power at MV side of RU [VA]: {result_b_str}").pack()
        tk.Label(result_window, text=f"Reactance at HV side [Ω]: {result_b_1_str}").pack()
        tk.Label(result_window, text=f"Reactance of HV/MV transformer [Ω]: {result_b_2_str}").pack()
        tk.Label(result_window, text=f"Reactance of MV line [Ω]: {result_b_3_str}").pack()

        result_c = substation.calculation_c(parameter_9_value, parameter_10_value, parameter_7_value, parameter_8_value, parameter_5_value, parameter_6_1_value, parameter_6_2_value)
        result_c_1 = result_c[0]
        rounded_result_c_1 = [round(num, 2) for num in result_c_1]
        rounded_result_c_1_str = ', '.join(map(str, rounded_result_c_1))
        tk.Label(result_window, text=f"Voltage drop at MV line [V]: {rounded_result_c_1_str}").pack()

        result_d = [round(num, 2) for num in substation.calculation_d(parameter_5_value, parameter_9_value, parameter_10_value, parameter_7_value, parameter_8_value, parameter_6_1_value, parameter_6_2_value)]
        result_d_str = ', '.join(map(str, result_d))
        tk.Label(result_window, text=f"Relative voltage drop in MV line [%]: {result_d_str}").pack()

        result_e = substation.calculation_e(parameter_9_value, parameter_4_value, parameter_10_value, result_b)
        result_e_1 = result_e[0]
        rounded_result_e_1 = [round(num, 2) for num in result_e_1]
        rounded_result_e_1_str = ', '.join(map(str, rounded_result_e_1))
        tk.Label(result_window, text=f"TS no-load voltage [V]: {rounded_result_e_1_str}").pack()

        result_g = [round(num, 3) for num in substation.calculation_g(result_e)]
        result_g_str = ', '.join(map(str, result_g))
        tk.Label(result_window, text=f"TS external characteristic slope: {result_g_str}").pack()

        result_h = [round(num, 3) for num in substation.calculation_h(result_g, parameter_9_value, parameter_4_value, parameter_10_value, result_b)]
        result_h_str = ', '.join(map(str, result_h))
        tk.Label(result_window, text=f"TS internal resistance for all RU [Ω]: {result_h_str}").pack()

        result_i = [round(num, 3) for num in substation.calculation_i(result_g, parameter_9_value, parameter_4_value, parameter_10_value, result_b)]
        result_i_str = ', '.join(map(str, result_i))
        tk.Label(result_window, text=f"TS internal resistance for a single RU [Ω]: {result_i_str}").pack()

        error_message.pack_forget()
        error_message_1.pack_forget()









class PageForTraction:
    def __init__(self, type_of_calculation):
        self.window = tk.Tk()
        self.window.title("Main railway 3kV DC - Traction system")
        self.window.geometry("1400x800")
        self.type_of_calculation = type_of_calculation
        self.type_of_calculations = tk.StringVar(value="Type of Calculation")
        self.parameter_1 = tk.StringVar(value="Rated voltage on the HV side (kV)")
        self.parameter_2 = tk.StringVar(value="Short-circuit power of the power supply system on the HV side (MVA)")
        self.parameter_3 = tk.StringVar(value="rated power of the HV/MV transformer (MVA)")
        self.parameter_4 = tk.StringVar(value="Percentage short-circuit voltage of the MV/LV transformer (%)")
        self.parameter_5 = tk.StringVar(value="Rated voltage on the MV side (kV)")
        self.parameter_6_1 = tk.StringVar(value="Type and cross-section of the MV line")
        self.parameter_6_2 = tk.StringVar(value="Type of MV line")
        self.parameter_6_3 = tk.StringVar(value="Cross-section of the MV line (mm^2)")
        self.parameter_7 = tk.StringVar(value="Length of the MV line (km)")
        self.parameter_8 = tk.StringVar(value="Unit reactance of the MV line (Ω/km)")
        self.parameter_9 = tk.StringVar(value="Type of rectifier unit")
        self.parameter_10 = tk.StringVar(value="Number of rectifier units")
        self.new_parameter_1 = tk.StringVar(value="Type & material")
        self.new_paramter_1_1 = tk.StringVar(value="Type & material2")
        self.new_parameter_2 = tk.StringVar(value="Cross-section (mm^2)1")
        self.new_parameter_3 = tk.StringVar(value="Cross-section (mm^2)2")
        self.new_parameter_4 = tk.StringVar(value="Number of wires1")
        self.new_parameter_5 = tk.StringVar(value="Number of wires2")
        self.new_parameter_5_1 = tk.StringVar(value="Length of the section1")
        self.new_parameter_5_2 = tk.StringVar(value="Length of the section2")
        self.new_parameter_6 = tk.StringVar(value="Catenary system type")
        self.new_parameter_7 = tk.StringVar(value="Rails type")
        self.new_parameter_8 = tk.StringVar(value="Number of tracks")
        self.new_parameter_9 = tk.StringVar(value="Type of traction power supply")
        self.new_parameter_10 = tk.StringVar(value="Locomotive current")
        self.new_parameter_11 = tk.StringVar(value="Length of the section")
        self.new_parameter_12 = tk.StringVar(value="Ground earth resistance")
        self.new_parameter_13 = tk.StringVar(value="manual no load voltage")

        self.create_page()

    def create_page(self):
        self.canvas = tk.Canvas(self.window, width=1200, height=230)
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=15)

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 1.8
        new_height = train_img.height // 1.8
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk

        # Create a Frame for each
        self.main_label1 = tk.Label(self.window, text="HV line", font=("Helvetica", 12, "bold"))
        self.main_label1.grid(row=3, column=0, padx=10, pady=10)
        self.frame1 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame1.grid(row=4, column=0, padx=10, pady=10)
        label1 = tk.Label(self.frame1, text="Rated voltage\non the HV side (kV)")
        label1.pack()
        self.parameter_1.set("Choose")
        option_menu1 = tk.OptionMenu(self.frame1, self.parameter_1, "110")
        option_menu1.pack()

        self.main_label2 = tk.Label(self.window, text="PCC Transformer", font=("Helvetica", 12, "bold"))
        self.main_label2.grid(row=3, column=1, padx=10, pady=10)
        self.frame2 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame2.grid(row=4, column=1, padx=10, pady=10)
        label2 = tk.Label(self.frame2, text="Short-circuit power of the power\nsupply system on the HV side (MVA)")
        label2.pack()
        self.parameter_2.set("")
        entry2 = tk.Entry(self.frame2, textvariable=self.parameter_2)
        entry2.pack()

        self.frame3 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame3.grid(row=5, column=1, padx=10, pady=10)
        label3 = tk.Label(self.frame3, text="Rated power of the\nHV/MV transformer (MVA)")
        label3.pack()
        self.parameter_3.set("Choose")
        option_menu3 = tk.OptionMenu(self.frame3, self.parameter_3, "40", "32", "25", "20", "16", "10", "6")
        option_menu3.pack()

        self.frame4 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame4.grid(row=6, column=1, padx=10, pady=10)
        label4 = tk.Label(self.frame4, text="Percentage short-circuit voltage\nof the MV/LV transformer (%)")
        label4.pack()
        self.parameter_4.set("")
        entry4 = tk.Entry(self.frame4, textvariable=self.parameter_4)
        entry4.pack()

        self.frame5 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame5.grid(row=7, column=1, padx=10, pady=10)
        label5 = tk.Label(self.frame5, text="Rated voltage on the MV side (kV)")
        label5.pack()
        self.parameter_5.set("Choose")
        option_menu5 = tk.OptionMenu(self.frame5, self.parameter_5, "30", "20", "15")
        option_menu5.pack()

        self.main_label3 = tk.Label(self.window, text="MV line", font=("Helvetica", 12, "bold"))
        self.main_label3.grid(row=3, column=2, padx=10, pady=10)
        self.frame6 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame6.grid(row=4, column=2, padx=10, pady=10)
        label6 = tk.Label(self.frame6, text="Type of the MV line")
        label6.pack()
        self.parameter_6_1.set("Choose")
        option_menu6 = tk.OptionMenu(self.frame6, self.parameter_6_1, "Cu cable", "Al cable", "Overhead AFL-6")
        option_menu6.pack()

        self.frame7 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame7.grid(row=5, column=2, padx=10, pady=10)
        label7 = tk.Label(self.frame7, text="Cross-section of the MV line (mm^2)")
        label7.pack()
        self.parameter_6_2.set("Choose")
        option_menu7 = tk.OptionMenu(self.frame7, self.parameter_6_2, "3x120", "3x150", "3x185", "3x240", "3x300", "3x70", "3x95")
        option_menu7.pack()

        self.frame8 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame8.grid(row=6, column=2, padx=10, pady=10)
        label8 = tk.Label(self.frame8, text="Length of the MV line (km)")
        label8.pack()
        self.parameter_7.set("")
        entry8 = tk.Entry(self.frame8, textvariable=self.parameter_7)
        entry8.pack()

        self.main_label4 = tk.Label(self.window, text="Rectifier unit", font=("Helvetica", 12, "bold"))
        self.main_label4.grid(row=3, column=3, padx=10, pady=10)
        self.frame9 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame9.grid(row=4, column=3, padx=10, pady=10)
        label9 = tk.Label(self.frame9, text="Unit reactance of the MV line (Ω/km)")
        label9.pack()
        self.parameter_8.set("")
        entry9 = tk.Entry(self.frame9, textvariable=self.parameter_8)
        entry9.pack()

        self.frame10 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame10.grid(row=5, column=3, padx=10, pady=10)
        label10 = tk.Label(self.frame10, text="Type of the rectifier unit")
        label10.pack()
        self.parameter_9.set("Choose")
        option_menu10 = tk.OptionMenu(self.frame10, self.parameter_9, "PD17", "PD1.7", "PD16", "PD12", "PK17")
        option_menu10.pack()

        self.frame11 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame11.grid(row=6, column=3, padx=10, pady=10)
        label11 = tk.Label(self.frame11, text="Number of the rectifier units")
        label11.pack()
        self.parameter_10.set("Choose")
        option_menu11 = tk.OptionMenu(self.frame11, self.parameter_10, "1", "2", "3", "4", "5")
        option_menu11.pack()

        #Calculate button
        tk.Button(self.window, text="Calculate", command=self.train_distance_simulation).place(x=550, y=640)
        #Go back button
        tk.Button(self.window, text="Go back", command=self.go_back).place(x=553, y=720)


        self.arrow_button = tk.Button(self.window, text="→", command=self.show_new_parameters, height=3, font=('Helvetica', '16'))
        self.arrow_button.place(x=1160, y=300)  # Example coordinates

        self.arrow_button1 = tk.Button(self.window, text="←", command=self.untoggle_parameters, height=3, font=('Helvetica', '16'))
        self.arrow_button1.place(x=1110, y=300)  # Example coordinates
        self.arrow_button1.config(state="disabled")

        # Keep track of the current state
        self.parameters_visible = True

    def go_back(self):
        self.window.destroy()
        app = Application()
        app.run()

    def run(self):
        self.window.mainloop()

    def toggle_parameters(self):
        if self.parameters_visible:
            # Hide current parameters
            self.hide_parameters()
        else:
            # Show new parameters
            self.show_new_parameters()
        self.parameters_visible = not self.parameters_visible

    def hide_parameters(self):
        self.canvas.delete(self.train_image)

        # Example of hiding a frame
        self.frame1.grid_forget()
        self.frame2.grid_forget()
        self.frame3.grid_forget()
        self.frame4.grid_forget()
        self.frame5.grid_forget()
        self.frame6.grid_forget()
        self.frame7.grid_forget()
        self.frame8.grid_forget()
        self.frame9.grid_forget()
        self.frame10.grid_forget()
        self.frame11.grid_forget()
        self.main_label1.grid_forget()
        self.main_label2.grid_forget()
        self.main_label3.grid_forget()
        self.main_label4.grid_forget()
        # Repeat for all frames you want to hide

    def show_new_parameters(self):
        # First, hide existing parameters if they are visible
        self.hide_parameters()

        self.arrow_button.config(state="disabled")
        self.arrow_button1.config(state="normal")

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS2.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 3.5
        new_height = train_img.height // 3.5
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk



        # Create and show new parameters
        # First table
        self.group_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.group_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.new_main_label1 = tk.Label(self.group_frame, text="Feeder Cable")
        self.new_main_label1.grid(row=4, column=1, padx=10, pady=10)

        self.new_main_label2 = tk.Label(self.group_frame, text="Return Cable")
        self.new_main_label2.grid(row=5, column=1, padx=10, pady=10)

        self.new_main_label3 = tk.Label(self.group_frame, text="Type & Material")
        self.new_main_label3.grid(row=3, column=2, padx=10, pady=10)

        self.new_main_label4 = tk.Label(self.group_frame, text="Cross-section (mm^2)")
        self.new_main_label4.grid(row=3, column=3, padx=10, pady=10)

        self.new_main_label5 = tk.Label(self.group_frame, text="Number of wires")
        self.new_main_label5.grid(row=3, column=4, padx=10, pady=10)

        self.new_main_label5_1 = tk.Label(self.group_frame, text="Length of the cable (m)")
        self.new_main_label5_1.grid(row=3, column=5, padx=10, pady=10)

        self.new_parameter_1.set("Choose")
        self.new_option_menu1 = tk.OptionMenu(self.group_frame, self.new_parameter_1, "Cu, YKY", "Cu, YKYy", "Al, YAKY", "Al, YAKYy")
        self.new_option_menu1.grid(row=4, column=2, padx=10, pady=10)

        self.new_paramter_1_1.set("Choose")
        self.new_option_menu1_1 = tk.OptionMenu(self.group_frame, self.new_paramter_1_1, "Cu, YKY", "Cu, YKYy", "Al, YAKY", "Al, YAKYy")
        self.new_option_menu1_1.grid(row=5, column=2, padx=10, pady=10)

        self.new_parameter_2.set("Choose")
        self.new_entry1 = tk.OptionMenu(self.group_frame, self.new_parameter_2, "120", "150", "185", "240", "300", "400", "500", "625", "800")
        self.new_entry1.grid(row=4, column=3, padx=10, pady=10)

        self.new_parameter_3.set("Choose")
        self.new_entry2 = tk.OptionMenu(self.group_frame, self.new_parameter_3, "120", "150", "185", "240", "300", "400", "500", "625", "800")
        self.new_entry2.grid(row=5, column=3, padx=10, pady=10)

        self.new_parameter_4.set("")
        self.new_entry3 = tk.Entry(self.group_frame, textvariable=self.new_parameter_4)
        self.new_entry3.grid(row=4, column=4, padx=10, pady=10)

        self.new_parameter_5.set("")
        self.new_entry4 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5)
        self.new_entry4.grid(row=5, column=4, padx=10, pady=10)

        self.new_parameter_5_1.set("")
        self.new_entry4_1 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5_1)
        self.new_entry4_1.grid(row=4, column=5, padx=10, pady=10)

        self.new_parameter_5_2.set("")
        self.new_entry4_2 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5_2)
        self.new_entry4_2.grid(row=5, column=5, padx=10, pady=10)


        # Second table
        self.group_frame1 = tk.Frame(self.window, bd=2, relief="groove")
        self.group_frame1.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.new_main_label6 = tk.Label(self.group_frame1, text="Catenary system type")
        self.new_main_label6.grid(row=7, column=0, padx=10, pady=10)

        self.new_main_label7 = tk.Label(self.group_frame1, text="Rails type")
        self.new_main_label7.grid(row=8, column=0, padx=10, pady=10)

        self.new_main_label8 = tk.Label(self.group_frame1, text="Number of tracks")
        self.new_main_label8.grid(row=9, column=0, padx=10, pady=10)

        self.new_main_label9 = tk.Label(self.group_frame1, text="Ground earth resistance (Ω/km)")
        self.new_main_label9.grid(row=10, column=0, padx=10, pady=10)

        # self.new_main_label9 = tk.Label(self.group_frame1, text="Type")
        # self.new_main_label9.grid(row=6, column=1, padx=10, pady=10)

        self.new_parameter_6.set("Choose")
        self.new_option_menu2 = tk.OptionMenu(self.group_frame1, self.new_parameter_6, "KB70-C", "C70-C", "C95-C", "Fe70-2C", "CuCd70-2C", "KB95-2C, YKB95-2C", "C95-2C, YC95-2C, YpC95-2C", "C150-C150, YC150-C150", "C120-2C, YC1202C, YpC120-2C, YzC120-2C, YSC120-2C, Yws120-2C", "C120-2C150, YC120-2C150", "2C120-2C, 2C120-2C-1, 2C120-2C-2", "C150-2C150")
        self.new_option_menu2.grid(row=7, column=1, padx=10, pady=10)
        self.new_option_menu2.config(width=55)

        self.new_parameter_7.set("Choose")
        self.new_option_menu3 = tk.OptionMenu(self.group_frame1, self.new_parameter_7, "S-49", "S-60")
        self.new_option_menu3.grid(row=8, column=1, padx=10, pady=10)

        self.new_parameter_8.set("Choose")
        self.new_option_menu4 = tk.OptionMenu(self.group_frame1, self.new_parameter_8, "Single-track", "Double-track")
        self.new_option_menu4.grid(row=9, column=1, padx=10, pady=10)

        self.new_parameter_12.set("")
        self.new_entry5 = tk.Entry(self.group_frame1, textvariable=self.new_parameter_12)
        self.new_entry5.grid(row=10, column=1, padx=10, pady=10)



        # Create a single frame to hold all elements
        self.combined_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.combined_frame.grid(row=6, column=2, columnspan=4, padx=10, pady=10, rowspan=3)  # Adjust rowspan as needed to fit all elements

        # Third table elements
        self.new_main_label10 = tk.Label(self.combined_frame, text="Type of traction power supply")
        self.new_main_label10.grid(row=0, column=0, padx=10, pady=10)  # Adjust grid positions as needed

        self.new_parameter_9.set("Choose")
        self.new_option_menu5 = tk.OptionMenu(self.combined_frame, self.new_parameter_9, "One-sided", "Two-sided", "Two-sided with sectioning cabin")
        self.new_option_menu5.grid(row=0, column=1, padx=10, pady=10)
        self.new_option_menu5.config(width=23)


        self.new_main_label11 = tk.Label(self.combined_frame, text="Locomotive current (A)")
        self.new_main_label11.grid(row=1, column=0, padx=10, pady=10)  # Adjust grid positions as needed

        self.new_parameter_10.set("")
        self.new_option_menu6 = tk.Entry(self.combined_frame, textvariable=self.new_parameter_10)
        self.new_option_menu6.grid(row=1, column=1, padx=10, pady=10)

        self.new_main_label12 = tk.Label(self.combined_frame, text="Length of the section (km)")
        self.new_main_label12.grid(row=2, column=0, padx=10, pady=10)  # Adjust grid positions as needed

        self.new_parameter_11.set("")
        self.new_option_menu7 = tk.Entry(self.combined_frame, textvariable=self.new_parameter_11)
        self.new_option_menu7.grid(row=2, column=1, padx=10, pady=10)
        # Continue adding other UI elements as needed
        # Remember to update the toggle or visibility state as appropriate

        self.new_main_label13 = tk.Label(self.combined_frame, text="Manual no load voltage (V)")
        self.new_main_label13.grid(row=3, column=0, padx=10, pady=10)

        self.new_parameter_13 = tk.StringVar()
        self.new_entry6 = tk.Entry(self.combined_frame, textvariable=self.new_parameter_13, state='disabled')
        self.new_entry6.grid(row=3, column=1, padx=10, pady=10)

        self.tick_button_var = tk.BooleanVar()
        self.tick_button = tk.Checkbutton(self.combined_frame, text="Enable", variable=self.tick_button_var, command=self.manual_no_load_voltage)
        self.tick_button.grid(row=3, column=2, padx=10, pady=10)  # Adjust grid position as needed

    def manual_no_load_voltage(self):
        if self.tick_button_var.get():
            self.new_entry6.config(state='normal')
        else:
            self.new_entry6.config(state='disabled')



    def toggle_existing_new_parameters(self):
        self.hide_parameters()

        self.arrow_button.config(state="disabled")
        self.arrow_button1.config(state="normal")

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS2.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 3.5
        new_height = train_img.height // 3.5
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk


        self.group_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.group_frame1.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.combined_frame.grid(row=6, column=2, columnspan=4, padx=10, pady=10, rowspan=3)  # Adjust grid positions as needed

    def untoggle_parameters(self):

        # Disable the left arrow button
        self.arrow_button1.config(state='disabled')
        # Enable the right arrow button
        self.arrow_button.config(state='normal', command=self.toggle_existing_new_parameters)

        self.canvas.delete(self.train_image)
        self.group_frame.grid_forget()
        self.group_frame1.grid_forget()
        self.combined_frame.grid_forget()

        self.canvas = tk.Canvas(self.window, width=1200, height=230)
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=15)

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 1.8
        new_height = train_img.height // 1.8
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk


        # Show the previously hidden frames and labels
        self.frame1.grid(row=4, column=0, padx=10, pady=10)
        self.frame2.grid(row=4, column=1, padx=10, pady=10)
        self.frame3.grid(row=5, column=1, padx=10, pady=10)
        self.frame4.grid(row=6, column=1, padx=10, pady=10)
        self.frame5.grid(row=7, column=1, padx=10, pady=10)
        self.frame6.grid(row=4, column=2, padx=10, pady=10)
        self.frame7.grid(row=5, column=2, padx=10, pady=10)
        self.frame8.grid(row=6, column=2, padx=10, pady=10)
        self.frame9.grid(row=4, column=3, padx=10, pady=10)
        self.frame10.grid(row=5, column=3, padx=10, pady=10)
        self.frame11.grid(row=6, column=3, padx=10, pady=10)
        self.main_label1.grid(row=3, column=0, padx=10, pady=10)
        self.main_label2.grid(row=3, column=1, padx=10, pady=10)
        self.main_label3.grid(row=3, column=2, padx=10, pady=10)
        self.main_label4.grid(row=3, column=3, padx=10, pady=10)
        # Update the visibility state
        self.parameters_visible = True

    # Calculation algorithm
    def calculation_a(self):
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
        else:
            parameter_9_1 = 4400000

        parameter_2_value = float(self.parameter_2.get())
        parameter_3_value = float(self.parameter_3.get())
        parameter_4_value = float(self.parameter_4.get())
        parameter_5_value = float(self.parameter_5.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_7_value = float(self.parameter_7.get())
        parameter_10_value = float(self.parameter_10.get())

        result_a = [(parameter_9_1 * parameter_10_value) / (math.sqrt(3) * (parameter_5_value * 1000))]
        return result_a, parameter_2_value, parameter_3_value, parameter_4_value, parameter_5_value, parameter_7_value, parameter_8_value, parameter_10_value

    def calculation_b(self):
        parameter_2_value = float(self.parameter_2.get())
        parameter_3_value = float(self.parameter_3.get())
        parameter_4_value = float(self.parameter_4.get())
        parameter_5_value = float(self.parameter_5.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_7_value = float(self.parameter_7.get())

        result_b_1 = (1.1 * ((parameter_5_value)**2)) / (parameter_2_value)
        result_b_2 = (parameter_4_value / 100) * ((parameter_5_value**2) / parameter_3_value)
        result_b_3 = (parameter_8_value) * (parameter_7_value)
        result_b = (1.1 * ((parameter_5_value * 1000)**2)) / (result_b_1 + result_b_2 + result_b_3)

        return [result_b], [result_b_1], [result_b_2], [result_b_3]

    def calculation_c(self):
        parameter_9_2 = 0 #initial default value
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD1.7":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD16":
            parameter_9_2 = 5280000
        elif parameter_9_value == "PD12":
            parameter_9_2 =  3960000
        elif parameter_9_value == "PK17":
            parameter_9_2 = 2475000

        parameter_10_value = float(self.parameter_10.get())
        parameter_7_value = float(self.parameter_7.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_5_value = float(self.parameter_5.get())

        #Resistance of wires and load currents for overhead lines
        parameter_6 = 0 #initial default value
        parameter_6_1_value = self.parameter_6_1.get()
        parameter_6_2_value = self.parameter_6_2.get()
        if parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.153
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.124
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.099
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.075
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.060
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.258
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.253
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.205
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.164
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.125
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.1
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.443
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.32
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x120":
            parameter_6 = 0.234
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x150":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x185":
            parameter_6 = 0.156
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x240":
            parameter_6 = 0.137
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x300":
            parameter_6 = 0.121

        result_c = [((parameter_9_2 * 2 * parameter_10_value) / ((math.sqrt(3)) * (parameter_5_value * 1000) * 0.95)) * (parameter_7_value * ((parameter_6 * 0.95) + (parameter_8_value * math.sqrt(1-0.95*0.95))))]
        return result_c, parameter_9_2

    def calculation_d(self):
        result_c, _ = self.calculation_c() #ignore the second value]
        parameter_5_value = float(self.parameter_5.get())
        result_d = [((math.sqrt(3) * result_c[0]) / (parameter_5_value * 1000)) * 100]
        return result_d

    def calculation_e(self):
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 53500
            parameter_9_5 = 3
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 38000
            parameter_9_5 = 3
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
            parameter_9_2 = 5280000
            parameter_9_3 = 1600
            parameter_9_4 = 46000
            parameter_9_5 = 3
        elif parameter_9_value == "PD12":
            parameter_9_1 = 5850000
            parameter_9_2 = 3960000
            parameter_9_3 = 1200
            parameter_9_4 = 36000
            parameter_9_5 = 3
        elif parameter_9_value == "PK17":
            parameter_9_1 = 5850000
            parameter_9_2 = 2475000
            parameter_9_3 = 750
            parameter_9_4 = 36000
            parameter_9_5 = 8

        parameter_4_value = float(self.parameter_4.get())
        parameter_10_value = float(self.parameter_10.get())
        result_b, _, _, _  = self.calculation_b()

        result_e = [(3300+(parameter_9_4/parameter_9_3)*((parameter_9_2/parameter_9_1)**2) + parameter_9_5 * 2) / (1 - (0.38*(parameter_4_value / 100)*(parameter_9_2/parameter_9_1))-(0.26*((parameter_10_value*parameter_9_1)/(result_b[0]))))]
        return result_e, parameter_9_3

    def calculation_f(self):
        _, parameter_9_2 = self.calculation_c() #ignore the second value
        return parameter_9_2

    def calculation_g(self):
        result_e, _= (self.calculation_e())

        result_g = [(result_e[0] - 3300) / result_e[0]]
        return result_g

    def calculation_h(self):
        result_g = self.calculation_g()
        _, parameter_9_3 = self.calculation_e()
        parameter_10_value = float(self.parameter_10.get())

        result_h = [(result_g[0] * 3300) / (parameter_10_value * parameter_9_3)]
        return result_h

    def calculation_i(self):
        result_g = self.calculation_g()
        _, parameter_9_3 = self.calculation_e()

        result_i = [(result_g[0] * 3300) / (parameter_9_3)]
        return result_i


    def parameter_collected(self):


        length_of_section = float(self.new_parameter_11.get())


        result_e, _ = self.calculation_e()

        if self.tick_button_var.get():
            u_oca = float(self.new_parameter_13.get())
        else:
            u_oca = float(result_e[0])


        result_h = self.calculation_h()
        r_ts = float(result_h[0])

        p_fc_tuple = (self.new_parameter_1.get(), self.new_parameter_2.get())

        if p_fc_tuple in [("Cu, YKY", "120"), ("Cu, YKYy", "120")]:
            p_fc = 0.153
        elif p_fc_tuple in [("Cu, YKY", "150"), ("Cu, YKYy", "150")]:
            p_fc = 0.124
        elif p_fc_tuple in [("Cu, YKY", "185"), ("Cu, YKYy", "185")]:
            p_fc = 0.098
        elif p_fc_tuple in [("Cu, YKY", "240"), ("Cu, YKYy", "240")]:
            p_fc = 0.075
        elif p_fc_tuple in [("Cu, YKY", "300"), ("Cu, YKYy", "300")]:
            p_fc = 0.060
        elif p_fc_tuple in [("Cu, YKY", "400"), ("Cu, YKYy", "400")]:
            p_fc = 0.045
        elif p_fc_tuple in [("Cu, YKY", "500"), ("Cu, YKYy", "500")]:
            p_fc = 0.036
        elif p_fc_tuple in [("Cu, YKY", "625"), ("Cu, YKYy", "625")]:
            p_fc = 0.036
        elif p_fc_tuple in [("Cu, YKY", "800"), ("Cu, YKYy", "800")]:
            p_fc = 0.0236
        elif p_fc_tuple in [("Al, YAKY", "120"), ("Al, YAKYy", "120")]:
            p_fc = 0.253
        elif p_fc_tuple in [("Al, YAKY", "150"), ("Al, YAKYy", "150")]:
            p_fc = 0.206
        elif p_fc_tuple in [("Al, YAKY", "185"), ("Al, YAKYy", "185")]:
            p_fc = 0.162
        elif p_fc_tuple in [("Al, YAKY", "240"), ("Al, YAKYy", "240")]:
            p_fc = 0.125
        elif p_fc_tuple in [("Al, YAKY", "300"), ("Al, YAKYy", "300")]:
            p_fc = 0.099
        elif p_fc_tuple in [("Al, YAKY", "400"), ("Al, YAKYy", "400")]:
            p_fc = 0.075
        elif p_fc_tuple in [("Al, YAKY", "500"), ("Al, YAKYy", "500")]:
            p_fc = 0.060
        elif p_fc_tuple in [("Al, YAKY", "625"), ("Al, YAKYy", "625")]:
            p_fc = 0.048
        elif p_fc_tuple in [("Al, YAKY", "800"), ("Al, YAKYy", "800")]:
            p_fc = 0.0375

        p_rc_tuple = (self.new_paramter_1_1.get(), self.new_parameter_3.get())

        if p_rc_tuple in [("Cu, YKY", "120"), ("Cu, YKYy", "120")]:
            p_rc = 0.153
        elif p_rc_tuple in [("Cu, YKY", "150"), ("Cu, YKYy", "150")]:
            p_rc = 0.124
        elif p_rc_tuple in [("Cu, YKY", "185"), ("Cu, YKYy", "185")]:
            p_rc = 0.098
        elif p_rc_tuple in [("Cu, YKY", "240"), ("Cu, YKYy", "240")]:
            p_rc = 0.075
        elif p_rc_tuple in [("Cu, YKY", "300"), ("Cu, YKYy", "300")]:
            p_rc = 0.060
        elif p_rc_tuple in [("Cu, YKY", "400"), ("Cu, YKYy", "400")]:
            p_rc = 0.045
        elif p_rc_tuple in [("Cu, YKY", "500"), ("Cu, YKYy", "500")]:
            p_rc = 0.036
        elif p_rc_tuple in [("Cu, YKY", "625"), ("Cu, YKYy", "625")]:
            p_rc = 0.036
        elif p_rc_tuple in [("Cu, YKY", "800"), ("Cu, YKYy", "800")]:
            p_rc = 0.0236
        elif p_rc_tuple in [("Al, YAKY", "120"), ("Al, YAKYy", "120")]:
            p_rc = 0.253
        elif p_rc_tuple in [("Al, YAKY", "150"), ("Al, YAKYy", "150")]:
            p_rc = 0.206
        elif p_rc_tuple in [("Al, YAKY", "185"), ("Al, YAKYy", "185")]:
            p_rc = 0.162
        elif p_rc_tuple in [("Al, YAKY", "240"), ("Al, YAKYy", "240")]:
            p_rc = 0.125
        elif p_rc_tuple in [("Al, YAKY", "300"), ("Al, YAKYy", "300")]:
            p_rc = 0.099
        elif p_rc_tuple in [("Al, YAKY", "400"), ("Al, YAKYy", "400")]:
            p_rc = 0.075
        elif p_rc_tuple in [("Al, YAKY", "500"), ("Al, YAKYy", "500")]:
            p_rc = 0.060
        elif p_rc_tuple in [("Al, YAKY", "625"), ("Al, YAKYy", "625")]:
            p_rc = 0.048
        elif p_rc_tuple in [("Al, YAKY", "800"), ("Al, YAKYy", "800")]:
            p_rc = 0.0375

        n_fc = float(self.new_parameter_4.get())
        n_rc = float(self.new_parameter_5.get())

        L_fc = float(self.new_parameter_5_1.get())
        L_rc = float(self.new_parameter_5_2.get())

        r_cs = self.new_parameter_6.get()
        if r_cs == "KB70-C":
            r_cs = 0.1230
        elif r_cs == "C70-C":
            r_cs = 0.1136
        elif r_cs == "C95-C":
            r_cs = 0.0985
        elif r_cs == "Fe70-2C":
            r_cs = 0.0961
        elif r_cs == "CuCd70-2C":
            r_cs = 0.0765
        elif r_cs == "KB95-2C, YKB95-2C":
            r_cs = 0.0705
        elif r_cs == "C95-2C, YC95-2C, YpC95-2C":
            r_cs = 0.0662
        elif r_cs == "C150-C150, YC150-C150":
            r_cs = 0.0642
        elif r_cs == "C120-2C, YC1202C, YpC120-2C, YzC120-2C, YSC120-2C, Yws120-2C":
            r_cs = 0.0613
        elif r_cs == "C120-2C150, YC120-2C150":
            r_cs = 0.0470
        elif r_cs == "2C120-2C, 2C120-2C-1, 2C120-2C-2":
            r_cs = 0.0440
        elif r_cs == "C150-2C150":
            r_cs = 0.0435

        r_rs_tuple = (self.new_parameter_7.get(), self.new_parameter_8.get())

        if r_rs_tuple == ("S-49", "Single-track"):
            r_rs = 0.0134
        elif r_rs_tuple == ("S-60", "Single-track"):
            r_rs = 0.0110
        elif r_rs_tuple == ("S-49", "Double-track"):
            r_rs = 0.0067
        elif r_rs_tuple == ("S-60", "Double-track"):
            r_rs = 0.0055

        r_e = float(self.new_parameter_12.get())

        a_fc = float(self.new_parameter_2.get())
        a_rc = float(self.new_parameter_3.get())


        r_fc = float((p_fc * L_fc) / (n_fc * a_fc))

        r_rc = float((p_rc * L_rc) / (n_rc* a_rc))

        i_loco = float(self.new_parameter_10.get())

        return length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, i_loco, a_fc, a_rc


    def train_distance_simulation(self):

        simulation_window = tk.Toplevel(self.window)
        simulation_window.title("Calculation Result")

        simulation_window.geometry("1300x300")

        error_message = tk.Label(simulation_window, text="Error!\nPlease review the input fields carefully and ensure all values are correctly filled out.\nMake sure to use a period for decimals instead of a comma.", font=("Helvetica", 12, "bold"), fg="red")
        # error_message.place(x=450, y=110)
        error_message.pack()

        length_of_section, *_ = self.parameter_collected()
        length_of_section_for_button = int(length_of_section) + 1

        self.canvas = tk.Canvas(simulation_window, width=500, height=100)
        self.canvas.pack()
        self.canvas.create_line(50, 50, 450, 50)  # Top rail
        self.canvas.create_line(50, 70, 450, 70)  # Bottom rail

        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "images/train.png")
        train_img = Image.open(img_path)
        new_width = train_img.width // 8
        new_height = train_img.height // 8
        train_img_resized = train_img.resize((new_width, new_height))
        self.train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(50, 60, image=self.train_img_tk)

        button_frame = tk.Frame(simulation_window)
        button_frame.pack()

        # Create a label for displaying results
        self.result_label = tk.Label(simulation_window, text="")
        self.result_label.pack()

        self.result_label_2 = tk.Label(simulation_window, text="")
        self.result_label_2.pack()

        self.result_label_3 = tk.Label(simulation_window, text="")
        self.result_label_3.pack()

        self.result_label_4 = tk.Label(simulation_window, text="")
        self.result_label_4.pack()

        self.result_label_5 = tk.Label(simulation_window, text="")
        self.result_label_5.pack()


        if self.new_parameter_9.get() == "One-sided":
            for i in range(0, length_of_section_for_button, 1):
                tk.Button(button_frame, text=f"{i}km", command=lambda km=i: (self.show_result(km), self.move_train_to(km))).pack(side=tk.LEFT)
        elif self.new_parameter_9.get() == "Two-sided":
            for i in range(0, length_of_section_for_button, 1):
                tk.Button(button_frame, text=f"{i}km", command=lambda km=i: (self.show_result_2(km), self.move_train_to(km))).pack(side=tk.LEFT)
        elif self.new_parameter_9.get() == "Two-sided with sectioning cabin":
            for i in range(0, length_of_section_for_button, 1):
                tk.Button(button_frame, text=f"{i}km", command=lambda km=i: (self.show_result_3(km), self.move_train_to(km))).pack(side=tk.LEFT)

        error_message.pack_forget()


    def move_train_to(self, km):
        length_of_section, *_ = self.parameter_collected()
        aaa = (400/length_of_section) * km
        x = 50 + aaa # Calculate the x-coordinate for the given distance
        self.canvas.coords(self.train_image, x, 60)  # Move the train image to the new position


    def one_sided_calculation(self, km):
        length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, i_loco, a_fc, a_rc = self.parameter_collected()

        length_of_section = float(length_of_section)
        # Ensure km is a float
        km = float(km)

        r_rc = float(r_rc)
        r_fc = float(r_fc)

        # Convert u_oca and r_ts back to float for calculation
        u_a = u_oca - ((r_ts) * i_loco)


        u_p = u_oca - (((r_ts + r_fc + ((r_cs + ((r_rs * r_e)/(r_rs + r_e))) * km) + r_rc)) * i_loco)

        return u_a, u_p

    def two_sided_calculation(self, km):
        length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, i_loco, a_fc, a_rc = self.parameter_collected()

        R_ts = r_ts + r_fc + r_rc
        R_crs = r_cs + ((r_rs * r_e) / (r_rs + r_e))

        U_p = ((u_oca / (R_ts + R_crs * km)) - i_loco + (u_oca / (R_ts + R_crs * (length_of_section - km)))) / (( 1 / (R_ts + R_crs * km)) + (1 / (R_ts + R_crs * (length_of_section - km))))

        I_a = ((0 - U_p + u_oca) / (R_ts + (R_crs * km)))
        I_b = ((0 - U_p + u_oca) / (R_ts + (R_crs * (length_of_section - km))))

        u_a = u_oca - ((r_ts) * I_a)
        u_b = u_oca - ((r_ts) * I_b)

        return U_p, I_a, I_b, R_ts, R_crs, u_a, u_b

    def sectioning_cabin_calculation(self, km):
        length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, i_loco, a_fc, a_rc = self.parameter_collected()

        if km <= (0.5 * length_of_section):
            km = float(km)
        else:
            km = length_of_section - km

        R_Ad = (r_fc + (r_cs * 0.5 * length_of_section))
        R_B = (r_ts + ((r_fc +r_cs * 0.5 * length_of_section) / 2) + (r_rc / 2) + (r_rc / 2) + ((r_rs * r_e * 0.5 * length_of_section) / (2 * (r_rs + r_e))))
        R_TSrca = (r_ts + (r_rc / 2))
        R_rs = ((r_rs * r_e) / ((r_rs + r_e)*2))

        R_11 = R_Ad + r_fc + r_cs * (0.5 * length_of_section)
        R_22 = (r_fc + (r_cs * (0.5 * length_of_section)) + R_B + (r_rs *(0.5 * length_of_section)) + R_TSrca)
        R_12 = r_fc + (r_cs * (0.5 * length_of_section))
        R_21 = R_12
        R_13 = r_cs * ((0.5 * length_of_section) - km)
        R_23 = R_B + ((r_cs + r_rs) * ((0.5 * length_of_section) - km))
        E_11 = 0
        E_22 = 0
        i_33 = float(i_loco)

        det_matrix = (R_11 * R_22) - ((-R_12) * (-R_21))
        det_matrix_1 = (((-R_13)*i_33)*R_22) - ((-R_12)*(R_23*i_33))
        det_matrix_2 = (R_11 * (R_23*i_33)) - ((-R_21)*((-R_13)*i_33))

        i_11 = det_matrix_1 / det_matrix
        i_22 = det_matrix_2 / det_matrix

        i_a = i_22
        i_b = i_33 - i_22

        i_ad = i_11

        i_au1 = i_22 - i_11
        i_au2 = i_11 - i_22 + i_33

        i_bd = i_b / 2
        i_bu = i_bd


        u_p = (-i_a) * ((r_rs * km)+ R_TSrca) + u_oca - (i_au1 * (r_fc + r_cs * km))



        u_a = u_oca - (r_ts * i_a)
        u_b = u_oca - (r_ts * i_b)

        return u_p, i_a, i_b, u_a, u_b


    def show_result(self, km):
        # Update the text of the existing label instead of creating a new one
        u_a, u_p= self.one_sided_calculation(km)

        u_a = round(u_a, 2)
        u_p = round(u_p, 2)

        self.result_label.config(text=f"Output voltage of traction substation Ua: {u_a} V at {km} km")
        self.result_label_2.config(text=f"Volatge of the pantograph Up: {u_p} V at {km} km")

    def show_result_2(self, km):
        U_p, I_a, I_b, R_ts, R_crs, u_a, u_b = self.two_sided_calculation(km)

        U_p = round(U_p, 2)
        I_a = round(I_a, 2)
        I_b = round(I_b, 2)
        u_a = round(u_a, 2)
        u_b = round(u_b, 2)

        self.result_label.config(text=f"Voltage of the pantograph Up: {U_p} V at {km} km")
        self.result_label_2.config(text=f"Current at the start of the section Ia: {I_a} A")
        self.result_label_3.config(text=f"Current at the end of the section Ib: {I_b} A")
        self.result_label_4.config(text=f"Voltage at the start of the section Va: {u_a} V")
        self.result_label_5.config(text=f"Voltage at the end of the section Vb: {u_b} V")

    def show_result_3(self, km):
        u_p, i_a, i_b, u_a, u_b = self.sectioning_cabin_calculation(km)

        u_p = round(u_p, 2)
        i_a = round(i_a, 2)
        i_b = round(i_b, 2)
        u_a = round(u_a, 2)
        u_b = round(u_b, 2)

        self.result_label.config(text=f"Voltage of the pantograph Up: {u_p} V at {km} km")
        self.result_label_2.config(text=f"Current at the start of the section Ia: {i_a} A")
        self.result_label_3.config(text=f"Current at the end of the section Ib: {i_b} A")
        self.result_label_4.config(text=f"Voltage at the start of the section Va: {u_a} V")
        self.result_label_5.config(text=f"Voltage at the end of the section Vb: {u_b} V")









class PageForShortCircuit:
    def __init__(self, type_of_calculation):
        self.window = tk.Tk()
        self.window.title("Main railway 3kV DC - Short-circuit")
        self.window.geometry("1400x800")
        self.type_of_calculation = type_of_calculation
        self.type_of_calculations = tk.StringVar(value="Type of Calculation")
        self.parameter_1 = tk.StringVar(value="Rated voltage on the HV side (kV)")
        self.parameter_2 = tk.StringVar(value="Short-circuit power of the power supply system on the HV side (MVA)")
        self.parameter_3 = tk.StringVar(value="rated power of the HV/MV transformer (MVA)")
        self.parameter_4 = tk.StringVar(value="Percentage short-circuit voltage of the MV/LV transformer (%)")
        self.parameter_5 = tk.StringVar(value="Rated voltage on the MV side (kV)")
        self.parameter_6_1 = tk.StringVar(value="Type and cross-section of the MV line")
        self.parameter_6_2 = tk.StringVar(value="Type of MV line")
        self.parameter_6_3 = tk.StringVar(value="Cross-section of the MV line (mm^2)")
        self.parameter_7 = tk.StringVar(value="Length of the MV line (km)")
        self.parameter_8 = tk.StringVar(value="Unit reactance of the MV line (Ω/km)")
        self.parameter_9 = tk.StringVar(value="Type of rectifier unit")
        self.parameter_10 = tk.StringVar(value="Number of rectifier units")
        self.new_parameter_1 = tk.StringVar(value="Type & material")
        self.new_paramter_1_1 = tk.StringVar(value="Type & material2")
        self.new_parameter_2 = tk.StringVar(value="Cross-section (mm^2)1")
        self.new_parameter_3 = tk.StringVar(value="Cross-section (mm^2)2")
        self.new_parameter_4 = tk.StringVar(value="Number of wires1")
        self.new_parameter_5 = tk.StringVar(value="Number of wires2")
        self.new_parameter_5_1 = tk.StringVar(value="Length of the section1")
        self.new_parameter_5_2 = tk.StringVar(value="Length of the section2")
        self.new_parameter_6 = tk.StringVar(value="Catenary system type")
        self.new_parameter_7 = tk.StringVar(value="Rails type")
        self.new_parameter_8 = tk.StringVar(value="Number of tracks")
        self.new_parameter_9 = tk.StringVar(value="Type of traction power supply")
        self.new_parameter_10 = tk.StringVar(value="Locomotive current")
        self.new_parameter_11 = tk.StringVar(value="Length of the section")
        self.new_parameter_12 = tk.StringVar(value="Ground earth resistance")
        self.create_page()

    def create_page(self):
        self.canvas = tk.Canvas(self.window, width=1200, height=230)
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=15)

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 1.8
        new_height = train_img.height // 1.8
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk

        # Create a Frame for each
        self.main_label1 = tk.Label(self.window, text="HV line", font=("Helvetica", 12, "bold"))
        self.main_label1.grid(row=3, column=0, padx=10, pady=10)
        self.frame1 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame1.grid(row=4, column=0, padx=10, pady=10)
        label1 = tk.Label(self.frame1, text="Rated voltage\non the HV side (kV)")
        label1.pack()
        self.parameter_1.set("Choose")
        option_menu1 = tk.OptionMenu(self.frame1, self.parameter_1, "110")
        option_menu1.pack()

        self.main_label2 = tk.Label(self.window, text="PCC Transformer", font=("Helvetica", 12, "bold"))
        self.main_label2.grid(row=3, column=1, padx=10, pady=10)
        self.frame2 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame2.grid(row=4, column=1, padx=10, pady=10)
        label2 = tk.Label(self.frame2, text="Short-circuit power of the power\nsupply system on the HV side (MVA)")
        label2.pack()
        self.parameter_2.set("")
        entry2 = tk.Entry(self.frame2, textvariable=self.parameter_2)
        entry2.pack()

        self.frame3 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame3.grid(row=5, column=1, padx=10, pady=10)
        label3 = tk.Label(self.frame3, text="Rated power of the\nHV/MV transformer (MVA)")
        label3.pack()
        self.parameter_3.set("Choose")
        option_menu3 = tk.OptionMenu(self.frame3, self.parameter_3, "40", "32", "25", "20", "16", "10", "6")
        option_menu3.pack()

        self.frame4 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame4.grid(row=6, column=1, padx=10, pady=10)
        label4 = tk.Label(self.frame4, text="Percentage short-circuit voltage\nof the MV/LV transformer (%)")
        label4.pack()
        self.parameter_4.set("")
        entry4 = tk.Entry(self.frame4, textvariable=self.parameter_4)
        entry4.pack()

        self.frame5 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame5.grid(row=7, column=1, padx=10, pady=10)
        label5 = tk.Label(self.frame5, text="Rated voltage on the MV side (kV)")
        label5.pack()
        self.parameter_5.set("Choose")
        option_menu5 = tk.OptionMenu(self.frame5, self.parameter_5, "30", "20", "15")
        option_menu5.pack()

        self.main_label3 = tk.Label(self.window, text="MV line", font=("Helvetica", 12, "bold"))
        self.main_label3.grid(row=3, column=2, padx=10, pady=10)
        self.frame6 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame6.grid(row=4, column=2, padx=10, pady=10)
        label6 = tk.Label(self.frame6, text="Type of the MV line")
        label6.pack()
        self.parameter_6_1.set("Choose")
        option_menu6 = tk.OptionMenu(self.frame6, self.parameter_6_1, "Cu cable", "Al cable", "Overhead AFL-6")
        option_menu6.pack()

        self.frame7 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame7.grid(row=5, column=2, padx=10, pady=10)
        label7 = tk.Label(self.frame7, text="Cross-section of the MV line (mm^2)")
        label7.pack()
        self.parameter_6_2.set("Choose")
        option_menu7 = tk.OptionMenu(self.frame7, self.parameter_6_2, "3x120", "3x150", "3x185", "3x240", "3x300", "3x70", "3x95")
        option_menu7.pack()

        self.frame8 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame8.grid(row=6, column=2, padx=10, pady=10)
        label8 = tk.Label(self.frame8, text="Length of the MV line (km)")
        label8.pack()
        self.parameter_7.set("")
        entry8 = tk.Entry(self.frame8, textvariable=self.parameter_7)
        entry8.pack()

        self.main_label4 = tk.Label(self.window, text="Rectifier unit", font=("Helvetica", 12, "bold"))
        self.main_label4.grid(row=3, column=3, padx=10, pady=10)
        self.frame9 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame9.grid(row=4, column=3, padx=10, pady=10)
        label9 = tk.Label(self.frame9, text="Unit reactance of the MV line (Ω/km)")
        label9.pack()
        self.parameter_8.set("")
        entry9 = tk.Entry(self.frame9, textvariable=self.parameter_8)
        entry9.pack()

        self.frame10 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame10.grid(row=5, column=3, padx=10, pady=10)
        label10 = tk.Label(self.frame10, text="Type of the rectifier unit")
        label10.pack()
        self.parameter_9.set("Choose")
        option_menu10 = tk.OptionMenu(self.frame10, self.parameter_9, "PD17", "PD1.7", "PD16", "PD12", "PK17")
        option_menu10.pack()

        self.frame11 = tk.Frame(self.window, bd=2, relief="groove")
        self.frame11.grid(row=6, column=3, padx=10, pady=10)
        label11 = tk.Label(self.frame11, text="Number of the rectifier units")
        label11.pack()
        self.parameter_10.set("Choose")
        option_menu11 = tk.OptionMenu(self.frame11, self.parameter_10, "1", "2", "3", "4", "5")
        option_menu11.pack()
        #Calculate button
        tk.Button(self.window, text="Calculate", command=self.train_distance_simulation).place(x=550, y=640)
        #Go back button
        tk.Button(self.window, text="Go back", command=self.go_back).place(x=553, y=720)

        self.arrow_button = tk.Button(self.window, text="→", command=self.show_new_parameters, height=3, font=('Helvetica', '16'))
        self.arrow_button.place(x=1110, y=300)  # Example coordinates

        self.arrow_button1 = tk.Button(self.window, text="←", command=self.untoggle_parameters, height=3, font=('Helvetica', '16'))
        self.arrow_button1.place(x=1060, y=300)  # Example coordinates
        self.arrow_button1.config(state="disabled")

        # Keep track of the current state
        self.parameters_visible = True

    def go_back(self):
        self.window.destroy()
        app = Application()
        app.run()

    def run(self):
        self.window.mainloop()

    def toggle_parameters(self):
        if self.parameters_visible:
            # Hide current parameters
            self.hide_parameters()
        else:
            # Show new parameters
            self.show_new_parameters()
        self.parameters_visible = not self.parameters_visible

    def hide_parameters(self):

        self.canvas.delete(self.train_image)

        # Example of hiding a frame
        self.frame1.grid_forget()
        self.frame2.grid_forget()
        self.frame3.grid_forget()
        self.frame4.grid_forget()
        self.frame5.grid_forget()
        self.frame6.grid_forget()
        self.frame7.grid_forget()
        self.frame8.grid_forget()
        self.frame9.grid_forget()
        self.frame10.grid_forget()
        self.frame11.grid_forget()
        self.main_label1.grid_forget()
        self.main_label2.grid_forget()
        self.main_label3.grid_forget()
        self.main_label4.grid_forget()
        # Repeat for all frames you want to hide

    def show_new_parameters(self):
        # First, hide existing parameters if they are visible
        self.hide_parameters()

        self.arrow_button.config(state="disabled")
        self.arrow_button1.config(state="normal")

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS2.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 3.5
        new_height = train_img.height // 3.5
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk

        # Create and show new parameters
        # First table
        self.group_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.group_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.new_main_label1 = tk.Label(self.group_frame, text="Feeder Cable")
        self.new_main_label1.grid(row=4, column=1, padx=10, pady=10)

        self.new_main_label2 = tk.Label(self.group_frame, text="Return Cable")
        self.new_main_label2.grid(row=5, column=1, padx=10, pady=10)

        self.new_main_label3 = tk.Label(self.group_frame, text="Type & Material")
        self.new_main_label3.grid(row=3, column=2, padx=10, pady=10)

        self.new_main_label4 = tk.Label(self.group_frame, text="Cross-section (mm^2)")
        self.new_main_label4.grid(row=3, column=3, padx=10, pady=10)

        self.new_main_label5 = tk.Label(self.group_frame, text="Number of wires")
        self.new_main_label5.grid(row=3, column=4, padx=10, pady=10)

        self.new_main_label5_1 = tk.Label(self.group_frame, text="Length of the cable (m)")
        self.new_main_label5_1.grid(row=3, column=5, padx=10, pady=10)

        self.new_parameter_1.set("Choose")
        self.new_option_menu1 = tk.OptionMenu(self.group_frame, self.new_parameter_1, "Cu, YKY", "Cu, YKYy", "Al, YAKY", "Al, YAKYy")
        self.new_option_menu1.grid(row=4, column=2, padx=10, pady=10)

        self.new_paramter_1_1.set("Choose")
        self.new_option_menu1_1 = tk.OptionMenu(self.group_frame, self.new_paramter_1_1, "Cu, YKY", "Cu, YKYy", "Al, YAKY", "Al, YAKYy")
        self.new_option_menu1_1.grid(row=5, column=2, padx=10, pady=10)

        self.new_parameter_2.set("Choose")
        self.new_entry1 = tk.OptionMenu(self.group_frame, self.new_parameter_2, "120", "150", "185", "240", "300", "400", "500", "625", "800")
        self.new_entry1.grid(row=4, column=3, padx=10, pady=10)

        self.new_parameter_3.set("Choose")
        self.new_entry2 = tk.OptionMenu(self.group_frame, self.new_parameter_3, "120", "150", "185", "240", "300", "400", "500", "625", "800")
        self.new_entry2.grid(row=5, column=3, padx=10, pady=10)

        self.new_parameter_4.set("")
        self.new_entry3 = tk.Entry(self.group_frame, textvariable=self.new_parameter_4)
        self.new_entry3.grid(row=4, column=4, padx=10, pady=10)

        self.new_parameter_5.set("")
        self.new_entry4 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5)
        self.new_entry4.grid(row=5, column=4, padx=10, pady=10)

        self.new_parameter_5_1.set("")
        self.new_entry4_1 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5_1)
        self.new_entry4_1.grid(row=4, column=5, padx=10, pady=10)

        self.new_parameter_5_2.set("")
        self.new_entry4_2 = tk.Entry(self.group_frame, textvariable=self.new_parameter_5_2)
        self.new_entry4_2.grid(row=5, column=5, padx=10, pady=10)


        # Second table
        self.group_frame1 = tk.Frame(self.window, bd=2, relief="groove")
        self.group_frame1.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.new_main_label6 = tk.Label(self.group_frame1, text="Catenary system type")
        self.new_main_label6.grid(row=7, column=0, padx=10, pady=10)

        self.new_main_label7 = tk.Label(self.group_frame1, text="Rails type")
        self.new_main_label7.grid(row=8, column=0, padx=10, pady=10)

        self.new_main_label8 = tk.Label(self.group_frame1, text="Number of tracks")
        self.new_main_label8.grid(row=9, column=0, padx=10, pady=10)

        self.new_main_label9 = tk.Label(self.group_frame1, text="Ground earth resistance (Ω/km)")
        self.new_main_label9.grid(row=10, column=0, padx=10, pady=10)

        # self.new_main_label9 = tk.Label(self.group_frame1, text="Type")
        # self.new_main_label9.grid(row=6, column=1, padx=10, pady=10)

        self.new_parameter_6.set("Choose")
        self.new_option_menu2 = tk.OptionMenu(self.group_frame1, self.new_parameter_6, "KB70-C", "C70-C", "C95-C", "Fe70-2C", "CuCd70-2C", "KB95-2C, YKB95-2C", "C95-2C, YC95-2C, YpC95-2C", "C150-C150, YC150-C150", "C120-2C, YC1202C, YpC120-2C, YzC120-2C, YSC120-2C, Yws120-2C", "C120-2C150, YC120-2C150", "2C120-2C, 2C120-2C-1, 2C120-2C-2", "C150-2C150")
        self.new_option_menu2.grid(row=7, column=1, padx=10, pady=10)
        self.new_option_menu2.config(width=55)

        self.new_parameter_7.set("Choose")
        self.new_option_menu3 = tk.OptionMenu(self.group_frame1, self.new_parameter_7, "S-49", "S-60")
        self.new_option_menu3.grid(row=8, column=1, padx=10, pady=10)

        self.new_parameter_8.set("Choose")
        self.new_option_menu4 = tk.OptionMenu(self.group_frame1, self.new_parameter_8, "Single-track", "Double-track")
        self.new_option_menu4.grid(row=9, column=1, padx=10, pady=10)

        self.new_parameter_12.set("")
        self.new_entry5 = tk.Entry(self.group_frame1, textvariable=self.new_parameter_12)
        self.new_entry5.grid(row=10, column=1, padx=10, pady=10)



        # Create a single frame to hold all elements
        self.combined_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.combined_frame.grid(row=6, column=2, columnspan=4, padx=10, pady=10, rowspan=3)  # Adjust rowspan as needed to fit all elements

        # Third table elements
        self.new_main_label10 = tk.Label(self.combined_frame, text="Type of traction power supply", state='disabled')
        self.new_main_label10.grid(row=0, column=0, padx=10, pady=10)  # Adjust grid positions as needed
        self.new_main_label10.config(fg="gray")  # Change text color to gray to indicate disabled

        self.new_parameter_9.set("Choose")
        self.new_option_menu5 = tk.OptionMenu(self.combined_frame, self.new_parameter_9, "One-sided", "Two-sided", "Two-sided with sectioning cabin")
        self.new_option_menu5.grid(row=0, column=1, padx=10, pady=10)
        self.new_option_menu5.config(width=23, state='disabled')  # Disable option menu

        self.new_main_label11 = tk.Label(self.combined_frame, text="Locomotive current (A)", state='disabled')
        self.new_main_label11.grid(row=1, column=0, padx=10, pady=10)  # Adjust grid positions as needed
        self.new_main_label11.config(fg="gray")  # Change text color to gray to indicate disabled

        self.new_parameter_10.set("")
        self.new_option_menu6 = tk.Entry(self.combined_frame, textvariable=self.new_parameter_10, state='disabled')
        self.new_option_menu6.grid(row=1, column=1, padx=10, pady=10)

        self.new_main_label12 = tk.Label(self.combined_frame, text="Length of the section (km)")
        self.new_main_label12.grid(row=2, column=0, padx=10, pady=10)  # Adjust grid positions as needed

        self.new_parameter_11.set("")
        self.new_option_menu7 = tk.Entry(self.combined_frame, textvariable=self.new_parameter_11)
        self.new_option_menu7.grid(row=2, column=1, padx=10, pady=10)
        # Continue adding other UI elements as needed
        # Remember to update the toggle or visibility state as appropriate

    def toggle_existing_new_parameters(self):
        self.hide_parameters()

        self.arrow_button.config(state="disabled")
        self.arrow_button1.config(state="normal")

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS2.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 3.5
        new_height = train_img.height // 3.5
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk

        self.group_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.group_frame1.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.combined_frame.grid(row=6, column=2, columnspan=4, padx=10, pady=10, rowspan=3)  # Adjust grid positions as needed

    def untoggle_parameters(self):

        # Disable the left arrow button
        self.arrow_button1.config(state='disabled')
        # Enable the right arrow button
        self.arrow_button.config(state='normal', command=self.toggle_existing_new_parameters)

        self.canvas.delete(self.train_image)

        self.group_frame.grid_forget()
        self.group_frame1.grid_forget()
        self.combined_frame.grid_forget()

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        img_path = os.path.join(script_dir, "images/TS.png")  # Join the directory of the script with the image filename

        train_img = Image.open(img_path)
        new_width = train_img.width // 1.8
        new_height = train_img.height // 1.8
        train_img_resized = train_img.resize((int(new_width), int(new_height)))
        train_img_tk = ImageTk.PhotoImage(train_img_resized)
        self.train_image = self.canvas.create_image(600, 120, image=train_img_tk)

        # Store the image in a global variable to prevent it from being garbage collected
        global _image
        _image = train_img_tk


        # Show the previously hidden frames and labels
        self.frame1.grid(row=4, column=0, padx=10, pady=10)
        self.frame2.grid(row=4, column=1, padx=10, pady=10)
        self.frame3.grid(row=5, column=1, padx=10, pady=10)
        self.frame4.grid(row=6, column=1, padx=10, pady=10)
        self.frame5.grid(row=7, column=1, padx=10, pady=10)
        self.frame6.grid(row=4, column=2, padx=10, pady=10)
        self.frame7.grid(row=5, column=2, padx=10, pady=10)
        self.frame8.grid(row=6, column=2, padx=10, pady=10)
        self.frame9.grid(row=4, column=3, padx=10, pady=10)
        self.frame10.grid(row=5, column=3, padx=10, pady=10)
        self.frame11.grid(row=6, column=3, padx=10, pady=10)
        self.main_label1.grid(row=3, column=0, padx=10, pady=10)
        self.main_label2.grid(row=3, column=1, padx=10, pady=10)
        self.main_label3.grid(row=3, column=2, padx=10, pady=10)
        self.main_label4.grid(row=3, column=3, padx=10, pady=10)
        # Update the visibility state
        self.parameters_visible = True

    # Calculation algorithm
    def calculation_a(self):
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
        else:
            parameter_9_1 = 4400000
        parameter_10_value = float(self.parameter_10.get())
        parameter_5_value = float(self.parameter_5.get())
        result_a = [(parameter_9_1 * parameter_10_value) / (math.sqrt(3) * (parameter_5_value * 1000))]
        return result_a

    def calculation_b(self):
        parameter_2_value = float(self.parameter_2.get())
        parameter_3_value = float(self.parameter_3.get())
        parameter_4_value = float(self.parameter_4.get())
        parameter_5_value = float(self.parameter_5.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_7_value = float(self.parameter_7.get())

        result_b_1 = (1.1 * ((parameter_5_value)**2)) / (parameter_2_value)
        result_b_2 = (parameter_4_value / 100) * ((parameter_5_value**2) / parameter_3_value)
        result_b_3 = (parameter_8_value) * (parameter_7_value)
        result_b = (1.1 * ((parameter_5_value * 1000)**2)) / (result_b_1 + result_b_2 + result_b_3)

        return [result_b], [result_b_1], [result_b_2], [result_b_3]

    def calculation_c(self):
        parameter_9_2 = 0 #initial default value
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD1.7":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD16":
            parameter_9_2 = 5280000
        elif parameter_9_value == "PD12":
            parameter_9_2 =  3960000
        elif parameter_9_value == "PK17":
            parameter_9_2 = 2475000

        parameter_10_value = float(self.parameter_10.get())
        parameter_7_value = float(self.parameter_7.get())
        parameter_8_value = float(self.parameter_8.get())
        parameter_5_value = float(self.parameter_5.get())

        #Resistance of wires and load currents for overhead lines
        parameter_6 = 0 #initial default value
        parameter_6_1_value = self.parameter_6_1.get()
        parameter_6_2_value = self.parameter_6_2.get()
        if parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.153
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.124
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.099
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.075
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.060
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.258
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.253
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.205
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.164
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.125
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.1
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.443
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.32
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x120":
            parameter_6 = 0.234
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x150":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x185":
            parameter_6 = 0.156
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x240":
            parameter_6 = 0.137
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x300":
            parameter_6 = 0.121

        result_c = [((parameter_9_2 * 2 * parameter_10_value) / ((math.sqrt(3)) * (parameter_5_value * 1000) * 0.95)) * (parameter_7_value * ((parameter_6 * 0.95) + (parameter_8_value * math.sqrt(1-0.95*0.95))))]
        return result_c, parameter_9_2

    def calculation_d(self):
        result_c, _ = self.calculation_c() #ignore the second value]
        parameter_5_value = float(self.parameter_5.get())
        result_d = [((math.sqrt(3) * result_c[0]) / (parameter_5_value * 1000)) * 100]
        return result_d

    def calculation_e(self):
        parameter_9_value = self.parameter_9.get()
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 53500
            parameter_9_5 = 3
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 38000
            parameter_9_5 = 3
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
            parameter_9_2 = 5280000
            parameter_9_3 = 1600
            parameter_9_4 = 46000
            parameter_9_5 = 3
        elif parameter_9_value == "PD12":
            parameter_9_1 = 5850000
            parameter_9_2 = 3960000
            parameter_9_3 = 1200
            parameter_9_4 = 36000
            parameter_9_5 = 3
        elif parameter_9_value == "PK17":
            parameter_9_1 = 5850000
            parameter_9_2 = 2475000
            parameter_9_3 = 750
            parameter_9_4 = 36000
            parameter_9_5 = 8

        parameter_4_value = float(self.parameter_4.get())
        parameter_10_value = float(self.parameter_10.get())
        result_b, _, _, _  = self.calculation_b()

        result_e = [(3300+(parameter_9_4/parameter_9_3)*((parameter_9_2/parameter_9_1)**2) + parameter_9_5 * 2) / (1 - (0.38*(parameter_4_value / 100)*(parameter_9_2/parameter_9_1))-(0.26*((parameter_10_value*parameter_9_1)/(result_b[0]))))]
        return result_e, parameter_9_3

    def calculation_f(self):
        _, parameter_9_2 = self.calculation_c() #ignore the second value
        return parameter_9_2

    def calculation_g(self):
        result_e, _= (self.calculation_e())

        result_g = [(result_e[0] - 3300) / result_e[0]]
        return result_g

    def calculation_h(self):
        result_g = self.calculation_g()
        _, parameter_9_3 = self.calculation_e()
        parameter_10_value = float(self.parameter_10.get())

        result_h = [(result_g[0] * 3300) / (parameter_10_value * parameter_9_3)]
        return result_h

    def calculation_i(self):
        result_g = self.calculation_g()
        _, parameter_9_3 = self.calculation_e()

        result_i = [(result_g[0] * 3300) / (parameter_9_3)]
        return result_i


    def parameter_collected(self):

        length_of_section = float(self.new_parameter_11.get())

        result_e, _ = self.calculation_e()  # Call calculation_e to get result_e and ignore the second return value
        u_oca = float(result_e[0])  # result_e is a list, so we take the first element if you're expecting a single value
        # Continue with the rest of your method using u_oca as needed

        result_h = self.calculation_h()
        r_ts = float(result_h[0])

        p_fc_tuple = (self.new_parameter_1.get(), self.new_parameter_2.get())

        if p_fc_tuple in [("Cu, YKY", "120"), ("Cu, YKYy", "120")]:
            p_fc = 0.153
        elif p_fc_tuple in [("Cu, YKY", "150"), ("Cu, YKYy", "150")]:
            p_fc = 0.124
        elif p_fc_tuple in [("Cu, YKY", "185"), ("Cu, YKYy", "185")]:
            p_fc = 0.098
        elif p_fc_tuple in [("Cu, YKY", "240"), ("Cu, YKYy", "240")]:
            p_fc = 0.075
        elif p_fc_tuple in [("Cu, YKY", "300"), ("Cu, YKYy", "300")]:
            p_fc = 0.060
        elif p_fc_tuple in [("Cu, YKY", "400"), ("Cu, YKYy", "400")]:
            p_fc = 0.045
        elif p_fc_tuple in [("Cu, YKY", "500"), ("Cu, YKYy", "500")]:
            p_fc = 0.036
        elif p_fc_tuple in [("Cu, YKY", "625"), ("Cu, YKYy", "625")]:
            p_fc = 0.036
        elif p_fc_tuple in [("Cu, YKY", "800"), ("Cu, YKYy", "800")]:
            p_fc = 0.0236
        elif p_fc_tuple in [("Al, YAKY", "120"), ("Al, YAKYy", "120")]:
            p_fc = 0.253
        elif p_fc_tuple in [("Al, YAKY", "150"), ("Al, YAKYy", "150")]:
            p_fc = 0.206
        elif p_fc_tuple in [("Al, YAKY", "185"), ("Al, YAKYy", "185")]:
            p_fc = 0.162
        elif p_fc_tuple in [("Al, YAKY", "240"), ("Al, YAKYy", "240")]:
            p_fc = 0.125
        elif p_fc_tuple in [("Al, YAKY", "300"), ("Al, YAKYy", "300")]:
            p_fc = 0.099
        elif p_fc_tuple in [("Al, YAKY", "400"), ("Al, YAKYy", "400")]:
            p_fc = 0.075
        elif p_fc_tuple in [("Al, YAKY", "500"), ("Al, YAKYy", "500")]:
            p_fc = 0.060
        elif p_fc_tuple in [("Al, YAKY", "625"), ("Al, YAKYy", "625")]:
            p_fc = 0.048
        elif p_fc_tuple in [("Al, YAKY", "800"), ("Al, YAKYy", "800")]:
            p_fc = 0.0375

        p_rc_tuple = (self.new_paramter_1_1.get(), self.new_parameter_3.get())

        if p_rc_tuple in [("Cu, YKY", "120"), ("Cu, YKYy", "120")]:
            p_rc = 0.153
        elif p_rc_tuple in [("Cu, YKY", "150"), ("Cu, YKYy", "150")]:
            p_rc = 0.124
        elif p_rc_tuple in [("Cu, YKY", "185"), ("Cu, YKYy", "185")]:
            p_rc = 0.098
        elif p_rc_tuple in [("Cu, YKY", "240"), ("Cu, YKYy", "240")]:
            p_rc = 0.075
        elif p_rc_tuple in [("Cu, YKY", "300"), ("Cu, YKYy", "300")]:
            p_rc = 0.060
        elif p_rc_tuple in [("Cu, YKY", "400"), ("Cu, YKYy", "400")]:
            p_rc = 0.045
        elif p_rc_tuple in [("Cu, YKY", "500"), ("Cu, YKYy", "500")]:
            p_rc = 0.036
        elif p_rc_tuple in [("Cu, YKY", "625"), ("Cu, YKYy", "625")]:
            p_rc = 0.036
        elif p_rc_tuple in [("Cu, YKY", "800"), ("Cu, YKYy", "800")]:
            p_rc = 0.0236
        elif p_rc_tuple in [("Al, YAKY", "120"), ("Al, YAKYy", "120")]:
            p_rc = 0.253
        elif p_rc_tuple in [("Al, YAKY", "150"), ("Al, YAKYy", "150")]:
            p_rc = 0.206
        elif p_rc_tuple in [("Al, YAKY", "185"), ("Al, YAKYy", "185")]:
            p_rc = 0.162
        elif p_rc_tuple in [("Al, YAKY", "240"), ("Al, YAKYy", "240")]:
            p_rc = 0.125
        elif p_rc_tuple in [("Al, YAKY", "300"), ("Al, YAKYy", "300")]:
            p_rc = 0.099
        elif p_rc_tuple in [("Al, YAKY", "400"), ("Al, YAKYy", "400")]:
            p_rc = 0.075
        elif p_rc_tuple in [("Al, YAKY", "500"), ("Al, YAKYy", "500")]:
            p_rc = 0.060
        elif p_rc_tuple in [("Al, YAKY", "625"), ("Al, YAKYy", "625")]:
            p_rc = 0.048
        elif p_rc_tuple in [("Al, YAKY", "800"), ("Al, YAKYy", "800")]:
            p_rc = 0.0375

        n_fc = float(self.new_parameter_4.get())
        n_rc = float(self.new_parameter_5.get())

        L_fc = float(self.new_parameter_5_1.get())
        L_rc = float(self.new_parameter_5_2.get())

        r_cs = self.new_parameter_6.get()
        if r_cs == "KB70-C":
            r_cs = 0.1230
        elif r_cs == "C70-C":
            r_cs = 0.1136
        elif r_cs == "C95-C":
            r_cs = 0.0985
        elif r_cs == "Fe70-2C":
            r_cs = 0.0961
        elif r_cs == "CuCd70-2C":
            r_cs = 0.0765
        elif r_cs == "KB95-2C, YKB95-2C":
            r_cs = 0.0705
        elif r_cs == "C95-2C, YC95-2C, YpC95-2C":
            r_cs = 0.0662
        elif r_cs == "C150-C150, YC150-C150":
            r_cs = 0.0642
        elif r_cs == "C120-2C, YC1202C, YpC120-2C, YzC120-2C, YSC120-2C, Yws120-2C":
            r_cs = 0.0613
        elif r_cs == "C120-2C150, YC120-2C150":
            r_cs = 0.0470
        elif r_cs == "2C120-2C, 2C120-2C-1, 2C120-2C-2":
            r_cs = 0.0440
        elif r_cs == "C150-2C150":
            r_cs = 0.0435

        r_rs_tuple = (self.new_parameter_7.get(), self.new_parameter_8.get())

        if r_rs_tuple == ("S-49", "Single-track"):
            r_rs = 0.0134
        elif r_rs_tuple == ("S-60", "Single-track"):
            r_rs = 0.0110
        elif r_rs_tuple == ("S-49", "Double-track"):
            r_rs = 0.0067
        elif r_rs_tuple == ("S-60", "Double-track"):
            r_rs = 0.0055

        r_e = float(self.new_parameter_12.get())

        a_fc = float(self.new_parameter_2.get())
        a_rc = float(self.new_parameter_3.get())


        r_fc = float((p_fc * L_fc) / (n_fc * a_fc))

        r_rc = float((p_rc * L_rc) / (n_rc* a_rc))





        return length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, a_fc, a_rc

    def train_distance_simulation(self):
        simulation_window = tk.Toplevel(self.window)
        simulation_window.title("Calculation Result")
        simulation_window.geometry("500x100")

        error_message = tk.Label(simulation_window, text="Error, Please review the input fields carefully!\nMake sure to use a period for decimals instead of a comma.", font=("Helvetica", 12, "bold"), fg="red")
        error_message.pack()
        # img_dir = os.getcwd()
        # train_img = Image.open(os.path.join(img_dir, "train.png"))
        # new_width = train_img.width // 8
        # new_height = train_img.height // 8
        # train_img_resized = train_img.resize((new_width, new_height))
        # self.train_img_tk = ImageTk.PhotoImage(train_img_resized)
        # self.train_image = self.canvas.create_image(50, 60, image=self.train_img_tk)


        i_max, i_zw13, i_zw12, i_zw1 = self.short_circuit_calculation()

        i_max = round(i_max, 2)
        i_zw13 = round(i_zw13, 2)
        i_zw12 = round(i_zw12, 2)
        i_zw1 = round(i_zw1, 2)


        # Create a label for displaying results
        self.result_label = tk.Label(simulation_window, text=f"Maximum short-circuit current: {i_max} A")
        self.result_label.pack()

        self.result_label_2 = tk.Label(simulation_window, text=f"Short-circuit current at 1/3 of the section: {i_zw13} A")
        self.result_label_2.pack()

        self.result_label_3 = tk.Label(simulation_window, text=f"Short-circuit current at 1/2 of the section: {i_zw12} A")
        self.result_label_3.pack()

        self.result_label_4 = tk.Label(simulation_window, text=f"Short-circuit current at the section: {i_zw1} A")
        self.result_label_4.pack()

        length_of_section, *_ = self.parameter_collected()
        length_of_section = int(length_of_section)

        error_message.pack_forget()



    def short_circuit_calculation(self):
        length_of_section, p_fc, p_rc, n_fc, n_rc, L_fc, L_rc, r_cs, r_rs, r_e, u_oca, r_ts, r_fc, r_rc, a_fc, a_rc = self.parameter_collected()

        # Ensure km is a float

        result_g = self.calculation_g()
        e_i = float(result_g[0])

        _, parameter_9_3 = self.calculation_e()

        i_dn = float(parameter_9_3)

        result_i = self.calculation_i()
        r_p = float(result_i[0])

        r_kp = float(r_rc)
        r_kz = float(r_fc)

        l_zw = float(length_of_section)

        r_s = float(r_cs + ((r_rs * r_e) / (r_rs + r_e)))

        n_max = float(self.parameter_10.get())


        i_max = ((3300 * (1+e_i) * (1 + (10/100)) - (i_dn * n_max * r_p) - 200) / (r_p + r_kp + r_kz))
        i_zw13 = ((3300 * (1+e_i) * (1 - (10/100)) - (i_dn * r_p) - 200) / (r_p + r_kz + r_kp + ((1/3) * l_zw * r_s)))
        i_zw12 = ((3300 * (1+e_i) * (1 - (10/100)) - (i_dn * r_p) - 200) / (r_p + r_kz + r_kp + ((1/2) * l_zw * r_s)))
        i_zw1 = ((3300 * (1+e_i) * (1 - (10/100)) - (i_dn * r_p) - 200) / (r_p + r_kz + r_kp + (l_zw * r_s)))

        return i_max, i_zw13, i_zw12, i_zw1


    def show_result(self):
        # Update the text of the existing label instead of creating a new one
        i_max, i_zw13, i_zw12, i_zw1= self.short_circuit_calculation()

        i_max = round(i_max, 2)
        i_zw13 = round(i_zw13, 2)
        i_zw12 = round(i_zw12, 2)
        i_zw1 = round(i_zw1, 2)

        self.result_label.config(text=f"Maximum short-circuit: {i_max} A")
        self.result_label_2.config(text=f"Short-circuit at 1/3 of the section: {i_zw13} A")
        self.result_label_3.config(text=f"Short-circuit at 1/2 of the section: {i_zw12} A")
        self.result_label_4.config(text=f"Short-circuit at the section: {i_zw1} A")




















