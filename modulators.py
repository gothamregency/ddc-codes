# Use CamelCase for entire document
import numpy as np
import matplotlib.pyplot as plt
import fileio

class ASK:
    def save(self, fileName : str, mod : str):
        saveFile = fileio.FileIO()
        saveFile.write(fileName, mod, [self.askArray.tolist(), self.timeArray.tolist(), self.bitArray.tolist()])

    def modulate(self, byte : str, frequency : float, amplitude=10, bitTime=100, samplingRate=100_000) -> None:
        '''
        frequency1 = frequency2 => KHz
        amplitude => V
        bitTime => ms
        samplingRate => KHz
        '''
        self.bitTime = bitTime
        self.byte = str(byte)
        self.frequency = frequency
        self.samplingRate = samplingRate
        self.amplitude = amplitude
        self.timeArray = np.linspace(0, 1, self.samplingRate * len(self.byte))
        self.bitArray = np.empty((len(self.byte), self.samplingRate))
        self.sineArray = self.amplitude * np.sin(2 * np.pi * self.frequency * self.timeArray)
        self.zeroArray = np.zeros_like(self.sineArray)
        i = 0

        for bit in byte:
            if bit == "0":
                self.bitArray[i] = np.zeros_like((self.bitTime))
            else:
                self.bitArray[i] = np.ones_like((self.bitTime)) * 5
            i += 1

        self.bitArray = self.bitArray.ravel()
        self.bitArray[0] = 0.0
        self.bitArray[len(self.bitArray) - 1] = 0.0
        self.askArray = np.empty_like((self.timeArray))
        for i in range(len(self.askArray)):
            self.askArray[i] = self.zeroArray[i] if self.bitArray[i] == 0 else self.sineArray[i]

    def display(self) -> None:
        fig, axes = plt.subplots(3, 1)
        axes[0].plot(self.timeArray, self.bitArray, color='red', label='Data Signal')
        axes[1].plot(self.timeArray, self.sineArray, color='green', label='Carrier Signal')
        axes[2].plot(self.timeArray, self.askArray, label='ASK Modulated Signal')
        for i in range(3):
            axes[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()

class FSK:
    def save(self, fileName : str, mod : str):
        saveFile = fileio.FileIO()
        saveFile.write(fileName, mod, [self.fskArray.tolist(), self.timeArray.tolist(), self.bitArray.tolist()])

    def modulate(self, byte : str, frequency1 : float, frequency2 : float, amplitude=10, bitTime=100, samplingRate=100_000) -> None:
        '''
        frequency1 = frequency2 => KHz
        amplitude => V
        bitTime => ms
        samplingRate => KHz
        '''
        self.bitTime = bitTime
        self.byte = str(byte)
        self.frequency1 = frequency1
        self.frequency2 = frequency2
        self.samplingRate = samplingRate
        self.amplitude = amplitude

        self.timeArray = np.linspace(0, 1, self.samplingRate * len(self.byte))
        self.bitArray = np.empty((len(self.byte), self.samplingRate))
        self.sineArray1 = self.amplitude * np.sin(2 * np.pi * self.frequency1 * self.timeArray)
        self.sineArray2 = self.amplitude * np.sin(2 * np.pi * self.frequency2 * self.timeArray)
        i = 0
        for bit in self.byte:
            if bit == "0":
                self.bitArray[i] = np.zeros_like((self.bitTime))
            else:
                self.bitArray[i] = np.ones_like((self.bitTime)) * 5
            i += 1

        self.bitArray = self.bitArray.ravel()
        self.bitArray[0] = 0.0
        self.bitArray[len(self.bitArray) - 1] = 0.0
        self.fskArray = np.empty_like((self.timeArray))
        for i in range(len(self.fskArray)):
            if self.bitArray[i] == 0: self.fskArray[i] = self.sineArray1[i]
            else: self.fskArray[i] = self.sineArray2[i]
    
    def display(self) -> None:
        fig, axes = plt.subplots(4, 1)
        axes[0].plot(self.timeArray, self.bitArray, color='red', label='Data Signal')
        axes[1].plot(self.timeArray, self.sineArray1, color='green', label='Carrier Signal (Logic 0)')
        axes[2].plot(self.timeArray, self.sineArray2, color='#00D000', label='Carrier Signal (Logic 1)')
        axes[3].plot(self.timeArray, self.fskArray, label='FSK Modulated Signal')
        for i in range(4):
            axes[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()

class BPSK:
    def save(self, fileName : str, mod : str):
        saveFile = fileio.FileIO()
        saveFile.write(fileName, mod, [self.bpskArray.tolist(), self.timeArray.tolist(), self.bitArray.tolist()])

    def modulate(self, byte : str, frequency : float, amplitude=10, bitTime=100, samplingRate=100_000) -> None:
        '''
        frequency1 => KHz
        amplitude => V
        bitTime => ms
        samplingRate => KHz
        '''
        self.bitTime = bitTime
        self.byte = str(byte)
        self.frequency = frequency
        self.samplingRate = samplingRate
        self.amplitude = amplitude
        self.timeArray = np.linspace(0, 1, self.samplingRate * len(self.byte))
        self.bitArray = np.empty((len(self.byte), self.samplingRate))
        self.sineArray = self.amplitude * np.sin(2 * np.pi * self.frequency * self.timeArray)
        self.phaseShifSineArray = self.amplitude * np.sin(2 * np.pi * self.frequency * self.timeArray + np.pi)
        i = 0

        for bit in self.byte:
            if bit == "0":
                self.bitArray[i] = np.zeros_like((self.bitTime))
            else:
                self.bitArray[i] = np.ones_like((self.bitTime)) * 5
            i += 1

        self.bitArray = self.bitArray.ravel()
        self.bpskArray = np.empty_like((self.timeArray))
        for i in range(len(self.bpskArray)):
            if self.bitArray[i] == 0: self.bpskArray[i] = self.phaseShifSineArray[i]
            else: self.bpskArray[i] = self.sineArray[i]
        self.bitArray[0] = 0.0
        self.bitArray[len(self.bitArray) - 1] = 0.0
    
    def display(self) -> None:
        fig, axes = plt.subplots(3, 1)
        axes[0].plot(self.timeArray, self.bitArray, color='red', label='Data Signal')
        axes[1].plot(self.timeArray, self.sineArray, color='green', label='Carrier Signal')
        axes[2].plot(self.timeArray, self.bpskArray, label='BPSK Modulated Signal')
        for i in range(3):
            axes[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()

class QPSK:
    def save(self, fileName : str, mod : str):
        saveFile = fileio.FileIO()
        saveFile.write(fileName, mod, [self.qpskArray.tolist(), self.timeArray.tolist(), self.bitArray.tolist()])

    def modulate(self, byte : str, frequency : float, amplitude=10, bitTime=100, samplingRate=100_000) -> None:
        '''
        frequency1 => KHz
        amplitude => V
        bitTime => ms
        samplingRate => KHz
        '''
        self.bitTime = bitTime
        self.byte = str(byte)
        if (len(self.byte) % 2) != 0:
            self.byte = "0" * abs(((len(self.byte) % 2) - 2)) + self.byte
        self.frequency = frequency
        self.samplingRate = samplingRate
        self.amplitude = amplitude
        self.timeArray = np.linspace(0, 1, self.samplingRate * len(self.byte))
        self.bitArray = np.empty((len(self.byte), self.samplingRate))
        self.sineArray = self.amplitude * np.sin(2 * np.pi * self.frequency * self.timeArray)
        self.sineArray45 = self.amplitude * np.sin(2 * np.pi * self.frequency * self.timeArray + (np.pi / 4))
        self.sineArray135 = self.amplitude * np.cos(2 * np.pi * self.frequency * self.timeArray + ((3 * np.pi) / 4))
        self.sineArray225 = self.amplitude * np.cos(2 * np.pi * self.frequency * self.timeArray + ((5 * np.pi) / 4))
        self.sineArray315 = self.amplitude * np.cos(2 * np.pi * self.frequency * self.timeArray + ((7 * np.pi) / 4))
        i = 0

        for bit in self.byte:
            if bit == "0":
                self.bitArray[i] = np.zeros_like((self.bitTime))
            else:
                self.bitArray[i] = np.ones_like((self.bitTime)) * 5
            i += 1

        self.bitArray = self.bitArray.ravel()
        self.bitArray[0] = 0.0
        self.bitArray[len(self.bitArray) - 1] = 0.0
        self.qpskArray = np.empty_like((self.timeArray))
        i = 0
        k = 0
        while i < int(len(self.byte) - 2):
            self.consecutiveBits = str(self.byte[i:i+2])
            for j in range(int(len(self.bitArray) / len(self.byte))):
                if self.consecutiveBits == '00':
                    self.qpskArray[j + k] = self.sineArray225[j + k]
                elif self.consecutiveBits == '01':
                    self.qpskArray[j + k] = self.sineArray135[j + k]
                elif self.consecutiveBits == '10':
                    self.qpskArray[j + k] = self.sineArray315[j + k]
                elif self.consecutiveBits == '11':
                    self.qpskArray[j + k] = self.sineArray45[j + k]
            k += j
            i += 1
        
    def display(self) -> None:
        fig, axes = plt.subplots(3, 1)
        axes[0].plot(self.timeArray, self.bitArray, color='red', label='Data Signal')
        axes[1].plot(self.timeArray, self.sineArray, color='green', label='Carrier Signal')
        axes[2].plot(self.timeArray, self.qpskArray, label='QPSK Modulated Signal')
        for i in range(3):
            axes[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()

class QAM:
    def save(self, fileName : str, mod : str):
        saveFile = fileio.FileIO()
        saveFile.write(fileName, mod, [self.qamArray.tolist(), self.timeArray.tolist(), self.bitArray.tolist()])

    def modulate(self, byte : str, frequency : float, amplitude=10, bitTime=100, samplingRate=100_000) -> None:
        '''
        frequency1 = frequency2 => KHz
        amplitude => V
        bitTime => ms
        samplingRate => KHz
        '''
        self.bitTime = bitTime
        self.byte = str(byte)
        if (len(self.byte) % 4) != 0:
            self.byte = "0" * abs(((len(self.byte) % 4) - 4)) + self.byte
        self.frequency = frequency
        self.samplingRate = samplingRate
        self.timeArray = np.linspace(0, 1, self.samplingRate * len(self.byte))
        self.bitArray = np.empty((len(self.byte), self.samplingRate))
        self.sineArray = np.sin(2 * np.pi * self.frequency * self.timeArray)
        self.sineArray15 = np.sin(2 * np.pi * self.frequency * self.timeArray + (np.pi / 12))
        self.sineArray45 = np.sin(2 * np.pi * self.frequency * self.timeArray + (np.pi / 4))
        self.sineArray75 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((5 * np.pi) / 12))
        self.sineArray105 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((7 * np.pi) / 12))
        self.sineArray135 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((3 * np.pi) / 4))
        self.sineArray165 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((11 * np.pi) / 12))
        self.sineArray195 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((13 * np.pi) / 12))
        self.sineArray225 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((5 * np.pi) / 4))
        self.sineArray255 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((17 * np.pi) / 12))
        self.sineArray285 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((19 * np.pi) / 12))
        self.sineArray315 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((7 * np.pi) / 4))
        self.sineArray345 = np.sin(2 * np.pi * self.frequency * self.timeArray + ((23 * np.pi) / 12))
        i = 0
        for bit in self.byte:
            if bit == "0":
                self.bitArray[i] = np.zeros_like((self.bitTime))
            else:  
                self.bitArray[i] = 5 * np.ones_like((self.bitTime))
            i += 1
        
        self.bitArray = self.bitArray.ravel()
        self.bitArray[0] = 0.0
        self.bitArray[len(self.bitArray) - 1] = 0.0
        self.qamArray = np.empty_like((self.timeArray))
        i = 0
        k = 0
        while i < int(len(self.byte) - 4):
            self.consecutiveBits = str(self.byte[i:i+4])
            for j in range(int(len(self.bitArray) / len(self.byte))):
                if self.consecutiveBits == "0000":
                    self.qamArray[j + k] = self.sineArray225[j + k] * 0.268
                elif self.consecutiveBits == "0001":
                    self.qamArray[j + k] = self.sineArray135[j + k] * 0.268
                elif self.consecutiveBits == "0010":
                    self.qamArray[j + k] = self.sineArray315[j + k] * 0.268
                elif self.consecutiveBits == "0011":
                    self.qamArray[j + k] = self.sineArray45[j + k] * 0.268
                elif self.consecutiveBits == "0100":
                    self.qamArray[j + k] = self.sineArray255[j + k] * 0.732
                elif self.consecutiveBits == "0101":
                    self.qamArray[j + k] = self.sineArray105[j + k] * 0.732
                elif self.consecutiveBits == "0110":
                    self.qamArray[j + k] = self.sineArray285[j + k] * 0.732
                elif self.consecutiveBits == "0111":
                    self.qamArray[j + k] = self.sineArray75[j + k] * 0.732
                elif self.consecutiveBits == "1000":
                    self.qamArray[j + k] = self.sineArray195[j + k] * 0.732
                elif self.consecutiveBits == "1001":
                    self.qamArray[j + k] = self.sineArray165[j + k] * 0.732
                elif self.consecutiveBits == "1010":
                    self.qamArray[j + k] = self.sineArray345[j + k] * 0.732
                elif self.consecutiveBits == "1011":
                    self.qamArray[j + k] = self.sineArray15[j + k] * 0.732
                elif self.consecutiveBits == "1100":
                    self.qamArray[j + k] = self.sineArray225[j + k]
                elif self.consecutiveBits == "1101":
                    self.qamArray[j + k] = self.sineArray135[j + k]
                elif self.consecutiveBits == "1110":
                    self.qamArray[j + k] = self.sineArray315[j + k]
                elif self.consecutiveBits == "1111":
                    self.qamArray[j + k] = self.sineArray45[j + k]
            k += j
            i += 3
        
    def display(self) -> None:
        fig, axes = plt.subplots(3, 1)
        axes[0].plot(self.timeArray, self.bitArray, color='red', label='Data Signal')
        axes[1].plot(self.timeArray, self.sineArray, color='green', label='Carrier Signal')
        axes[2].plot(self.timeArray, self.qamArray, label='QAM Modulated Signal')
        for i in range(3):
            axes[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()
