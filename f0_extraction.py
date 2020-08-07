############################################
# Name of this library: <f0_extraction.py> #
############################################
# 
# <f0_extraction.py> is a property of Antônio Roberto Monteiro Simões - All Rights Reserved ©️ 2020 
# <f0_extraction.py> é propriedade de Antônio Roberto Monteiro Simões - Todos os direitos reservados ©️ 2020
# This file is licensed under the MIT License
#
# The <f0_extraction> is a software library for f0 (pitch) extraction into a PANDAS Data Frame. It is 
# designed to produce the following outputs from sound recordings in .wav extension: 
# (1) an FFT oscillographic image (bidimensinal); 
# (2) an FFT 3D static image (tridimensional); 
# (3) an f0 plot; 
# (4) automatic .csv files with measurements of musical notes associated with duration, f0, intensity 
# (amplitude), f0 acceleration, intensity acceleration and other related parameters. These measurements in .csv 
# files are meant to be imported from Excel for statistical analyses. 
# (5) an FFT 3D dynamic image (tridimensional); and 
# (6) a MIDI file to create musical notation in a music software and MIDI outputs through a MidiEditor. 
#
# The <f0_extraction> is designed to execute software libraries, other functions, plug-ins, etc. in the
# notebook <Notebook_Prosodies_to_NOTATION.ipynb>.
#
# NOTE: It is common to confuse pitch and fundamental frequency (f0). The f0 is the acoustical equivalent of 
# pitch. Pitch is perceptual. Pitch is what the human ear hears, it is what one feels. In order to study 
# sound pitch it is necessary to extract the fundamental frequency (f0).
# 
############################################

import numpy
import pandas

def f0_extraction_to_dataframe(freq,time,f0_strength,energy,A4=440,division=12):
    
    ##############################################################
    # This code is based on the Equal Temperament Standard found at
    # (https://pages.mtu.edu/~suits/NoteFreqCalcs.html) 
    # A4 is the reference note
    # <division> is the standard for the Equal Temperament scale
    ##############################################################
   
    a = 2**(1/division) 
    
         # It checks the division of the selected notes. Currently it is supported only in the
         # the extensions TET-12 and TET-24. Other extensions can be included if needed.
    
    if division == 24: 
        name = ["ND","A","A+", "A#","B-", "B","B+","C", "C+","C#", "D-","D","D+", "D#", "E-","E","E+", "F","F+",
            "F#","G-","G","G+", "G#", "A-"]
    elif division == 12:
        name = ["ND", "A", "A#", "B","C", "C#", "D", "D#", "E", "F",
            "F#","G", "G#"]
    else: 
        warnings.warn("Division notation not defined")
        return None
    
    semitones = numpy.where(freq>0,numpy.log(numpy.array(freq)/A4,where=freq>0)/numpy.log(a),-1000) 
    
         # It calculates the logarithmic function for the positive frequencies. Otherwise, it returns -1000.    

    error = semitones - numpy.around(semitones) 
    
         # It calculates the pitch deviation of the nearest note.
        
    notes = numpy.where(semitones>-1000,numpy.around(semitones)%division+1,0) 
    
         # It calculates the semitone distance of the reference note 'La' (A)
        
    note = numpy.where(semitones>-1000,numpy.around(semitones+0.25*division)%division+1,0) 
    
         # It calculates the semitone distance of the reference note 'Do' (C)
    
    tone = numpy.around(semitones) 
    
         # It calculates the absolute distance (positive and negative) in semitones for the reference note A4.
    
    octave = numpy.round((tone+(3*division+0.75*division))/division) 
    
         # It calculates the octave relative to the note

    freq[freq==0] = numpy.nan

    notation = [name[int(i)]+str(int(j)) for i,j in zip(notes,octave)] 
    
         # It searches for musical notations in the musical notation list for the chosen division
         # (Procura a notação musical na lista de notações para a divisão escolhida)
    
    df = pandas.DataFrame(list(zip(freq,time,f0_strength,energy,octave,tone,notes,error,notation)),columns=['freq','time','f0_strength','energy','octave','tone','notes','error','notation'])
    df['energy_accel'] = df.energy.diff().fillna(0)
    df['freq_accel'] = df.freq.diff().fillna(0)

         # It returns a PANDAS DataFrame with the information extracted and calculated.
    
    return df
