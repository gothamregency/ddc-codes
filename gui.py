import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import modulators
import re
import os
import fileio
import numpy as np
import matplotlib.pyplot as plt
import json

class GUI:
    def __init__(self, root) -> None:
        self.progressBarVal = 0
        self.root = root
        self.root.grid()
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title("Shift Keying Waveforms")
        self.selection = tk.StringVar(self.root)
        self.selection.set("1")
        self.checked = tk.StringVar(value="1")
        menu = tk.Menu(self.root)
        modMenu = tk.Menu(menu, tearoff=0)
        modMenu.add_radiobutton(label="Modulation", variable=self.checked, value="1")
        modMenu.add_radiobutton(label="Demodulation", variable=self.checked, value="2", command=self.initDemod)
        modMenu.add_command(label="Exit")
        menu.add_cascade(label="Mode", menu=modMenu)
        self.root.config(menu=menu)
        self.homePage()
        self.fileName = ""
    
    def initDemod(self):
        self.checked.set("2")
        self.mainMenu.grid_forget()
        self.demodulators()
    
    def displayInfo(self, headings : list, paragraphs : list) -> None:
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        textBox = tk.Toplevel(self.root)
        textBox.title("ASK Modulation")
        textBox.geometry("1300x500")
        canvas = tk.Canvas(textBox)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(textBox, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        main_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        main_frame.bind("<Configure>", on_configure)
        headings = headings
        paragraphs = paragraphs
        for i, (heading, paragraph) in enumerate(zip(headings, paragraphs)):
            heading_label = ttk.Label(main_frame, text=heading, font=("Helvetica", 14, "bold"))
            heading_label.grid(row=i * 2, column=0, sticky="w")
            paragraph_label = ttk.Label(main_frame, text=paragraph, wraplength=1200, font=("Helvetica", 10))
            paragraph_label.grid(row=i * 2 + 1, column=0, padx=20, pady=5, sticky="w")
        textBox.grid_columnconfigure(0, weight=1)
        textBox.grid_rowconfigure(0, weight=1)

    def isValidFilename(self, filename):
        if not filename or len(filename) > 255:
            return False

        invalid_chars = r'[<>:"/\\|?*]'
        if re.search(invalid_chars, filename):
            return False

        reserved_names = ['CON', 'PRN', 'AUX', 'NUL'] + \
                         ['COM{}'.format(i) for i in range(1, 10)] + \
                         ['LPT{}'.format(i) for i in range(1, 10)]
        if filename.upper() in reserved_names:
            return False

        valid_chars = r'^[^<>:"/\\|?*]+$'
        if not re.match(valid_chars, filename):
            return False
        
        if filename == "" or filename == " ":
            return False
        
        if os.path.exists(filename):
            return False

        return True

    def progressBar(self, title):
        def update():
            progressBar.start(20)
            load.after(3000, progressBar.stop)
            self.root.after(3000, close)
        
        def close():
            load.destroy()

        load = tk.Toplevel(self.root)
        load.title(title)
        load.focus_force()
        text = ttk.Label(load, text=f"{title}...")
        text.grid(row=0, column=0, pady=10, padx=5)
        progressBar = ttk.Progressbar(load, orient="horizontal", length=200, mode="determinate")
        progressBar.grid(row=1, column=0, padx=10, pady=10)
        update()
    
    def calculate(self, root, obj):
        self.progressBar("Calculating...")
        root.after(3200, obj.display)

    def savePopUp(self, command, extension):
        def perform():
            if self.isValidFilename(fileName.get()):
                if not os.path.exists(f"{fileName.get()}.{extension}"):
                    self.fileName = fileName.get()
                    command()
                    self.progressBar("Saving")
                else:
                    if messagebox.askyesno(f"File {fileName.get()} already exists", "Do you want to replace the file?"):
                        command()
                        self.progressBar("Saving")
                    else:
                        messagebox.showwarning("File not saved", "Try changing the name of the file")

            else:
                messagebox.showerror("Error", "Invalid filename or File already exists in the foolder")
        self.top = tk.Toplevel(self.root)
        self.top.title("Save As")
        self.top.focus_force()
        body = ttk.Frame(self.top)
        body.grid(row=0, column=0, padx=60, pady=20, sticky="")
        saveLabel = ttk.Label(body, text="Enter file name")
        saveLabel.grid(row=0, column=0)
        fileName = ttk.Entry(body, justify="left")
        fileName.grid(row=1, column=0)
        saveButton = ttk.Button(body, text="Save", command=perform)
        saveButton.grid(row=2, column=0, pady=10)

    
    def check_byte(self, input_string):
        for char in input_string:
            if char != '0' and char != '1':
                return False
        return True

    def homePage(self):
        def displayGUIFromChoice():
            if self.selection.get() == "1":
                self.mainMenu.grid_forget()
                self.ASKPage()
            elif self.selection.get() == "2":
                self.mainMenu.grid_forget()
                self.FSKPage()
            elif self.selection.get() == "3":
                self.mainMenu.grid_forget()
                self.BPSKPage()
            elif self.selection.get() == "4":
                self.mainMenu.grid_forget()
                self.QPSKPage()
            elif self.selection.get() == "5":
                self.mainMenu.grid_forget()
                self.QAMPage()
        self.root.title("Shift Keying Waveforms")
        self.mainMenu = ttk.Frame(self.root)
        self.mainMenu.grid(column=0, row=0, sticky="nsew")
        self.mainMenu.grid_anchor("center")
        groupLabel = ttk.LabelFrame(self.mainMenu, text="Select Shift Keying Waveform")
        groupLabel.grid(padx=20, pady=10)
        radioButtons1 = ttk.Radiobutton(groupLabel, text="Amplitude Shift Keying (ASK)", value='1', variable=self.selection)
        radioButtons2 = ttk.Radiobutton(groupLabel, text="Frequency Shift Keying (FSK)", value='2', variable=self.selection)
        radioButtons3 = ttk.Radiobutton(groupLabel, text="Binary Phase Shift Keying (BPSK)", value='3', variable=self.selection)
        radioButtons4 = ttk.Radiobutton(groupLabel, text="Quadrature Frequency Shift Keying (QPSK)", value='4', variable=self.selection)
        radioButtons5 = ttk.Radiobutton(groupLabel, text="Quadrature Amplitude Modulation (QAM)", value='5', variable=self.selection)
        radioButtons1.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        radioButtons2.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        radioButtons3.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        radioButtons4.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        radioButtons5.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        submitButton = ttk.Button(self.mainMenu, text="Proceed", command=displayGUIFromChoice)
        submitButton.grid(row=1, column=0, pady=10)

    def ASKPage(self):
        ask = modulators.ASK()
        def showAdvanced(event):
            samplingRateInput.grid(row=3, column=1, pady=10, padx=5)
            samplingRateLabel.grid(row=3, column=0, pady=10, padx=5, sticky="e")
            advancedTextButton.grid(row=4, column=2)

        def navigateToHomePage():
            ASKPage.grid_forget()
            self.homePage()
        
        def save():
            def saveFile():
                ask.save(self.fileName, "ask")
            self.savePopUp(saveFile, "ask")
        def showInfo():
            askHead = ["Amplitude Shift Keying (ASK)", "Introduction:", "Principle:", "Applications:", "Advantages:", "Disadvantages:", "Conclusion:"]
            askPara = [" ", 
                              "Amplitude Shift Keying (ASK) is a digital modulation technique used in telecommunications to transmit digital data over a communication channel by varying the amplitude of a carrier signal. ASK is a form of amplitude modulation (AM), where the amplitude of the carrier wave is varied in proportion to the digital signal being transmitted. It is a simple and straightforward modulation technique that is easy to implement and suitable for low-cost communication systems.", 
                              "In ASK modulation, the digital data signal (consisting of binary bits) is represented by changing the amplitude of the carrier signal. Typically, one amplitude level is assigned to one binary digit (e.g., '1' corresponds to high amplitude, and '0' corresponds to low amplitude). During transmission, the modulator encodes the digital data onto the carrier signal by varying its amplitude according to the input binary sequence.\tMathematically, if Ac is the amplitude of the carrier signal and D(t) represents the digital data signal, the ASK modulated signal S(t) is given by:\n\tS(t) = Ac * D(t) * cos(2πfct)\n\twhere:\n\t\t- S(t) is the ASK modulated signal,\n\t\t- Ac is the amplitude of the carrier signal,\n\t\t- D(t) is the digital data signal (binary sequence),\n\t\t- fc is the carrier frequency, and\n\t\t- cos(2πfct) represents the carrier wave.\n",
                             "ASK modulation finds applications in various communication systems, including:\n\t- Radio broadcasting: ASK modulation is used in radio broadcasting to transmit digital audio signals.\n\t- RFID (Radio Frequency Identification): ASK modulation is used in RFID systems for identification and tracking purposes.\n\t- Remote control systems: ASK modulation is employed in remote control devices (e.g., garage door openers, wireless keyboards) for transmitting control signals.\n\t- Optical communication: In optical communication systems, ASK modulation is used to encode digital data onto optical carriers for transmission through optical fibers.\n",
                            "\t- Simple implementation: ASK modulation is relatively easy to implement using basic electronic components.\n\t- Spectral efficiency: ASK modulation provides better spectral efficiency compared to analog modulation techniques like AM.\n\t- Suitable for low-cost systems: ASK modulation is suitable for low-cost communication systems due to its simplicity and ease of implementation.\n",
                            "\t- Susceptible to noise: ASK modulation is susceptible to noise and interference, which can degrade the quality of the received signal.\n\t- Limited bandwidth utilization: ASK modulation does not efficiently utilize the available bandwidth compared to other modulation techniques like phase shift keying (PSK) or quadrature amplitude modulation (QAM).\n",
                            "\tAmplitude Shift Keying (ASK) is a simple yet effective digital modulation technique used in various communication systems. While it offers simplicity and ease of implementation, it may not be suitable for applications requiring high data rates or robustness against noise and interference. ASK modulation is best suited for low-cost communication systems where simplicity and cost-effectiveness are prioritized over data rate and spectral efficiency.\n"
                        ]
            self.displayInfo(askHead, askPara)

        def showASK():
            byte = byteInput.get()
            fc = carrierFrequencyInput.get()
            fs = samplingRateInput.get()
            if byte == "" or not self.check_byte(byte) or fc == "":
                messagebox.showerror("Error", "Please enter valid data")
                byteInput.delete(0, 'end')
                carrierFrequencyInput.delete(0, 'end')
            else:
                if fs == "": ask.modulate(byte, int(fc)) 
                else: ask.modulate(byte, int(fc), samplingRate=int(fs))
                self.calculate(ASKPage, ask)

        self.root.title('ASK Modulation')
        advancedText = "Advanced"
        ASKPage = ttk.Frame(self.root)
        ASKPage.grid()
        icon = ttk.Button(ASKPage, text="←", command=navigateToHomePage, width=5,)
        icon.grid(row=0, column=0)
        iconLabel = ttk.Label(ASKPage, text="")
        iconLabel.grid(row=0 ,column=1)
        groupLabel = ttk.LabelFrame(ASKPage, text="ASK Modulation")
        groupLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        byteInputLabel = ttk.Label(groupLabel, text="Byte :", anchor="e")
        byteInputLabel.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        byteInput = ttk.Entry(groupLabel, justify="right")
        byteInput.grid(row=1, column=1, pady=10)
        carrierFrequencyLabel = ttk.Label(groupLabel, text="Carrier Frequency :", anchor="e")
        carrierFrequencyLabel.grid(row=2, column=0, pady=10, padx=5)
        carrierFrequencyInput = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput.grid(row=2, column=1, pady=10, padx=5)
        carrierFrequencyUnit = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit.grid(row=2, column=2, pady=10)
        samplingRateLabel = ttk.Label(groupLabel, text="Sampling rate :")
        samplingRateInput = ttk.Entry(groupLabel, justify="right")
        advancedTextButton= ttk.Label(groupLabel, text=advancedText, underline=True)
        advancedTextButton.bind("<Button-1>", showAdvanced) 
        advancedTextButton.grid(row=3, column=2)
        buttonGroup = ttk.Frame(ASKPage)
        buttonGroup.grid(row=2, column=0, columnspan=2, sticky="e", padx=30, pady=10)
        calculateButton = ttk.Button(buttonGroup, text="Calculate", command=showASK)
        calculateButton.grid(row=0, column=0)
        infoButton = ttk.Button(buttonGroup, text="ɪ", width=2, command=showInfo)
        infoButton.grid(row=0, column=1)
        saveButton = ttk.Button(buttonGroup, text="Save", command=save)
        saveButton.grid(row=0, column=2)


    def FSKPage(self):
        fsk = modulators.FSK()
        def showAdvanced(event):
            samplingRateInput.grid(row=4, column=1, pady=10, padx=5)
            samplingRateLabel.grid(row=4, column=0, pady=10, padx=5, sticky="e")
            advancedTextButton.grid(row=5, column=2)
        
        def navigateToHomePage():
            FSKpage.grid_forget()
            self.homePage()
        
        def save():
            def saveFile():
                fsk.save(self.fileName, "fsk")
            self.savePopUp(saveFile, "fsk")

        def showInfo():
            fskHead = ["Frequency Shift Keying (FSK)", "Introduction:", "Principle:", "Applications:", "Advantages:", "Disadvantages:", "Conclusion:"]
            fskPara = [" ", "Frequency Shift Keying (FSK) is a digital modulation technique used in telecommunications to transmit digital data over a communication channel by varying the frequency of a carrier signal. FSK is a form of frequency modulation (FM), where the frequency of the carrier wave is varied in proportion to the digital signal being transmitted. It is commonly used in applications such as wireless communication, data transmission, and radio broadcasting.", "In FSK modulation, the digital data signal (consisting of binary bits) is represented by changing the frequency of the carrier signal. Typically, one frequency is assigned to one binary digit (e.g., '1' corresponds to high frequency, and '0' corresponds to low frequency). During transmission, the modulator encodes the digital data onto the carrier signal by varying its frequency according to the input binary sequence.", "FSK modulation finds applications in various communication systems, including:\n\t- Wireless communication: FSK modulation is used in wireless communication systems (e.g., Wi-Fi, Bluetooth) for transmitting digital data between devices.\n\t- Data transmission: FSK modulation is employed in modems and digital communication systems for transmitting data over long distances.\n\t- Radio broadcasting: FSK modulation is used in radio broadcasting to transmit digital audio signals and data services.", "\t- Resistance to noise: FSK modulation offers better resistance to noise and interference compared to other modulation techniques like Amplitude Shift Keying (ASK).\n\t- Simple demodulation: FSK modulation can be easily demodulated using simple receiver circuits, making it suitable for low-cost communication systems.\n\t- Narrow bandwidth: FSK modulation requires narrower bandwidth compared to other modulation techniques like Amplitude Shift Keying (ASK), enabling efficient use of the available frequency spectrum.", "\t- Bandwidth efficiency: FSK modulation may have lower bandwidth efficiency compared to modulation techniques like Phase Shift Keying (PSK) or Quadrature Amplitude Modulation (QAM), especially for high data rates.\n\t- Complexity at high data rates: Implementing FSK modulation for high data rates may require more complex modulation and demodulation circuits, increasing system complexity and cost.\n", "\tFrequency Shift Keying (FSK) is a widely used digital modulation technique that offers advantages such as resistance to noise, simple demodulation, and narrow bandwidth. However, it may not be the most bandwidth-efficient option for high-speed data transmission, and implementing FSK modulation for high data rates may introduce complexity and cost. Overall, FSK modulation is suitable for various communication applications where robustness and simplicity are prioritized."]
            self.displayInfo(fskHead, fskPara)

        def showFSK():
            byte = byteInput.get()
            fc0 = carrierFrequencyInput1.get()
            fc1 = carrierFrequencyInput2.get()
            fs = samplingRateInput.get()
            if byte == "" or not self.check_byte(byte) or fc0 == "" or fc1 == "":
                print(byte == "")
                print(byte not in ("0", "1"))
                print(fc0 == "")
                print(fc1 == "")
                messagebox.showerror("Error", "Please enter valid data")
                byteInput.delete(0, 'end')
                carrierFrequencyInput1.delete(0, 'end')
                carrierFrequencyInput2.delete(0, 'end')
            else:
                if fs == "": fsk.modulate(byte, int(fc0), int(fc1)) 
                else: fsk.modulate(byte, int(fc0), int(fc1),samplingRate=int(fs))
                self.calculate(FSKpage, fsk)
            
        advancedText = "Advanced"
        self.root.title('FSK Modulation')
        FSKpage = ttk.Frame(self.root)
        FSKpage.grid()
        icon = ttk.Button(FSKpage, text="←", command=navigateToHomePage, width=5)
        icon.grid(row=0, column=0)
        iconLabel = ttk.Label(FSKpage, text="")
        iconLabel.grid(row=0 ,column=1)
        groupLabel = ttk.LabelFrame(FSKpage, text="FSK Modulation")
        groupLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        byteInputLabel = ttk.Label(groupLabel, text="Byte :", anchor="e")
        byteInputLabel.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        byteInput = ttk.Entry(groupLabel, justify="right")
        byteInput.grid(row=1, column=1, pady=10)
        carrierFrequencyLabel1 = ttk.Label(groupLabel, text="Carrier Frequency (0) for Logic 0 :", anchor="e")
        carrierFrequencyLabel1.grid(row=2, column=0, pady=10, padx=5)
        carrierFrequencyInput1 = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput1.grid(row=2, column=1, pady=10, padx=5)
        carrierFrequencyUnit1 = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit1.grid(row=2, column=2, pady=10)
        carrierFrequencyLabel2 = ttk.Label(groupLabel, text="Carrier Frequency (1) for Logic 1 :", anchor="e")
        carrierFrequencyLabel2.grid(row=3, column=0, pady=10, padx=5)
        carrierFrequencyInput2 = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput2.grid(row=3, column=1, pady=10, padx=5)
        carrierFrequencyUnit2 = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit2.grid(row=3, column=2, pady=10)
        samplingRateLabel = ttk.Label(groupLabel, text="Sampling rate :")
        samplingRateInput = ttk.Entry(groupLabel, justify="right")
        advancedTextButton= ttk.Label(groupLabel, text=advancedText, underline=True)
        advancedTextButton.bind("<Button-1>", showAdvanced) 
        advancedTextButton.grid(row=4, column=2)
        buttonGroup = ttk.Frame(FSKpage)
        buttonGroup.grid(row=2, column=0, columnspan=2, sticky="e", padx=30, pady=10)
        calculateButton = ttk.Button(buttonGroup, text="Calculate", command=showFSK)
        calculateButton.grid(row=0, column=0)
        infoButton = ttk.Button(buttonGroup, text="ɪ", width=2, command=showInfo)
        infoButton.grid(row=0, column=1)
        saveButton = ttk.Button(buttonGroup, text="Save", command=save)
        saveButton.grid(row=0, column=2)

    def BPSKPage(self):
        bpsk = modulators.BPSK()
        def showAdvanced(event):
            samplingRateInput.grid(row=3, column=1, pady=10, padx=5)
            samplingRateLabel.grid(row=3, column=0, pady=10, padx=5, sticky="e")
            advancedTextButton.grid(row=4, column=2)

        def navigateToHomePage():
            BPSKPage.grid_forget()
            self.homePage()
        
        def save():
            def saveFile():
                bpsk.save(self.fileName, "bpsk")
            self.savePopUp(saveFile, "bpsk")

        def showInfo():
            bpskHead = ["Binary Phase Shift Keying (BPSK)", "Introduction:", "Principle:", "Applications:", "Advantages:", "Disadvantages:", "Conclusion:"]
            bpskPara = [" ", "Binary Phase Shift Keying (BPSK) is a digital modulation technique used in telecommunications to transmit digital data over a communication channel by varying the phase of a carrier signal. BPSK is a form of phase modulation (PM), where the phase of the carrier wave is varied in proportion to the digital signal being transmitted. It is widely used in applications such as wireless communication, satellite communication, and digital data transmission.", "In BPSK modulation, the digital data signal (consisting of binary bits) is represented by changing the phase of the carrier signal. Typically, one phase is assigned to one binary digit (e.g., '0' corresponds to one phase, and '1' corresponds to another phase). During transmission, the modulator encodes the digital data onto the carrier signal by varying its phase according to the input binary sequence.", "BPSK modulation finds applications in various communication systems, including:\n\t- Wireless communication: BPSK modulation is used in wireless communication systems (e.g., Wi-Fi, cellular networks) for transmitting digital data between devices.\n\t- Satellite communication: BPSK modulation is employed in satellite communication systems for transmitting data between ground stations and satellites.\n\t- Digital data transmission: BPSK modulation is used in digital communication systems (e.g., modems, digital television) for transmitting data over long distances.", "\t- Robustness: BPSK modulation offers robust performance in noisy communication channels, making it suitable for applications where reliability is essential.\n\t- Simplified demodulation: BPSK modulation can be demodulated using simple receiver circuits, leading to cost-effective receiver designs.\n\t- Spectral efficiency: BPSK modulation provides good spectral efficiency, enabling efficient use of the available frequency spectrum.", "\t- Bandwidth inefficiency: BPSK modulation may have lower bandwidth efficiency compared to modulation techniques like Quadrature Phase Shift Keying (QPSK) or higher-order modulation schemes.\n\t- Sensitivity to phase noise: BPSK modulation may be sensitive to phase noise in the communication channel, which can degrade the quality of the received signal.\n", "\tBinary Phase Shift Keying (BPSK) is a widely used digital modulation technique that offers robust performance, simplified demodulation, and good spectral efficiency. While it may not be the most bandwidth-efficient option, BPSK modulation is suitable for various communication applications where reliability and simplicity are prioritized."]
            self.displayInfo(bpskHead, bpskPara)

        def showBPSK():
            byte = byteInput.get()
            fc = carrierFrequencyInput.get()
            fs = samplingRateInput.get()
            if byte == "" or not self.check_byte(byte) or fc == "":
                messagebox.showerror("Error", "Please enter valid data")
                byteInput.delete(0, 'end')
                carrierFrequencyInput.delete(0, 'end')
            else:
                if fs == "": bpsk.modulate(byte, int(fc))
                else: bpsk.modulate(byte, int(fc), samplingRate=int(fs))
                self.calculate(BPSKPage, bpsk)

        self.root.title('BPSK Modulation')
        advancedText = "Advanced"
        BPSKPage = ttk.Frame(self.root)
        BPSKPage.grid()
        icon = ttk.Button(BPSKPage, text="←", command=navigateToHomePage, width=5)
        icon.grid(row=0, column=0)
        iconLabel = ttk.Label(BPSKPage, text="")
        iconLabel.grid(row=0 ,column=1)
        groupLabel = ttk.LabelFrame(BPSKPage, text="BPSK Modulation")
        groupLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        byteInputLabel = ttk.Label(groupLabel, text="Byte :", anchor="e")
        byteInputLabel.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        byteInput = ttk.Entry(groupLabel, justify="right")
        byteInput.grid(row=1, column=1, pady=10)
        carrierFrequencyLabel = ttk.Label(groupLabel, text="Carrier Frequency :", anchor="e")
        carrierFrequencyLabel.grid(row=2, column=0, pady=10, padx=5)
        carrierFrequencyInput = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput.grid(row=2, column=1, pady=10, padx=5)
        carrierFrequencyUnit = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit.grid(row=2, column=2, pady=10)
        samplingRateLabel = ttk.Label(groupLabel, text="Sampling rate :")
        samplingRateInput = ttk.Entry(groupLabel, justify="right")
        advancedTextButton= ttk.Label(groupLabel, text=advancedText, underline=True)
        advancedTextButton.bind("<Button-1>", showAdvanced) 
        advancedTextButton.grid(row=3, column=2)
        buttonGroup = ttk.Frame(BPSKPage)
        buttonGroup.grid(row=2, column=0, columnspan=2, sticky="e", padx=30, pady=10)
        calculateButton = ttk.Button(buttonGroup, text="Calculate", command=showBPSK)
        calculateButton.grid(row=0, column=0)
        infoButton = ttk.Button(buttonGroup, text="ɪ", width=2, command=showInfo)
        infoButton.grid(row=0, column=1)
        saveButton = ttk.Button(buttonGroup, text="Save", command=save)
        saveButton.grid(row=0, column=2)

    def QPSKPage(self):
        qpsk = modulators.QPSK()
        def showAdvanced(event):
            samplingRateInput.grid(row=3, column=1, pady=10, padx=5)
            samplingRateLabel.grid(row=3, column=0, pady=10, padx=5, sticky="e")
            advancedTextButton.grid(row=4, column=2)

        def navigateToHomePage():
            QPSKPage.grid_forget()
            self.homePage()

        def save():
            def saveFile():
                qpsk.save(self.fileName, "qpsk")
            self.savePopUp(saveFile, "qpsk")

        def showInfo():
            qpskHead = ["Quadrature Phase Shift Keying (QPSK)", "Introduction:", "Principle:", "Applications:", "Advantages:", "Disadvantages:", "Conclusion:"]
            qpskPara = [" ", "Quadrature Phase Shift Keying (QPSK) is a digital modulation technique used in telecommunications to transmit digital data over a communication channel by varying both the phase and amplitude of a carrier signal. QPSK is a form of phase modulation (PM), where the phase of the carrier wave is varied in proportion to the digital signal being transmitted. It is widely used in applications such as satellite communication, digital television, and wireless networking.", "In QPSK modulation, the digital data signal (consisting of binary bits) is represented by changing both the phase and amplitude of the carrier signal. Typically, two bits are encoded per symbol, allowing four possible phase shifts (hence the name Quadrature Phase Shift Keying). During transmission, the modulator encodes the digital data onto the carrier signal by varying its phase and amplitude according to the input binary sequence.", "QPSK modulation finds applications in various communication systems, including:\n\t- Satellite communication: QPSK modulation is extensively used in satellite communication systems for transmitting data between ground stations and satellites.\n\t- Digital television: QPSK modulation is employed in digital television broadcasting for transmitting high-quality video and audio signals.\n\t- Wireless networking: QPSK modulation is used in wireless networking standards such as Wi-Fi and WiMAX for transmitting data between devices.", "\t- Spectral efficiency: QPSK modulation offers good spectral efficiency by encoding multiple bits per symbol, enabling higher data rates within the available bandwidth.\n\t- Robustness to noise: QPSK modulation provides robust performance in noisy communication channels, making it suitable for applications where reliability is essential.\n\t- Bandwidth utilization: QPSK modulation efficiently utilizes the available bandwidth, allowing more data to be transmitted within the allocated frequency spectrum.", "\t- Complexity: QPSK modulation may require more complex modulation and demodulation circuits compared to simpler modulation techniques like Binary Phase Shift Keying (BPSK).\n\t- Susceptibility to phase noise: QPSK modulation may be sensitive to phase noise in the communication channel, which can degrade the quality of the received signal.\n", "\tQuadrature Phase Shift Keying (QPSK) is a versatile digital modulation technique that offers good spectral efficiency, robustness to noise, and efficient bandwidth utilization. While it may introduce complexity in the modulation and demodulation circuits, QPSK modulation is suitable for various communication applications where high data rates and reliability are essential."]
            self.displayInfo(qpskHead, qpskPara)

        def showQPSK():
            byte = byteInput.get()
            fc = carrierFrequencyInput.get()
            fs = samplingRateInput.get()
            if byte == "" or not self.check_byte(byte) or fc == "":
                messagebox.showerror("Error", "Please enter valid data")
                byteInput.delete(0, 'end')
                carrierFrequencyInput.delete(0, 'end')
            else:
                if fs == "": qpsk.modulate(byte, int(fc))
                else: qpsk.modulate(byte, int(fc), samplingRate=int(fs))
                self.calculate(QPSKPage, qpsk)
  
        self.root.title('QPSK Modulation')
        advancedText = "Advanced"
        QPSKPage = ttk.Frame(self.root)
        QPSKPage.grid()
        icon = ttk.Button(QPSKPage, text="←", command=navigateToHomePage, width=5)
        icon.grid(row=0, column=0)
        iconLabel = ttk.Label(QPSKPage, text="")
        iconLabel.grid(row=0 ,column=1)
        groupLabel = ttk.LabelFrame(QPSKPage, text="BPSK Modulation")
        groupLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        byteInputLabel = ttk.Label(groupLabel, text="Byte :", anchor="e")
        byteInputLabel.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        byteInput = ttk.Entry(groupLabel, justify="right")
        byteInput.grid(row=1, column=1, pady=10)
        carrierFrequencyLabel = ttk.Label(groupLabel, text="Carrier Frequency :", anchor="e")
        carrierFrequencyLabel.grid(row=2, column=0, pady=10, padx=5)
        carrierFrequencyInput = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput.grid(row=2, column=1, pady=10, padx=5)
        carrierFrequencyUnit = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit.grid(row=2, column=2, pady=10)
        samplingRateLabel = ttk.Label(groupLabel, text="Sampling rate :")
        samplingRateInput = ttk.Entry(groupLabel, justify="right")
        advancedTextButton= ttk.Label(groupLabel, text=advancedText, underline=True)
        advancedTextButton.bind("<Button-1>", showAdvanced) 
        advancedTextButton.grid(row=3, column=2)
        buttonGroup = ttk.Frame(QPSKPage)
        buttonGroup.grid(row=2, column=0, columnspan=2, sticky="e", padx=30, pady=10)
        calculateButton = ttk.Button(buttonGroup, text="Calculate", command=showQPSK)
        calculateButton.grid(row=0, column=0)
        infoButton = ttk.Button(buttonGroup, text="ɪ", width=2, command=showInfo)
        infoButton.grid(row=0, column=1)
        saveButton = ttk.Button(buttonGroup, text="Save", command=save)
        saveButton.grid(row=0, column=2)
    
    def QAMPage(self):
        qam = modulators.QAM()
        def showAdvanced(event):
            samplingRateInput.grid(row=3, column=1, pady=10, padx=5)
            samplingRateLabel.grid(row=3, column=0, pady=10, padx=5, sticky="e")
            advancedTextButton.grid(row=4, column=2)
        
        def navigateToHomePage():
            QAMPage.grid_forget()
            self.homePage()

        def save():
            def saveFile():
                qam.save(self.fileName, "qam")
            self.savePopUp(saveFile, "qam")
        
        def showInfo():
            qamHead = ["Quadrature Amplitude Modulation (QAM)", "Introduction:", "Principle:", "Applications:", "Advantages:", "Disadvantages:", "Conclusion:"]
            qamPara = [" ", "Quadrature Amplitude Modulation (QAM) is a digital modulation technique used in telecommunications to transmit digital data over a communication channel by varying both the amplitude and phase of a carrier signal. QAM combines amplitude modulation (AM) and phase modulation (PM) to encode digital information into the amplitude and phase of the carrier wave. It is widely used in applications such as digital television, cable modems, and wireless communication systems.", "In QAM modulation, the digital data signal (consisting of binary bits) is represented by varying both the amplitude and phase of the carrier signal. The amplitude and phase of the carrier signal are modulated independently to encode multiple bits per symbol. The modulated signal is then transmitted over the communication channel.", "QAM modulation finds applications in various communication systems, including:\n\t- Digital television: QAM modulation is extensively used in digital television broadcasting for transmitting high-definition video and audio signals.\n\t- Cable modems: QAM modulation is employed in cable modem systems for transmitting data over cable television networks.\n\t- Wireless communication: QAM modulation is used in wireless communication standards such as LTE (Long-Term Evolution) for transmitting data between mobile devices and base stations.", "\t- High spectral efficiency: QAM modulation offers high spectral efficiency by encoding multiple bits per symbol, allowing higher data rates within the available bandwidth.\n\t- Robustness to noise: QAM modulation provides robust performance in noisy communication channels, making it suitable for applications where reliability is essential.\n\t- Flexible data rates: QAM modulation supports a wide range of data rates, enabling adaptation to varying communication requirements.", "\t- Complexity: QAM modulation may require more complex modulation and demodulation circuits compared to simpler modulation techniques like Binary Phase Shift Keying (BPSK) or Quadrature Phase Shift Keying (QPSK).\n\t- Higher power consumption: Implementing QAM modulation may require higher power consumption due to the increased complexity of modulation and demodulation circuits.\n", "\tQuadrature Amplitude Modulation (QAM) is a versatile digital modulation technique that offers high spectral efficiency, robustness to noise, and flexible data rates. While it may introduce complexity and higher power consumption, QAM modulation is suitable for various communication applications where high data rates and reliability are essential."]
            self.displayInfo(qamHead, qamPara)

        def showQAM():
            byte = byteInput.get()
            fc = carrierFrequencyInput.get()
            fs = samplingRateInput.get()
            if byte == "" or not self.check_byte(byte) or fc == "":
                messagebox.showerror("Error", "Please enter valid data")
                byteInput.delete(0, 'end')
                carrierFrequencyInput.delete(0, 'end')
            else:
                if fs == "": qam.modulate(byte, int(fc)) 
                else: qam.modulate(byte, int(fc), samplingRate=int(fs))
                self.calculate(QAMPage, qam)
            
        self.root.title('QAM Modulation')
        advancedText = "Advanced"
        QAMPage = ttk.Frame(self.root)
        QAMPage.grid()
        icon = ttk.Button(QAMPage, text="←", command=navigateToHomePage, width=5)
        icon.grid(row=0, column=0)
        iconLabel = ttk.Label(QAMPage, text="")
        iconLabel.grid(row=0 ,column=1)
        groupLabel = ttk.LabelFrame(QAMPage, text="QAM Modulation")
        groupLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        byteInputLabel = ttk.Label(groupLabel, text="Byte :", anchor="e")
        byteInputLabel.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        byteInput = ttk.Entry(groupLabel, justify="right")
        byteInput.grid(row=1, column=1, pady=10)
        carrierFrequencyLabel = ttk.Label(groupLabel, text="Carrier Frequency :", anchor="e")
        carrierFrequencyLabel.grid(row=2, column=0, pady=10, padx=5)
        carrierFrequencyInput = ttk.Entry(groupLabel, justify="right")
        carrierFrequencyInput.grid(row=2, column=1, pady=10, padx=5)
        carrierFrequencyUnit = ttk.Label(groupLabel, text="kHz")
        carrierFrequencyUnit.grid(row=2, column=2, pady=10)
        samplingRateLabel = ttk.Label(groupLabel, text="Sampling rate :")
        samplingRateInput = ttk.Entry(groupLabel, justify="right")
        advancedTextButton= ttk.Label(groupLabel, text=advancedText, underline=True)
        advancedTextButton.bind("<Button-1>", showAdvanced) 
        advancedTextButton.grid(row=3, column=2)
        buttonGroup = ttk.Frame(QAMPage)
        buttonGroup.grid(row=2, column=0, columnspan=2, sticky="e", padx=30, pady=10)
        calculateButton = ttk.Button(buttonGroup, text="Calculate", command=showQAM)
        calculateButton.grid(row=0, column=0)
        infoButton = ttk.Button(buttonGroup, text="ɪ", width=2, command=showInfo)
        infoButton.grid(row=0, column=1)
        saveButton = ttk.Button(buttonGroup, text="Save", command=save)
        saveButton.grid(row=0, column=2)

    
    def demodulators(self):
        def mounting():
            self.progressBar("Mounting")
        def reading():
            self.progressBar("Reading")
        def calculating():
            self.progressBar("Calculating")

        def showDemodulation():
            self.progressBar("Seaching")
            if not os.path.exists(f"{fileNameInput.get()}{extensionDropDown.get()}"):
                messagebox.showerror("Error", f"Cannot find the file {fileNameInput.get()}{extensionDropDown.get()}")
            else:
                demodulatorPage.after(3200, mounting)
                file = fileio.FileIO()
                data = file.read(fileNameInput.get(), extensionDropDown.get().lstrip("."))
                demodulatorPage.after(6400, reading)
                modulatedData = np.array(data[0])
                timingData = np.array(data[1])
                demodulatedData = np.array(data[2])
                demodulatedData[0] = 0.0
                demodulatedData[len(demodulatedData) - 1] = 0.0
                demodulatorPage.after(9600, calculating)
                figs, axes = plt.subplots(2, 1)
                axes[0].plot(timingData, modulatedData, color='red', label='Modulated Wave')
                axes[1].plot(timingData, demodulatedData, label='Demodulated Wave')
                for i in range(2):
                    axes[i].legend(loc='upper right')
                plt.tight_layout()
                demodulatorPage.after(12800, plt.show)
        self.root.title("Shift Keying Waveforms")
        demodulatorPage = ttk.Frame(self.root)
        groupLabel = ttk.Labelframe(demodulatorPage, text="Demodulators")
        fileNameInput = ttk.Entry(groupLabel, justify="left")
        fileNameInput.grid(row=0, column=0, pady=10, padx=5)
        frame = ttk.Frame(groupLabel)
        frame.grid(row=0, column=1, padx=5)
        extensionDropDown = ttk.Combobox(frame, values=[".ask", ".fsk", ".bpsk", ".qpsk", ".qam"], state="readonly", width=6)
        extensionDropDown.grid(row=0, column=1, padx=5, pady=5)
        groupLabel.grid(row=0, column=0, sticky="", padx=30, pady=30)
        button = ttk.Button(demodulatorPage, text="Load", command=showDemodulation)
        button.grid(row=1, column=0, sticky="", padx=10, pady=5)
        demodulatorPage.grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()