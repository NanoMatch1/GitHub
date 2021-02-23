#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import os
import glob
import sys
import subprocess
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pylab import *
plt.style.use('ggplot')
pi = math.pi

###Imports .dat file from SQUID measurements###
###Puts Field, Temp, Long Moment, and Long Reg Fit into a new dataframe df1###
def Batch_plot_MH():
    
    folder_name = 'H:\\HTS Aircraft\\SQUID\\MH Loops\\HoTb'
    os.chdir(folder_name) 
    files = glob.glob('*.rso.dat')
    #MH Loop squid data files should be labelled "004_SAMPLE NAME_TEMPERATURE_MH_MAX FIELD.rso.dat"
    Ms_pos= []
    Ms_neg= []
    Name = []
    df_fit = []
    sample_name = []
    Ms_uncert = []
    Pos_uncert = []
    Neg_uncert = []
    Max_moment = []
    Reduction = []
    
    areas = { #Units are in cm^2, Note that B Block microscope measures in microns^2,divide by 100000000 to get cm^2#
    'TB0032': 0.06865148,
    'TB0033': 0.13348948,
    'TB0034': 0.08846026,
    'TB0035': 0.08590154,
    'TB0036': 0.10251015,
    'TB0037': 0.06557546,
    'TB0038': 0.07695362,
    'TB0039': 0.07890537,
    'TB0040': 0.07290076,} # TB0040 requires area to be measured, possible remeasure new sample in SQUID#
    thick = 0.00001 #100nm in cm
      
    for file_name in files:
        sample_name = file_name[4:10]
        area = areas[sample_name]
        data =  np.genfromtxt(file_name,delimiter=',',usecols=(2,3,4,9),skip_header=31,names=None) #picks out useful columns from the .dat
        c_names = ['Field','Temp','Long Moment','Long Reg Fit' ]    
        df1 = pd.DataFrame(data[:].copy(), columns=c_names)
        df1['Moment Denisty (T)']=df1['Long Moment']*4*pi/(area*thick*10000)
        df1['Field (T)']=df1['Field']/10000
        
    
        matplotlib.rc('axes.formatter', useoffset=False)
        fig1, ax = plt.subplots(nrows=1, ncols=2)
        fig1.tight_layout(pad=5.0, w_pad=3.0, h_pad=1.0)    
        plt.suptitle(sample_name, y=0.95, fontsize = 10) 
        
    
        for tick in ax[0].get_xticklabels():
            tick.set_rotation(45)
        plt.xticks(rotation='45')
        ax[0].plot(df1['Field (T)'], df1['Moment Denisty (T)'],'o', c='black', label='cycle 1')
        ax[0].set_title('Moment',y=1.08)
        ax[0].set_xlabel('Field (T)')
        ax[0].set_ylabel('Moment Denisty (T)')

        ax[1].plot(df1['Field (T)'], df1['Long Reg Fit'],'o', c='black', label='cycle 1')
        ax[1].set_title('Reg Fit',y=1.08)
        ax[1].set_xlabel('Field (T)')
        ax[1].set_ylabel('Long Reg Fit')

    
        plt.setp(plt.xticks()[1], rotation=45)

        plt.savefig(os.path.join(os.getcwd(), "%s.png" % sample_name), figsize=(5,5), dpi=600)
        df1.to_csv(os.path.join(os.getcwd(), "pro"+"%s.csv" % sample_name))
        
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        fig2.tight_layout()
        
        df_a = df1[df1['Long Reg Fit'] > 0.95] #Only fits to data points that have long reg fit greater than #VALUE - default=0.95, then puts thpose points in new dataframe
        x1 = df_a['Field'].values 
        y1 = df_a['Moment Denisty (T)'].values
        

        try:
            
            df_b = df_a[df_a['Field']>55000]    #Only fits to positive high field data points - default=55000, then puts thpose points in new dataframe
            x2 = df_b['Field'].values
            y2 = df_b['Moment Denisty (T)'].values
            fit2 = np.polyfit(x2,y2,1)
            polynomial2 = np.poly1d(fit2)
            y2s = polynomial2(x2)
            F_neg=fit2[0]
            int2=fit2[1]

            df_c = df_a[df_a['Field']<-55000] #Only fits to negative high field data points - default=55000, then puts thpose points in new dataframe
            x3 = df_c['Field'].values
            y3 = df_c['Moment Denisty (T)'].values
            fit3 = np.polyfit(x3,y3,1)
            polynomial3 = np.poly1d(fit3)
            y3s = polynomial3(x3)
            F_neg=fit3[0]
            int3=fit3[1]

            ax2.plot(x3, y3, 'o')
            ax2.plot(x3, y3s, color='blue')
            ax2.plot(x2, y2, 'o')
            ax2.plot(x2, y2s, color='red')
            
            maxmoment = df_a['Moment Denisty (T)'].max() #Finds the max moment measured - usually the correpsonding moment at 7T
            delta_int = int3+int2 #find the difference between the positive and negative high field fit intercepts - Ms 
            pos_uncert = delta_int/int2*100 #This is percentage error of the positive high field intercept for the difference in calcualted positive and negative high field intercepts
            neg_uncert = delta_int/int3*100 #This is percentage error of the negative high field intercept for the difference in calcualted positive and negative high field intercepts
            Ms_pos.append(int2) # This is Ms (units - Tesla) as calculated from linear fit to the positive high field
            Ms_neg.append(int3) # This is Ms (units - Tesla) as calculated from linear fit to the negative high field
            
            reduction = (maxmoment-((int2-int3)/2.0))*100 #By how much does the max moment at 10K reduce when the linear contribution is subtracted?
            Reduction.append(reduction)
            Name.append(sample_name) #Appends the sample name to a column for each .dat that gets processed
            Ms_uncert.append(delta_int) #This is the difference between the intercept calculated from positive and negative high fields. 
            Pos_uncert.append(pos_uncert) # percentage uncertainty of positive intercept
            Neg_uncert.append(neg_uncert) # percentage uncertainty of negative intercept
            Max_moment.append(maxmoment) 

            df_fit = pd.DataFrame({'Name': Name,'Ms_pos':Ms_pos,'Ms_neg':Ms_neg,'Ms_uncert':Ms_uncert, 'Pos_uncert' :Pos_uncert,'Neg_uncert':Neg_uncert,'Max_moment':Max_moment, 'Reduction':Reduction }).sort_values(['Name'])
            df_fit.to_csv(os.path.join(os.getcwd(), "Ms_MH_10K_Master.csv"))
                        
        except TypeError:
            print (file_name)
            print ("Check this scan")
            
    print(df_fit)


# In[3]:


Batch_plot_MH()


# In[27]:


###Imports pro........csv files and plots Magnetic Field against Field. Loops this for all files within the directory##
### This script will normalise all MH loops in a directory, useful for seeing how easy/hard it is to flip the magnetization
### You will need to run "Batch_plot_MH()" to turn your data into the correct format ##


def SQUID_NORM():
    
    folder_name = 'H:\\HTS Aircraft\\SQUID\\MH Loops\\HoTb'
    os.chdir(folder_name)
    files = glob.glob('pro'+'*.csv')
    
    growth_conditions = { #Enter sample name into left hand column - this should be somewhere in the filename. need to be able to call this name later for legend
    'TB0032': 'Ho 0.1 nm/s',#Enter the 'growth conditions' of that sample into the right hand column - this will important for the legend. 
    'TB0033': 'Ho 0.2 nm/s',
    'TB0034': 'Ho 0.3 nm/s',
    'TB0035': 'Tb 0.1 nm/s',
    'TB0036': 'Tb 0.2 nm/s',
    'TB0037': 'Tb 0.3 nm/s',
    'TB0038': 'HoTb 0.2 nm/s (50:50)',
    'TB0039': 'HoTb 0.2 nm/s (80:20)',
    'TB0040': 'HoTb 0.2 nm/s (19:81)'}
    
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = fig.add_subplot(1, 1, 1)
    cmap = mpl.cm.jet
    
    
    i=0
    for file_name in files:
        i=i+1
        data =  np.genfromtxt(file_name,delimiter=',',usecols=(1,2,5,6),skip_header=0,names=None)
        c_names = ['Field (Oe)','Temp','Moment Denisty (T)','Field (T)' ]    
        df1 = pd.DataFrame(data[:].copy(), columns=c_names)
        sample_name = file_name[3:9]
        growth_condition = growth_conditions[sample_name]
        
        df1['norm'] = (df1['Moment Denisty (T)'] - df1[('Moment Denisty (T)')].min()) / (df1[('Moment Denisty (T)')].max() - df1[('Moment Denisty (T)')].min())
#Each data set is assigned a colour from jet colourmap. color=cmap(i/no of files you want to plot).#
        fig.tight_layout(pad=3.0, w_pad=10.0, h_pad=1.0) 
        ax1.plot(df1['Field (Oe)'], df1['norm'],'-o', color=cmap(i/9), label=growth_condition )
        ax1.set_title('Rare-earth films Normalized Moment/V')
        ax1.set_xlabel('Field (Oe)')
        ax1.set_xlim(-10000, 10000)
        ax1.set_ylim(-0.2, 1.2)
        ax1.set_ylabel('Normalized moment/V')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        
        handles, labels = ax1.get_legend_handles_labels()
        lgd = ax1.legend(handles, labels, loc=2, bbox_to_anchor=(1.05,1))
        plt.show()
    fig.savefig('Rare-earth films MH Loop 10K Normalized_Low field.png', bbox_extra_artists=(lgd,), bbox_inches='tight', figsize=(5,5), dpi=600)


# In[28]:


SQUID_NORM()


# In[22]:


def Batch_plot_FC():
    
    folder_name = 'H:\\HTS Aircraft\\SQUID\\Field Cooled\\HoTb'
    os.chdir(folder_name) 
    files = glob.glob('*.rso.dat')
    #MH Loop squid data files should be labelled "004_SAMPLE NAME_TEMPERATURE_MH_MAX FIELD.rso.dat"
    Ms_pos= []
    Ms_neg= []
    Name = []
    df_fit = []
    sample_name = []
    Ms_uncert = []
    Pos_uncert = []
    Neg_uncert = []
    Max_moment = []
    Reduction = []
    
    areas = { #Units are in cm^2, Note that B Block microscope measures in microns^2,divide by 100000000 to get cm^2#
    'TB0032': 0.06865148,
    'TB0033': 0.13348948,
    'TB0034': 0.08846026,
    'TB0035': 0.08590154,
    'TB0036': 0.10251015,
    'TB0037': 0.06557546,
    'TB0038': 0.07695362,
    'TB0039': 0.07890537,
    'TB0040': 0.07290076,} # TB0040 requires area to be measured, possible remeasure new sample in SQUID#
    thick = 0.00001 #100nm in cm
      
    for file_name in files:
        sample_name = file_name[4:10]
        area = areas[sample_name]
        data =  np.genfromtxt(file_name,delimiter=',',usecols=(2,3,4,9),skip_header=31,names=None) #picks out useful columns from the .dat
        c_names = ['Field','Temp','Long Moment','Long Reg Fit' ]    
        df1 = pd.DataFrame(data[:].copy(), columns=c_names)
        df1['Moment Denisty (T)']=df1['Long Moment']*4*pi/(area*thick*10000)
        FC_field = df1['Field'].mean()
    
        matplotlib.rc('axes.formatter', useoffset=False)
        fig1, ax = plt.subplots(nrows=1, ncols=2)
        fig1.tight_layout(pad=5.0, w_pad=3.0, h_pad=1.0)    
        plt.suptitle(sample_name, y=0.95, fontsize = 10) 

        
    
        for tick in ax[0].get_xticklabels():
            tick.set_rotation(45)
        plt.xticks(rotation='45')
        ax[0].plot(df1['Temp'], df1['Moment Denisty (T)'],'o', c='black', label='cycle 1')
        ax[0].set_title('Moment',y=1.08)
        ax[0].set_xlabel('Temperature (K)')
        ax[0].set_ylabel('Moment Denisty (T)')

        ax[1].plot(df1['Temp'], df1['Long Reg Fit'],'o', c='black', label='cycle 1')
        ax[1].set_title('Reg Fit',y=1.08)
        ax[1].set_xlabel('Temperature (K)')
        ax[1].set_ylabel('Long Reg Fit')

    
        plt.setp(plt.xticks()[1], rotation=45)

        plt.savefig(os.path.join(os.getcwd(), "%s.png" % sample_name), figsize=(5,5), dpi=600)
        df1.to_csv(os.path.join(os.getcwd(), "pro"+"%s_FC(7T).csv" % sample_name))
        
def Batch_plot_FC_oneplot():
    
    folder_name = 'H:\\HTS Aircraft\\SQUID\\Field Cooled\\HoTb'
    os.chdir(folder_name)
    files = sorted(glob.glob('pro'+'*.csv'))
    
    growth_conditions = { #Enter sample name into left hand column - this should be somewhere in the filename. need to be able to call this name later for legend
    'TB0032': 'Ho 0.1 nm/s',#Enter the 'growth conditions' of that sample into the right hand column - this will important for the legend. 
    'TB0033': 'Ho 0.2 nm/s',
    'TB0034': 'Ho 0.3 nm/s',
    'TB0035': 'Tb 0.1 nm/s',
    'TB0036': 'Tb 0.2 nm/s',
    'TB0037': 'Tb 0.3 nm/s',
    'TB0038': 'HoTb 0.2 nm/s (50:50)',
    'TB0039': 'HoTb 0.2 nm/s (80:20)',
    'TB0040': 'HoTb 0.2 nm/s (19:81)'}
    
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = fig.add_subplot(1, 1, 1)
    cmap = mpl.cm.jet
    
    
    i=0
    for file_name in files:
        i=i+1
        data =  np.genfromtxt(file_name,delimiter=',',usecols=(1,2,5),skip_header=0,names=None)
        c_names = ['Field (Oe)','Temp','Moment Denisty (T)']    
        df1 = pd.DataFrame(data[:].copy(), columns=c_names)
        sample_name = file_name[3:9]
        growth_condition = growth_conditions[sample_name]
        
        df1['norm'] = (df1['Moment Denisty (T)'] - df1[('Moment Denisty (T)')].min()) / (df1[('Moment Denisty (T)')].max() - df1[('Moment Denisty (T)')].min())
#Each data set is assigned a colour from jet colourmap. color=cmap(i/no of files you want to plot).#
        fig.tight_layout(pad=3.0, w_pad=10.0, h_pad=1.0) 
        ax1.plot(df1['Temp'], df1['Moment Denisty (T)'],'-o', color=cmap(i/9), label=growth_condition )
        ax1.set_title('Saturation magnetization of rare-earth films FC (7T)')
        ax1.set_xlabel('Field (Oe)')
        ax1.set_xlim(0, 400)
        ax1.set_ylim(0, 3)
        ax1.set_ylabel('Moment Denisty (T)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        
        handles, labels = ax1.get_legend_handles_labels()
        lgd = ax1.legend(handles, labels, loc=2, bbox_to_anchor=(1.05,1))
        plt.show()
    fig.savefig('Rare-earth films FC-7T.png', bbox_extra_artists=(lgd,), bbox_inches='tight', figsize=(5,5), dpi=600)


# In[23]:


Batch_plot_FC()


# In[24]:


Batch_plot_FC_oneplot()


# In[ ]:




